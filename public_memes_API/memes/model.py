from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Meme(Base):
    __tablename__ = "memes"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True, nullable=False)
    text = Column(String)

    def __str__(self):
        return f"Meme {self.file_name} #id={self.id}"
