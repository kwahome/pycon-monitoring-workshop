from app import db


class BaseModel(db.Model):
    """
    Base data model for all objects

    Defines `__repr__` & `json` methods or any common method that you need
    for all your models
    """
    __abstract__ = True


class Notification(BaseModel):
    """
    Model for the `notifications` table
    """
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payload = db.Column(db.String(255), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
