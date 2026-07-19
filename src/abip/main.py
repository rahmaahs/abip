from __future__ import annotations

import argparse
from pathlib import Path

from abip.ingestion.video_reader import VideoReader
from abip.ingestion.video_writer import VideoWriter
from abip.planning.corridor import CorridorAnalyzer
from abip.planning.overlay import draw_corridor_overlay, draw_plan_overlay
from abip.planning.planner import BehaviorPlanner
from abip.risk.scorer import RiskScorer
from abip.scene.scene_builder import SceneBuilder
from abip.tracking.yolo_tracker import YOLOTracker
from abip.visualization.annotator import (
    draw_basic_overlay,
    draw_risk_overlay,
    draw_tracks,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="ABIP Phase 1: cycling video intelligence pipeline"
    )
    parser.add_argument(
        "--video",
        type=Path,
        required=True,
        help="Path to a cycling video file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/videos/corridor.mp4"),
        help="Path to the output video file",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="yolov8n.pt",
        help="YOLO model name or path",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.35,
        help="Minimum detection confidence",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("ABIP starting")
    print(f"Input video: {args.video}")
    print(f"Output video: {args.output}")
    print(f"YOLO model: {args.model}")
    print(f"Confidence threshold: {args.confidence}")

    tracker = YOLOTracker(
        model_name=args.model,
        confidence_threshold=args.confidence,
        target_classes=("person", "car", "bicycle"),
    )

    with VideoReader(args.video) as reader:
        metadata = reader.metadata()

        print("\nVideo metadata:")
        print(f"  Path: {metadata.path}")
        print(f"  Frames: {metadata.frame_count}")
        print(f"  FPS: {metadata.fps}")
        print(f"  Width: {metadata.width}")
        print(f"  Height: {metadata.height}")

        scene_builder = SceneBuilder(
            frame_width=metadata.width,
            frame_height=metadata.height,
        )
        corridor_analyzer = CorridorAnalyzer()
        risk_scorer = RiskScorer()
        planner = BehaviorPlanner()

        with VideoWriter(args.output, metadata) as writer:
            print("\nRunning tracking + scene understanding + corridor planning...")
            frame_count = 0

            for index, frame in reader.frames():
                frame_tracks = tracker.track(frame_index=index, frame=frame)
                scene_state = scene_builder.build(frame_tracks)
                corridor_state = corridor_analyzer.analyze(scene_state)
                risk_state = risk_scorer.score(scene_state)
                plan_state = planner.plan(scene_state, risk_state, corridor_state)

                annotated_frame = draw_basic_overlay(
                    frame=frame,
                    frame_index=index,
                    total_frames=metadata.frame_count,
                )
                annotated_frame = draw_tracks(
                    frame=annotated_frame,
                    frame_tracks=frame_tracks,
                )
                annotated_frame = draw_risk_overlay(
                    frame=annotated_frame,
                    risk_state=risk_state,
                )
                annotated_frame = draw_corridor_overlay(
                    frame=annotated_frame,
                    corridor_state=corridor_state,
                )
                annotated_frame = draw_plan_overlay(
                    frame=annotated_frame,
                    plan_state=plan_state,
                )

                writer.write(annotated_frame)
                frame_count += 1

                if index < 3:
                    print(
                        f"  Frame {index}: "
                        f"{scene_state.summary} | "
                        f"corridor={corridor_state.corridor_pressure}/{corridor_state.corridor_clear} | "
                        f"risk={risk_state.level} ({risk_state.score:.2f}) | "
                        f"plan={plan_state.maneuver} ({plan_state.urgency})"
                    )

            print(f"\nWrote {frame_count} annotated frames to {args.output}")


if __name__ == "__main__":
    main()