from fwin_data_entry.models.catch_summary import CatchSummary
from fwin_data_entry.services.catch_summary_service import (
    create_catch_summary,
)

DB_PATH = "data/examples/test_project.sqlite"

record = CatchSummary(
    prj_cd="26_PB_FW01",
    sam=1,
    eff=999,
    spc=334,
    catcnt=10,
    biocnt=25,
)

try:
    create_catch_summary(DB_PATH, record)
    print("ERROR: validation failed")
except ValueError as e:
    print(f"PASS: {e}")