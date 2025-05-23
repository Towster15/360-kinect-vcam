import queue
import pyvirtualcam
import numpy as np
from threading import Thread

from gui import GUI
from kinect_manager import KinectManager


if __name__ == "__main__":
    video_frame_queue = queue.Queue()
    tilt_queue = queue.Queue()

    kinect_manager = KinectManager(video_frame_queue, tilt_queue)
    kinect_manager.start()

    gui_thread = Thread(target=GUI, args=[tilt_queue])
    gui_thread.start()

    with pyvirtualcam.Camera(width=640, height=480, fps=60) as vcam:
        print(f"Using virtual camera: {vcam.device}")
        default_frame = np.zeros((vcam.height, vcam.width, 3), np.uint8)
        default_frame[:] = (100, 100, 100)
        data = None
        while gui_thread.is_alive():
            try:
                data = video_frame_queue.get_nowait()
                vcam.send(data)
            except queue.Empty:
                if data is None:
                    vcam.send(default_frame)
                else:
                    vcam.send(data)
            vcam.sleep_until_next_frame()

    kinect_manager.interrupt()
    kinect_manager.join()
