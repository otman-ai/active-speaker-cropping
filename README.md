# Active Speaker Cropping

Standalone Python workflow that uses NVIDIA hosted ASR to diarize speech, sends
the video, audio, and word-level speaker data to NVIDIA Active Speaker Detection
(ASD), then renders a smoothed vertical crop around the active speaker.

## Included demo videos

- [`sample_video.mp4`](samples/sample_video.mp4)
- [`002.mp4`](samples/002.mp4)

These are included as workflow examples. Make sure you have the rights needed to
redistribute the videos if you fork or republish this repository.

## Requirements

- Python 3.10 or newer
- FFmpeg with `ffmpeg` available on `PATH` and built with `libx264`
- NVIDIA Build access and an NVIDIA API key for both hosted NIM functions
- Internet access to `grpc.nvcf.nvidia.com:443`

### Install FFmpeg

Install FFmpeg for your operating system from [ffmpeg.org](https://ffmpeg.org/download.html),
and verify `ffmpeg -version` works in a new terminal.

### Install Python dependencies

From this repository directory:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On macOS/Linux, create/activate the virtual environment with `python3 -m venv
.venv` and `source .venv/bin/activate`, then run the same pip commands.

## NVIDIA API setup

1. Sign in to [NVIDIA Build](https://build.nvidia.com/).
2. Open the [Active Speaker Detection NIM](https://build.nvidia.com/nvidia/active-speaker-detection)
   page, accept its terms if prompted, and copy its function ID from the API page.
3. Create an NVIDIA/NGC API key from NVIDIA Build. Keep it private; never put a
   real key in source code or commit it.
4. The ASR service uses NVIDIA's hosted Nemotron ASR Streaming endpoint at
   `grpc.nvcf.nvidia.com:443`. Its default function ID is configured in the
   runner and can be overridden with `RIVA_FUNCTION_ID`.

Create a local `.env` from the template:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set:

```dotenv
NVCF_API_KEY=your_nvidia_api_key
NVCF_FUNCTION_ID=your_active_speaker_detection_function_id
```

`NVCF_API_KEY` is used for both hosted calls. `RIVA_API_KEY` is optional and
defaults to `NVCF_API_KEY`; `RIVA_FUNCTION_ID` defaults to NVIDIA's hosted
Nemotron ASR Streaming function ID. `.env` is excluded by `.gitignore`.

## Run

```powershell
python run_workflow.py --input .\samples\sample_video.mp4 --output .\output\sample_video_crop.mp4
```

Use the other bundled example:

```powershell
python run_workflow.py --input .\samples\002.mp4 --output .\output\002_crop.mp4
```

The workflow writes the output video and a sibling `.diarization.json` file.
The diarization JSON contains recognized words, timestamps, and speaker IDs.

Common options:

```text
--language en-US
--max-speakers 5
--face-fraction 0.24
--riva-server grpc.nvcf.nvidia.com:443
--riva-function-id <ASR NVCF function ID>
--function-id <ASD NVCF function ID>
```

Nemotron ASR Streaming accepts streaming audio and returns word-level speaker
tags; the workflow uses Riva's streaming gRPC API. See the [NVIDIA hosted ASR
API instructions](https://build.nvidia.com/nvidia/nemotron-asr-streaming/api)
and [ASR diarization documentation](https://docs.nvidia.com/nim/speech/latest/asr/customization/customization.html).

## Project files

- `run_workflow.py` — transcode, diarize, call ASD, and render the crop
- `riva_diarization.py` — hosted Riva streaming ASR and diarization adapter
- `nim_client.py` — NVIDIA ASD NVCF gRPC client
- `crop_video.py` — speaker-aware smoothed 9:16 crop renderer
- `interfaces/` — NVIDIA ASD protobuf client interfaces
- `samples/` — demo input videos

