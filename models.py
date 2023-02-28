from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from uuid import uuid4
from datetime import datetime
from database import Base
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

class Item(Base):
    __tablename__ = "items"
    id_post = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(String)
    post_date = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"id_post={self.id_post} username={self.username} caption={self.caption} post_date={self.post_date}"