# API Reference

This page provides detailed documentation for all functions in the Swiss Address Tools package.

## Main Functions

### get_egid_from_address

```{eval-rst}
.. function:: get_egid_from_address(df_data_raw, col_address='address', col_house_no='HausNr', separators=['/', ','], exact_match=True, fuzzy_match=True)

   Add EGID mapping columns to a dataframe containing Swiss addresses.
   
   Handles three address-to-EGID mapping scenarios:
   
   1. **1:1** - One address to one EGID (most common)
   2. **1:many** - One address to multiple EGIDs (e.g., 17 → 17a, 17b, 17c)
   3. **many:many** - Multiple addresses to multiple EGIDs (e.g., "10-12" → 10, 11, 12)
   
   :param df_data_raw: Input dataframe with address columns
   :type df_data_raw: pandas.DataFrame
   :param col_address: Name of the address column (default: 'address')
   :type col_address: str
   :param col_house_no: Name of the house number column (default: 'HausNr')
   :type col_house_no: str
   :param separators: List of separators for multiple house numbers (default: ['/', ','])
   :type separators: list
   :param exact_match: Require exact house number match (default: True)
   :type exact_match: bool
   :param fuzzy_match: Try fuzzy matching if exact match fails (default: True)
   :type fuzzy_match: bool
   :return: Dataframe with added columns: 'EGID', 'EGID map', 'EGID note'
   :rtype: pandas.DataFrame
   :raises ValueError: If required columns are not found in the dataframe
```

**Example:**

```python
import pandas as pd
from swiss_address_tools import get_egid_from_address

df = pd.DataFrame({
    'address': ['Bahnhofstrasse 10, 8001 Zürich'],
    'HausNr': ['10']
})

df_result = get_egid_from_address(df)
print(df_result[['address', 'EGID', 'EGID map']])
```

---

### get_bldg_attrs_from_address

```{eval-rst}
.. function:: get_bldg_attrs_from_address(address, lang='de', debug=False)

   Get building attributes (including EGID) from a postal address using GeoAdmin API.
   
   :param address: Postal address to search
   :type address: str
   :param lang: Language code ('de', 'fr', 'it', 'en') (default: 'de')
   :type lang: str
   :param debug: Print debug information (default: False)
   :type debug: bool
   :return: List of result dictionaries from the API
   :rtype: list
```

**Example:**

```python
from swiss_address_tools import get_bldg_attrs_from_address

results = get_bldg_attrs_from_address("Bahnhofstrasse 10, 8001 Zürich")
if results:
    egid = results[0]['attrs']['featureId']
    print(f"EGID: {egid}")
```

---

### get_egid_house_no_from_request

```{eval-rst}
.. function:: get_egid_house_no_from_request(li_results, target_house_no, target_address='', exact_match=True)

   Extract EGID and house numbers from API results.
   
   :param li_results: Results from address query
   :type li_results: list
   :param target_house_no: Target house number to match
   :type target_house_no: str
   :param target_address: Full target address for validation (default: '')
   :type target_address: str
   :param exact_match: Only return exact house number matches (default: True)
   :type exact_match: bool
   :return: Tuple of (list of EGIDs, list of house numbers, list of skipped house numbers)
   :rtype: tuple
```

---

### expand_egid_to_rows

```{eval-rst}
.. function:: expand_egid_to_rows(df_data, egid_col='EGID list', max_egid_count=20)

   Expand rows with multiple EGIDs into separate rows per EGID.
   
   :param df_data: Input dataframe with comma-separated EGID list
   :type df_data: pandas.DataFrame
   :param egid_col: Column name containing comma-separated EGIDs (default: 'EGID list')
   :type egid_col: str
   :param max_egid_count: Maximum number of EGIDs to process (default: 20)
   :type max_egid_count: int
   :return: Expanded dataframe with one row per EGID
   :rtype: pandas.DataFrame
```

**Example:**

```python
from swiss_address_tools import expand_egid_to_rows
import pandas as pd

df = pd.DataFrame({
    'EGID list': ['123,456', '789'],
    'address': ['Street 1', 'Street 2']
})

df_expanded = expand_egid_to_rows(df)
print(len(df_expanded))  # Output: 3 rows
```

---

## Utility Functions

### li2str

```{eval-rst}
.. function:: li2str(li, sep='; ')

   Convert a list to a string with specified separator.
   
   :param li: Input list
   :type li: list
   :param sep: Separator string (default: '; ')
   :type sep: str
   :return: Joined string
   :rtype: str
```

---

### expand_house_number_ranges

```{eval-rst}
.. function:: expand_house_number_ranges(house_no_str, separator=',')

   Expand house number ranges in a string into individual house numbers.
   
   This function parses a string containing house numbers and ranges (e.g., "1-5, 10, 20-22")
   and expands them into a list of individual house numbers.
   
   :param house_no_str: A string containing house numbers and ranges
   :type house_no_str: str
   :param separator: Separator between house numbers or ranges (default: ',')
   :type separator: str
   :return: A list of individual house numbers as strings
   :rtype: list
```

**Example:**

```python
from swiss_address_tools import expand_house_number_ranges

# Expand a range
result = expand_house_number_ranges("1-5, 10, 20-22")
print(result)
# Output: ['1', '2', '3', '4', '5', '10', '20', '21', '22']

# Handle non-integer values
result = expand_house_number_ranges("10a, 12-14, 20b")
print(result)
# Output: ['10a', '12', '13', '14', '20b']
```

---

## Data Structures

### Result Columns

When using `get_egid_from_address()`, the following columns are added to your DataFrame:

| Column Name | Type | Description |
|-------------|------|-------------|
| `EGID` | str | Federal Building Identifier(s). Multiple EGIDs are separated by ';' |
| `EGID map` | str | Mapping ratio in format "input:output" (e.g., "1:1", "2:3") |
| `EGID note` | str | Detailed notes about the mapping process, including house numbers and any issues |

### API Response Structure

The GeoAdmin API returns results with the following structure:

```python
{
    'attrs': {
        'featureId': 'EGID_12345',
        'label': 'Bahnhofstrasse 10 <b>8001 Zürich</b>',
        # ... other attributes
    }
}
```

---

## Error Handling

All functions include error handling. Common exceptions:

- `ValueError`: Raised when required columns are missing from input DataFrame
- `requests.RequestException`: Raised when API requests fail
- `KeyError`: Raised when expected keys are missing from API responses

---

## Constants

### Default Parameters

- **Language codes**: `'de'`, `'fr'`, `'it'`, `'en'`
- **Default separators**: `['/', ',']`
- **Max EGID count**: `20` (for expand_egid_to_rows)
- **Coordinate system**: `2056` (Swiss LV95)

---

## See Also

- [Usage Guide](usage.md) - Practical examples and workflows
- [Examples](examples.md) - Real-world use cases
- [GeoAdmin API Documentation](https://api3.geo.admin.ch/) - Official API documentation
