from src.entities.like import InsertLike, Like
from src.mappers.base import EntityMapper

insert_likes_mapper = EntityMapper(InsertLike)
likes_mapper = EntityMapper(Like)
