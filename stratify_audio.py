import pandas as pd


def stratify_file(filename):
    df = pd.read_csv(filename)

    # select only viable clips (durations at least one minute) and filter for Comment data availability
    viable_clips = df[df["Duration"] >= 60.0].dropna(subset=["Comment"])

    # override StartDateTime with comment date and clean data for clip parsing
    viable_clips['StartDateTime'] = viable_clips['Comment'].str[12:31]
    dates = pd.to_datetime(viable_clips["StartDateTime"], format="%H:%M:%S %d/%m/%Y")
    viable_clips['StartDateTime'] = dates

    # find AudioMoth objects that have fewer than 24 clips for standard data
    clip_count = viable_clips.AudioMothCode.value_counts()
    to_remove = clip_count[clip_count < 24].index
    viable_clips = viable_clips[~viable_clips.AudioMothCode.isin(to_remove)]

    # add hour column to increase selection capability for standard data
    hours = viable_clips['StartDateTime'].dt.hour.tolist()
    viable_clips['Hour'] = hours

    # export 24 random clips per AudioMoth object representing each hour of the day
    stratified_clips = viable_clips.groupby(['AudioMothCode', 'Hour']).sample(1, random_state=1).reset_index()

    # drop index for csv prep
    stratified_clips = stratified_clips.drop('index', 1)
    stratified_clips.to_csv("Stratified_Clips.csv", index=False)

    return not stratified_clips.empty


stratify_file()
