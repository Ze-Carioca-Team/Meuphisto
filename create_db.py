from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, Float, create_engine, text

Base = declarative_base()

class Utterance(Base):
    __tablename__ = 'utterance'

    id = Column(Integer, primary_key=True)
    dialogue_id = Column(String)
    agent_id = Column(String)
    text = Column(String)
    episode_done = Column(Boolean)
    update_id = Column(String)
    timestamp = Column(Float)
    def __repr__(self):
       return "<Utterance(agent_id='%s', text='%s', timestamp='%s')>" % (
                            self.agent_id, self.text, self.timestamp)


def create_db(path: str):
    path = f"sqlite:///{path}/dialogues.db"
    engine = create_engine(path, echo=True)
    Base.metadata.create_all(engine)
    return path