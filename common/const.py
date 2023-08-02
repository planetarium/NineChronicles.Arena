import os

ARENA_START_SCORE = 1000

TARGET_ACTION_LIST = (
    "join_arena3",
    "battle_arena12",
    "patch_table_sheet",
    # For Test
    "hack_and_slash21",
)

HOST_DICT = {
    "development": [
        os.environ.get("HEADLESS", "http://localhost")
    ],
    "internal": [
        "https://9c-internal-rpc-1.nine-chronicles.com",
    ],
    "mainnet": [
        "https://9c-main-rpc-1.nine-chronicles.com",
        "https://9c-main-rpc-2.nine-chronicles.com",
        "https://9c-main-rpc-3.nine-chronicles.com",
        "https://9c-main-rpc-4.nine-chronicles.com",
        "https://9c-main-rpc-5.nine-chronicles.com",
    ],
}
