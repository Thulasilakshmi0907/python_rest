import os
import re
import pandas as pd
from simple_salesforce import Salesforce
from dotenv import load_dotenv

load_dotenv(override=True)

# --- 1. Read credentials from environment (never hardcode) ---
instance_url = os.environ["SF_INSTANCE_URL"]
access_token = os.environ["SF_ACCESS_TOKEN"]

# --- 2. Connect ---
sf = Salesforce(instance_url=instance_url, session_id=access_token)
print("Connected to Salesforce!")

# --- 3. Query Account records ---
result = sf.query("SELECT Id, Name, Phone, Industry FROM Account LIMIT 20")
print(f"Records returned: {result['totalSize']}")

# --- 4. Convert to DataFrame and drop 'attributes' ---
df = pd.DataFrame(result["records"])
df = df.drop(columns=["attributes"])

# --- 5. clean_phone: keep digits only ---
def clean_phone(phone):
    if pd.isna(phone):
        return None
    return re.sub(r"\D", "", str(phone))

if "Phone" in df.columns:
    df["Phone_Clean"] = df["Phone"].apply(clean_phone)

# --- 6. Print the first rows ---
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", None)
print(df.head())