from fwin_data_entry.models.catch_summary import CatchSummary

record = CatchSummary(
    prj_cd="26_PB_FW01",
    sam=1,
    eff=999,
    spc=334,
    catcnt=25,
    biocnt=10,
)

print(record)