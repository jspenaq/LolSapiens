from fastapi import APIRouter, Query
from backend.api.constants import s, lane_param, tier_param


bans_router = APIRouter()


@bans_router.get("/bans/top10")
def get_top10_bans(lane: str = lane_param, tier: str = tier_param):
    return s.get_top10_bans(lane, tier)
