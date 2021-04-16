import numpy as np
import pandas as pd
import matplotlib
# pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier

df = pd.read_csv("Peru_2019_AudioMoth_Data_Full.csv")

# select only viable clips (durations at least one minute) and exclude rows with null values in date
viable_clips = df[df["Duration"] >= 60.0].dropna(subset=["StartDateTime"])
# convert format to standard datetime for clip parsing
dates = pd.to_datetime(viable_clips["StartDateTime"], format="%d.%m.%Y %H:%M")
viable_clips["StartDateTime"] = dates
# test_duration = viable_clips.groupby("AudioMothCode")["Duration"].transform(min) == min(df["Duration"])
# print(viable_clips["AudioMothCode"].value_counts())
clip_count = viable_clips.AudioMothCode.value_counts().sort_index()
counts_clips = viable_clips.AudioMothCode.value_counts()
# viable_clips.drop(viable_clips[viable_clips["AudioMothCode"].value_counts() < 24])
to_remove = counts_clips[counts_clips < 24].index

# Keep rows where the city column is not in to_remove
viable_clips = viable_clips[~viable_clips.AudioMothCode.isin(to_remove)]
hours = viable_clips['StartDateTime'].dt.hour.tolist()
viable_clips['Hour'] = hours
print(viable_clips)
sample_viable = viable_clips.set_index("StartDateTime").groupby("AudioMothCode")
print(sample_viable)
random_files = viable_clips.groupby(['AudioMothCode', 'Hour']).sample(1, random_state=1, replace=True).reset_index()
print(random_files)

