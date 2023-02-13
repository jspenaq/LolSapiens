from fastapi import APIRouter, Query
from backend.api.constants import s, lane_param, tier_param


picks_router = APIRouter()


@picks_router.get("/spicy-picks")
def get_spicy_picks(
    lane: str = lane_param,
    tier: str = tier_param,
    limit: int = Query(10, title="limit", description="Limit size"),
    random: int = Query(0, title="random", description="Return a sample of size given"),
):
    return s.get_spicy_picks(lane, tier, limit, random)
