#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Fade Zhao'
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,Text
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    art_url = Column(String(255))
    artURL_id = Column(String(255))
    front_url = Column(String(255))
    front_img_path = Column(String(255))
    title = Column(String(255))
    up_count = Column(Integer)
    collect_count = Column(Integer)
    comment_count = Column(Integer)
    create_date = Column(String(255))
    category = Column(String(255))
    tags = Column(String(255))
    content = Column(Text)

class Interface:
    engine = create_engine("mysql+pymysql://root:zhaoyinghan@localhost/JobboleArticles?charset=utf8",encoding='utf8', echo=True)
    Session = sessionmaker(bind=engine)
    def __init__(self):
        '''初始化'''
        self.session = self.Session()
        # 创建表结构
        Base.metadata.create_all(self.engine)

    def add_data(self,data_dict):
        try:
            article = Article(**data_dict)
            self.session.add(article)
            self.session.commit()
        except Exception as e:
            print('发生错误：',e)
            self.session.rollback()


