from sqlalchemy.orm import Session
from src import models, schemas


def create_bank(db: Session, bank: schemas.BankCreate):
    """
    Добавление нового банка
    """
    db_data = models.Bank(name=bank.name, address=bank.address)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def create_atm(db: Session, atm: schemas.AtmCreate, bank_id: int):
    """
    Добавление нового банкомата
    """
    db_data = models.Atm(**atm.dict(), bank_id=bank_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def create_client(db: Session, client: schemas.ClientCreate, bank_id: int):
    """
    Добавление нового пользователя
    """
    db_data = models.Client(**client.dict(), bank_id=bank_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def create_operation(db: Session, operation: schemas.OperationCreate, client_id: int, atm_id: int):
    """
    Добавление новой операции
    """
    db_data = models.Operation(**operation.dict(), client_id=client_id, atm_id=atm_id)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_user(db: Session, user_id: int):
    """
    Получить пользователя по его id
    """
    return db.query(models.Client).filter(models.Client.id == user_id).first()


def get_user_by_card(db: Session, card_code: str):
    """
    Получить пользователя по его карте
    """
    return db.query(models.Client).filter(models.Client.card_code == card_code).first()


def get_bank(db: Session, bank_id: int):
    """
    Получить банк по его id
    """
    return db.query(models.Bank).filter(models.Bank.id == bank_id).first()


def get_atm(db: Session, atm_id: int):
    """
    Получить АТМ по его id
    """
    return db.query(models.Atm).filter(models.Atm.id == atm_id).first()


def get_operation(db: Session, operation_id: int):
    """
    Получить АТМ по его id
    """
    return db.query(models.Operation).filter(models.Operation.id == operation_id).first()


def get_operations_by_client(db: Session, client_id: int, skip: int = 0, limit: int = 100):
    """
    Получить операций по клиенту
    """
    return db.query(models.Operation).filter(models.Operation.client_id == client_id).offset(skip).limit(limit).all()


def get_operations_by_atm(db: Session, atm_id: int, skip: int = 0, limit: int = 100):
    """
    Получить операций по банкомату
    """
    return db.query(models.Operation).filter(models.Operation.atm_id == atm_id).offset(skip).limit(limit).all()
