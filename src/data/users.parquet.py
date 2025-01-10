import requests
import pandas as pd
import io
import sys

url = "https://raw.githubusercontent.com/elaval/bskyusers/refs/heads/main/bsky_users_history.csv"

# If you trust the source or must disable SSL verification
# you can pass 'verify=False' below (insecure).
response = requests.get(url)  # or verify=False if truly needed
response.raise_for_status()    # raise an error if the request failed

data = pd.read_csv(io.StringIO(response.text))

# Convert the DataFrame to Parquet in memory
buffer = io.BytesIO()
data.to_parquet(buffer, engine="pyarrow", index=False)

sys.stdout.buffer.write(buffer.getvalue())
