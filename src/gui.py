import queue
import tkinter as tk
import tkinter.ttk as ttk


class GUI:
    def __init__(self, tilt_queue: queue.Queue) -> None:
        self.__window = tk.Tk()
        self.__window.title("Kinect Controller")
        # self.__frame = self.__window.frame

        self.__frame = ttk.Frame()

        self.__tilt_angle = tk.IntVar()
        self.__tilt_scale = tk.Scale(
            master=self.__frame,
            orient="vertical",
            length=200,
            from_=27,
            to=-27,
            variable=self.__tilt_angle,
            command=self.__tilt_scale_to_int,
        )
        self.__tilt_scale.grid(row=0, column=0, rowspan=3)

        self.__tilt_top_label = ttk.Label(master=self.__frame, text="+27°")
        self.__tilt_top_label.grid(row=0, column=1)
        self.__tilt_middle_label = ttk.Label(master=self.__frame, text="0°")
        self.__tilt_middle_label.grid(row=1, column=1)
        self.__tilt_bottom_label = ttk.Label(master=self.__frame, text="-27°")
        self.__tilt_bottom_label.grid(row=2, column=1)

        self.__close_button = ttk.Button(
            master=self.__frame, text="Quit", command=self.__close
        )
        self.__close_button.grid(row=3, column=0, columnspan=2, pady=(5, 0))

        self.__tilt_queue = tilt_queue

        self.__frame.pack(padx=10, pady=10)

        self.__window.mainloop()

    def __tilt_scale_to_int(self, arg) -> None:
        with self.__tilt_queue.mutex:
            self.__tilt_queue.queue.clear()
        self.__tilt_queue.put(arg)

    def __close(self) -> None:
        self.__window.destroy()


if __name__ == "__main__":
    gui = GUI(queue.Queue())
