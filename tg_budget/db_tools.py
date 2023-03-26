from tg_budget import db, models


async def add_user(tg_id: int):
    with db.SessionLocal() as session:
        db_user = session.query(models.User).filter_by(tg_id=str(tg_id)).first()
        if not db_user:
            user = models.User(tg_id=str(tg_id))
            session.add(user)
        session.commit()


async def get_currencies():
    with db.SessionLocal() as session:
        db_currencies = session.query(models.Currency).all()
        if not db_currencies:
            return []
        return [db_currency.name for db_currency in db_currencies]
