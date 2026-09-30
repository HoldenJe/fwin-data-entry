from fwin_data_entry.models.fish_sample import FishSample

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

print(fish)