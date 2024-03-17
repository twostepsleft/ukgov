import requests
import pandas as pd
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for easy configuration
BASE_URL = "https://members-api.parliament.uk/api/Members/Search"
PAGE_SIZE = 20  # Consider making this configurable via environment variable or command line argument

def requests_retry_session(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    """Set up retry logic for handling API requests."""
    session = session or requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_members(is_current_member, house):
    """Fetch members data from the API based on member status and house."""
    session = requests_retry_session()
    params = {
        "IsCurrentMember": is_current_member,
        "House": house,
        "take": PAGE_SIZE
    }
    all_members = []

    while True:
        response = session.get(BASE_URL, params=params)
        response.raise_for_status()  # Check for HTTP request errors
        data = response.json()
        all_members.extend(data['items'])
        if len(data['items']) < PAGE_SIZE:
            break  # Exit loop if last page
        params['skip'] = params.get('skip', 0) + PAGE_SIZE

    for member in all_members:
        member['value']['IsCurrentMember'] = is_current_member
        member['value']['MemberType'] = "MP" if house == "Commons" else "Lord"

    return all_members

def get_all_members():
    """Combine current and non-current MPs and Lords data."""
    combinations = [("true", "Commons"), ("false", "Commons"), ("true", "Lords"), ("false", "Lords")]
    all_members = [member for is_current, house in combinations for member in get_members(is_current, house)]
    return all_members

def expand_json_column(df, column_name):
    """Normalize and combine JSON column data with the original DataFrame."""
    expanded_df = pd.json_normalize(df.pop(column_name))
    expanded_df.columns = [f"{column_name}_{col}" for col in expanded_df.columns]
    return df.join(expanded_df)

def main():
    all_members_data = get_all_members()
    df = pd.DataFrame([member['value'] for member in all_members_data])
    df = expand_json_column(df, 'latestParty')
    df = expand_json_column(df, 'latestHouseMembership')

    csv_file_path = 'membership.csv'
    df.to_csv(csv_file_path, index=False)
    logging.info(f'DataFrame is written to {csv_file_path} successfully.')

if __name__ == "__main__":
    main()
