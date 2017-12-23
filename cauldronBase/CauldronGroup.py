from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship
from Base import Base
from helpers import to_json
from Base import ma

class CauldronGroup(Base):
    __tablename__ = "CauldronGroup"
    id = Column(Integer, Sequence("cauldrongroup_seq"), primary_key=True);
    name = Column(String);
    hosts = relationship("CauldronGroupHostAssoc", back_populates = "group") 
    def __repr__(self):
        return "CAULDRONGROUP: " + str(self.id) + ", " + self.name

class CauldronGroupSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

