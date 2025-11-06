# Usage Guide

This guide provides detailed information on how to use Swiss Address Tools.

## Basic Usage

### Import the Package

```python
from swiss_address_tools import get_egid_from_address
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

# Display results
print(result[['address', 'EGID', 'EGID map', 'EGID note']])
```

## Understanding the Results

The function returns a DataFrame with additional columns:

- **EGID**: The Federal Building Identifier (if found)
- **EGID map**: Boolean indicating if mapping was successful
- **EGID note**: Detailed notes about the mapping process

### Result Columns

| Column | Type | Description |
|--------|------|-------------|
| EGID | str | Federal Building Identifier |
| EGID map | bool | True if mapping successful |
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
from swiss_address_tools import get_egid_from_address

# 1. Load your data
df = pd.read_csv('addresses.csv')

# 2. Map addresses to EGID
df_result = get_egid_from_address(df, col_house_no='HausNr')

# 3. Filter successful mappings
successful = df_result[df_result['EGID map'] == True]
print(f"Successfully mapped {len(successful)} addresses")

# 4. Analyze failures
failed = df_result[df_result['EGID map'] == False]
print(f"Failed to map {len(failed)} addresses")
print(failed[['address', 'EGID note']])

# 5. Save results
df_result.to_csv('addresses_with_egid.csv', index=False)
```

## Next Steps

- Check the [API Reference](api.md) for detailed function documentation
- See [Examples](examples.md) for more real-world use cases
