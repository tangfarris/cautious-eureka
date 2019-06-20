import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
class Posts(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    content = Column(String(250), nullable=False)

# creates an engine that stores data in the local dir's db file
engine = create_engine('sqlite:///sqlalchemy_example.db')

# equivalent to create table statements in raw sql
Base.metadata.create_all(engine)