import os
import googleapiclient.discovery as discovery
from src.data.models.video import Video

class Youtube:
    _api_service_name = 'youtube'
    _api_version = 'v3'
    _api_key = os.getenv("YT_API_KEY")
    def __init__(self):
        self.youtube = discovery.build(
            serviceName = self._api_service_name,
            version = self._api_version,
            developerKey = self._api_key,
        )
    def search(self, emotion: str, count: int=10):
        if count > 50:
            raise ValueError('Video count should be <= 50')
        query = f'{emotion} music'
        response = self.youtube.search().list(
            q = query,
            part = 'id, snippet',
            type = 'video',
            maxResults = count
        ).execute()
        videos = []
        for item in response['items']:
            video = Video(
                video_id=item['id']['videoId'],
                title=item['snippet']['title'],
                thumbnail=item['snippet']['thumbnails']['high']['url'],
                url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                emotion=emotion
            )
            videos.append(video)
        return videos
