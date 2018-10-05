from app import db


class BaseModel(db.Model):
    """
    Base data model for all objects

    Defines `__repr__` & `json` methods or any common method that you need
    for all your models
    """
    __abstract__ = True

    # Define State Machine
    received, in_progress, failed, submitted, completed = (
        "received",
        "in_progress",
        "failed",
        "submitted",
        "completed",
    )

    STATE_CHOICES = (
        (received, received),
        (in_progress, in_progress),
        (failed, failed),
        (submitted, submitted),
        (completed, completed),
    )


class Messages(BaseModel):
    """
    Model for the `notifications` table
    """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_id = db.Column(db.String(50), nullable=False)
    sender_id = db.Column(db.String(50))
    recipient = db.Column(db.String(50))
    message = db.Column(db.String(200))
    priority = db.Column(db.String(50))
    status = db.Column(db.String(50), default="")
    # FSM state
    state = db.Column(db.String(50), default="")
    created_at = db.Column(db.DateTime, nullable=False)
    modified_at = db.Column(db.DateTime)
