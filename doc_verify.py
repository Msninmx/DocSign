import requests
import hashlib
import pandas as pd


def hash_from_url(url):
    hasher = hashlib.sha256()
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        print("The file could not be downloaded.")

    for chunk in response.iter_content():
        if chunk:
            hasher.update(chunk)

    return hasher.hexdigest()


df = pd.read_csv("links.csv")

for i in range(len(df)):
    row = df.iloc[i]

    hash = hash_from_url(row["Link"])
    if hash != row["Hash"]:
        df.loc[i, "Hash"] = hash
        print(f"Article no. {row['Article']} has been changed!")
    else:
        print(f"Article no. {row['Article']} is unchanged.")

df.to_csv("links.csv", index=False)
