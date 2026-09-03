import pandas as pd
import numpy as np

# Load the cleaned CSV file
df = pd.read_csv("data/trends_clean.csv")

# Display basic information
print("Loaded data:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

# Calculate average score and comments
average_score = df["score"].mean()
average_comments = df["num_comments"].mean()

print("\nAverage score   :", round(average_score, 2))
print("Average comments:", round(average_comments, 2))


# ---------------- NumPy Stats ----------------

# Convert score column into a NumPy array
scores = df["score"].to_numpy()

mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)
max_score = np.max(scores)
min_score = np.min(scores)

print("\n--- NumPy Stats ---")
print("Mean score   :", round(mean_score, 2))
print("Median score :", round(median_score, 2))
print("Std deviation:", round(std_score, 2))
print("Max score    :", max_score)
print("Min score    :", min_score)


# Find the category with the most stories
category_counts = df["category"].value_counts()
most_common_category = category_counts.idxmax()
most_common_count = category_counts.max()

print(
    "\nMost stories in:",
    most_common_category,
    f"({most_common_count} stories)"
)


# Find the story with the most comments
most_commented_index = df["num_comments"].idxmax()
most_commented_title = df.loc[most_commented_index, "title"]
most_comments = df.loc[most_commented_index, "num_comments"]

print(
    '\nMost commented story:',
    f'"{most_commented_title}" — {most_comments} comments'
)


# ---------------- Add New Columns ----------------

# Engagement shows comments compared to the story score
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Mark stories whose score is above the average score
df["is_popular"] = df["score"] > average_score


# ---------------- Save Result ----------------

df.to_csv("data/trends_analysed.csv", index=False)

print("\nSaved to data/trends_analysed.csv")