"""Client for the hosted Active Speaker Detection service."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _modules():
    try:
        import grpc
    except ImportError as exc:
        raise RuntimeError(
            "Active Speaker Detection requires grpcio. Install requirements.txt from this project."
        ) from exc

    interface_root = str(Path(__file__).parent / "interfaces")
    if interface_root not in sys.path:
        sys.path.insert(0, interface_root)
    from nvidia.ai4m.activespeakerdetection.v1 import activespeakerdetection_pb2 as asd_pb2
    from nvidia.ai4m.activespeakerdetection.v1 import activespeakerdetection_pb2_grpc as asd_grpc
    from nvidia.ai4m.audio.v1 import audio_pb2
    from nvidia.ai4m.video.v1 import video_pb2
    return grpc, asd_pb2, asd_grpc, audio_pb2, video_pb2


def _chunks(path: str, chunk_size: int = 64 * 1024):
    with open(path, "rb") as source:
        while chunk := source.read(chunk_size):
            yield chunk


def detect(video_path: str, audio_path: str, diarization: dict, function_id: str, api_key: str):
    grpc, asd_pb2, asd_grpc, audio_pb2, video_pb2 = _modules()

    def requests():
        detection_config = asd_pb2.ActiveSpeakerDetectionConfig(
            input_video_config=video_pb2.VideoConfig(codec=video_pb2.VIDEO_CODEC_H264),
            input_audio_config=audio_pb2.AudioConfig(encoding=audio_pb2.AUDIO_CODEC_WAV),
            audio_source_config=asd_pb2.AUDIO_SOURCE_CONFIG_SEPARATE_STREAM,
        )
        yield asd_pb2.DetectActiveSpeakerRequest(config=detection_config)

        segments = [
            asd_pb2.AudioSegmentInfo(
                start_time=int(round(word["start"] * 1000)),
                end_time=int(round(word["end"] * 1000)),
                speaker_id=int(word["speaker_id"]),
                word=word["text"],
                language_code=diarization.get("language_code", ""),
            )
            for word in diarization["words"]
        ]
        for start in range(0, len(segments), 100):
            batch = segments[start:start + 100]
            batch_info = asd_pb2.AudioDiarizationInfo(
                segments=batch,
                transcript=diarization.get("text", "") if start + len(batch) >= len(segments) else "",
            )
            yield asd_pb2.DetectActiveSpeakerRequest(
                data=asd_pb2.ActiveSpeakerDetectionData(diarization_info=batch_info)
            )

        video_iter, audio_iter = iter(_chunks(video_path)), iter(_chunks(audio_path))
        video_done = audio_done = False
        while not (video_done and audio_done):
            if not video_done:
                chunk = next(video_iter, None)
                video_done = chunk is None
                if chunk is not None:
                    yield asd_pb2.DetectActiveSpeakerRequest(
                        data=asd_pb2.ActiveSpeakerDetectionData(video_data=chunk)
                    )
            if not audio_done:
                chunk = next(audio_iter, None)
                audio_done = chunk is None
                if chunk is not None:
                    yield asd_pb2.DetectActiveSpeakerRequest(
                        data=asd_pb2.ActiveSpeakerDetectionData(audio_data=chunk)
                    )

    metadata = (
        ("authorization", "Bearer " + api_key),
        ("function-id", function_id),
    )
    channel = grpc.secure_channel("grpc.nvcf.nvidia.com:443", grpc.ssl_channel_credentials())
    frame_results = {}
    try:
        stub = asd_grpc.ActiveSpeakerDetectionServiceStub(channel)
        responses = stub.DetectActiveSpeaker(requests(), metadata=metadata, timeout=3600)
        for response in responses:
            if not response.HasField("active_speaker_detection_result"):
                continue
            result = response.active_speaker_detection_result
            frame_results[int(result.frame_id)] = [
                {
                    "face_id": int(speaker.face_id),
                    "speaking": bool(speaker.is_speaking),
                    "confidence": float(speaker.face_detection_confidence),
                    "bbox": (
                        float(speaker.speaker_bbox.x),
                        float(speaker.speaker_bbox.y),
                        float(speaker.speaker_bbox.width),
                        float(speaker.speaker_bbox.height),
                    ),
                }
                for speaker in result.speaker_data
            ]
    finally:
        channel.close()
    if not frame_results:
        raise RuntimeError("NVIDIA ASD returned no frame detections.")
    return frame_results
