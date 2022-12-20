from pydantic import BaseModel


class User(BaseModel):
    id: str
    user_id: str
    username: str
    first_name: str
    last_name: str
    about: str
    country: str
    state: str
    province: str
    city: str
    town: str
    latitude: str
    longitude: str
    updated_location: str
    ban: str
    # avatar: str
    # gatherings: list

    class Config:
        orm_mode = True
