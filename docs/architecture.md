# ABIP Phase 1 Architecture

## Purpose

ABIP is a software-first bicycle intelligence system for cycling scene understanding. Phase 1 focuses on prerecorded video input and builds the core autonomy pipeline before any hardware deployment.

The system should take cycling footage as input and produce:

* object detections
* object tracks
* scene-state summaries
* risk scores
* recommended actions

## High-Level Pipeline

**Video Input**
→ **Frame Ingestion**
→ **Object Detection**
→ **Object Tracking**
→ **Scene Understanding**
→ **Risk Assessment**
→ **Decision Engine**
→ **Annotated Output Video + Logs**

## Design Principles

1. **Modular**

   * Each stage should be independently testable.
   * Modules should communicate through clear data structures, not ad hoc globals.

2. **Swappable**

   * Detection, tracking, and decision logic should be replaceable without rewriting the whole system.

3. **Traceable**

   * Every frame should be inspectable through logs or saved outputs.

4. **Hardware-ready**

   * The software layout should later map cleanly onto a real robot stack.

## Proposed Modules

### 1. `ingestion`

Responsible for reading video files and converting them into frames.

Inputs:

* video path

Outputs:

* frames
* timestamps
* metadata such as FPS and resolution

### 2. `perception`

Responsible for detecting relevant objects in each frame.

Initial target classes:

* pedestrian
* car
* bike

Outputs:

* bounding boxes
* class labels
* confidence scores

### 3. `tracking`

Responsible for maintaining object identity across frames.

Outputs:

* stable track IDs
* object trajectories
* basic motion history

### 4. `scene`

Responsible for turning raw detections and tracks into a compact scene representation.

Example scene facts:

* object is ahead
* object is close to lane
* object is approaching
* object is crossing

### 5. `risk`

Responsible for converting scene state into numerical risk levels.

Example outputs:

* low
* medium
* high
* collision-risk score

### 6. `planning`

Responsible for mapping risk and scene state to an action recommendation.

Example outputs:

* continue
* slow down
* brake
* steer left
* steer right

### 7. `visualization`

Responsible for drawing boxes, labels, track IDs, and decision overlays onto video frames.

### 8. `evaluation`

Responsible for logging outputs, comparing runs, and summarizing failures.

## Data Flow Contract

Each stage should receive a clean input and return a clean output.

Example:

* `ingestion` returns a frame
* `perception` returns detections
* `tracking` returns tracked objects
* `scene` returns structured scene state
* `risk` returns scores
* `planning` returns an action

This keeps the pipeline understandable and testable.

## Phase 1 Scope

Phase 1 will use:

* prerecorded cycling videos
* pretrained object detection
* one tracking method
* rule-based risk assessment
* rule-based decision logic

Phase 1 will not yet include:

* real bicycle control
* live sensor fusion
* on-bike embedded deployment
* end-to-end learned driving policy

## First Engineering Milestone

The first usable milestone is a video processing pipeline that can:

1. load a cycling clip
2. detect relevant objects
3. track them over time
4. output a simple scene summary
5. assign a risk level
6. recommend an action
7. save an annotated result video

## Immediate Next Steps

1. create the main pipeline entry point
2. define configuration values
3. add a placeholder pipeline runner
4. prepare sample video paths for testing
5. start the video ingestion module
