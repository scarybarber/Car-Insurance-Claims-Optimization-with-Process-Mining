import pandas as pd
from datetime import timedelta
df = pd.read_csv("Insurance_claims_event_log.csv")

print(df.head())

## data wrangling

# parse the timestamp column

def parse_time(t):
    # use try..except to safely skip or handle errors when parsing
    try:
        minutes, rest = t.split(":")
        seconds, milliseconds = rest.split(".")
        return timedelta(minutes= int(minutes), seconds= int(seconds), milliseconds= int(milliseconds))
    except:
        return pd.NaT # Not a Time (for missing or invalid time/duration values)
df['parsed_timestamp'] = df['timestamp'].apply(parse_time)

# sort events by case_id and parsed_timestamp

df_sorted = df.sort_values(by= ['case_id', 'parsed_timestamp']).reset_index(drop= True)

# calculate activity_duration and case_duration

df_sorted['next_timestamp'] = df_sorted.groupby('case_id')['parsed_timestamp'].shift(-1)
df_sorted['activity_duration'] = (df_sorted['next_timestamp'] - df_sorted['parsed_timestamp']).dt.total_seconds()

case_durations = df_sorted.groupby('case_id')['parsed_timestamp'].agg(['min','max'])
case_durations ['case_duration_sec'] = (case_durations['max'] - case_durations['min']).dt.total_seconds()


## exploratory data analysis (EDA) -- discovery phase

# plot activity durations "which steps take the most time?"

import seaborn as sns
import matplotlib.pyplot as plt
sns.boxplot(data= df_sorted, x= "activity_name", y= "activity_duration")
plt.xticks (rotation = 90) # angle 
plt.title("Activity Duration (sec) by Activity Type")
plt.show()

# plot case duration "How long does a full claim take?"

plt.figure(figsize =(10,6)) # create a blank canvas for plotting with specific size
sns.histplot(data= case_durations, x= "case_duration_sec", bins= 50, kde= True) 
# bin divides the x-axis into 50 intervals (or "bins"); More bins = more detail, but may be noisier
# KDE stands for Kernel Density Estimate — it adds a smooth curve over the histogram that estimates the probability density function.
plt.title ("Distribution of Case Durations (Seconds)")
plt.xlabel("Case Duration (sec)")
plt.ylabel("Number of Claims")
plt.tight_layout()
plt.show()

# activity count per case "How complex are our claims?"

activity_counts = df_sorted.groupby("case_id").size().reset_index(name="activity_count")
# .size() counts the number of rows in each group
# rest_index(name= "activity_count") resets the index back to a regular column
sns.histplot(data= activity_counts, x= "activity_count", bins= 5)
plt.title("Case Complexity")
plt.show()

# the most common event sequences

common_sequences = df_sorted.groupby("case_id")["activity_name"].apply(list) 
# group each case_id's activity sequence into a list
common_sequences_str = common_sequences.apply(lambda x: "->".join(x))
# convert each list into a string (lambda defines a function in an easy way)
sequence_counts = common_sequences_str.value_counts().reset_index()
# value_counts() counts how many times each unique activity sequence (now a string) appears
sequence_counts.columns = ["activity_sequence","count"]
print(sequence_counts.head(10))

# find the standard path (happy path)
plt.figure(figsize= (12,6))
sns.barplot(data= sequence_counts.head(10), x="count", y="activity_sequence", palette= "viridis")
plt.title("Top 10 Most Common Claim Sequences")
plt.xlabel("Number of Cases")
plt.ylabel("Activity Sequences")
plt.tight_layout()
plt.show()

# find the rare or strange paths (broken workflows)
rare_sequences = sequence_counts[sequence_counts['count'] == 1]
print(rare_sequences.head(10))

# group average delays(activity duration) by agent
# identify slow performers and overloaded roles
df_sorted.groupby("agent_name")["activity_duration"].mean().sort_values(ascending= False).head(10)

# segment delays by claim type: type of policy, type of accident, car year
claim_metadata = df_sorted.drop_duplicates(subset='case_id')[['case_id', 'type_of_policy', 'type_of_accident', 'car_year']]
case_with_meta = pd.merge(case_durations, claim_metadata, on='case_id')

avg_by_policy = case_with_meta.groupby('type_of_policy')['case_duration_sec'].mean().sort_values(ascending=False)
print(avg_by_policy)

plt.figure(figsize=(10, 6))
sns.barplot(data=case_with_meta, x='type_of_accident', y='case_duration_sec')
plt.xticks(rotation=45)
plt.title("Average Case Duration by Type of Accident")
plt.ylabel("Avg Duration (sec)")
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(data=case_with_meta, x='car_year', y='case_duration_sec')
plt.xticks(rotation=45)
plt.title("Case Duration Distribution by Car Year")
plt.tight_layout()
plt.show()


## KPI dashboard

# prepare a clean csv for power bi
df_sorted.to_csv("cleaned_event_log.csv", index= False) # activity - level analysis
case_with_meta.to_csv("case_summary.csv", index= False) # case - level analysis



