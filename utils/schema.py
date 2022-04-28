from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey

Base = declarative_base()

class Story(Base):
    __tablename__ = "story"

    id = Column(Integer, primary_key=True)
    dialog_id = Column(String(64))
    text_client = Column(String)
    text_system = Column(String)

    def __repr__(self):
       return "<Story(id='%s', dialog_id='%s')>" % (self.id, self.dialog_id)


class Utterance(Base):
    __tablename__ = "utterance"

    id = Column(Integer, primary_key=True)
    dialogue_id = Column(String, ForeignKey('story.dialog_id'),
                        nullable=False)
    agent_id = Column(String, nullable=False)
    turn = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    episode_done = Column(Boolean)
    update_id = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(),
                    nullable=False)

    def __repr__(self):
       return "<Utterance(agent_id='%s', text='%s', timestamp='%s')>" % (
                            self.agent_id, self.text, self.timestamp)