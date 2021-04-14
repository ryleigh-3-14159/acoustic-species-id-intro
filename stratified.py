import pandas as pd
import matplotlib
# pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier

df = pd.read_csv("Peru_2019_AudioMoth_Data_Full.csv")

# select only viable clips (durations at least one minute) and exclude rows with null values in date
viable_clips = df[df["Duration"] >= 60].dropna(subset=["StartDateTime"])
# convert format to standard datetime for clip parsing
dates = pd.to_datetime(viable_clips["StartDateTime"], infer_datetime_format=True)
viable_clips["StartDateTime"] = dates

print(viable_clips["StartDateTime"])

# hourly_clips = viable_clips.resample('H').first()  # resample for each hour and use first value of hour
# print(viable_clips)
