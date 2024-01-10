import customtkinter as ctk
from customtkinter.windows.widgets.image import CTkImage
from src.data.models.emotion import EmotionStats
from src.data.models.video import Video
from PIL import Image
import requests
from io import BytesIO
from concurrent import futures
from src.presenter.request_executor import RequestExecutor
from src.data.emotion_detector import EmotionDetector
from sqlite3 import Connection
import webbrowser


class App(ctk.CTk):

    def __init__(self, db:Connection):
        super().__init__()
        self.title('MoodSync')
        self.geometry('800x400')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.emotion_detector = EmotionDetector()
        self.emotion_detector_executor = futures.ThreadPoolExecutor(max_workers=1)
        self.request_executor_executor = futures.ThreadPoolExecutor(max_workers=1)
        self.thumbnail_image_request_executor = futures.ThreadPoolExecutor(max_workers=100)
        self.request_executor = RequestExecutor(self.request_executor_executor, db)

        self.emotion_detector_executor.submit(
            self.emotion_detector.start_detection, 
            5, # secs
            self.make_request
        )
        self.bind('<Destroy>', self.on_close)
        self.current_frame: ctk.CTkScrollableFrame | None = None
        self.videos: list[Video] = []

    def ui(self):
        videos = self.videos
        frame = ctk.CTkScrollableFrame(self)
        self.current_frame = frame
        frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
        frame.grid_columnconfigure((0,1), weight=1)
        #label = ctk.CTkLabel(self, text='Videos')
        #label.grid(column=0, row=0)

        title_text = ''
        if len(videos) == 0:
            title_text = 'Nothing to show'
        else:
            title_text = f'Showing recommendations based on your "{videos[0].emotion}" mood'

        image_components = list(self.thumbnail_image_request_executor.map(self.get_thumbnail, videos))
        title_label = ctk.CTkLabel(frame, text=title_text, font=("Helvetica", 16))
        title_label.grid(column=0, row=0, columnspan=2, sticky='ew', padx=2, pady=2)
        for idx, (video, img) in enumerate(zip(videos, image_components)):
            img_btn = ctk.CTkButton(frame, image=img, text=video.title, compound='top', command=self.redirect_user_wrapper(video.url))
            img_btn.grid(column=idx%2, row=idx//2+1, sticky='ew', padx=2, pady=2, columnspan=1)


    def redirect_user_wrapper(self, url):
        def redirect():
            webbrowser.open(url=url)
        return redirect


    def get_thumbnail(self, video: Video) -> CTkImage:
        parsed_img = Image.open(BytesIO(requests.get(video.thumbnail).content))
        img_component = ctk.CTkImage(parsed_img, parsed_img, (400, 300))
        return img_component

    def on_close(self, _):
        self.emotion_detector.stop_detection()
        self.request_executor_executor.shutdown(wait=False, cancel_futures=True)
        self.emotion_detector_executor.shutdown(wait=False, cancel_futures=True)

    def make_request(self, emotion_stats: EmotionStats):
        print("making request")
        self.request_executor.request(
            emotion=emotion_stats.dominant_emotion.emotion.value,
            callback=self.refresh
        )

    # make changes to reuse frame and destroy children instead
    def refresh(self, videos: list[Video]):
        self.videos = videos
        self.after(500, self.ui)
