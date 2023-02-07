from fastapi import APIRouter, Query
from backend.api.constants import s


picks_router = APIRouter()


@picks_router.get("/picks/top10")
def get_top10_picks(
    lane: str = Query("default", title="lane", description="Lane"),
    tier: str = Query("platinum_plus", title="tier", description="Tier data"),
):
    return s.get_top10_picks(lane, tier)
