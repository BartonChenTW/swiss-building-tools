"""Functions for mapping Swiss addresses to EGID using GeoAdmin API."""

import pandas as pd
import requests
from typing import List, Tuple, Dict

from .utils import li2str


def get_bldg_attrs_from_address(address: str, lang: str = 'de', debug: bool = False) -> List[Dict]:
    """
    Get building attributes (including EGID) from a postal address using GeoAdmin API.
    
    Args:
        address: Postal address to search
        lang: Language code ('de', 'fr', 'it', 'en')
        debug: Print debug information
    
    Returns:
        List of result dictionaries from the API
    
    Example:
        >>> results = get_bldg_attrs_from_address("Bahnhofstrasse 10, 8001 Zürich")
        >>> print(results[0]['attrs']['featureId'])
    """
    search_url = "https://api3.geo.admin.ch/rest/services/api/SearchServer"
    params = {
        'searchText': address,
        'type': 'locations',
        'origins': 'address',
        'sr': 2056,
        'lang': lang
    }
    
    try:
        r = requests.get(search_url, params=params)
        r.raise_for_status()
        results = r.json().get('results', [])
        return results
    except Exception as e:
        if debug:
            print(f"Error during address search for '{address}': {e}")
        return []


def get_egid_house_no_from_request(
    li_results: List[Dict],
    target_house_no: str,
    target_address: str = '',
    exact_match: bool = True
) -> Tuple[List[str], List[str], List[str]]:
    """
    Extract EGID and house numbers from API results.
    
    Args:
        li_results: Results from address query
        target_house_no: Target house number to match
        target_address: Full target address for validation
        exact_match: Only return exact house number matches
    
    Returns:
        Tuple of (list of EGIDs, list of house numbers, list of skipped house numbers)
    """
    li_egid = []
    li_house_no = []        
    li_house_no_skip = []

    for dict_result in li_results:
        # Extract the address and house number
        str_address = dict_result['attrs']['label'].split(' <b>')[0]
        str_no = str_address.split(' ')[-1]

        if len(str_no) > 0:
            str_street = str_address.split(str_no)[0]

            # Skip if street name is not in address
            try:
                if target_address and str_street not in target_address:
                    print(f'Street: {str_street} not in address: {target_address} → skip')            
                    continue
            except Exception as e:
                print(f'Error checking street in address: {target_address} → skip')
                continue

        # Skip if house number does not match
        if exact_match and target_house_no != str_no:
            li_house_no_skip.append(str_no)
            continue
        
        # Add to EGID and note
        li_egid.append(dict_result['attrs']['featureId'].split('_')[0])
        li_house_no.append(str_no)

    return li_egid, li_house_no, li_house_no_skip


