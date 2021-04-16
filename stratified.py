import pandas as pd


def stratify_file(filename="Peru_2019_AudioMoth_Data_Full.csv"):
    df = pd.read_csv(filename)

    # select only viable clips (durations at least one minute) and filter for date parsing based on the availability of data
    viable_clips = df[df["Duration"] >= 60.0].dropna(subset=["StartDateTime"])
    wwf_clips = df[df["Duration"] >= 60.0].dropna(subset=["FileCreateDate"])
    wwf_clips = wwf_clips[wwf_clips["StartDateTime"].isna()]

    # clean dates for clip parsing
    dates = pd.to_datetime(viable_clips["StartDateTime"], format="%d.%m.%Y %H:%M")
    viable_clips["StartDateTime"] = dates

    # clean world wildlife dates for clip parsing
    wwf_clips['FileCreateDate'] = wwf_clips['Comment'].str[12:31]
    ww_dates = pd.to_datetime(wwf_clips["FileCreateDate"], format="%H:%M:%S %d/%m/%Y")
    wwf_clips['FileCreateDate'] = ww_dates

    # find AudioMoth objects that have fewer than 24 clips for standard data
    clip_count = viable_clips.AudioMothCode.value_counts()
    to_remove = clip_count[clip_count < 24].index
    viable_clips = viable_clips[~viable_clips.AudioMothCode.isin(to_remove)]

    # find AudioMoth objects that have fewer than 24 clips for wwf data
    wwf_clip_count = wwf_clips.AudioMothCode.value_counts()
    wwf_to_remove = wwf_clip_count[wwf_clip_count < 24].index
    wwf_clips = wwf_clips[~wwf_clips.AudioMothCode.isin(wwf_to_remove)]

    # add hour column to increase selection capability for standard data
    hours = viable_clips['StartDateTime'].dt.hour.tolist()
    viable_clips['Hour'] = hours

    # add hour column to increase selection capability for wwf data
    hours = wwf_clips['FileCreateDate'].dt.hour.tolist()
    wwf_clips['Hour'] = hours

    # merge standard and wwf clips
    frames = [viable_clips, wwf_clips]
    combined_clips = pd.concat(frames)

    # export 24 random clips per AudioMoth object representing each hour of the day
    stratified_clips = combined_clips.groupby(['AudioMothCode', 'Hour']).sample(1, random_state=1,
                                                                                replace=True).reset_index()
    # drop index for csv prep
    stratified_clips = stratified_clips.drop('index', 1)
    stratified_clips.to_csv("Stratified_Clips.csv", index=False)

    return not stratified_clips.empty


stratify_file()
