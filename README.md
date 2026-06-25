---
title: Real-Time Object Detection
emoji: 🎥
colorFrom: green
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# Real-Time Object Detection

🚀 **[Live demo on Hugging Face Spaces](https://huecraft143-yolo-webcam-demo.hf.space)**

> ⚠️ **Heads up:** the demo runs on the Hugging Face free tier (CPU only, no GPU), so inference is slow (~5-7 fps). For the best experience, **run it locally** following the instructions below — you'll get smooth real-time detection at full speed. 🐢

Real-time object detection via webcam using **YOLOv8s** and **WebSockets**. Deployed on Hugging Face Spaces.

The browser streams frames from your webcam to a Python backend over a WebSocket. YOLOv8s runs inference server-side and returns bounding boxes; the frontend draws them directly on a canvas at full render FPS.

## Stack

| Layer | Tech |
|-------|------|
| Model | Ultralytics YOLOv8s (COCO, 80 classes) |
| Backend | Python · FastAPI · OpenCV |
| Transport | WebSocket (binary frames → JSON detections) |
| Frontend | Vanilla HTML/JS · Canvas API |
| Deploy | Docker · Hugging Face Spaces |

## How it works

```
Webcam → canvas.toBlob() → WebSocket (JPEG) → YOLOv8s → JSON → draw boxes
```

1. The browser captures webcam video and encodes frames as JPEG (~10 fps) over a WebSocket.
2. The server decodes each frame with OpenCV, runs YOLOv8s inference, and returns a JSON array of detections `[{x1, y1, x2, y2, label, conf}]`.
3. The frontend renders the live video to a canvas and overlays labelled bounding boxes at the display frame rate (~30 fps).

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
# open http://localhost:8000
```

## Run with Docker

```bash
docker build -t yolo-demo .
docker run -p 7860:7860 yolo-demo
# open http://localhost:7860
```
