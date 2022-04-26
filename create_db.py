from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float, create_engine

Base = declarative_base()

class Utterance(Base):
    __tablename__ = 'utterance'

    id = Column(Integer, primary_key=True)
    agent_id = Column(String)
    text = Column(String)
    episode_done = Column(Boolean)
    update_id = Column(String)
    timestamp = Column(Float)
    def __repr__(self):
       return "<Utterance(agent_id='%s', text='%s', timestamp='%s')>" % (
                            self.agent_id, self.text, self.timestamp)


def main():
    engine = create_engine("sqlite:///dialogues.db", echo=True, future=True)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    main()