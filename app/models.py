
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List


class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
 

service_mechanics = db.Table(
    'service_mechanics',
    Base.metadata,
    db.Column('ticket_id',db.ForeignKey('service_tickets.id')),
    db.Column('mechanic_id',db.ForeignKey('mechanics.id'))
)

class Customer(Base):
    __tablename__ = 'customers'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(db.String(255),nullable=False)
    email:Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
    address:Mapped[str] = mapped_column(db.String(455),nullable=False)
    
    service_tickets:Mapped[List['Invoice']] = db.relationship(back_populates='customer')
    
class Invoice(Base):
    __tablename__ = 'service_tickets'
    
    id:Mapped[int] = mapped_column(primary_key=True)
    customer_id:Mapped[int] = mapped_column(db.ForeignKey('customers.id'))
    ticket_date:Mapped[date] = mapped_column(db.Date)
    
    customer:Mapped['Customer'] = db.relationship(back_populates='service_tickets')
    mechanics:Mapped[List['Mechanics']] = db.relationship(secondary=service_mechanics,back_populates='service_tickets')
    
    
class Mechanics(Base):
    __tablename__ = 'mechanics'
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(db.String(255), nullable=False)
    email:Mapped[str] = mapped_column(db.String(255), nullable=False)
    phone:Mapped[int] = mapped_column(db.String(4), nullable=False)
    salary:Mapped[int] = mapped_column(db.String(4), nullable=False)
    
    service_tickets:Mapped[List['Invoice']] = db.relationship(secondary=service_mechanics, back_populates='mechanics')
