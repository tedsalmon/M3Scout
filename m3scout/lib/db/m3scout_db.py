from sqlalchemy import Integer, Unicode, Boolean, DateTime, Date, Text, Enum
from sqlalchemy import ForeignKey, Column, BigInteger, Float
from sqlalchemy.ext.declarative import declarative_base

from m3scout.lib.db.db_helper import TableInitiator, DatabaseInitiator

Base = declarative_base(cls=TableInitiator)

class Items(Base):
    _id = Column(Integer(), primary_key=True)
    id = Column(Unicode())
    source = Column(Unicode())
    price = Column(Unicode())
    link = Column(Unicode())
    short_text = Column(Unicode())
    body = Column(Unicode())
    info = Column(Unicode())
    status = Column(Integer())
    md5sum = Column(Unicode())
    
class M3ScoutDB(DatabaseInitiator):
    ''' DB ORM  '''
    
    def __init__(self, engine=False, ):
        '''
            Define DATAIT Database Structure and attach an engine
            @param Dialect  engine  Pre-established db engine,
                                        False to create one
        '''
        super(M3ScoutDB, self).__init__(__name__, Base, engine)