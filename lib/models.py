from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, backref

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)
engine = create_engine("sqlite:///casting.db")
Session = sessionmaker(bind=engine)
session = Session()

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    character_name = Column(String, nullable=False)
    auditions = relationship('Audition', backref=backref('role', lazy=True))
    
    def actors(self):
        return [audition.actor for audition in self.auditions]

    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        hired_actors = [audition for audition in self.auditions if audition.hired]
        return hired_actors[0] if hired_actors else 'no actor has been hired for this role'
    
    def understudy(self):
        hired_actors = [audition for audition in self.auditions if audition.hired]
        return hired_actors[1] if len(hired_actors) > 1 else 'no actor has been hired for understudy for this role'


