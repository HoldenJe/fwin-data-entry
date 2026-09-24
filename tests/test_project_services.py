from fwin_data_entry.services.project_service import (
    create_project,
    get_project,
)

DB_PATH = "data/examples/test_project.sqlite"

create_project(
    db_path=DB_PATH,
    prj_cd="26_PB_FW01",
    prj_nm="Rice Lake FWIN 2026",
    wby_nm="Rice Lake",
    prj_date0="2026-09-15",
    prj_date1="2026-10-15",
    comment="Test project",
)

project = get_project(DB_PATH, "26_PB_FW01")

print(project)