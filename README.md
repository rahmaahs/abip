# Autonomous Bicycle Intelligence Platform (ABIP)

ABIP is a robotics and computer vision project for cycling scene understanding. The long-term goal is to build a modular autonomy stack for an electric bicycle, starting with video-based perception and decision-making on a laptop before moving to real hardware later.

## Project Goal

This project aims to develop a bicycle intelligence system that can:

* detect pedestrians, cars, bikes, and road features
* track objects over time
* understand the current traffic scene
* estimate risk
* recommend actions such as slowing down, braking, or steering away

The first stage is software-only and runs on prerecorded cycling video. Hardware deployment will come later.

## Phase 1 Scope

Phase 1 focuses on building the “brain” of the system using video input only.

### Inputs

* GoPro footage
* cycling videos
* public driving or riding datasets
* other prerecorded scene videos

### Core pipeline

* video ingestion
* object detection
* object tracking
* scene state construction
* risk scoring
* decision recommendation
* annotated video output

### Example outputs

* `Slow down`
* `Brake`
* `Steer left`
* `Steer right`
* `Pedestrian entering lane`
* `Vehicle approaching from behind`
* `High collision risk`

## What This Project Is Not Yet

This project is **not**:

* a ChatGPT wrapper
* a full autonomous bicycle
* a hardware control system
* a sensor-fusion stack yet
* a model-train-from-scratch project
* a finished real-world safety system

Phase 1 is about building a strong software architecture that can later support real robotics and embedded deployment.

## Architecture

The system is designed like a real autonomy stack:

Camera / Video Input
→ Perception
→ Object Tracking
→ Scene Understanding
→ Risk Assessment
→ Path / Action Planning
→ Decision Engine
→ Recommended Action

The architecture is intentionally modular so each component can be improved or replaced later without rewriting the whole system.

## Tech Stack

Planned core tools for Phase 1:

* Python
* OpenCV
* PyTorch
* YOLO-based object detection
* Multi-object tracking
* NumPy / SciPy
* Git and GitHub

Optional additions later:

* FastAPI
* Docker
* PyTest
* ROS 2
* ONNX / TensorRT for deployment

## Repository Structure

```text
abip/
├── README.md
├── .gitignore
├── configs/
├── data/
│   ├── raw/
│   └── samples/
├── docs/
├── outputs/
│   ├── logs/
│   └── videos/
├── src/
│   └── abip/
│       ├── __init__.py
│       ├── main.py
│       └── utils.py
└── tests/
```

## Current Status

* Project repo initialized
* Basic folder structure created
* README in progress
* Phase 1 development starting with the video pipeline and project scaffolding

## Near-Term Plan

1. Build the video ingestion pipeline
2. Add object detection
3. Add tracking
4. Build scene-state logic
5. Add a rule-based risk engine
6. Generate a polished demo video
7. Document the system clearly

## Why This Project

This project is meant to grow over time into something that reflects real robotics software design. It is intended to strengthen both software engineering and machine learning skills while leaving room for future hardware deployment and research-level extensions.
