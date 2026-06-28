from pydantic import BaseModel
from typing import Optional


class PokemonType(BaseModel):
    name: str


class PokemonStat(BaseModel):
    name: str
    base_stat: int


class PokemonAbility(BaseModel):
    name: str
    is_hidden: bool


class PokemonSummary(BaseModel):
    id: int
    name: str
    image: Optional[str]
    types: list[PokemonType]


class PokemonDetail(BaseModel):
    id: int
    name: str
    height_meters: float
    weight_kg: float
    base_experience: Optional[int]
    image: Optional[str]
    image_shiny: Optional[str]
    types: list[PokemonType]
    stats: list[PokemonStat]
    abilities: list[PokemonAbility]