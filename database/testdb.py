#!/usr/bin/python
import orm
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

if __name__ == '__main__':
    engine = create_engine('sqlite://')
    engine.echo = True
    session_factory = sessionmaker(bind=engine)
    session = scoped_session(session_factory)
    orm.Base.metadata.create_all(engine)
    user1 = orm.user(email="pddenhar@gmail.com", password="peter")
    user1.vehicles.append(orm.vehicle(model="volvo"))
    user1.vehicles.append(orm.vehicle(model="saab"))
    session.merge(user1)
    session.commit()
    