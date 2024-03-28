import cv2
import tkinter as tk
from tkinter import filedialog
import datetime

class VideoRecorderApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.video_source = 0
        self.vid = None

        self.btn_record = tk.Button(window, text="Record", width=50, command=self.open_camera)
        self.btn_record.pack(padx=10, pady=10)

        # Button for opening the video player
        self.btn_player = tk.Button(window, text="Open Player", width=50, command=self.open_player)
        self.btn_player.pack(padx=10, pady=10)

        self.window.mainloop()

    def open_camera(self):
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", self.video_source)

        self.record_video()

    def record_video(self):
        frame_width = int(self.vid.get(3))
        frame_height = int(self.vid.get(4))
        out = cv2.VideoWriter(f'{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.mp4',
                              cv2.VideoWriter_fourcc(*'mp4v'), 10, (frame_width, frame_height))

        recording = True
        while recording:
            ret, frame = self.vid.read()
            if ret:
                out.write(frame)
                cv2.imshow("Recording... Press 'q' to stop", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    recording = False
            else:
                break

        self.vid.release()
        out.release()
        cv2.destroyAllWindows()

    def open_player(self):
        # Open file dialog to select the video file
        file_path = filedialog.askopenfilename()
        if file_path:
            self.play_video(file_path)

    def play_video(self, file_path):
        cap = cv2.VideoCapture(file_path)
        last_frame = None
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        seek_amount = int(fps * 5)  # Seek amount in frames, here set to 5 seconds

        while True:
            ret, frame = cap.read()

            if ret:
                last_frame = frame
                cv2.imshow("Video (Use arrow keys to seek, 'p' to pause/play, 'r' to replay, 'q' to quit)", frame)

                key = cv2.waitKey(25) & 0xFF

                if key == ord('p'):  # Pause the video
                    cv2.waitKey(-1)  # Wait indefinitely until any key is pressed to resume

                elif key == ord('q'):  # Quit the player
                    break

                elif key == ord('b'):  # Left arrow key for seeking backward
                    current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, current_frame - seek_amount))

                elif key == ord('f'):  # Right arrow key for seeking forward
                    current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                    cap.set(cv2.CAP_PROP_POS_FRAMES, min(total_frames, current_frame + seek_amount))

            else:  # Video has ended, display last frame and wait for user input
                key = cv2.waitKey(-1)  # Wait indefinitely for user input

                if key == ord('r'):  # Replay the video
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Move the video to the first frame
                elif key == ord('q'):  # Quit the player
                    break

        cap.release()
        cv2.destroyAllWindows()


def main():
    root = tk.Tk()
    app = VideoRecorderApp(root, "Video Recorder and Player")

if __name__ == '__main__':
    main()
