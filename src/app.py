from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(filename='.env'))

from src.presenter.home import App
import sqlite3 as sql


if __name__ == '__main__':
    db = sql.connect('moodsync.db', check_same_thread=False)
    #vs = VideoService()
    #print(vs.get_videos('happy'))
    app = App(db)
    app.mainloop()
