"""empty message

Revision ID: first_data
Revises: e3b39a6439b4
Create Date: 2022-11-13 12:24:12.171841

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import orm

from src.models import Bank, Atm, Client

# revision identifiers, used by Alembic.
revision = 'first_data'
down_revision = 'e3b39a6439b4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    avr_bank = Bank(name='AVR-bank', address='Yugorskya 999')
    abbavar_bank = Bank(name='AbbaVaR-bank', address='Chehova 809')

    session.add_all([avr_bank, abbavar_bank])
    session.flush()

    avr_atm_1 = Atm(address='Yugorskya 999', bank_id=avr_bank.id)
    avr_atm_2 = Atm(address='Yugorskya 75', bank_id=avr_bank.id)
    abbavar_atm_1 = Atm(address='Chehova 809', bank_id=abbavar_bank.id)

    ivanov = Client(card_code='0000000', second_name='Ivanov', name='Tester',
                    patronymic='Testorovich', address='Testovaya 55', bank_id=avr_bank.id)
    petrov = Client(card_code='0000001', second_name='Petrov', name='Tester',
                    address='Testovaya 78', bank_id=abbavar_bank.id)

    session.add_all([avr_atm_1, avr_atm_2, abbavar_atm_1, ivanov, petrov])
    session.commit()


def downgrade() -> None:
    pass
