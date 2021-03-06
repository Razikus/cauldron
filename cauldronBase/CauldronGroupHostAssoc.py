from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship
from Base import Base
from helpers import to_json
from Base import ma
from CauldronGroup import CauldronGroupSchema

class CauldronGroupHostAssoc(Base):
    __tablename__ = "CauldronGroupHostAssoc"
    host_id = Column(Integer, ForeignKey("CauldronHost.id"), primary_key = True)
    group_id = Column(Integer, ForeignKey("CauldronGroup.id"), primary_key = True)

    group = relationship("CauldronGroup", back_populates = "hosts")
    host = relationship("CauldronHost", back_populates = "groups")
    def __repr__(self):
        return "CAULDRONGROUPHOSTASSOC: " + str(self.host_id) + ", " + str(self.group_id)

class CauldronGroupHostAssocSchema(ma.Schema):
    group = ma.Nested(CauldronGroupSchema, only = ["name"]) 
    name = ma.Nested("CauldronHostSchema", only = ["name"]) 

