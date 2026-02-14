import requests
from pathlib import Path

URL = "https://montreal-prod.storage.googleapis.com/resources/aacc4576-97b3-4d8d-883d-22bbca41dbe6/actes-criminels.geojson?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=test-datapusher-delete%40amplus-data.iam.gserviceaccount.com%2F20260202%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20260202T025724Z&X-Goog-Expires=604800&X-Goog-SignedHeaders=host&x-goog-signature=bc1c36be8a31b598692c887d7ff643c9a3bfe6de0f6759bb54a2b0b6b71000c807810d0d9dda57017bdba4fc7408de366e0921d6c0e70dc7f8658411197a7605079f3f37e848de8e252080c228bca51c5bee18d579d45d34e056c0e9e834a447a7c7114ef16595398f03f0c5caadad1bfff57037c293be0f4787a2653958b39d811a34672fed6fe38f3d3a3dc03f93fe2c3566be37fe45c244de95df6986591eedcd7b198e28086157992419c857a5398676cd78b17504ce61dbf236b66a00b185aad217862d2196fab5158f70c836ca9b5ff77ff2638a4ff6e313c70ffb2c01bc0195b5c7714ff996b4324016fd7c6d8499c8ae59d23d0becc285e361ce022f"

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "actes-criminels.geojson"

def download():
    print("Downloading Montreal crime data...")
    with requests.get(URL, stream=True) as r:
        r.raise_for_status()
        with open(OUTPUT_FILE, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    print(f"Saved to {OUTPUT_FILE}")
    print(f"File size: {OUTPUT_FILE.stat().st_size / 1024 / 1024:.1f} MB")

if __name__ == "__main__":
    download()