def get_egid_from_address(
    df_data_raw: pd.DataFrame,
    col_address: str = 'address',
    col_house_no: str = 'HausNr',
    separators: List[str] = ['/', ','],
    exact_match: bool = True,
    fuzzy_match: bool = True
) -> pd.DataFrame:
    """
    Add EGID mapping columns to a dataframe containing Swiss addresses.
    
    Handles three address-to-EGID mapping scenarios:
    1. 1:1 - One address to one EGID (most common)
    2. 1:many - One address to multiple EGIDs (e.g., 17 → 17a, 17b, 17c)
    3. many:many - Multiple addresses to multiple EGIDs (e.g., "10-12" → 10, 11, 12)
    
    Args:
        df_data_raw: Input dataframe with address columns
        col_address: Name of the address column
        col_house_no: Name of the house number column
        separators: List of separators for multiple house numbers
        exact_match: Require exact house number match
        fuzzy_match: Try fuzzy matching if exact match fails
    
    Returns:
        Dataframe with added columns: 'EGID', 'EGID map', 'EGID note'
    
    Example:
        >>> df = pd.DataFrame({
        ...     'address': ['Bahnhofstrasse 10, 8001 Zürich'],
        ...     'HausNr': ['10']
        ... })
        >>> df_result = get_egid_from_address(df)
        >>> print(df_result[['address', 'EGID', 'EGID map']])
    """
    # Check if required columns exist
    for col_req in [col_address, col_house_no]:
        if col_req not in df_data_raw.columns:
            raise ValueError(f'Column "{col_req}" not found in dataframe')
    
    df_data = df_data_raw.copy()

    # Add result columns
    for col in ['EGID list', 'EGID map', 'EGID note']:
        if col not in df_data.columns:
            df_data[col] = ''

    for indx in df_data.index:
        di_no2address = {}
        egid_cnt = 0

        row = df_data.loc[indx]
        house_no_raw = str(row[col_house_no])
        address_raw = row[col_address]

        # Preprocess house number string
        house_no_clean = house_no_raw.replace(' ', '')
        for sep in separators[1:]:
            house_no_clean = house_no_clean.replace(sep, separators[0])

        if house_no_raw != house_no_clean:
            print(f'Preprocessed house number: "{house_no_raw}" → "{house_no_clean}"')

        # Handle multiple house numbers
        if separators[0] in house_no_clean:
            li_no = house_no_clean.split(separators[0])
            for no in li_no:
                di_no2address[no] = address_raw.replace(house_no_raw, no)
            print('Multiple house number detected:', di_no2address)
        else:
            di_no2address[house_no_clean] = address_raw

        # Get EGID for each address
        for house_no, address in di_no2address.items():
            li_egid = []
            li_house_no = []
            egid_note = ''

            li_results = get_bldg_attrs_from_address(address)

            if len(li_results) == 0:
                print(f"Address: {address} → No EGID found")
                egid_note += f'No data found from address {address}. '
            else:
                li_egid, li_house_no, li_house_no_skip = get_egid_house_no_from_request(
                    li_results, house_no, address, exact_match=exact_match
                )

                # Try fuzzy match if no exact match found
                if len(li_egid) == 0 and exact_match and fuzzy_match:
                    print(f"Address: {address} → No exact match found, trying non-exact match")
                    li_egid, li_house_no, li_house_no_skip = get_egid_house_no_from_request(
                        li_results, house_no, address, exact_match=False
                    )
                    egid_note += 'Fuzzy match. '

            # Store results
            df_data.at[indx, 'EGID list'] += li2str(li_egid) + '; '
            egid_cnt += len(li_egid)

            egid_note += 'HausNr: ' + li2str(li_house_no, ', ')
            if len(li_house_no_skip) > 0:
                egid_note += f' (skipped: {li2str(li_house_no_skip, ", ")})'

            df_data.at[indx, 'EGID note'] += egid_note + '; '

        df_data.at[indx, 'EGID map'] = f'{len(di_no2address)}:{egid_cnt}'
        df_data.at[indx, 'EGID list'] = df_data.at[indx, 'EGID list'][:-2]  # Remove last '; '
        df_data.at[indx, 'EGID note'] = df_data.at[indx, 'EGID note'][:-2]

    return df_data


def expand_egid_to_rows(
    df_data: pd.DataFrame,
    col_egid: str = 'EGID list',
    cols_divider: list[str] = [''],
) -> pd.DataFrame:
    """
    Expand rows with multiple EGIDs into separate rows per EGID.
    
    Args:
        df_data: Input dataframe with comma-separated EGID list
        egid_col: Column name containing comma-separated EGIDs
        max_egid_count: Maximum number of EGIDs to process (filter out rows with more)
    
    Returns:
        Expanded dataframe with one row per EGID
    
    Example:
        >>> df = pd.DataFrame({
        ...     'EGID list': ['123,456', '789'],
        ...     'address': ['Street 1', 'Street 2']
        ... })
        >>> df_expanded = expand_egid_to_rows(df)
        >>> print(len(df_expanded))  # 3 rows
    """
   
    df_egid = pd.DataFrame()

    # check if cols_divider is in the columns
    cols_divider = [col for col in cols_divider if col in df_data.columns]

    for indx in df_data.index:
        # Split EGID list by both ',' and '; '
        egid_string = df_data.at[indx, col_egid]
        egid_string = egid_string.replace('; ', ',')
        li_egid = egid_string.split(',')
        li_egid = [egid for egid in li_egid if egid!='']

        for egid in li_egid:
            row_data = df_data.loc[indx].to_dict()
            row_data['EGID'] = egid.strip()

            for col in cols_divider:
                try:
                    row_data[col] = row_data[col] / len(li_egid)
                except:
                    print(f'Warning: Could not divide column "{col}" by {len(li_egid)}')

            df_egid = pd.concat([df_egid, pd.DataFrame([row_data])], ignore_index=True)

    return df_egid