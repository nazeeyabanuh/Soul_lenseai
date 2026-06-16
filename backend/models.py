from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Analysis(Base):

    __tablename__ = "analysis"

    id = Column(Integer, primary_key=True)

    text = Column(String)

    emotion = Column(String)

    sentiment = Column(String)

    manipulation_type = Column(String)

    #created_at = Column( DateTime,default=datetime.utcnow)