# API Reference

This page provides detailed documentation for all functions in the Swiss Building Tools package.

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
   :return: Dataframe with added columns: 'EGID list', 'EGID map', 'EGID note'
   :rtype: pandas.DataFrame
   :raises ValueError: If required columns are not found in the dataframe
```

**Example:**

```python
import pandas as pd
from swiss_building_tools import get_egid_from_address

df = pd.DataFrame({
    'address': ['Bahnhofstrasse 10, 8001 Zürich'],
    'HausNr': ['10']
})

df_result = get_egid_from_address(df)
print(df_result[['address', 'EGID list', 'EGID map']])
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
from swiss_building_tools import get_bldg_attrs_from_address

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
.. function:: expand_egid_to_rows(df_data, col_egid='EGID list', cols_divider=[''])

   Expand rows with multiple EGIDs into separate rows per EGID.
   
   :param df_data: Input dataframe with comma-separated EGID list
   :type df_data: pandas.DataFrame
   :param col_egid: Column name containing the EGID list (default: 'EGID list')
   :type col_egid: str
   :param cols_divider: Numeric columns to divide proportionally among expanded EGIDs
   :type cols_divider: list
   :return: Expanded dataframe with one row per EGID
   :rtype: pandas.DataFrame
```

**Example:**

```python
from swiss_building_tools import expand_egid_to_rows
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
from swiss_building_tools import expand_house_number_ranges

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

### get_df_by_key

```{eval-rst}
.. function:: get_df_by_key(df_data, label, by='EGID', separate=';', col_sum=[], col_avg=[], col_join=[], col_first=[], col_unique=[], col_max=[])

   Aggregate a dataframe by key column with various groupby operations.
   
   This function groups data by a key column (e.g., EGID) and applies different aggregation
   functions to specified columns: sum, average, join (concatenate), first value, unique values, and max.
   
   :param df_data: Input dataframe to aggregate
   :type df_data: pandas.DataFrame
   :param label: Label to use in the count column name (e.g., 'dist_heat', 'PV')
   :type label: str
   :param by: Column name to group by (default: 'EGID')
   :type by: str
   :param separate: Separator for joined string values (default: ';')
   :type separate: str
   :param col_sum: List of columns to sum
   :type col_sum: list
   :param col_avg: List of columns to average
   :type col_avg: list
   :param col_join: List of columns to concatenate as strings
   :type col_join: list
   :param col_first: List of columns to take first value
   :type col_first: list
   :param col_unique: List of columns to get unique values
   :type col_unique: list
   :param col_max: List of columns to get maximum value
   :type col_max: list
   :return: Aggregated dataframe with the key as index
   :rtype: pandas.DataFrame
```

**Example:**

```python
from swiss_building_tools import get_df_by_key
import pandas as pd

df = pd.DataFrame({
    'EGID': [123, 123, 456, 456],
    'energy': [100, 150, 200, 250],
    'type': ['solar', 'wind', 'solar', 'solar'],
    'year': [2020, 2021, 2020, 2021]
})

# Aggregate by EGID
result = get_df_by_key(
    df, 
    label='renewables',
    by='EGID',
    col_sum=['energy'],
    col_join=['type'],
    col_max=['year']
)
print(result)
# Output shows aggregated data with count, sum of energy, joined types, and max year
```

---

### process_expand_house_numbers

```{eval-rst}
.. function:: process_expand_house_numbers(df_data, col_house_no, separator='/', range_sign='-')

   Process a dataframe to expand house number ranges in a specified column.
   
   This function finds rows containing range indicators (e.g., '-') in house numbers
   and expands them. The original value is preserved in a new column with '_raw' suffix.
   
   :param df_data: Input dataframe with house numbers
   :type df_data: pandas.DataFrame
   :param col_house_no: Column name containing house numbers to expand
   :type col_house_no: str
   :param separator: Separator to use for expanded house numbers (default: '/')
   :type separator: str
   :param range_sign: Character indicating a range (default: '-')
   :type range_sign: str
   :return: Dataframe with expanded house numbers
   :rtype: pandas.DataFrame
```

**Example:**

```python
from swiss_building_tools import process_expand_house_numbers
import pandas as pd

df = pd.DataFrame({
    'address': ['Main St', 'Oak Ave'],
    'house_no': ['10-12', '5']
})

result = process_expand_house_numbers(df, col_house_no='house_no')
print(result)
# house_no column: '10/11/12' for first row, '5' for second
# house_no_raw column: '10-12' (original value preserved)
```

---

## Data Aggregation Classes

### DataAggregator

