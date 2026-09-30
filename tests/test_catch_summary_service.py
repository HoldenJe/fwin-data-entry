from fwin_data_entry.models.catch_summary import CatchSummary
from fwin_data_entry.services.catch_summary_service import (
    create_catch_summary,
    get_catch_summary,
)

DB_PATH = "data/examples/test_project.sqlite"

record = CatchSummary(
    prj_cd="26_PB_FW01",
    sam=1,
    eff=999,
    spc=334,
    catcnt=25,
    biocnt=10,
)

create_catch_summary(DB_PATH, record)

result = get_catch_summary(
    DB_PATH,
    "26_PB_FW01",
    1,
    999,
    334,
)

print(result)