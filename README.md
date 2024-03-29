# ukgov
This repo contains python scripts that can be used to gather data from public UK government apis.

New scripts will be added weekly.

The repo covers the following UK government apis:

UK Pariament: https://developer.parliament.uk/



## get_all_members.py
### Overview

This Python script retrieves information about members of both houses of the UK Parliament using the UK Parliament's Members API. The script can fetch data on current and former Members of Parliament (MPs) and Lords, then normalize and export the data to a CSV file.

### How it Works

The script is structured as follows:

    Constants: The BASE_URL and PAGE_SIZE are set to target the API and define the number of results per page.
    Session Setup: A requests session with retry logic is established to handle potential API request failures.
    Data Retrieval: Functions get_members() and get_all_members() fetch members' data based on their current status and house, combining results for current and non-current MPs and Lords.
    Data Normalization: The expand_json_column() function normalizes nested JSON data from the API response and merges it with the main data frame.
    CSV Export: The processed data is written to a CSV file, and the script logs the successful completion of this operation.

### Results

The script outputs a CSV file with the following columns and descriptions:

![image](https://github.com/twostepsleft/ukgov/assets/30218592/33ead10e-b888-4c38-85c9-042b631589cc)

(* indicates that there are multiple columns starting with this prefix, each pertaining to different attributes of the party or house membership.)
Usage

To use this script:

    Install Python on your system if it's not already installed.
    Install the required packages: requests and pandas.
    Run the script with Python in your terminal or command prompt.
    The script will generate a membership.csv file in the same directory.

Requirements

    Python 3.x
    requests library (install with pip install requests)
    pandas library (install with pip install pandas)


