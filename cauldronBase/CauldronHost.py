from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from Base import Base

class CauldronHost(Base):
    __tablename__ = "CauldronHost"
    id = Column(Integer, Sequence("cauldronhost_seq"), primary_key=True);
    ip = Column(String);
    def __repr__(self):
        return "CAULDRONHOST: " + str(self.id) + ", " + self.ip
