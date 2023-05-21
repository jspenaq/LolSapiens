from fastapi import APIRouter, Query
from backend.api.constants import s, lane_param, tier_param, limit_param


bans_router = APIRouter()


@bans_router.get("/bans/top10", tags=["tierlist"])
def get_top_bans(
    lane: str = lane_param,
    tier: str = tier_param,
    limit: int = limit_param,
):
    return s.get_top_bans(lane, tier, limit)
