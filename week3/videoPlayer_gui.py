import cv2
import os
from tkinter import Tk, Button, Label, StringVar, Frame, X
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import datetime

class VideoPlayerRecorder:
    def __init__(self, window, title):
        self.window = window
        self.window.title(title)
        self.label = Label(self.window)
        self.label.pack()

        # Combobox for listing video files
        self.video_list_var = StringVar()
        self.video_list = Combobox(self.window, textvariable=self.video_list_var, state="readonly")
        self.video_list.pack(side='top')
        self.update_video_list()

        bottom_frame = Frame(self.window)
        bottom_frame.pack(side='bottom', fill=X)

        # Control buttons
        self.btn_play = Button(bottom_frame, text="Play", command=self.play_video)
        self.btn_play.pack(side='left', padx=5, pady=5)

        self.btn_pause = Button(bottom_frame, text="Pause", command=self.pause_video)
        self.btn_pause.pack(side='left', padx=5, pady=5)

        self.btn_stop = Button(bottom_frame, text="Stop", command=self.stop_video)
        self.btn_stop.pack(side='left', padx=5, pady=5)

        self.btn_record = Button(bottom_frame, text="Record", command=self.start_recording)
        self.btn_record.pack(side='left', padx=5, pady=5)

        self.filter_list_var = StringVar()
        self.filter_list = Combobox(bottom_frame, textvariable= self.filter_list_var, state="readonly")
        self.filter_list.pack(side='right')
        filter_names = ['None',
                        'Gray',
                        'Black&White'
                        ]
        self.filter_list['values'] = filter_names
        if filter_names:
            self.filter_list.current(0)

        label = Label(bottom_frame, text="Filters:")
        label.pack(side='right', padx=(0, 10))

        self.cap = None
        self.paused = False
        self.recording = False
        self.out = None

    def get_filter(self, frame):
        filter_dict = {
            'None': frame,
            'Gray': cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        }
        return filter_dict[self.filter_list.get()]
    def update_video_list(self):
        video_files = [file for file in os.listdir('.') if file.endswith(('.avi', '.mp4'))]
        self.video_list['values'] = video_files
        if video_files:
            self.video_list.current(0)

    def play_video(self):
        if self.recording:
            # Don't allow video playback during recording
            return

        if not self.cap or not self.cap.isOpened() or self.paused:
            # If the video capture is not initialized, initialize it with the selected video file
            selected_video = self.video_list.get()
            if selected_video:
                if self.cap:
                    self.cap.release()
                self.cap = cv2.VideoCapture(selected_video)

        if self.cap and self.cap.isOpened():
            # If the video capture is initialized and opened, resume playing from the current frame
            self.paused = False
            self.update_frame()

    def pause_video(self):
        self.paused = True

    def stop_video(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
            self.label.config(image='')  # Clear the label
            self.update_video_list()  # Refresh the video list in case new videos were added

    def start_recording(self):
        self.recording = True
        self.paused = False
        if not self.cap or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)  # Open default webcam
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(f'recording-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.mp4', fourcc, 20.0, (640, 480))
        self.update_frame()

    def stop_recording(self):
        self.recording = False
        if self.out:
            self.out.release()
            self.out = None

        if self.cap:
            self.cap.release()
            self.cap = None

        self.update_video_list()  # Refresh the video list to include the newly recorded video
        self.btn_record['state'] = 'normal'

    def update_frame(self):
        if self.cap and self.cap.isOpened() and not self.paused:
            ret, frame = self.cap.read()
            if ret:
                if self.recording:
                    _frame = self.get_filter(frame)
                    self.out.write(_frame)
                frame = self.get_filter(frame)
                photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.label.config(image=photo)
                self.label.image = photo
                self.window.after(10, self.update_frame)
            else:
                self.stop_video()

def main():
    root = Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    app = VideoPlayerRecorder(root, "Tkinter Video Player and Recorder")
    root.mainloop()

if __name__ == '__main__':
    main()
