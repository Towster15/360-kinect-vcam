import queue
import cv2
import numpy as np
import pyvirtualcam
from pykinect import nui

WIDTH = 640
HEIGHT = 480
FPS = 30


def video_frame_ready(frame):
    video = np.empty((HEIGHT, WIDTH, 4), np.uint8)
    frame.image.copy_bits(video.ctypes.data)
    video = cv2.cvtColor(cv2.flip(video, 1), cv2.COLOR_RGBA2BGR)
    video_frame_queue.put(video)


kinect = nui.Runtime()
kinect.video_frame_ready += video_frame_ready
kinect.video_stream.open(
    nui.ImageStreamType.Video,
    2,
    nui.ImageResolution.Resolution640x480,
    nui.ImageType.Color,
)

video_frame_queue = queue.Queue()

with pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=FPS) as vcam:
    print(f"Using virtual camera: {vcam.device}")
    default_frame = np.zeros((vcam.height, vcam.width, 3), np.uint8)
    while True:
        try:
            data = video_frame_queue.get_nowait()
            vcam.send(data)
        except queue.Empty:
            c = (vcam.frames_sent % 100) / 100
            default_frame[:] = (c * 100, c * 100, c * 100)
            vcam.send(default_frame)
        vcam.sleep_until_next_frame()
