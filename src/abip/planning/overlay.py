from __future__ import annotations

from typing import Any

import cv2

from abip.planning.free_space import FreeSpaceState
from abip.planning.state import PlanState


def draw_plan_overlay(frame: Any, plan_state: PlanState) -> Any:
    height, width = frame.shape[:2]

    box_width = 560
    box_height = 120
    margin = 20

    x1 = margin
    y1 = height - box_height - margin
    x2 = x1 + box_width
    y2 = y1 + box_height

    color = (0, 255, 0)
    if plan_state.urgency == "medium":
        color = (0, 165, 255)
    elif plan_state.urgency == "high":
        color = (0, 0, 255)

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=-1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), thickness=2)

    cv2.putText(
        frame,
        f"PLAN: {plan_state.maneuver.upper()}",
        (x1 + 15, y1 + 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        f"Urgency: {plan_state.urgency.upper()}",
        (x1 + 15, y1 + 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    return frame


def draw_free_space_overlay(frame: Any, free_space_state: FreeSpaceState) -> Any:
    height, width = frame.shape[:2]

    box_width = 740
    box_height = 130
    x1 = width // 2 - box_width // 2
    y1 = height - box_height - 20
    x2 = x1 + box_width
    y2 = y1 + box_height

    color = (0, 255, 0)
    if not free_space_state.right_open:
        color = (0, 165, 255)
    if not free_space_state.path_clear:
        color = (0, 0, 255)

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=-1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), thickness=2)

    cv2.putText(
        frame,
        f"FREE SPACE: {free_space_state.preferred_side.upper()}",
        (x1 + 15, y1 + 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        f"L:{free_space_state.left_pressure:.2f}  C:{free_space_state.center_pressure:.2f}  R:{free_space_state.right_pressure:.2f}",
        (x1 + 15, y1 + 75),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        f"Path clear: {str(free_space_state.path_clear).upper()}",
        (x1 + 15, y1 + 110),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    return frame