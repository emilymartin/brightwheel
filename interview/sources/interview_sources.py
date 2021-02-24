import pandas as pd
import requests
from re import search
from typing import Optional

def get_bw_data() -> Optional[pd.DataFrame]:
    url = "https://bw-interviews.herokuapp.com/data/providers"
    response = requests.get(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        print("Error on bw api: " + str(e))
        return None

    reponse_json = response.json()
    provider_json = reponse_json.get('providers')
    bw = pd.json_normalize(provider_json)

    return bw


def get_naccrra_data() -> Optional[pd.DataFrame]:

    url = "http://naccrrapps.naccrra.org/navy/directory/programs.php?program=omcc&state=CA&pagenum=1"
    response = requests.get(url, verify=False)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        print("Error on naccrra: " + str(e))
        return None

    # get number of pages on website
    html = response.text
    num = search(r'Page \w+ of (\w+)', html)
    pages = int(num.group(1))

    print(f"number of pages: {pages}")

    df_list = []
    # loop through all pages of teh caccrra website
    for i in range(1, pages + 1):
        url = 'https://naccrrapps.naccrra.org/navy/directory/programs.php?program=omcc&state=CA&pagenum=%d' %i
        response = requests.get(url, verify=False)
        df = pd.read_html(response.content, attrs={'class': 'sortable'})
        df_list.append(df[0])
    df = pd.concat(df_list, ignore_index=True)

    return df


def get_csv_data() -> Optional[pd.DataFrame]:
    df_csv = pd.read_csv("x_ca_omcc_providers.csv",
                        header=None,
                        names=['provider_name', 'type_of_care',
                                'address', 'city', 'state', 'zip', 'phone'])
    print(f"csv shape: {df_csv.shape}")
    return df_csv
