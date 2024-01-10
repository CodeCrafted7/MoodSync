from sqlite3 import Connection
from src.data.youtube import Youtube
from src.data.videos import VideoTable
from src.data.models.emotion import Emotions

class VideoService:
    THRESHOLD_PER_EMOTION_VIDEO_COUNT = 50
    def __init__(self, db:Connection) -> None:
        self.video_table = VideoTable(db)
        self.youtube = Youtube()

    def get_videos(self, emotion: str):
        print('get_videos started', emotion)
        if emotion not in list(map(lambda e: e.value, Emotions)):
            raise ValueError('Not a valid emotion')

        current_unwatched_video_count = self.video_table.get_count(emotion=emotion, watched=False)
        print('current_unwatched_video_count', current_unwatched_video_count)

        print('get_videos ended', emotion)
        #return []
        if current_unwatched_video_count < self.THRESHOLD_PER_EMOTION_VIDEO_COUNT:
            print('Querying new videos from youtube')
            videos = self.youtube.search(emotion=emotion, count=50)
            self.video_table.save_videos(videos)
        else:
            print('Querying videos from DB')
        return self.video_table.get_videos(emotion=emotion, watched=False)

    #def get_videos(self, emotion: str, callback: Callable[[list[Video]],None]):
    #    if emotion not in list(map(lambda e: e.value, Emotions)):
    #        raise ValueError('Not a valid emotion')

    #    current_unwatched_video_count = self.video_table.get_count(emotion=emotion, watched=False)
    #    print('current_unwatched_video_count', current_unwatched_video_count)
    #    if current_unwatched_video_count < self.THRESHOLD_PER_EMOTION_VIDEO_COUNT:
    #        print('Querying new videos from youtube')
    #        videos = self.youtube.search(emotion=emotion, count=50)
    #        self.video_table.save_videos(videos)
    #    else:
    #        print('Querying videos from DB')
    #    callback(self.video_table.get_videos(emotion=emotion, watched=False))
