"""End-to-end Active Speaker Cropping workflow."""

from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

from dotenv import load_dotenv

from crop_video import render_crop
from nim_client import detect
from riva_diarization import save_diarization, transcribe_with_diarization

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(PROJECT_ROOT / ".env", override=False)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def run(args):
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    if not input_path.is_file():
        raise FileNotFoundError(input_path)
    if not args.api_key:
        raise ValueError("Set NVCF_API_KEY or pass --api-key.")
    if not args.function_id:
        raise ValueError("Set NVCF_FUNCTION_ID or pass --function-id.")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="active_speaker_cropping_", dir=output_path.parent) as work:
        normalized_video = str(Path(work) / "streamable_video.mp4")
        audio_path = str(Path(work) / "audio.wav")
        crop_path = str(Path(work) / "speaker_crop.mp4")
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(input_path), "-map", "0:v:0", "-an",
                "-vf", "fps=25,pad=ceil(iw/2)*2:ceil(ih/2)*2", "-c:v", "libx264",
                "-preset", "veryfast", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                normalized_video, "-loglevel", "error",
            ], check=True,
        )
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(input_path), "-map", "0:a:0", "-vn", "-ac", "1",
                "-ar", "16000", "-c:a", "pcm_s16le", audio_path, "-loglevel", "error",
            ], check=True,
        )

        diarization = transcribe_with_diarization(
            audio_path,
            server=args.riva_server,
            language=args.language,
            max_speakers=args.max_speakers,
            use_ssl=args.riva_ssl,
            api_key=args.riva_api_key,
            function_id=args.riva_function_id,
        )
        diarization_path = str(output_path.with_suffix(".diarization.json"))
        save_diarization(diarization, diarization_path)
        print("Riva diarization saved to:", diarization_path)

        frame_results = detect(
            normalized_video,
            audio_path,
            diarization,
            function_id=args.function_id,
            api_key=args.api_key,
        )
        render_crop(normalized_video, crop_path, frame_results, face_fraction=args.face_fraction)
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", crop_path, "-i", str(input_path), "-map", "0:v:0",
                "-map", "1:a:0?", "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-shortest", "-movflags", "+faststart", str(output_path),
                "-loglevel", "error",
            ], check=True,
        )
    print("Speaker crop written to:", output_path)


def main():
    parser = argparse.ArgumentParser(description="Active Speaker Cropping with hosted speech diarization")
    parser.add_argument("--input", required=True, help="Input video with an audio stream")
    parser.add_argument("--output", default="speaker_crop.mp4")
    parser.add_argument("--riva-server", default=os.getenv("RIVA_SERVER", "grpc.nvcf.nvidia.com:443"))
    parser.add_argument("--riva-ssl", action="store_true", default=_env_bool("RIVA_SSL", True),
                        help="Use TLS for the Riva connection (enabled for NVIDIA hosted ASR)")
    parser.add_argument(
        "--riva-function-id",
        default=os.getenv("RIVA_FUNCTION_ID", "bb0837de-8c7b-481f-9ec8-ef5663e9c1fa"),
        help="NVIDIA hosted Nemotron ASR Streaming function ID",
    )
    parser.add_argument(
        "--riva-api-key",
        default=os.getenv("RIVA_API_KEY") or os.getenv("NVCF_API_KEY"),
        help="NVIDIA API key; defaults to NVCF_API_KEY",
    )
    parser.add_argument("--language", default=os.getenv("RIVA_LANGUAGE", "en-US"))
    parser.add_argument("--max-speakers", type=int, default=int(os.getenv("RIVA_MAX_SPEAKERS", "5")))
    parser.add_argument("--face-fraction", type=float, default=float(os.getenv("FACE_FRACTION", "0.24")),
                        help="Target speaker face height as a fraction of the 9:16 crop")
    parser.add_argument("--function-id", default=os.getenv("NVCF_FUNCTION_ID"))
    parser.add_argument("--api-key", default=os.getenv("NVCF_API_KEY"), help="Prefer NVCF_API_KEY env var")
    args = parser.parse_args()
    if not 0.05 <= args.face_fraction <= 0.8:
        parser.error("--face-fraction must be between 0.05 and 0.8")
    run(args)


if __name__ == "__main__":
    main()
