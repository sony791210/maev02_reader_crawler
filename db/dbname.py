from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, TIMESTAMP, Text, func, \
    UniqueConstraint
from sqlalchemy.dialects.mysql import LONGTEXT
BaseModel = declarative_base()
engine = create_engine("mysql+pymysql://root:19990704@mysql:3306/app", echo=True)


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class Novel_crawler_zhou(BaseModel):
    __tablename__ = 'novel_crawler_zhou'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nid = Column(Integer, comment="小說id")
    pid = Column(Integer, comment="頁數id")
    novel_id = Column(Integer, comment="小說id")
    create_time = Column(TIMESTAMP, server_default=func.now())


class Novel_crawler_sto(BaseModel):
    __tablename__ = 'novel_crawler_sto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nid = Column(Integer, comment="小說id")
    pid = Column(Integer, comment="頁數id")
    create_time = Column(TIMESTAMP, server_default=func.now())


class Novel(BaseModel):
    __tablename__ = 'novel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(60), comment="章節")
    content = Column(LONGTEXT, comment="內容")
    page = Column(Integer, comment="小說章節")
    novel_name_id = Column(String(60), comment="小說章節")
    create_time = Column(TIMESTAMP, server_default=func.now())
    update_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    UniqueConstraint(page, novel_name_id)


class Novel_list(BaseModel):
    __tablename__ = 'novel_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    novel_name = Column(String(60), comment="小說名稱")
    novel_name_id = Column(String(60), comment="小說id")
    create_time = Column(TIMESTAMP, server_default=func.now())


class Novel_info(BaseModel):
    __tablename__ = 'novel_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(60), comment="名稱")
    novel_name_id = Column(String(60), comment="小說id")
    comic_name_id = Column(String(60), comment="漫畫id")
    title_photo_url = Column(LONGTEXT, comment="封面圖片")
    data_update_time = Column(TIMESTAMP, comment="更新時間")
    author = Column(String(60), comment="作者")
    long_info = Column(Text, comment="簡介")
    tags = Column(String(60), comment="tags")
    cat = Column(String(60), comment="類型")
    content_type = Column(String(60), comment="text or png")
    crawbing = Column(Integer, comment="是否抓取中")
    update_time = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    UniqueConstraint(novel_name_id, comic_name_id)


