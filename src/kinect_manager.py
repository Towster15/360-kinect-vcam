import queue
from threading import Thread
from time import sleep

from kinect import Kinect


class KinectManager(Thread):
    def __init__(self, frame_queue: queue.Queue, tilt_queue: queue.Queue) -> None:
        super().__init__()
        self.__quit = False
        self.__kinect = Kinect(frame_queue)
        self.__tilt_queue = tilt_queue

    def run(self) -> None:
        while not self.__quit:
            try:
                self.__kinect.adjust_angle(self.__tilt_queue.get_nowait())
            except queue.Empty:
                # busy waiting solves everything
                sleep(0.1)

    def interrupt(self) -> None:
        self.__quit = True
