from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from . import engine

Session = scoped_session(sessionmaker(bind=engine))

__all__ = ['Session', 'ithAtom', 'ithCategory', 'ithCategValue', 'ithWordType', 'ithSlot', 'ithMorpheme', 'ithMorphemeSlot']

Base = declarative_base()

class ithWordType(Base):
    '''Class representing a type of a word'''
    __tablename__ = 'ith_wordtype'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    description = Column(Text)

wordtypes_categories = Table('ith_wordtype_category', Base.metadata,
                        Column('wordtype_id', Integer, ForeignKey('ith_wordtype.id')),
                        Column('category_id', Integer, ForeignKey('ith_category.id')))

class ithCategory(Base):
    '''Class representing a grammatical category'''
    __tablename__ = 'ith_category'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    description = Column(Text)
    word_types = relationship('ithWordType', secondary=wordtypes_categories, backref='categories')

class ithSlot(Base):
    '''Class representing a morphological slot in a word'''
    __tablename__ = 'ith_slot'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(8))
    description = Column(Text)
    
    wordtype_id = Column(Integer, ForeignKey('ith_wordtype.id'))
    wordtype = relationship('ithWordType', backref='slots')

class ithMorpheme(Base):
    '''Class representing a morpheme'''
    __tablename__ = 'ith_morpheme'
    
    id = Column(Integer, primary_key=True)
    morpheme = Column(String(8))

class ithMorphemeSlot(Base):
    __tablename__ = 'ith_morpheme_slot'

    id = Column(Integer, primary_key=True)
    morpheme_id = Column(Integer, ForeignKey('ith_morpheme.id'))
    slot_id = Column(Integer, ForeignKey('ith_slot.id'))

    morpheme = relationship('ithMorpheme', backref='slots')
    slot = relationship('ithSlot', backref='morphemes')
    
morpheme_slot_atom = Table('ith_morpheme_slot_atom', Base.metadata,
                        Column('atom_id', Integer, ForeignKey('ith_atom.id')),
                        Column('morpheme_slot_id', Integer, ForeignKey('ith_morpheme_slot.id')))

class ithAtom(Base):
    __tablename__ = 'ith_atom'
    
    id = Column(Integer, primary_key=True)
    morpheme_slots = relationship('ithMorphemeSlot', secondary=morpheme_slot_atom, backref='atoms')    

atom_value = Table('ith_atom_value', Base.metadata,
                        Column('atom_id', Integer, ForeignKey('ith_atom.id')),
                        Column('categvalue_id', Integer, ForeignKey('ith_categvalue.id')))

class ithCategValue(Base):
    '''Class representing a value of a grammatical category'''
    __tablename__ = 'ith_categvalue'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(8))
    name = Column(String(128))
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('ith_category.id'))
    category = relationship('ithCategory')
    atoms = relationship('ithAtom', secondary=atom_value, backref='values')
