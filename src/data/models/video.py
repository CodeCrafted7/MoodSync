from src.data.models.emotion import Emotions

class Video:
    def __init__(self, video_id: str, title: str, thumbnail: str, url: str, emotion: str):
        if emotion not in map(lambda e: e.value, Emotions):
            raise ValueError(f'Invalid emotion: {emotion}')
        self.video_id = video_id
        self.title = title
        self.thumbnail = thumbnail
        self.url = url
        self.emotion = emotion
    def __str__(self):
        return f'Video(video_id={self.video_id}, title={self.title}, thumbnail={self.thumbnail}, url={self.url}, emotion={self.emotion})'
