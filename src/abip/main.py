from __future__ import annotations

import argparse
from pathlib import Path

from abip.ingestion.video_reader import VideoReader
from abip.ingestion.video_writer import VideoWriter


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
        default=Path("outputs/videos/copy.mp4"),
        help="Path to the output video file",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("ABIP starting")
    print(f"Input video: {args.video}")
    print(f"Output video: {args.output}")

    with VideoReader(args.video) as reader:
        metadata = reader.metadata()

        print("\nVideo metadata:")
        print(f"  Path: {metadata.path}")
        print(f"  Frames: {metadata.frame_count}")
        print(f"  FPS: {metadata.fps}")
        print(f"  Width: {metadata.width}")
        print(f"  Height: {metadata.height}")

        with VideoWriter(args.output, metadata) as writer:
            print("\nCopying frames...")
            frame_count = 0

            for index, frame in reader.frames():
                writer.write(frame)
                frame_count += 1

                if index < 3:
                    print(f"  Frame {index}: shape={frame.shape}")

            print(f"\nWrote {frame_count} frames to {args.output}")


if __name__ == "__main__":
    main()