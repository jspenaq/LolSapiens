from fastapi import APIRouter, Query
from backend.api.constants import s


bans_router = APIRouter()


@bans_router.get("/bans/top10")
def get_top10_bans(
    lane: str = Query("default", title="lane", description="Lane"),
    tier: str = Query("platinum_plus", title="tier", description="Tier data"),
):
    return s.get_top10_bans(lane, tier)
