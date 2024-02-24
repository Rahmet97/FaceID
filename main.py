import cv2
import customtkinter as ctk
from PIL import Image, ImageTk


class FaceRecognitionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Recognition App")
        self.geometry("640x480")
        self.resizable(False, False)

        self.video_frame = ctk.CTkFrame(self, width=640, height=480)
        self.video_frame.pack()

        self.cap = cv2.VideoCapture(0)
        self.canvas = ctk.CTkCanvas(self.video_frame, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                                    height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.delay = 5
        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=ctk.NW)

        self.after(self.delay, self.update)


def main():
    app = FaceRecognitionApp()
    app.mainloop()


if __name__ == "__main__":
    main()
