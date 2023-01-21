from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    def __repr__(self):  # pragma: no cover
        return f"<{type(self).__name__}(id={self.id})>"


class Bank(BaseModel):
    __tablename__ = "banks"
    name = Column(String, index=True)
    address = Column(String, index=True)
    atms = relationship("Atm", back_populates="bank")
    clients = relationship("Client", back_populates="bank")


class Atm(BaseModel):
    __tablename__ = "atms"
    address = Column(String, index=True)
    bank_id = Column(Integer,  ForeignKey("banks.id"), nullable=False)
    bank = relationship("Bank", back_populates="atms")
    operations = relationship("Operation", back_populates="atm")


class Client(BaseModel):
    __tablename__ = "clients"
    card_code = Column(String, index=True, unique=True)
    second_name = Column(String, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    patronymic = Column(String, index=True)
    address = Column(String, index=True)
    bank_id = Column(Integer,  ForeignKey("banks.id"), nullable=False)
    bank = relationship("Bank", back_populates="clients")
    operations = relationship("Operation", back_populates="client")


class Operation(BaseModel):
    __tablename__ = "operations"
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    client = relationship("Client", back_populates="operations")
    atm_id = Column(Integer, ForeignKey("atms.id"), nullable=False)
    atm = relationship("Atm", back_populates="operations")
    date = Column(DateTime)
    commission = Column(Boolean)
    amount = Column(Integer, nullable=True)
