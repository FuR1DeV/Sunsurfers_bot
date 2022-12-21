from sqlalchemy import Column, Integer, BigInteger, sql, Text, ForeignKey, String

from data.db_gino import BaseModel


class Sungatherings(BaseModel):
    __tablename__ = "sungatherings"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False, unique=True)
    thailand = Column(Integer, server_default="0")
    thailand_info = Column(Text)
    india = Column(Integer, server_default="0")
    india_info = Column(Text)
    vietnam = Column(Integer, server_default="0")
    vietnam_info = Column(Text)
    philippines = Column(Integer, server_default="0")
    philippines_info = Column(Text)
    georgia = Column(Integer, server_default="0")
    georgia_info = Column(Text)
    indonesia = Column(Integer, server_default="0")
    indonesia_info = Column(Text)
    nepal = Column(Integer, server_default="0")
    nepal_info = Column(Text)
    morocco = Column(Integer, server_default="0")
    morocco_info = Column(Text)
    turkey = Column(Integer, server_default="0")
    turkey_info = Column(Text)
    mexico = Column(Integer, server_default="0")
    mexico_info = Column(Text)
    srilanka = Column(Integer, server_default="0")
    srilanka_info = Column(Text)

    query: sql.select


class Events(BaseModel):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String)
    country = Column(String)
    year = Column(Integer)

    query: sql.select
