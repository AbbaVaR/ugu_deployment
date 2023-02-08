import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from pydantic.class_validators import List
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.database import SessionLocal, engine



app = FastAPI()


# Dependency
def get_db():  # pragma: no cover
    """
    Задаем зависимость к БД. При каждом запросе будет создаваться новое
    подключение.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.Client)
def create_user(client: schemas.ClientCreate, bank_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_card(db, card_code=client.card_code)
    if db_user:
        raise HTTPException(status_code=400, detail="Client already registered")
    db_bank = crud.get_bank(db, bank_id=bank_id)
    if not db_bank:
        raise HTTPException(status_code=400, detail="Bank not found")
    return crud.create_client(db=db, client=client, bank_id=bank_id)


@app.post("/bank/", response_model=schemas.Bank)
def create_bank(bank: schemas.BankCreate, db: Session = Depends(get_db)):
    """
    Создание банка
    """
    return crud.create_bank(db=db, bank=bank)


@app.post("/atm/", response_model=schemas.Atm)
def create_atm(atm: schemas.AtmCreate, bank_id: int, db: Session = Depends(get_db)):
    """
    Создание банкомата
    """
    db_bank = crud.get_bank(db, bank_id=bank_id)
    if not db_bank:
        raise HTTPException(status_code=400, detail="Bank not found")
    return crud.create_atm(db=db, atm=atm, bank_id=bank_id)


@app.post("/operation/", response_model=schemas.Operation)
def create_operation(operation: schemas.OperationCreate, client_id: int, atm_id: int, db: Session = Depends(get_db)):
    """
    Создание банкомата
    """
    db_user = crud.get_user(db, user_id=client_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    db_atm = crud.get_atm(db, atm_id=atm_id)
    if not db_atm:
        raise HTTPException(status_code=400, detail="ATM not found")
    return crud.create_operation(db=db, operation=operation, client_id=client_id, atm_id=atm_id)


@app.get("/users/{user_id}", response_model=schemas.Client)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Получение пользователя по id, если такого id нет, то выдается ошибка
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_user


@app.get("/banks/{bank_id}", response_model=schemas.Bank)
def read_bank(bank_id: int, db: Session = Depends(get_db)):
    """
    Получение пользователя по id, если такого id нет, то выдается ошибка
    """
    db_bank = crud.get_bank(db, bank_id=bank_id)
    if db_bank is None:
        raise HTTPException(status_code=404, detail="Bank not found")
    return db_bank


@app.get("/atms/{atm_id}", response_model=schemas.Atm)
def read_atm(atm_id: int, db: Session = Depends(get_db)):
    """
    Получение пользователя по id, если такого id нет, то выдается ошибка
    """
    db_atm = crud.get_atm(db, atm_id=atm_id)
    if db_atm is None:
        raise HTTPException(status_code=404, detail="ATM not found")
    return db_atm


@app.get("/client_operation/{user_id}", response_model=List[schemas.Operation])
def read_client_operation(user_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Получение пользователя по id, если такого id нет, то выдается ошибка
    """
    db_operations = crud.get_operations_by_client(db=db, client_id=user_id, skip=skip, limit=limit)
    return db_operations


@app.get("/atm_operation/{atm_id}", response_model=List[schemas.Operation])
def read_client_operation(atm_id: int, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """
    Получение пользователя по id, если такого id нет, то выдается ошибка
    """
    db_operations = crud.get_operations_by_atm(db=db, atm_id=atm_id, skip=skip, limit=limit)
    return db_operations


@app.get("/operation/{operation_id}", response_model=schemas.Operation)
def read_atm(operation_id: int, db: Session = Depends(get_db)):
    db_operation = crud.get_operation(db, operation_id=operation_id)
    if db_operation is None:
        raise HTTPException(status_code=404, detail="Operation not found")
    return db_operation


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)  # pragma: no cover
