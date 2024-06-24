import pandas as pd
import json

# Load the JSON data from a file
with open('reviews.json', 'r') as file:
    data = json.load(file)

# Convert the JSON data to a pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv('reviews.csv', index=False)

