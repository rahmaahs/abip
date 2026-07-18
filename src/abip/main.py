from __future__ import annotations

import argparse
from pathlib import Path

from abip.ingestion.video_reader import VideoReader


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
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("ABIP starting")
    print(f"Video: {args.video}")

    with VideoReader(args.video) as reader:
        metadata = reader.metadata()

        print("\nVideo metadata:")
        print(f"  Path: {metadata.path}")
        print(f"  Frames: {metadata.frame_count}")
        print(f"  FPS: {metadata.fps}")
        print(f"  Width: {metadata.width}")
        print(f"  Height: {metadata.height}")

        print("\nFirst 3 frames:")
        for index, frame in reader.frames():
            print(f"  Frame {index}: shape={frame.shape}")
            if index >= 2:
                break


if __name__ == "__main__":
    main()