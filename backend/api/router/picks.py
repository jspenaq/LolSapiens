from fastapi import APIRouter, Query
from backend.api.constants import s


picks_router = APIRouter()


@picks_router.get("/picks/top10")
def get_top10_picks(
    lane: str = Query("default", title="lane", description="Lane"),
    tier: str = Query("platinum_plus", title="tier", description="Tier data"),
    limit: int = Query(10, title="limit", description="Limit size"),
    random: int = Query(0, title="random", description="Return a sample of size given"),
):
    return s.get_top10_picks(lane, tier, limit, random)
