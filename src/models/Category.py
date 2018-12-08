from sqlalchemy import Column, Integer, String

from .base import Base


class CategoryModel(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Integer, default=1)

    def __repr__(self):
        return "<CategoryModel(id='%s', name='%s', active='%d')>" % (
            self.id, self.name, self.active)
