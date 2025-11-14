# Usage Guide

This guide provides detailed information on how to use Swiss Building Tools.

## Basic Usage

### Import the Package

```python
from swiss_building_tools import get_egid_from_address
import pandas as pd
```

### Prepare Your Data

The main function `get_egid_from_address()` expects a pandas DataFrame with address information:

```python
df = pd.DataFrame({
    'address': [
        'Bahnhofstrasse 10, 8001 Zürich',
        'Bundesplatz 3, 3003 Bern',
        'Seestrasse 120, 8700 Küsnacht'
    ],
    'house_number': ['10', '3', '120']
})
```

### Map Addresses to EGID

```python
# Basic usage
result = get_egid_from_address(df, col_house_no='house_number')

# Display results (EGIDs are in 'EGID list')
print(result[['address', 'EGID list', 'EGID map', 'EGID note']])
```

## Understanding the Results

The function returns a DataFrame with additional columns:

- **EGID list**: Semicolon/comma-separated list of EGIDs found for the input address/house numbers
- **EGID map**: Mapping summary in format `input_count:egid_count` (e.g., `1:1`, `2:3`)
- **EGID note**: Detailed notes about the mapping process

### Result Columns

| Column | Type | Description |
|--------|------|-------------|
| EGID list | str | One or multiple EGIDs separated by `;` or `,` |
| EGID map | str | Mapping ratio `source_addresses:egids_found` |
| EGID note | str | Details about the mapping |

## Advanced Usage

### Handling Multiple House Numbers

The tool can handle addresses with multiple house numbers:

```python
df = pd.DataFrame({
    'address': ['Hauptstrasse 10/12, 8000 Zürich'],
    'house_number': ['10/12']
})

result = get_egid_from_address(df, col_house_no='house_number')
```

### Working with Different Address Formats

The package supports various Swiss address formats:

```python
addresses = [
    'Bahnhofstrasse 10, 8001 Zürich',          # Full address
    'Bundesplatz 3, 3003 Bern',                 # Standard format
    'Seestrasse 120-122, 8700 Küsnacht',       # Range
    'Hauptstrasse 10a, 5000 Aarau'             # With letter suffix
]
```

## Best Practices

```{tip}
**For optimal results:**
1. Ensure addresses are in Swiss format
2. Include postal codes for better accuracy
3. Clean and standardize your address data before processing
4. Check the 'EGID note' column for mapping details
```

## Error Handling

The function includes built-in error handling:

```python
try:
    result = get_egid_from_address(df, col_house_no='house_number')
except Exception as e:
    print(f"Error processing addresses: {e}")
```

## Performance Considerations

```{warning}
**Rate Limiting:**
The GeoAdmin API has rate limits. For large datasets:
- Process in batches
- Add delays between requests if needed
- Monitor the 'EGID note' column for API errors
```

## Example Workflow

Here's a complete example workflow:

```python
import pandas as pd
from swiss_building_tools import get_egid_from_address

# 1. Load your data
df = pd.read_csv('addresses.csv')

# 2. Map addresses to EGID
df_result = get_egid_from_address(df, col_house_no='HausNr')

# 3. Inspect mapping summary
print(df_result[['address','HausNr','EGID list','EGID map']].head())

# 4. Analyze failures (rows with no EGIDs)
failed = df_result[df_result['EGID list'] == '']
print(f"Failed to map {len(failed)} addresses")
print(failed[['address', 'EGID note']])

# 5. Save results
df_result.to_csv('addresses_with_egid.csv', index=False)
```

## Working with Swiss PV Data

The `swiss_pv` module provides tools for working with rooftop photovoltaic datasets.

### Basic PV Workflow

```python
from swiss_building_tools import get_egid_from_address
from swiss_pv import get_roof_aspect_tilt_classes
import pandas as pd

# 1. Get EGID for your buildings
df_addresses = pd.DataFrame({
    'address': ['Gernstrasse 1, 8311 Brütten'],
    'house_no': ['1']
})
df_egid = get_egid_from_address(df_addresses, col_house_no='house_no')

# 2. Load roof data (from Swiss rooftop datasets)
df_roofs = pd.read_csv('rooftop_data.csv')  # Contains ROOF_TILT, ROOF_ASPECT
df_roofs = df_roofs[df_roofs['EGID'].isin(df_egid['EGID list'].str.split(';'))]

# 3. Classify roof geometry
df_classified = get_roof_aspect_tilt_classes(df_roofs)
print(df_classified[['EGID', 'ROOF_TILT_CLASS', 'ROOF_ASPECT_CLASS', 'ROOF_AREA']])
```

### Understanding Roof Classifications

The `get_roof_aspect_tilt_classes()` function converts continuous roof measurements into discrete classes:

**Tilt Classes** (degrees from horizontal):
- 0°, 10°, 20°, 30°, 40°, 50°

**Aspect Classes** (orientation):
- N (North), E (East), SE (Southeast), S (South), SW (Southwest), W (West), flat

These classes match the format used in published Swiss solar irradiance datasets, allowing you to link roof geometry to hourly generation profiles.

### Data Sources

Compatible with these public datasets:
- [Global tilted radiation on Swiss rooftops (2016)](https://zenodo.org/records/4770483) - Hourly irradiance by municipality
- [Rooftop PV potential data](https://zenodo.org/records/3609833) - Roof geometry linked to EGID

## Next Steps

- Check the [API Reference](api.md) for detailed function documentation
- See [Examples](examples.md) for more real-world use cases
