"""Create a speaker-following 9:16 crop from active speaker detections."""

from __future__ import annotations

import cv2
import numpy as np


def render_crop(input_video: str, output_video: str, frame_results: dict, face_fraction=0.24):
    capture = cv2.VideoCapture(input_video)
    fps = capture.get(cv2.CAP_PROP_FPS) or 25.0
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if frame_width <= 0 or frame_height <= 0:
        capture.release()
        raise RuntimeError("Could not read dimensions from the normalized video.")

    output_width = max(2, min(frame_width, frame_height * 9 // 16))
    output_height = max(2, min(frame_height, frame_width * 16 // 9))
    writer = cv2.VideoWriter(
        output_video, cv2.VideoWriter_fourcc(*"mp4v"), fps, (output_width, output_height)
    )
    max_crop_height = min(frame_height, frame_width * 16 / 9)
    crop_height = None
    center = (frame_width / 2, frame_height / 2)
    current_face = None
    challenger_face = None
    challenger_frames = 0
    frame_index = 0

    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            visible = [
                item for item in frame_results.get(frame_index, [])
                if item["speaking"] and item["confidence"] >= 0
            ]
            if visible:
                best = max(visible, key=lambda item: item["confidence"])
                if current_face is None:
                    current_face = best["face_id"]
                elif best["face_id"] != current_face:
                    if challenger_face == best["face_id"]:
                        challenger_frames += 1
                    else:
                        challenger_face = best["face_id"]
                        challenger_frames = 1
                    if challenger_frames >= 5:
                        current_face = challenger_face
                        challenger_face = None
                        challenger_frames = 0
                else:
                    challenger_face = None
                    challenger_frames = 0

                selected = next((item for item in visible if item["face_id"] == current_face), None)
                if selected is None:
                    selected = best
                    current_face = best["face_id"]
                    challenger_face = None
                    challenger_frames = 0
                x, y, width, height = selected["bbox"]
                detected_center = (x + width / 2, y + height / 2)
                center = (
                    center[0] + 0.25 * (detected_center[0] - center[0]),
                    center[1] + 0.25 * (detected_center[1] - center[1]),
                )
                desired_height = min(max_crop_height, max(2.0, height / face_fraction))
                crop_height = desired_height if crop_height is None else crop_height + 0.2 * (desired_height - crop_height)
            elif crop_height is None:
                crop_height = max_crop_height

            crop_height = max(2, min(max_crop_height, crop_height))
            crop_width = max(2, min(frame_width, int(round(crop_height * 9 / 16))))
            crop_height = max(2, min(frame_height, int(round(crop_width * 16 / 9))))
            left = max(0, min(frame_width - crop_width, int(center[0] - crop_width / 2)))
            top = max(0, min(frame_height - crop_height, int(center[1] - crop_height / 2)))
            crop = frame[top:top + crop_height, left:left + crop_width]
            writer.write(cv2.resize(crop, (output_width, output_height), interpolation=cv2.INTER_LINEAR))
            frame_index += 1
    finally:
        capture.release()
        writer.release()
    if frame_index == 0:
        raise RuntimeError("No video frames were read for cropping.")
    return frame_index
