##### all_game_data.py


def get_latest_version():
    version_data = API_GET("http://ddragon.leagueoflegends.com/api/versions.json")
    return version_data[0]


def get_all_champions():
    champions = Champions()
    champions_data = API_GET(
        f"http://ddragon.leagueoflegends.com/cdn/{get_latest_version()}/data/en_US/champion.json"
    )
    for _, champion in champions_data["data"].items():
        champions.add(Champion(champion["key"], champion["id"]))

    return champions


async def LCU_GET(connection, endpoint):
    request = await connection.request("GET", endpoint)
    status_code = request.status

    if not request.ok:
        return status_code, None

    response = await request.json()
    return status_code, response


async def LCU_POST(connection, endpoint, payload):
    request = await connection.request("POST", endpoint, data=payload)
    status_code = request.status
    return status_code


async def LCU_DELETE(connection, endpoint):
    request = await connection.request("DELETE", endpoint)
    status_code = request.status
    return status_code


##############################################################


def print_summoner_data(summoner):
    print("Connected\n")
    print(f"Summoner Name:     {summoner['displayName']}")
    print(f"Summoner Level:    {summoner['summonerLevel']}")
    print(f"Level Completion:  {summoner['percentCompleteForNextLevel']}%")


def print_game_details(connection):
    print()
    print("Entered Champion Select")
    print("Locked in:", connection.locals["champion"].name)
    print()


async def get_summoner_data(connection):
    print("\nInitiating Connection...\n")
    status, summoner = await LCU_GET(connection, "/lol-summoner/v1/current-summoner")
    if status == 200:
        print_summoner_data(summoner)
    else:
        print("Please run league client first")


async def initialize_variables(connection):
    connection.locals["game_mode"] = ""
    connection.locals["champion"] = None


async def update_game_mode(connection, event):
    in_champ_select = await is_champ_select_phase(connection, event)
    if in_champ_select:
        game_mode = event.data["gameData"]["queue"]["gameMode"]
        status, summoner = await LCU_POST(
            connection, "/lol-gameflow/v1/session/dodge", ""
        )
        connection.locals["game_mode"] = game_mode


async def is_champ_select_phase(_, event):
    if event.data["phase"] == "ChampSelect":
        return True
    return False


#############################################################
#               CHAMPION SELECT CHAMPION LISTENER           #
#############################################################


async def get_current_champion(_, event):
    champions = get_all_champions()
    return champions.from_id(event.data)


async def update_current_champion_and_runes(connection, event):
    current_champion = await get_current_champion(connection, event)

    if not current_champion:
        return
    if connection.locals["champion"] == current_champion:
        return

    connection.locals["champion"] = current_champion
    print_game_details(connection)

    await update_rune_page(connection)


#############################################################
#                           RUNES                           #
#############################################################

from lcu_driver import Connector

# from lcu_change_runes.handler.lcu_handler import (
# get_summoner_data,
# initialize_variables,
# update_current_champion_and_runes,
# update_game_mode,
# )

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
async def champion_select_champ_listener(connection, event):
    await update_current_champion_and_runes(connection, event)


@connector.close
async def disconnect(_):
    print("The client has been closed")
    await connector.stop()


connector.start()
