from fwin_data_entry.models.fish_sample import FishSample
from fwin_data_entry.services.fish_sample_service import (
    create_fish_sample,
    get_fish_sample,
)

DB_PATH = "data/examples/test_project.sqlite"

fish = FishSample(
    prj_cd="26_PB_FW01",
    sam=1,
    eff=999,
    spc=334,
    fish=1,
    flen=425,
    tlen=450,
    rwt=980,
)

create_fish_sample(DB_PATH, fish)

record = get_fish_sample(
    DB_PATH,
    "26_PB_FW01",
    1,
    999,
    334,
    1,
)

print(record)