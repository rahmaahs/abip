from __future__ import annotations

from typing import Any, Iterable

from ultralytics import YOLO

from abip.perception.detections import BoundingBox, Detection, FrameDetections


class YOLODetector:
    def __init__(
        self,
        model_name: str = "yolov8n.pt",
        confidence_threshold: float = 0.35,
        target_classes: Iterable[str] = ("person", "car", "bicycle"),
    ) -> None:
        if not model_name.endswith(".pt"):
            model_name = f"{model_name}.pt"

        self.model_name = model_name
        self.confidence_threshold = confidence_threshold
        self.target_classes = set(target_classes)
        self.model = YOLO(self.model_name)

    def detect(self, frame_index: int, frame: Any) -> FrameDetections:
        results = self.model.predict(
            frame,
            conf=self.confidence_threshold,
            verbose=False,
        )

        result = results[0]
        detections: list[Detection] = []
        names = result.names

        for box in result.boxes:
            class_id = int(box.cls.item())
            class_name = names[class_id]

            if self.target_classes and class_name not in self.target_classes:
                continue

            confidence = float(box.conf.item())
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]

            detections.append(
                Detection(
                    class_name=class_name,
                    confidence=confidence,
                    box=BoundingBox(
                        x1=x1,
                        y1=y1,
                        x2=x2,
                        y2=y2,
                    ),
                )
            )

        return FrameDetections(
            frame_index=frame_index,
            detections=detections,
        )