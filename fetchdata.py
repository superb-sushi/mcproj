import requests
import json
from simulationdb import add_real_lightning_data
from datetime import date, timedelta

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
    if response:
        jsonData = json.loads(response.content)
        # jsonData is in the form of {code: int, data: {object}, errorMsg: str}
        for record in jsonData['data']["records"]:
            if record['item']['readings'] and record['item']['readings'][0]['type'].lower() == type.lower():
                print(f"{record['item']['readings'][0]['datetime']}: Type={record['item']['readings'][0]['type']}, ({record['item']['readings'][0]['location']['latitude']}, {record['item']['readings'][0]['location']['longitude']})")
                results.append([record['item']['readings'][0]['datetime'], record['item']['readings'][0]['type'], record['item']['readings'][0]['location']['latitude'], record['item']['readings'][0]['location']['longitude']])
        
        return results
    else:
        print(f"Failed to fetch data for date {date}. Status code: {response.status_code}")
        return []

def get_all_dates_for_year(year: int):
    start = date(year, 1, 1)
    end = date(year, 12, 31)

    curr = start
    while curr <= end:
        yield curr.strftime("%Y-%m-%d")
        curr += timedelta(days=1)

def save_data_into_db(year, lightning_type):
    for date in get_all_dates_for_year(year):
        all_data = fetch_data(date, lightning_type)
        if all_data:
            for d in all_data:
                add_real_lightning_data(d[0], d[1], d[2], d[3])

save_data_into_db(2025, "G")