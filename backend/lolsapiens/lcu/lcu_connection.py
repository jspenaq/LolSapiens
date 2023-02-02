from lcu_driver import Connector

from backend.lolsapiens.lcu.utils import (
    get_summoner_data,
    initialize_variables,
    update_game_mode,
    # is_champ_select_phase,
    # get_current_champion,
    # update_current_champion_and_runes,
)

connector = Connector()


@connector.ready
async def connect(connection):
    await initialize_variables(connection)
    await get_summoner_data(connection)


@connector.ws.register("/lol-gameflow/v1/session", event_types=("UPDATE",))
async def gameflow_session_listener(connection, event):
    await update_game_mode(connection, event)


@connector.ws.register(
    "/lol-champ-select/v1/current-champion",
    event_types=(
        "CREATE",
        "UPDATE",
        "DELETE",
    ),
)
# async def champion_select_champ_listener(connection, event):
#     await update_current_champion_and_runes(connection, event)


@connector.close
async def disconnect(_):
    print("The client has been closed")
    await connector.stop()


def main_loop():
    connector.start()
