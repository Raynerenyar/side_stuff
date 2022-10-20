from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


engine = create_engine('sqlite:///:memory:', echo=True) # echo -> false in production


Session = sessionmaker(bind=engine)
session = Session()


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)

    def __repr__(self):
        return f'User {self.name}'
    

    @classmethod
    def find_by_name(cls, session, name):
        return session.query(cls).filter_by(name=name).all()

Base.metadata.create_all(engine)


user = User(name='John Snow', password='johnspassword')
session.add(user)

print(user.id)  # None

session.commit()

query = session.query(User).filter_by(name='John')
query.count()
session.query(User).filter(User.name=='John').first()
User.find_by_name(session, 'John')