from fastapi import APIRouter, Query

from backend.api.constants import s


build_router = APIRouter()


@build_router.get("/build")
def create_build(
    champion_id: str = Query(None, title="champion_id", description="Champion ID"),
    lane: str = Query(
        None,
        title="lane",
        description="Lane to play ['top', 'jungle', 'middle', 'bottom', 'support']",
    ),
    tier: str = Query("1trick", title="tier", description="Tier data"),
    mode: str = Query(
        "ranked", title="mode", description="Queue mode ('ranked', 'aram')"
    ),
    keystone_id: int = Query(None, title="keystone_id", description="Tier data"),
    spicy: int = Query(
        0,
        title="spicy factor",
        description="Give a int value (0, 1 or 2) to modify final champion build",
    ),
):
    return s.generate_build(champion_id, lane, tier, mode, keystone_id, spicy)


@build_router.get("/runes")
def get_runes(
    champion_id: str = Query(None, title="champion_id", description="Champion ID"),
    lane: str = Query(
        None,
        title="lane",
        description="Lane to play ['top', 'jungle', 'middle', 'bottom', 'support']",
    ),
    tier: str = Query("1trick", title="tier", description="Tier data"),
    queue_mode: str = Query(
        "ranked", title="queue_mode", description="Queue mode ('ranked', 'aram')"
    ),
):
    return s._get_champion_runes(champion_id, lane, tier, queue_mode)
