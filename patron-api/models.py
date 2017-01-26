from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

class Patron(Base):
    __tablename__ = 'patron'

    id = Column(Integer, primary_key=True)
    client = Column(String)
    contact = Column(String)
    contactphone = Column(String)
    contactemail = Column(String)
    # relational data
    user = relationship(
        "User", back_populates='patron',
        cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return "<Patron(id='%s', client='%s', contact='%s', user='%s')>" % (
            self.id, self.client, self.contact, self.user
        )


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    team = Column(String)
    patron_id = Column(Integer, ForeignKey('patron.id'))
    # relational data
    patron = relationship("Patron", back_populates="user")

    def __repr__(self):
        return "<User(id='%s', name='%s', team='%s', patron_id='%s')>" % (
            self.id, self.name, self.team, self.patron_id
        )
