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
    description="The tier of data that you would like to use. Default: platinum_plus",
    example="gold",
)
queue_mode_param = Query(
    "ranked",
    title="queue_mode",
    description="Queue mode to play. Options include: 'ranked', 'aram'. Default: ranked",
    example="aram",
)
keystone_id_param = Query(
    0,
    title="keystone_id",
    description="Unique identifier associated with keystone to play",
    example=8214,
)
spicy_param = Query(
    0,
    title="spicy_factor",
    description="Spicy factor, an int value between 0 and 4. Default: 0",
    example=1
)
