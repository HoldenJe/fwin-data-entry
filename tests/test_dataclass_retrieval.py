from fwin_data_entry.services.project_service import get_project
from fwin_data_entry.services.effort_service import get_effort
from fwin_data_entry.services.catch_summary_service import get_catch_summary
from fwin_data_entry.services.fish_sample_service import get_fish_sample

DB_PATH = "data/examples/test_project.sqlite"

project = get_project(DB_PATH, "26_PB_FW02")
print(project)

effort = get_effort(DB_PATH, "26_PB_FW01", 1)
print(effort)

catch = get_catch_summary(
    DB_PATH,
    "26_PB_FW01",
    1,
    999,
    334,
)
print(catch)

fish = get_fish_sample(
    DB_PATH,
    "26_PB_FW01",
    1,
    999,
    334,
    1,
)
print(fish)
