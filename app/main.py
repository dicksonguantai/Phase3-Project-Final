from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Boolean
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,  declarative_base

Base = declarative_base()

class MP(Base):
    __tablename__ = 'mps'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    party_affiliation = Column(String)

    bills = relationship("Bill", back_populates="sponsor")
    votes = relationship("Vote", back_populates="mp")


    def __repr__(self):
        return f"<MP(id={self.id}, name={self.name}, party ={self.party_affiliation})>"
    
class Bill(Base):
    __tablename__ = 'bills'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    sponsor_id = Column(Integer, ForeignKey('mps.id'))
    sponsor = relationship("MP", back_populates="bills")
    votes = relationship("Vote", back_populates="bill")


class Vote(Base):
    __tablename__ = 'votes'

    id = Column(Integer, primary_key=True)
    mp_id = Column(Integer, ForeignKey('mps.id'))
    bill_id = Column(Integer, ForeignKey('bills.id'))
    vote_status = Column(Boolean)  # True for 'yes', False for 'no'
    mp = relationship("MP", back_populates="votes")
    bill = relationship("Bill", back_populates="votes")
