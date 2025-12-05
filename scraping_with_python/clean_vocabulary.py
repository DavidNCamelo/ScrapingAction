"""
Created By David Camelo on 05/12/2024
Helped by ChatGPT
"""

import pandas as pd
import re
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
INPUT_VOCAB = os.getenv("INPUT_VOCAB")
OUTPUT_VOCAB = os.getenv("OUTPUT_VOCAB")

# Load CSV
df = pd.read_csv(INPUT_VOCAB)

# Drop "index" column
df = df.drop(columns=["index"], errors="ignore")


# Extract url parts
def extract_mission(url):
    match = re.search(r"/mission/([^/]+)/", url)
    return match.group(1) if match else None


def extract_lesson_parts(url):
    match = re.search(r"/lesson/([^/]+)/", url)
    if not match:
        return None, None, None

    parts = match.group(1).split("_")

    # language = first two parts (EN + GB)
    language = "_".join(parts[:2])

    # level = third part (A2)
    level = parts[2]

    # topic = rest
    topic = "_".join(parts[3:])

    return language, level, topic


# Create new coluimns
df["mission"] = df["url"].apply(extract_mission)

df[["language", "level", "topic"]] = df["url"].apply(
    lambda x: pd.Series(extract_lesson_parts(x))
)

# Sorting columns
cols = ["mission", "language", "level", "topic"] + [
    c for c in df.columns if c not in ["mission", "language", "level", "topic", "url"]
]

df = df[cols]

# Saving results
df.to_csv(OUTPUT_VOCAB, index=False)
