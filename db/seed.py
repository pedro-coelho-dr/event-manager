import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.models import User, Category, Event, EventAttendees, db
from app.config import Config

def seed_data():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()


    users = [
        User(username='user1', role='user'),
        User(username='user2', role='user'),
        User(username='producer1', role='producer'),
        User(username='producer2', role='producer'),
    ]

    session.add_all(users)

    categories = [
        Category(name='Música'),
        Category(name='Teatro'),
        Category(name='Cinema'),
        Category(name='Esportes'),
        Category(name='Arte'),
        Category(name='Tecnologia'),
        Category(name='Culinária'),
    ]

    session.add_all(categories)
    
    session.commit()

    producers = users[2:]
    categories = session.query(Category).all()

    for i in range(10):
        event = Event(
            producer_id=random.choice(producers).id,
            category_id=random.choice(categories).id,
            name=f'Evento {i + 1}',
            date=date.today() + timedelta(days=random.randint(1, 30))
        )
        session.add(event)
    
    session.commit()

    events = session.query(Event).all()
    for event in events:
        attendees_count = random.randint(1, 2)
        attendees = random.sample(users[:2], attendees_count)
        for attendee in attendees:
            session.add(EventAttendees(event_id=event.id, user_id=attendee.id))

    
    session.commit()

    print("Seeding completed.")

if __name__ == "__main__":
    seed_data()
