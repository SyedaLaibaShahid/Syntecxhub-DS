

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")

plt.rcParams["figure.figsize"] = (8,5)


if not os.path.exists("outputs"):
    os.makedirs("outputs")

df = pd.read_csv("dataset.csv")

print("Shape of dataset:", df.shape)
print("\nData Types:\n", df.dtypes)
print("\nMissing Values:\n", df.isnull().sum())

df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Unknown")

df["date_added"] = df["date_added"].str.strip()
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

df["year_added"] = df["date_added"].dt.year

type_counts = df["type"].value_counts()
plt.figure()
sns.barplot(
    x=type_counts.index,
    y=type_counts.values,
    width=0.4
)
plt.title("Count of Movies vs TV Shows")
plt.xlabel("Type")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("outputs/type_distribution.png")
plt.show()

print("\nType Counts:\n", type_counts)


yearly_content = df.groupby("year_added")["show_id"].count()

plt.figure()
yearly_content.plot()
plt.title("Content Added Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.tight_layout()
plt.savefig("outputs/content_growth.png")
plt.show()

top_years = df["release_year"].value_counts().head(10)

plt.figure()
sns.barplot(
    x=top_years.values,
    y=top_years.index
)
plt.title("Top 10 Release Years")
plt.xlabel("Count")
plt.ylabel("Year")
plt.tight_layout()
plt.savefig("outputs/top_10_release_years.png")
plt.show()


print("\nTop 10 Release Years:\n", top_years)


df_genres = df.assign(listed_in=df["listed_in"].str.split(", ")).explode("listed_in")
top_genres = df_genres["listed_in"].value_counts().head(10)


plt.figure(figsize=(10,6))  
sns.barplot(
    x=top_genres.values,
    y=top_genres.index
)
plt.title("Top 10 Genres on Netflix")
plt.xlabel("Count")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig("outputs/top_10_genres.png")
plt.show()

movies = df[df["type"] == "Movie"].copy()
tvshows = df[df["type"] == "TV Show"].copy()

movies["duration"] = movies["duration"].str.replace(" min", "")
movies["duration"] = pd.to_numeric(movies["duration"], errors="coerce")

tvshows["duration"] = tvshows["duration"].str.replace(" Seasons", "")
tvshows["duration"] = tvshows["duration"].str.replace(" Season", "")
tvshows["duration"] = pd.to_numeric(tvshows["duration"], errors="coerce")


plt.figure()
sns.histplot(movies["duration"].dropna(), bins=20)
plt.title("Movie Duration Distribution (Minutes)")
plt.xlabel("Minutes")
plt.tight_layout()
plt.savefig("outputs/movie_runtime_distribution.png")
plt.show()

plt.figure()
sns.histplot(tvshows["duration"].dropna(), bins=10)
plt.title("TV Show Season Distribution")
plt.xlabel("Number of Seasons")
plt.tight_layout()
plt.savefig("outputs/tvshow_season_distribution.png")
plt.show()



summary_text = f"""
NETFLIX DATASET EDA SUMMARY
===========================

1. Total Titles: {len(df)}

2. Movies: {type_counts.get("Movie",0)}
   TV Shows: {type_counts.get("TV Show",0)}

3. Peak Content Addition Year:
   {yearly_content.idxmax()} with {yearly_content.max()} titles added.

4. Most Common Genre:
   {top_genres.idxmax()} ({top_genres.max()} titles)

5. Most Frequent Release Year:
   {top_years.idxmax()} ({top_years.max()} titles)

INSIGHTS:
- Netflix content increased significantly after 2015.
- Movies dominate the platform compared to TV shows.
- Drama and International genres are highly common.
- Most movies range between 80–120 minutes.
- Most TV shows have 1–3 seasons.
"""

with open("outputs/netflix_eda_summary.txt", "w") as f:
    f.write(summary_text)

print("\nReport exported successfully inside 'outputs' folder!")
print("\nProject Completed Successfully")
