import requests
import pandas as pd
from datetime import datetime

scheme_code = "119551"

url = f"https://api.mfapi.in/mf/{scheme_code}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    nav_df = pd.DataFrame(data["data"])

    nav_df["fetch_date"] = datetime.now()

    nav_df.to_csv(
    r"D:\bluestock_mf_capstone\BONUS_CHALLENGES\B1\Schedule_ETL_atest_nav.csv",
    index=False
)

    print("NAV Updated Successfully")
else:
    print("API Fetch Failed")

##Integrate with ETL

def fetch_nav():
    pass

def clean_nav():
    pass

def load_to_sqlite():
    pass

if __name__ == "__main__":
    fetch_nav()
    clean_nav()
    load_to_sqlite()