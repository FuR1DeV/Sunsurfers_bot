from sqlalchemy import Column, Integer, BigInteger, sql, Text, ForeignKey, String

from data.db_gino import BaseModel


class EventMembers(BaseModel):
    __tablename__ = "event_members"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False, unique=True)
    thailand = Column(Integer)
    thailand_info = Column(Text)
    india = Column(Integer)
    india_info = Column(Text)
    vietnam = Column(Integer)
    vietnam_info = Column(Text)
    philippines = Column(Integer)
    philippines_info = Column(Text)
    georgia = Column(Integer)
    georgia_info = Column(Text)
    indonesia = Column(Integer)
    indonesia_info = Column(Text)
    nepal = Column(Integer)
    nepal_info = Column(Text)
    morocco = Column(Integer)
    morocco_info = Column(Text)
    turkey = Column(Integer)
    turkey_info = Column(Text)
    mexico = Column(Integer)
    mexico_info = Column(Text)
    srilanka = Column(Integer)
    srilanka_info = Column(Text)

    query: sql.select


class SunGatherings(BaseModel):
    __tablename__ = "sungatherings"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String)
    country = Column(String)
    year = Column(Integer)

    query: sql.select


class SunUniversities(BaseModel):
    __tablename__ = "sununiversities"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String)
    country = Column(String)
    year = Column(Integer)

    query: sql.select


class SunAtoriums(BaseModel):
    __tablename__ = "sunatoriums"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String)
    country = Column(String)
    year = Column(Integer)

    query: sql.select


class YogaRetreats(BaseModel):
    __tablename__ = "yogaretreats"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String)
    country = Column(String)
    year = Column(Integer)

    query: sql.select


class SunWomanCamps(BaseModel):
    __tablename__ = "sunwomancamps"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String)
    country = Column(String)
    year = Column(Integer)

    query: sql.select


class Meetups(BaseModel):
    __tablename__ = "meetups"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String)
    country = Column(String)
    year = Column(Integer)

    query: sql.select
