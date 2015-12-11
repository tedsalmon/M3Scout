# -*- coding: utf-8 -*-
import os
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declared_attr, DeclarativeMeta

from inspect import getmembers, isclass
from sys import modules

class DatabaseInitiator(object):
    '''
        Parent class for ORM dbs
    '''
    
    DB_FILE = '/etc/m3scout/m3data.db'
    
    def __init__(self, module_name, Base, engine=False):
        ''' Attach table objects    '''
        if not engine:
            engine = create_engine(
                'sqlite:///%s' % self.DB_FILE, poolclass=NullPool
            )
        self._base = Base
        self._engine = engine
        self._db_sess = scoped_session(
            sessionmaker(bind=engine, expire_on_commit=False)
        )
        Base.query = self._db_sess.query_property()
        Base.metadata.create_all(bind=engine)
        is_table = lambda cls: isclass and isinstance(cls, DeclarativeMeta)
        for table in getmembers(modules[module_name], is_table):
            name, cls = table
            setattr(self, name, cls)


    def session_bind(self, ):
        '''
            Re-bind the query_property before each request
            This should only be used by Flask
        '''
        self._base.query = self.get_session().query_property()


    def session_unbind(self, ):
        '''
            Kill the scoped session after the request
            This should only be used by Flask
        '''
        session = self.get_session()
        try:
            session.commit()
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.remove()
            


    def insert(self, obj, should_commit=True, ):
        '''
            Insert a table object
            @param  mixed   sqlalchemy.Table object (or list of them) to Insert into DB
            @param  bool    Should this transaction be auto-commited? Default is True
        '''
        if isinstance(obj, list):
            self.get_session().add_all(obj)
        else:
            self.get_session().add(obj)
        self.get_session().flush()
        if should_commit:
            self.commit()
            
    def delete(self, obj, ):
        '''
            Delete a table object
            @param  mixed   sqlalchemy.Table object (or list of them) to Delete from DB
        '''
        if isinstance(obj, list):
            for item in obj:
                self.get_session().delete(item)
        else:
            self.get_session().delete(obj)
        self.commit()
        
    def get_session(self, ):
        '''
            Return session if required
            @return Current database session
        '''
        return self._db_sess
    
    def commit(self, obj=[]):
        '''
            Commit to session, refresh obj if defined
            @param  mixed   obj DB obj to refresh, or list of them
        '''
        try:
            self.get_session().commit()
            if isinstance(obj, list):
                for i in obj:
                    self.get_session().refresh(i)
            else:
                self.get_session().refresh(obj)
        except SQLAlchemyError:
            self.rollback()
            raise
        finally:
            self.get_session().remove()

    def rollback(self, ):
        '''
            Rollback DB Changes
        '''
        self.get_session().rollback()


class TableInitiator(object):
    '''
        Parent for SQL ORM tables
    '''
    
    # Default MySQL Opts
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset':'utf8',
    }
    __mapper_args__= {'always_refresh': True} #< Default Opts
    
    @declared_attr
    def __tablename__(cls):
        '''
            Return the class name as our table name
            @return str Name of the class
        '''
        return cls.__name__
    
    def __repr__(self, ):
        '''
            Return repr of the table object
            @return str Repr of table
        '''
        return_str = []
        for col in self.__table__.c:
            return_str.append('%s: %r' % (col.name, getattr(self, col.name)))
        return '<%s %s>' % (self.__tablename__, ' '.join(return_str))
