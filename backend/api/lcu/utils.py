# from lcu_change_runes.game_data.all_game_data import get_all_champions

# from lcu_change_runes.handler.lcu_apis import LCU_DELETE, LCU_GET, LCU_POST
# from lcu_change_runes.parser.opgg import generate_runes


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


async def is_champ_select_phase(_, event):
    if event.data["phase"] == "ChampSelect":
        return True
    return False


async def update_game_mode(connection, event):
    in_champ_select = await is_champ_select_phase(connection, event)
    if in_champ_select:
        print(event.data)
        game_mode = event.data["gameData"]["queue"]["gameMode"]
        connection.locals["game_mode"] = game_mode


#############################################################
#               CHAMPION SELECT CHAMPION LISTENER           #
#############################################################

# async def get_current_champion(_, event):
# champions = get_all_champions()
#     return champions.from_id(event.data)


async def update_current_champion_and_runes(connection, event):
    champion_id = event.data
    name = input("What is your name?\n")
    print(name)
    # if not current_champion:
    #     return
    # if connection.locals["champion"] == current_champion:
    #     return

    # connection.locals["champion"] = current_champion
    # print_game_details(connection)

    # await update_rune_page(connection)


#############################################################
#                           RUNES                           #
#############################################################


# async def update_rune_page(connection):
#     await delete_current_rune_page(connection)
# await create_new_rune_page(connection)


# async def delete_current_rune_page(connection):
#     status, current_page = await LCU_GET(connection, "/lol-perks/v1/currentpage")
#     if status == 200:
#         await LCU_DELETE(connection, "/lol-perks/v1/pages/" + str(current_page["id"]))
#     else:
#         print("Rune page did not exist 🤔", status, current_page)


# async def create_new_rune_page(connection):
#     opgg = generate_runes(connection.locals["champion"], connection.locals["game_mode"])
#     runes = opgg.runes

#     selected_runes = opgg.all_rune_ids()
#     del selected_runes[0]
#     del selected_runes[4]

#     payload = {
#         "name": connection.locals["champion"].name + " Runes",
#         "primaryStyleId": runes[0].id,
#         "subStyleId": runes[5].id,
#         "selectedPerkIds": selected_runes,
#     }

#     await LCU_POST(connection, "/lol-perks/v1/pages", payload)


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
