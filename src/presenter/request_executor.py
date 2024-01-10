from concurrent.futures import Future, ThreadPoolExecutor
import threading
from collections import deque, Counter
from src.domain.video_service import VideoService
from src.data.models.video import Video
from typing import Callable
from sqlite3 import Connection


class Request:
    def __init__(self, emotion: str, future: Future):
        self.emotion = emotion
        self.future = future

class RequestExecutor:
    def __init__(self, executor: ThreadPoolExecutor, db: Connection):
        self.lock = threading.Lock()
        self.queue = deque(maxlen=10)
        self.prev_req : Request|None = None
        self.video_service = VideoService(db)
        self.executor = executor


    def request(self, emotion:str, callback: Callable[[list[Video]],None]):
        self.lock.acquire()
        self.queue.append(emotion)
        print('emotion queue', self.queue)
        freq_emotion,count = Counter(self.queue).most_common(1)[0]
        print('freq_emotion, count =', freq_emotion, count)

        if self.prev_req != None:
            if self.prev_req.emotion == freq_emotion:
                print('request not cancelled')
                self.lock.release()
                return
            else:
                print('request cancelled')
                self.prev_req.future.cancel()

        self.prev_req = Request(
            emotion=freq_emotion,
            future=self.executor.submit(self.request_executor, freq_emotion, callback)
        )
        self.lock.release()

    def request_executor(self, emotion: str, callback: Callable[[list[Video]],None]):
        #print('request_executor started', emotion)
        videos = self.video_service.get_videos(emotion)
        #print('request_executor ended', emotion, videos)
        callback(videos)
