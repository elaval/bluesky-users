import pandas as pd
import io
import sys

# Load the CSV file from the URL
url = "https://raw.githubusercontent.com/elaval/bskyusers/refs/heads/main/bsky_users_history.csv"
data = pd.read_csv(url)


# Create an in-memory buffer
buffer = io.BytesIO()

# Convert the DataFrame to a Parquet file in memory
data.to_parquet(buffer, engine='pyarrow', index=False)

# Write the buffer content to sys.stdout
sys.stdout.buffer.write(buffer.getvalue())