```{eval-rst}
.. class:: DataAggregator(index_name='EGID', index_type=int)

   A class for aggregating multiple datasets by a common index (e.g., EGID).
   
   This class manages loading, merging, and spatially joining datasets into a single
   aggregated dataframe. It supports both index-based merging and spatial geometry-based joins.
   
   :param index_name: Name of the index column (default: 'EGID')
   :type index_name: str
   :param index_type: Data type of the index (default: int)
   :type index_type: type
```

**Methods:**

- `add_dataset(dataset_name, path, description, override=True, **kwargs)` - Load a dataset from file
- `merge_dataset_by_index(dataset_name, header_index=None)` - Merge dataset using index column
- `merge_dataset_by_geometry(dataset_name, header_geometry='geometry', header_point='geometry', method='search')` - Spatial join using geometries

**Example:**

```python
from swiss_building_tools import DataAggregator

# Initialize aggregator
agg = DataAggregator(index_name='EGID', index_type=int)

# Add datasets
agg.add_dataset('buildings', 'buildings.csv', 'Building data')
agg.add_dataset('energy', 'energy.parquet', 'Energy consumption')

# Merge by EGID
agg.merge_dataset_by_index('buildings')
agg.merge_dataset_by_index('energy')

# Access aggregated data
print(agg.aggregated_data.head())
print(f"Total rows: {len(agg.aggregated_data)}")
```

---

## Data Structures

### Result Columns

When using `get_egid_from_address()`, the following columns are added to your DataFrame:

| Column Name | Type | Description |
|-------------|------|-------------|
| `EGID list` | str | One or multiple EGIDs separated by ';' or ',' |
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

## Swiss PV Module

The `swiss_pv` module provides functions for working with Swiss rooftop photovoltaic (PV) data, including mapping roof characteristics to standardized classes used in solar irradiance datasets.

### get_roof_aspect_tilt_classes

```{eval-rst}
.. function:: get_roof_aspect_tilt_classes(df_roof)

   Convert continuous roof tilt and aspect values into standardized classes.
   
   This function maps raw roof measurements (ROOF_TILT in degrees, ROOF_ASPECT in degrees from south)
   to the classification system used in Swiss rooftop PV datasets:
   
   - **Tilt classes**: 0°, 10°, 20°, 30°, 40°, 50°
   - **Aspect classes**: 'N', 'E', 'SE', 'S', 'SW', 'W', 'flat'
   
   Flat roofs (tilt class 0) are automatically assigned aspect class 'flat'.
   
   :param df_roof: Dataframe with 'ROOF_TILT' and 'ROOF_ASPECT' columns
   :type df_roof: pandas.DataFrame
   :return: Dataframe with added 'ROOF_TILT_CLASS' and 'ROOF_ASPECT_CLASS' columns
   :rtype: pandas.DataFrame
   :raises KeyError: If required columns 'ROOF_TILT' or 'ROOF_ASPECT' are missing
```

**Example:**

```python
import pandas as pd
from swiss_pv import get_roof_aspect_tilt_classes

# Sample roof data
df = pd.DataFrame({
    'EGID': [123456, 789012],
    'ROOF_TILT': [25.3, 5.2],      # degrees
    'ROOF_ASPECT': [180.5, 90.0]   # degrees from south
})

# Convert to classes
df_result = get_roof_aspect_tilt_classes(df)
print(df_result[['EGID', 'ROOF_TILT', 'ROOF_TILT_CLASS', 
                 'ROOF_ASPECT', 'ROOF_ASPECT_CLASS']])
# Output:
#    EGID  ROOF_TILT  ROOF_TILT_CLASS  ROOF_ASPECT ROOF_ASPECT_CLASS
# 0  123456      25.3               20        180.5                S
# 1  789012       5.2                0         90.0             flat
```

**Classification Rules:**

Tilt Classes:
- 0°: [0, 5)
- 10°: [5, 15)
- 20°: [15, 25)
- 30°: [25, 35)
- 40°: [35, 45)
- 50°: [45+)

Aspect Classes (clockwise from south):
- S: [165, 195) and [345, 15)
- SW: [195, 255)
- W: [255, 285)
- N: [285, 345) and [15, 75)
- E: [75, 105)
- SE: [105, 165)
- flat: tilt = 0°

**Data Sources:**

This function is designed to work with Swiss rooftop PV datasets:
- [Global tilted radiation on Swiss rooftops (2016)](https://zenodo.org/records/4770483)
- [Rooftop photovoltaic (PV) potential data](https://zenodo.org/records/3609833)

**Reference:**

Walch, A., et al. (2020). "Big data mining for the estimation of hourly rooftop photovoltaic potential and its uncertainty." *Applied Energy*, 262, 114404. [DOI: 10.1016/j.apenergy.2019.114404](https://doi.org/10.1016/j.apenergy.2019.114404)

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
