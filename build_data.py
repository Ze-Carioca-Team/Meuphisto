from sqlalchemy import create_engine
from utils.gen_stories import populate_stories
from utils.schema import Base, Story
import argparse

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--num_stories', default=25, type=int,
                        help='an integer for number of stories to generate')
    parser.add_argument('--name', default="dialogues.db", type=str,
                        help='name to save database.')

    args = parser.parse_args()
    path = "sqlite:///"+args.name
    engine = create_engine(path, echo=True)
    Base.metadata.drop_all(bind=engine, tables=[Story.__table__])
    Base.metadata.create_all(engine)
    populate_stories(path, args.num_stories)

if __name__ == "__main__":
    main()