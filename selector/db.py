from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


engine = create_engine('postgresql://postgres:pass@localhost:5432/postgres', echo=True)
Session = sessionmaker(bind=engine)


def add_column(table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))


class Developer(Base):
    __tablename__ = 'developers'
    login = Column(String, primary_key=True)

    def __init__(self, login, mentor):
        self.login = login

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.login, self.mentor)


class Mentor(Base):
    __tablename__ = 'mentors'
    login = Column(String, primary_key=True)

    def __init__(self, login):
        self.login = login

    def __repr__(self):
        return "<User('%s')>" % self.login


class Precedents(Base):
    __tablename__ = 'precedents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    developer = Column(String)
    mentor = Column(String)

    def __init__(self, developer, mentor):
        self.developer = developer
        self.mentor = mentor

    def __repr__(self):
        return "<User('%s', '%s')>" % self.developer, self.mentor


Base.metadata.create_all(engine)
