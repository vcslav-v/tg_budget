from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    pass


users_currencies = Table(
    'users_currencies',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('currency_id', ForeignKey('currencies.id'), primary_key=True),
)


class User(Base):
    '''Users.'''

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(unique=True)

    currencies: Mapped[List['Currency']] = relationship(
        secondary=users_currencies, back_populates='users'
    )


class Income(Base):
    '''Incomes.'''
    __tablename__ = 'incomes'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'))
    currency: Mapped['Currency'] = relationship(back_populates='incomes')


class Currency(Base):
    '''Currencies.'''

    __tablename__ = 'currencies'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[List[User]] = relationship(
        secondary=users_currencies, back_populates='currencies'
    )

    exchange_rate: Mapped[List['ExchangeRate']] = relationship(back_populates='currency')

    incomes: Mapped[List['Income']] = relationship(back_populates='currency')


class ExchangeRate(Base):
    '''Exchange Rates'''

    __tablename__ = 'exchange_rates'

    id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[datetime]
    value: Mapped[float]

    currency_id: Mapped[int] = mapped_column(ForeignKey('currencies.id'))
    currency: Mapped['Currency'] = relationship(back_populates='exchange_rate')
