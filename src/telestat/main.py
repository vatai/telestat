import argparse
import json
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def get_data():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest="path")
    args = parser.parse_args()
    path = Path(args.path).expanduser()
    print("path is", path)
    with open(path) as f:
        data = json.load(f)
    return data


def process_messages(messages):
    stats = defaultdict(lambda: {"count": 0, "len": 0})
    for i, m in enumerate(messages):
        if m["type"] != "message":
            continue
        stat = stats[m["from"]]
        stat["count"] += 1
        stat["len"] += len(m["text"])

    df = pd.DataFrame(dict(stats))
    df = df.transpose()
    df["avg"] = df["len"] / df["count"]
    return df


def plot_stats(df, channel, key):
    plt.figure(figsize=(10, 8))
    df[key].plot.bar()
    title = f"{channel}: {key}"
    plt.title(title)
    plt.xticks(rotation=20, ha="right")
    # plt.show()
    fname = f"{channel}--{key}.png".replace(" ", "_")
    print(fname)
    plt.savefig(fname)


def main():
    data = get_data()
    messages = data["messages"]
    channel = data["name"]
    df = process_messages(messages)

    print(df)

    plot_stats(df, channel, "len")
    plot_stats(df, channel, "count")
    plot_stats(df, channel, "avg")


if True or __name__ == "__main__":
    main()
