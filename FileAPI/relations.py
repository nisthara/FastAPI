# from sqlalchemy import Column, ForeignKey, Integer, Table
# from sqlalchemy.orm import declarative_base, relationship

# Base = declarative_base()

# class Parent(Base):
    # __tablename__ = "parent"
    # id = Column(Integer, primary_key=True)
    # children = relationship("Child")


# class Child(Base):
    # __tablename__ = "child"
    # id = Column(Integer, primary_key=True)
    # parent_id = Column(Integer, ForeignKey("parent.id"))
    


import urllib
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy.orm import relationship

params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
                                 "SERVER=localhost;"
                                 "DATABASE=estdb;"
                                 "UID=sa;"
                                 "PWD=estuate@123")
engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
print("mssql+pyodbc:///?odbc_connect={}".format(params))
class Customer(Base):
   __tablename__ = 'customers'

   id = Column(Integer, primary_key = True)
   name = Column(String)
   address = Column(String)
   email = Column(String)

class Invoice(Base):
   __tablename__ = 'invoices'
   
   id = Column(Integer, primary_key = True)
   custid = Column(Integer, ForeignKey('customers.id'))
   invno = Column(Integer)
   amount = Column(Integer)
   customer = relationship("Customer", back_populates = "invoices")

Customer.invoices = relationship("Invoice", order_by = Invoice.id, back_populates = "customer")
Base.metadata.create_all(engine)