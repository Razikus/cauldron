from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship
from Base import Base
from helpers import to_json
from Base import ma
from CauldronGroupHostAssoc import CauldronGroupHostAssocSchema

class CauldronHost(Base):
    __tablename__ = "CauldronHost"
    id = Column(Integer, Sequence("cauldronhost_seq"), primary_key=True);
    ip = Column(String);
    groups = relationship("CauldronGroupHostAssoc", back_populates = "host") 
    def __repr__(self):
        return "CAULDRONHOST: " + str(self.id) + ", " + self.ip

class CauldronHostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ip', 'groups')
    groups = ma.Nested(CauldronGroupHostAssocSchema)

