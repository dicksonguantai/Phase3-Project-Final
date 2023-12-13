from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, MP, Bill, Vote

fake = Faker()

# Create an SQLAlchemy engine
engine = create_engine('sqlite:///parliamentary_bill_tracker.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def create_fake_data():
    session = Session()

    # Generate fake MPs
    for _ in range(10):
        mp = MP(name=fake.name())
        session.add(mp)

    session.commit()

    # Generate fake bills and votes
    mps = session.query(MP).all()
    for _ in range(20):
        bill = Bill(title=fake.catch_phrase(), sponsor_id=fake.random_element(mps).id)
        session.add(bill)

        for _ in range(fake.random_int(min=5, max=15)):
            mp = fake.random_element(mps)
            vote = Vote(mp_id=mp.id, bill_id=bill.id, vote_status=fake.boolean())
            session.add(vote)

    session.commit()
    session.close()

if __name__ == '__main__':
    create_fake_data()
