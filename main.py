import asyncio
import cv2
import json
import numpy as np
import pathlib
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from ultralytics import YOLO

app = FastAPI()
model = YOLO("yolov8s.pt")
executor = ThreadPoolExecutor(max_workers=2)


def detect(frame_bytes: bytes) -> list[dict]:
    arr = np.frombuffer(frame_bytes, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if frame is None:
        return []
    results = model(frame, conf=0.4, verbose=False)[0]
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        detections.append({
            "x1": round(x1), "y1": round(y1),
            "x2": round(x2), "y2": round(y2),
            "label": model.names[int(box.cls[0])],
            "conf": round(float(box.conf[0]), 2),
        })
    return detections


@app.get("/")
async def index():
    return HTMLResponse(pathlib.Path("index.html").read_text())


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    loop = asyncio.get_event_loop()
    try:
        while True:
            data = await ws.receive_bytes()
            detections = await loop.run_in_executor(executor, detect, data)
            await ws.send_text(json.dumps(detections))
    except WebSocketDisconnect:
        pass
    except Exception:
        pass
