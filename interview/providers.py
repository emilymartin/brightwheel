import pandas as pd
import requests
from re import search
from interview.sources import interview_sources


def clean_email(row: pd.Series) -> pd.Series:
    """[function to clean the email addresses, limit NA's and combine the 
    two sources]

    Args:
        row (pd.Series): [description]

    Returns:
        pd.Series: [description]
    """

    if pd.notnull(row['email_x']):
        row['email'] = row['email_x']
    else:
        row['email'] = row['email_y']

    return row

def clean_providers(row: pd.Series) -> pd.Series:
    """[function to clean and combine the address columns and the 
    type of care column]

    Args:
        row (pd.Series): [description]

    Returns:
        pd.Series: [description]
    """
    if pd.notnull(row['type_of_care_x']):
        row['type_of_care'] = row['type_of_care_x']
    else:
        row['type_of_care'] = row['type_of_care_y']
    if pd.notnull(row['address_x']):
        row['address'] = row['address_x']
    else:
        row['address'] = row['address_y']
    if pd.notnull(row['city_x']):
        row['city'] = row['city_x']
    else:
        row['city'] = row['city_y']
    if pd.notnull(row['state_x']):
        row['state'] = row['state_x']
    else:
        row['state'] = row['state_y']
    if pd.notnull(row['zip_x']):
        row['zip'] = row['zip_x']
    else:
        row['zip'] = row['zip_y']
    return row


def get_provider_data() -> pd.DataFrame:

    # reading in data from 3 different sources
    bw_api = interview_sources.get_bw_data()
    csv_data = interview_sources.get_csv_data()
    nccrra = interview_sources.get_naccrra_data()

    # clean and mergine brightwheel api with the ncrra website data
    nccrra.rename(columns={'Provider Name': 'provider_name',
                   'Type Of Care': 'type_of_care',
                   'Address': 'address',
                   'City': 'city',
                   'State': 'state',
                   'Zip': 'zip',
                   'Phone': 'phone',
                   'Email': 'email'}, inplace=True)
    
    # make sure all columns are type string
    nccrra = nccrra.astype(str)
    # joining on provider name and phone number b/c there are multiple proviers
    # with the same name
    all_providers = bw_api.merge(nccrra, on=['provider_name','phone'], how='outer')

    all_providers = all_providers.apply(clean_email, 1)
    all_providers.drop(columns=['email_x', 'email_y'], inplace=True)
    all_providers.drop_duplicates(inplace=True)

    # make sure all columns are type string
    csv_data = csv_data.astype(str)

    # clean phone number I kept the parenthasis becuase it makes them easier to read
    csv_data['phone'] = csv_data.phone.apply(lambda y: 
                                        '(' + y[:3] + ') ' +
                                        y[3:6] + '-' + y[6:10])

    all_providers2 = all_providers.merge(csv_data,
                                         on=['provider_name', 'phone'],
                                         how='outer')
    all_providers2.drop_duplicates(inplace=True)
    all_providers2 = all_providers2.apply(clean_providers, 1)

    # dropping excess columns so we only keep the clean ones
    all_providers_final = all_providers2.drop(columns = ['type_of_care_x', 'type_of_care_y',
                                                    'address_x', 'address_y',
                                                    'city_x', 'city_y',
                                                    'state_x', 'state_y',
                                                    'zip_x', 'zip_y'])

    all_providers_final.drop_duplicates(inplace=True)

    return all_providers_final


