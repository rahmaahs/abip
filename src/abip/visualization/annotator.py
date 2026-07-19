from __future__ import annotations

from typing import Any

import cv2


def draw_basic_overlay(frame: Any, frame_index: int, total_frames: int) -> Any:
    """
    Draw a simple status overlay on a video frame.

    Parameters
    ----------
    frame:
        The image to annotate.
    frame_index:
        The current frame number.
    total_frames:
        The total number of frames in the video.

    Returns
    -------
    The same frame with text drawn on top of it.
    """
    # Draw a dark rectangle behind the text so it is readable.
    cv2.rectangle(frame, (20, 20), (520, 90), (0, 0, 0), thickness=-1)

    # Write the project name.
    cv2.putText(
        frame,
        "ABIP Phase 1",
        (35, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    # Write progress through the video.
    progress_text = f"Frame {frame_index + 1} / {total_frames}"
    cv2.putText(
        frame,
        progress_text,
        (35, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )

    return frame


from abip.perception.detections import FrameDetections


def draw_detections(frame: Any, frame_detections: FrameDetections) -> Any:
    """
    Draw detection boxes and labels on a frame.
    """
    for detection in frame_detections.detections:
        box = detection.box

        # Draw the rectangle around the object.
        cv2.rectangle(
            frame,
            (box.x1, box.y1),
            (box.x2, box.y2),
            (0, 255, 0),
            thickness=2,
        )

        # Create the label text.
        label = f"{detection.class_name} {detection.confidence:.2f}"

        # Draw a filled box behind the text so it is readable.
        text_x = box.x1
        text_y = max(20, box.y1 - 10)

        cv2.rectangle(
            frame,
            (text_x, text_y - 22),
            (text_x + 220, text_y + 5),
            (0, 255, 0),
            thickness=-1,
        )

        cv2.putText(
            frame,
            label,
            (text_x + 5, text_y - 3),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2,
            cv2.LINE_AA,
        )

    return frame


from abip.tracking.tracks import FrameTracks


def draw_tracks(frame: Any, frame_tracks: FrameTracks) -> Any:
    """
    Draw tracked object boxes and IDs on a frame.
    """
    for track in frame_tracks.tracks:
        box = track.box

        cv2.rectangle(
            frame,
            (box.x1, box.y1),
            (box.x2, box.y2),
            (255, 0, 0),
            thickness=2,
        )

        label = f"ID {track.track_id}: {track.class_name} {track.confidence:.2f}"
        text_x = box.x1
        text_y = max(20, box.y1 - 10)

        cv2.rectangle(
            frame,
            (text_x, text_y - 22),
            (text_x + 260, text_y + 5),
            (255, 0, 0),
            thickness=-1,
        )

        cv2.putText(
            frame,
            label,
            (text_x + 5, text_y - 3),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    return frame