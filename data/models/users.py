from sqlalchemy import Column, Integer, BigInteger, String, sql, Text

from data.db_gino import BaseModel


class Users(BaseModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(BigInteger, nullable=False, unique=True)
    username = Column(String)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    about = Column(Text)
    country = Column(String)
    state = Column(String)
    province = Column(String)
    city = Column(String)
    town = Column(String)
    address = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    updated_location = Column(String)
    ban = Column(Integer, nullable=False, server_default="0")

    query: sql.select
