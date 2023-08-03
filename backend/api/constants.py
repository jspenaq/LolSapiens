from backend.api.sapiens import Sapiens
from fastapi import Query

s = Sapiens()

champion_id_param = Query(
    None,
    title="champion_id",
    description="Unique identifier assigned to champion in the game",
    example=1,
)
lane_param = Query(
    "default",
    title="lane",
    description="Specific lane for champion to play in. Options include: 'default', 'top', 'jungle', 'middle', 'bottom', 'support'. Default: default",
    example="support",
)
tier_param = Query(
    "platinum_plus",
    title="tier",
    description="The tier of data that you would like to use. Some options: 'gold', 'gold_plus', 'platinum_plus', 'emerald_plus', '1trick', etc. Default: platinum_plus",
    example="gold_plus",
)
queue_mode_param = Query(
    "ranked",
    title="queue_mode",
    description="Queue mode to play. Options include: 'ranked', 'aram'. Default: ranked",
    example="ranked",
)
keystone_id_param = Query(
    0,
    title="keystone_id",
    description="Unique identifier associated with keystone to play. \
        If the keystone_id is zero uses recommended keystone. Default: 0",
    example=8214,
)
spicy_param = Query(
    0,
    title="spicy_factor",
    description="Spicy factor, an int value between 0 and 4. Default: 0",
    example=1,
)
limit_param = Query(
    10,
    title="limit",
    description="The maximum number of items to return in a single request. Default: 10",
    example=12,
)
random_param = Query(
    0,
    title="random",
    description="Return a random sample of a specified size from the available results. \
        If the size is set to zero, all available results will be returned. Default: 0",
    example=5,
)
