import sqlite3 as sql
from sqlite3 import Connection
from src.data.models.emotion import Emotions
from src.data.models.video import Video

class VideoTable:
    def __init__(self, db: Connection):
        self.db = db
        table_exists = self.db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='videos';").fetchone()
        if not table_exists:
            print('Creating Video Table')
            self.db.execute('''
                CREATE TABLE videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
                    video_id TEXT NOT NULL UNIQUE, 
                    title TEXT NOT NULL, 
                    thumbnail TEXT NOT NULL,
                    url TEXT NOT NULL,
                    emotion TEXT CHECK( emotion in ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')) NOT NULL,
                    watched INTEGER NOT NULL CHECK( watched in (0, 1) ) DEFAULT 0
                );
            '''
            )
            self.db.commit()
            return
        print('Video Table Already Exists')

    def parse(self, videos: list[tuple]):
        parsed_value : list[Video]= []
        for video in videos:
            _, video_id, title, thumbnail, url, emotion, _ = video 
            parsed_value.append(Video(video_id=video_id, title=title, thumbnail=thumbnail, url=url, emotion=emotion))
        return parsed_value

    def save_videos(self, videos: list[Video]):
        if len(videos) == 0:
            return

        data = list(map(lambda video: (video.video_id, video.title, video.thumbnail, video.url, video.emotion),videos))
        print('videos to be saved',data)
        self.db.executemany('''
            INSERT OR IGNORE INTO videos (video_id, title, thumbnail, url, emotion) VALUES (?, ?, ?, ?, ?);
        ''', data)
        self.db.commit()

    def save_video(self, video: Video):
        self.db.execute('''
            INSERT OR IGNORE INTO videos (video_id, title, thumbnail, url, emotion) VALUES (?, ?, ?, ?, ?);
        ''', (video.video_id, video.title, video.thumbnail, video.url, video.emotion))
        self.db.commit()

    def get_videos(self, emotion:None|str=None, watched:None|bool=None, page=0, page_size=10):
        if emotion != None and watched != None:
            w = 0
            if watched:
                w = 1
            return self.parse(self.db.execute('''
                SELECT * FROM videos WHERE watched = ? AND emotion = ? LIMIT ? OFFSET ?;
            ''', (w, emotion, page_size, page*page_size)).fetchall())

        if watched != None:
            w = 0
            if watched:
                w = 1
            return self.parse(self.db.execute('''
                SELECT * FROM videos WHERE watched = ? LIMIT ? OFFSET ?; 
            ''', (w, page_size, page*page_size)).fetchall())

        if emotion != None:
            return self.parse(self.db.execute('''
                SELECT * FROM videos WHERE emotion = ? LIMIT ? OFFSET ?; 
            ''', (emotion, page_size, page*page_size)).fetchall())

        return self.parse(self.db.execute('''
            SELECT * FROM videos LIMIT ? OFFSET ?;
        ''', (page_size, page*page_size)).fetchall())

    def get_count(self, emotion:str|None=None, watched:None|bool=None) -> int:
        if emotion != None and emotion not in list(map(lambda e: e.value, Emotions)):
            raise ValueError('Not a valid emotion')

        count = 0
        if emotion!=None and watched!=None:
            w = 0
            if watched:
                w = 1
            count, = self.db.execute('''
                SELECT COUNT(*) FROM videos WHERE emotion = ? AND watched = ?;
            ''', (emotion, w)).fetchone()
            return count

        if emotion != None:
            count, = self.db.execute('''
                SELECT COUNT(*) FROM videos WHERE emotion = ?;
            ''', (emotion)).fetchone()
            return count

        if watched != None:
            w = 0
            if watched:
                w = 1
            count, = self.db.execute('''
                SELECT COUNT(*) FROM videos WHERE watched = ?;
            ''', str(w)).fetchone()
            return count

        count,  = self.db.execute('''
            SELECT COUNT(*) FROM videos;
        ''').fetchone()

        return count

