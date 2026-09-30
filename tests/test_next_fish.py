from fwin_data_entry.services.fish_sample_service import (
    get_next_fish,
)

DB_PATH = "data/examples/test_project.sqlite"

next_fish = get_next_fish(
    DB_PATH,
    "26_PB_FW01",
    1,
    999,
    334,
)

print(next_fish)