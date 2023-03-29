from sqlalchemy import Column, String, Integer, Text

from config.config import DEFAULT_PATH_LOGO
from models.base import BaseModel


class Platform(BaseModel):
    __tablename__ = 'platforms'
    igdb_id = Column(String(length=50), default="")
    sgdb_id = Column(String(length=50), default="")
    slug = Column(String(length=500), primary_key=True)
    name = Column(String(length=500), default="")
    path_logo = Column(Text, default=DEFAULT_PATH_LOGO)
    n_roms = Column(Integer, default=0)