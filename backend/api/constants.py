from backend.api.sapiens import Sapiens
from fastapi import Query

s = Sapiens()

champion_id_param = Query(
    None,
    title="champion_id",
    description="Unique identifier assigned to champion in the game",
)
lane_param = Query(
    "default",
    title="lane",
    description="Specific lane for champion to play in. Options include: 'default', 'top', 'jungle', 'middle', 'bottom', 'support'. Default: default",
)
tier_param = Query(
    "platinum_plus",
    title="tier",
    description="The tier of data that you would like to use. Default: platinum_plus",
)
queue_mode_param = Query(
    "ranked",
    title="mode",
    description="Queue mode to play. Options include: 'ranked', 'aram'. Default: ranked",
)
keystone_id_param = Query(
    0,
    title="keystone_id",
    description="Unique identifier associated with keystone to play",
)
spicy_param = Query(
    0,
    title="spicy factor",
    description="Spicy factor, an int value between 0 and 2. Default: 0",
)
