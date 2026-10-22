"""Download the Ott et al. Deceptive Opinion Spam Corpus from ACL Anthology.

Source: https://aclanthology.org/P11-1032/
Dataset attachment: https://aclanthology.org/attachments/P11-1032.Datasets.zip

The script downloads the research dataset for local evaluation. It does not
ship the corpus in this repository because the source's licensing/copyright
terms should be respected by the user.
"""
from pathlib import Path
import io
import urllib.request
import zipfile

URL = "https://aclanthology.org/attachments/P11-1032.Datasets.zip"
BASE = Path(__file__).resolve().parent
OUT = BASE / "data" / "op_spam_v1.4"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Downloading: {URL}")
    with urllib.request.urlopen(URL, timeout=60) as response:
        payload = response.read()
    with zipfile.ZipFile(io.BytesIO(payload)) as z:
        z.extractall(OUT)
    print(f"Dataset extracted to: {OUT}")
    print("Expected corpus: 1,600 hotel reviews, balanced between truthful and deceptive labels.")


if __name__ == "__main__":
    main()
