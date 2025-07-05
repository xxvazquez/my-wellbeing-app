import os
import pandas as pd
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# === Step 1: Rebuild credentials.json from GitHub secret ===
creds_raw = os.environ.get("GDRIVE_CREDENTIALS")
if not creds_raw:
    raise RuntimeError("Missing Google Drive credentials!")

with open("credentials.json", "w") as f:
    f.write(creds_raw)

# === Step 2: Write service settings.yaml dynamically ===
settings_yaml = """
client_config_backend: service
service_config:
  client_json_file_path: credentials.json
"""
with open("settings.yaml", "w") as f:
    f.write(settings_yaml)

# === Step 3: Authenticate with Google Drive ===
gauth = GoogleAuth(settings_file="settings.yaml")
gauth.ServiceAuth()
drive = GoogleDrive(gauth)

# === Step 4: Look for Bearable export in specific folder ===
folder_id = "1qWNDl_z2moMSds07dvv2tFzA3dYNfTB6"
query = f"'{folder_id}' in parents and trashed=false"
file_list = drive.ListFile({'q': query}).GetList()

target_file = None
for file in file_list:
    if file['title'].startswith("bearable-export") and file['title'].endswith(".csv"):
        target_file = file
        break

if not target_file:
    raise FileNotFoundError("No Bearable export file found in the specified folder.")

print(f"✅ Found file: {target_file['title']}")

# === Step 5: Download and load ===
target_file.GetContentFile("bearable_export.csv")
df = pd.read_csv("bearable_export.csv")

# === Step 6: Preview ===
print("📄 First 5 rows of the export:")
print(df.head())
