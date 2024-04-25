import queue
import cv2
import numpy as np
from pykinect import nui


class Kinect:
    def __init__(self, frame_queue: queue.Queue) -> None:
        self.__frame_queue = frame_queue
        self.__kinect = nui.Runtime()
        self.__kinect.camera.set_elevation_angle(0)

        self.__kinect.video_frame_ready += self.__video_frame_ready
        self.__kinect.video_stream.open(
            nui.ImageStreamType.Video,
            2,
            nui.ImageResolution.Resolution640x480,
            nui.ImageType.Color,
        )

    def __video_frame_ready(self, frame) -> None:
        video = np.empty((480, 640, 4), np.uint8)
        frame.image.copy_bits(video.ctypes.data)
        video = cv2.cvtColor(cv2.flip(video, 1), cv2.COLOR_RGBA2BGR)
        self.__frame_queue.put(video)

    def adjust_angle(self, angle: int = 0) -> None:
        if -27 <= angle <= 27:
            self.__kinect.camera.set_elevation_angle()

    def close(self):
        self.__kinect.close()


if __name__ == "__main__":
    pass
