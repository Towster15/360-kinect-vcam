import queue
import pyvirtualcam
import numpy as np

from gui import GUI
from kinect import Kinect


if __name__ == "__main__":
    video_frame_queue = queue.Queue()
    tilt_queue = queue.Queue()

    gui = GUI(tilt_queue)
    kinect = Kinect(video_frame_queue)

    with pyvirtualcam.Camera(width=640, height=480, fps=30) as vcam:
        print(f"Using virtual camera: {vcam.device}")
        default_frame = np.zeros((vcam.height, vcam.width, 3), np.uint8)
        while True:
            try:
                kinect.adjust_angle(tilt_queue.get_nowait())
            except queue.Empty:
                pass
            try:
                data = video_frame_queue.get_nowait()
                vcam.send(data)
            except queue.Empty:
                c = (vcam.frames_sent % 100) / 100
                default_frame[:] = (c * 100, c * 100, c * 100)
                vcam.send(default_frame)
            vcam.sleep_until_next_frame()
