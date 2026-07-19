from __future__ import annotations

import argparse
from pathlib import Path

from abip.ingestion.video_reader import VideoReader
from abip.ingestion.video_writer import VideoWriter
from abip.perception.fake_detector import FakeDetector
from abip.visualization.annotator import draw_basic_overlay, draw_detections


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
        default=Path("outputs/videos/detections.mp4"),
        help="Path to the output video file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("ABIP starting")
    print(f"Input video: {args.video}")
    print(f"Output video: {args.output}")

    detector = FakeDetector()

    with VideoReader(args.video) as reader:
        metadata = reader.metadata()

        print("\nVideo metadata:")
        print(f"  Path: {metadata.path}")
        print(f"  Frames: {metadata.frame_count}")
        print(f"  FPS: {metadata.fps}")
        print(f"  Width: {metadata.width}")
        print(f"  Height: {metadata.height}")

        with VideoWriter(args.output, metadata) as writer:
            print("\nRunning fake detection...")
            frame_count = 0

            for index, frame in reader.frames():
                frame_detections = detector.detect(frame_index=index, frame=frame)

                annotated_frame = draw_basic_overlay(
                    frame=frame,
                    frame_index=index,
                    total_frames=metadata.frame_count,
                )
                annotated_frame = draw_detections(
                    frame=annotated_frame,
                    frame_detections=frame_detections,
                )

                writer.write(annotated_frame)
                frame_count += 1

                if index < 3:
                    print(
                        f"  Frame {index}: "
                        f"{len(frame_detections.detections)} fake detections"
                    )

            print(f"\nWrote {frame_count} annotated frames to {args.output}")


if __name__ == "__main__":
    main()