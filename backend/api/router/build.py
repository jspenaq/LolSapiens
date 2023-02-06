from fastapi import APIRouter, Query

from backend.api.constants import s


router = APIRouter()


@router.get("/build")
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
    keystone_id: str = Query(None, title="keystone_id", description="Tier data"),
):
    # print(sapiens.get_current_patch())
    print(champion_id,lane,tier,mode,keystone_id)
    return s.generate_build(champion_id,lane,tier,mode,keystone_id)