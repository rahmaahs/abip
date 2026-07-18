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