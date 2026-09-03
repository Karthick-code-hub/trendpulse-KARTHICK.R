import requests
import json
import os
import time
from datetime import datetime


# HackerNews API URL
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"


# User-Agent required by the assignment
headers = {
    "User-Agent": "TrendPulse/1.0"
}


# Categories and keywords
categories = {
    "technology": [
        "AI", "software", "tech", "code", "computer",
        "data", "cloud", "API", "GPU", "LLM"
    ],

    "worldnews": [
        "war", "government", "country", "president",
        "election", "climate", "attack", "global"
    ],

    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team",
        "player", "league", "championship"
    ],

    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "NASA", "genome"
    ],

    "entertainment": [
        "movie", "film", "music", "Netflix", "game",
        "book", "show", "award", "streaming"
    ]
}


# Step 1: Fetch top 500 story IDs
try:
    response = requests.get(
        TOP_STORIES_URL,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    story_ids = response.json()[:500]

    print(f"Fetched {len(story_ids)} story IDs.")

except requests.RequestException as error:
    print("Failed to fetch story IDs:", error)
    story_ids = []


# Store collected stories
stories = []


# Count stories in each category
category_count = {
    category: 0 for category in categories
}


# Step 2: Fetch story details
for story_id in story_ids:

    # Stop when all categories have 25 stories
    if all(count >= 25 for count in category_count.values()):
        break

    try:
        story_url = ITEM_URL.format(story_id)

        response = requests.get(
            story_url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        story = response.json()

        # Skip if story data is missing
        if not story:
            continue

        title = story.get("title", "")

        selected_category = None

        # Check title against category keywords
        for category, keywords in categories.items():

            # Maximum 25 stories per category
            if category_count[category] >= 25:
                continue

            for keyword in keywords:

                if keyword.lower() in title.lower():
                    selected_category = category
                    break

            if selected_category:
                break

        # Skip stories without a matching category
        if selected_category is None:
            continue

        # Create story record
        story_data = {
            "post_id": story.get("id"),
            "title": title,
            "category": selected_category,
            "score": story.get("score", 0),
            "num_comments": story.get("descendants", 0),
            "author": story.get("by", "unknown"),
            "collected_at": datetime.now().isoformat()
        }

        stories.append(story_data)

        # Increase category count
        category_count[selected_category] += 1

        print(
            f"Collected {selected_category}: "
            f"{category_count[selected_category]}/25"
        )

    except requests.RequestException as error:
        print(f"Failed to fetch story {story_id}: {error}")
        continue


# Step 3: Create data folder
os.makedirs("data", exist_ok=True)


# Create today's filename
today = datetime.now().strftime("%Y%m%d")

file_path = f"data/trends_{today}.json"


# Save stories to JSON
with open(file_path, "w", encoding="utf-8") as file:

    json.dump(
        stories,
        file,
        indent=4,
        ensure_ascii=False
    )


# Print final result
print(f"\nCollected {len(stories)} stories.")
print(f"Saved to {file_path}")


# Print category summary
print("\nCategory summary:")

for category, count in category_count.items():

    print(f"{category}: {count}")