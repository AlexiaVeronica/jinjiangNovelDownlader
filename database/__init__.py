from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database_models import Base, ChapterSql, BookInfoSql, CatalogueSql

# check_same_thread:False 允许多线程
check_same_thread = False
sqlite_name = "jinjiang.db"

engine = create_engine('sqlite:///{}'.format(sqlite_name), connect_args={'check_same_thread': check_same_thread})

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

__all__ = ["session", "ChapterSql", "BookInfoSql", "CatalogueSql"]
