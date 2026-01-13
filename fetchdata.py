import requests
import json
from db import add_real_lightning_data

def fetch_data(date: str, type: str) -> str:
    """
    Fetch data from the given URL.

    Parameters:
    url (str): The URL to fetch data from.

    Returns:
    Array of all relevant lightning data records for the specified date, type, latitude and longitude.
    """
    results = []
    url = f"https://api-open.data.gov.sg/v2/real-time/api/weather?api=lightning&date={date}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    jsonData = json.loads(response.content)
    # jsonData is in the form of {code: int, data: {object}, errorMsg: str}
    for record in jsonData['data']["records"]:
        if record['item']['readings'] and record['item']['readings'][0]['type'].lower() == type.lower():
            print(f"{record['item']['readings'][0]['datetime']}: Type={record['item']['readings'][0]['type']}, ({record['item']['readings'][0]['location']['latitude']}, {record['item']['readings'][0]['location']['longitude']})")
            results.append([record['item']['readings'][0]['datetime'], record['item']['readings'][0]['type'], record['item']['readings'][0]['location']['latitude'], record['item']['readings'][0]['location']['longitude']])
    
    return results

dates = ["2025-05-01", "2025-05-02", "2025-05-03", "2025-05-04", "2025-05-05", "2025-05-06", "2025-05-07", "2025-05-08", "2025-05-09", "2025-05-10", "2025-05-11", "2025-05-12", "2025-05-13", "2025-05-14", "2025-05-15", "2025-05-16", "2025-05-17", "2025-05-18", "2025-05-19", "2025-05-20", "2025-05-21", "2025-05-22", "2025-05-23", "2025-05-24", "2025-05-25", "2025-05-26", "2025-05-27", "2025-05-28", "2025-05-29", "2025-05-30", "2025-05-31"]
for date in dates:
    all_data = fetch_data(date, "C")
    if all_data:
        for d in all_data:
            add_real_lightning_data(d[0], d[1], d[2], d[3])