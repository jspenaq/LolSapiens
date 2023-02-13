from fastapi import APIRouter
from backend.api.constants import (
    s,
    champion_id_param,
    lane_param,
    tier_param,
    queue_mode_param,
    keystone_id_param,
    spicy_param,
)


build_router = APIRouter()


@build_router.get("/build")
def create_build(
    champion_id: str = champion_id_param,
    lane: str = lane_param,
    tier: str = tier_param,
    mode: str = queue_mode_param,
    keystone_id: int = keystone_id_param,
    spicy: int = spicy_param,
):
    return s.generate_build(champion_id, lane, tier, mode, keystone_id, spicy)


@build_router.get("/keystones")
def get_keystones(
    champion_id: str = champion_id_param,
    lane: str = lane_param,
    tier: str = tier_param,
    queue_mode: str = queue_mode_param,
    spicy: int = spicy_param,
):
    return s._get_champion_runes(champion_id, lane, tier, queue_mode, spicy)


# @build_router.get("/runes")
# def get_runes(
#     champion_id: str = champion_id_param,
#     lane: str = lane_param,
#     tier: str = tier_param,
#     queue_mode: str = queue_mode_param,
#     spicy: int = spicy_param,
# ):
#     return s._get_champion_runes(champion_id, lane, tier, queue_mode, spicy)
