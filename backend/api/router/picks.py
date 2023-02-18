from fastapi import APIRouter, Query
from backend.api.constants import s, lane_param, tier_param, limit_param, random_param


picks_router = APIRouter()


@picks_router.get("/spicy-picks")
def get_spicy_picks(
    lane: str = lane_param,
    tier: str = tier_param,
    limit: int = limit_param,
    random: int = random_param,
):
    return s.get_spicy_picks(lane, tier, limit, random)
