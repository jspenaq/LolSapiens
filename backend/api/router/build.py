from fastapi import APIRouter
from backend.api.constants import (
    champion_id_param,
    keystone_id_param,
    lane_param,
    queue_mode_param,
    s,
    spicy_param,
    tier_param,
)
from backend.api.utils import convert_queue_mode

build_router = APIRouter()


@build_router.get("/build", tags=["champion"])
def create_build(
    champion_id: str = champion_id_param,
    lane: str = lane_param,
    tier: str = tier_param,
    mode: str = queue_mode_param,
    keystone_id: int = keystone_id_param,
    spicy: int = spicy_param,
):
    queue_mode = convert_queue_mode(mode)
    if queue_mode == 450:
        lane = "middle"
    return s.generate_build(champion_id, lane, tier, queue_mode, keystone_id, spicy)


@build_router.get("/items", tags=["champion"])
def get_items(
    champion_id: str = champion_id_param,
    lane: str = lane_param,
    tier: str = tier_param,
    mode: str = queue_mode_param,
    keystone_id: int = keystone_id_param,
    spicy: int = spicy_param,
):
    queue_mode = convert_queue_mode(mode)
    if queue_mode == 450:
        lane = "middle"
    return s._get_items(champion_id, lane, tier, queue_mode, keystone_id, spicy)


@build_router.get("/keystones", tags=["champion"])
def get_keystones(
    champion_id: str = champion_id_param,
    lane: str = lane_param,
    tier: str = tier_param,
    queue_mode: str = queue_mode_param,
    spicy: int = spicy_param,
):
    queue_mode = convert_queue_mode(queue_mode)
    if queue_mode == 450:
        lane = "middle"
    return s._get_champion_keystones(champion_id, lane, tier, queue_mode, spicy)


@build_router.get("/runes", tags=["champion"])
def get_runes(
    champion_id: str = champion_id_param,
    lane: str = lane_param,
    tier: str = tier_param,
    queue_mode: str = queue_mode_param,
    keystone_id: int = keystone_id_param,
    spicy: int = spicy_param,
):
    queue_mode = convert_queue_mode(queue_mode)
    if queue_mode == 450:
        lane = "middle"
    return s._get_champion_runes(
        champion_id, lane, tier, queue_mode, keystone_id, spicy
    )
