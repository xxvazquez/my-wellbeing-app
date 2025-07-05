import os
import json
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# === Step 1: Rebuild credentials.json from secret ===
creds_raw = os.environ.get("GDRIVE_CREDENTIALS")
if not creds_raw:
    raise RuntimeError("Missing Google Drive credentials!")

with open("credentials.json", "w") as f:
    f.write(creds_raw)

# === Step 2: Authenticate ===
gauth = GoogleAuth()
gauth.LoadServiceConfigFile("credentials.json")
gauth.ServiceAuth()
drive = GoogleDrive(gauth)

# === Step 3: Find latest Bearable export ===
query = "'root' in parents and trashed=false"
file_list = drive.ListFile({'q': query}).GetList()

target_file = None
for file in file_list:
    if file['title'].startswith("bearable-export") and file['title'].endswith(".csv"):
        target_file = file
        break

if not target_file:
    raise FileNotFoundError("No Bearable export file found.")

print(f"Found file: {target_file['title']}")

# === Step 4: Download and read the file ===
target_file.GetContentFile("bearable_export.csv")
df = pd.read_csv("bearable_export.csv")

# === Step 5: Preview the data ===
print("First 5 rows:")
print(df.head())
