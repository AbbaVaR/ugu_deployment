from datetime import datetime
from pydantic import BaseModel
from typing import Union


class OperationBase(BaseModel):
    date: datetime
    commission: bool
    amount: Union[None, int]


class OperationCreate(OperationBase):
    pass


class Operation(OperationBase):
    id: int
    client_id: int
    atm_id: int

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    card_code: str
    second_name: str
    name: str
    patronymic: Union[None, str]
    address: str


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int
    bank_id: int
    operations: list[Operation]

    class Config:
        orm_mode = True


class AtmBase(BaseModel):
    address: str


class AtmCreate(AtmBase):
    pass


class Atm(AtmBase):
    id: int
    bank_id: int
    operations: list[Operation]

    class Config:
        orm_mode = True


class BankBase(BaseModel):
    name: str
    address: str


class BankCreate(BankBase):
    pass


class Bank(BankBase):
    id: int
    atms: list[Atm]
    clients: list[Client]

    class Config:
        orm_mode = True






