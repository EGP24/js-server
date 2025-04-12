from src.entities.card import Card, InsertCard
from src.mappers.base import EntityMapper

insert_cards_mapper = EntityMapper(InsertCard)
cards_mapper = EntityMapper(Card)
