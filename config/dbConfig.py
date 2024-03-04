from urllib.parse import quote
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import pytz

timezone = pytz.timezone('Asia/Kolkata')


def get_epoch(timeD):
  current_time = datetime.now(timezone)
  y_date = current_time.date() - timedelta(days=timeD)
  e_epoch = int(
      datetime.strptime(datetime.strftime(y_date, "%d/%m/%Y 23:59:59"),
                        "%d/%m/%Y %H:%M:%S").timestamp()) * 1000
  s_epoch = int(
      datetime.strptime(datetime.strftime(y_date, "%d/%m/%Y 00:00:00"),
                        "%d/%m/%Y %H:%M:%S").timestamp()) * 1000
  return s_epoch, e_epoch


def db_config():
  db_engine = create_engine(
      'postgresql+psycopg2://spotify_feb_28_user:%s@dpg-cnfar0gl5elc7393103g-a.oregon-postgres.render.com/spotify_feb_28'
      % quote('vY99EVlPq24E6yKiuIBnRo8OYApVIUpb'))
  db_con = db_engine.connect()
  return db_con, db_engine
