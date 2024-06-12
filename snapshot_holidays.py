import requests
import json
import os
from datetime import datetime

def fetch_and_save_data():
    # Create the data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)

    # URLs to fetch the data
    url_tc = 'https://www.1823.gov.hk/common/ical/tc.json'
    url_en = 'https://www.1823.gov.hk/common/ical/en.json'

    # Fetch the data
    response_tc = requests.get(url_tc, timeout=30)
    response_en = requests.get(url_en, timeout=30)

    if response_tc.status_code == 200 and response_en.status_code == 200:
        response_tc.encoding = 'utf-8'
        response_en.encoding = 'utf-8'
        data_tc = response_tc.json()
        data_en = response_en.json()

        # Extract vcalendar data
        vcalendar_tc = data_tc['vcalendar'][0]['vevent']
        vcalendar_en = data_en['vcalendar'][0]['vevent']

        # Process and save the data
        for event_tc, event_en in zip(vcalendar_tc, vcalendar_en):
            date = event_tc['dtstart'][0]
            summary_tc = event_tc['summary']
            summary_en = event_en['summary']

            event_data = {
                'date': date,
                'name_zh': summary_tc,
                'name_en': summary_en
            }

            # Save the data to a JSON file
            filename = f'data/{date}.json'
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(event_data, file, ensure_ascii=False, indent=4)
    else:
        print('Failed to fetch data.')

if __name__ == '__main__':
    fetch_and_save_data()
