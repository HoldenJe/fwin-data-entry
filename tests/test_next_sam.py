from fwin_data_entry.services.effort_service import get_next_sam

DB_PATH = "data/examples/test_project.sqlite"

next_sam = get_next_sam(
    DB_PATH,
    "26_PB_FW01",
)

print(next_sam)