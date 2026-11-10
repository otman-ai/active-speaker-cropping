"""Run streaming NVIDIA Riva ASR with word timestamps and speaker diarization."""

from __future__ import annotations

import json
def transcribe_with_diarization(
    audio_path: str,
    server: str,
    language: str = "en-US",
    max_speakers: int = 5,
    use_ssl: bool = False,
    api_key: str | None = None,
    function_id: str | None = None,
):
    try:
        import riva.client
    except ImportError as exc:
        raise RuntimeError(
            "Riva ASR requires nvidia-riva-client. Install the optional "
            "dependencies in nvidia_speaker_crop/requirements.txt."
        ) from exc

    metadata_args = None
    if api_key or function_id:
        if not api_key or not function_id:
            raise ValueError("Hosted Riva access requires both an NVIDIA API key and ASR function ID.")
        metadata_args = [["authorization", "Bearer " + api_key], ["function-id", function_id]]
    auth = riva.client.Auth(uri=server, use_ssl=use_ssl, metadata_args=metadata_args)
    service = riva.client.ASRService(auth)
    config = riva.client.StreamingRecognitionConfig(
        config=riva.client.RecognitionConfig(
            encoding=riva.client.AudioEncoding.LINEAR_PCM,
            sample_rate_hertz=16000,
            audio_channel_count=1,
            language_code=language,
            max_alternatives=1,
            enable_automatic_punctuation=True,
            enable_word_time_offsets=True,
        ),
        interim_results=False,
    )
    riva.client.add_speaker_diarization_to_config(
        config, diarization_enable=True, diarization_max_speakers=max_speakers
    )

    words = []
    transcript_parts = []
    try:
        with riva.client.AudioChunkFileIterator(audio_path, chunk_n_frames=1600) as audio_chunks:
            responses = service.streaming_response_generator(audio_chunks, config)
            for response in responses:
                for result in response.results:
                    if not result.is_final or not result.alternatives:
                        continue
                    alternative = result.alternatives[0]
                    if alternative.transcript:
                        transcript_parts.append(alternative.transcript)
                    for word in alternative.words:
                        # Riva speaker tags are zero-based; ASD diarization IDs are one-based.
                        words.append(
                            {
                                "text": word.word,
                                "start": max(0.0, float(word.start_time) / 1000.0),
                                "end": max(0.0, float(word.end_time) / 1000.0),
                                "speaker_id": int(word.speaker_tag) + 1,
                            }
                        )
    except Exception as exc:
        raise RuntimeError(
            "Hosted Riva ASR streaming failed. Check the NVIDIA API key, ASR function ID, "
            "network access, and that the selected endpoint supports speaker diarization."
        ) from exc

    if not words:
        raise RuntimeError(
            "Riva returned no word-level speaker tags. Verify the selected ASR endpoint "
            "supports speaker diarization and that speech is audible."
        )
    return {
        "language_code": language,
        "text": " ".join(transcript_parts).strip(),
        "words": words,
    }


def save_diarization(data: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as output:
        json.dump(data, output, ensure_ascii=False, indent=2)
