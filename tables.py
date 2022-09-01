from sqlalchemy import Column, ForeignKey, Identity, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    address = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))
    email = Column(String(collation='SQL_Latin1_General_CP1_CI_AS'))

    invoices = relationship('Invoices', back_populates='customers')


class Employees(Base):
    __tablename__ = 'employees'

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    email = Column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))
    password = Column(String(255, 'SQL_Latin1_General_CP1_CI_AS'))


class Invoices(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    custid = Column(ForeignKey('customers.id'))
    invno = Column(Integer)
    amount = Column(Integer)

    customers = relationship('Customers', back_populates='invoices')
