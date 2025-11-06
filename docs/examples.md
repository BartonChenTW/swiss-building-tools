# Examples

This page provides real-world examples and use cases for Swiss Address Tools.

## Example 1: Basic Address Mapping

Map a simple list of addresses to their EGIDs:

```python
import pandas as pd
from swiss_address_tools import get_egid_from_address

# Create sample data
df = pd.DataFrame({
    'address': [
        'Bahnhofstrasse 10, 8001 Zürich',
        'Bundesplatz 3, 3003 Bern',
        'Quai du Mont-Blanc 30, 1201 Genève'
    ],
    'house_no': ['10', '3', '30']
})

# Map to EGID
result = get_egid_from_address(df, col_house_no='house_no')

# Display results
print(result[['address', 'EGID', 'EGID map', 'EGID note']])
```

---

## Example 2: Handling Multiple House Numbers

Process addresses with multiple house numbers (e.g., buildings that span multiple numbers):

```python
import pandas as pd
from swiss_address_tools import get_egid_from_address

# Addresses with multiple house numbers
df = pd.DataFrame({
    'address': [
        'Hauptstrasse 10/12, 8000 Zürich',
        'Seestrasse 120-122, 8700 Küsnacht',
        'Bahnhofstrasse 1, 3, 5, 8000 Zürich'
    ],
    'house_no': ['10/12', '120-122', '1, 3, 5']
})

# Map with custom separators
result = get_egid_from_address(
    df, 
    col_house_no='house_no',
    separators=['/', ',', '-']
)

print(result[['address', 'EGID', 'EGID map']])
```

---

## Example 3: Processing CSV Files

Load addresses from a CSV file, process them, and save results:

```python
import pandas as pd
from swiss_address_tools import get_egid_from_address

# Load data from CSV
df = pd.read_csv('input_addresses.csv')

# Ensure required columns exist
print(f"Columns: {df.columns.tolist()}")

# Map addresses
df_result = get_egid_from_address(
    df,
    col_address='full_address',
    col_house_no='house_number'
)

# Check success rate
total = len(df_result)
mapped = df_result['EGID map'].str.split(':').str[1].astype(int).sum()
print(f"Mapped {mapped}/{total} addresses successfully")

# Save results
df_result.to_csv('output_with_egid.csv', index=False)
```

---

## Example 4: Fuzzy Matching

Use fuzzy matching when exact matches fail:

```python
import pandas as pd
from swiss_address_tools import get_egid_from_address

df = pd.DataFrame({
    'address': [
        'Bahnhofstrasse 10a, 8001 Zürich',  # Has letter suffix
        'Hauptstrasse 17b, 8000 Zürich'
    ],
    'house_no': ['10a', '17b']
})

# Enable fuzzy matching
result = get_egid_from_address(
    df,
    col_house_no='house_no',
    exact_match=True,   # Try exact first
    fuzzy_match=True    # Fall back to fuzzy if needed
)

# Check which addresses used fuzzy matching
fuzzy_matches = result[result['EGID note'].str.contains('Fuzzy')]
print(f"Fuzzy matches: {len(fuzzy_matches)}")
```

---

## Example 5: Expanding Multiple EGIDs

Convert rows with multiple EGIDs into separate rows:

```python
import pandas as pd
from swiss_address_tools import get_egid_from_address, expand_egid_to_rows

# Get addresses with multiple EGIDs
df = pd.DataFrame({
    'address': ['Hauptstrasse 17, 8000 Zürich'],
    'house_no': ['17']
})

result = get_egid_from_address(df, col_house_no='house_no')

# Some addresses may return multiple EGIDs (e.g., 17a, 17b, 17c)
# Rename column for expansion
result['EGID list'] = result['EGID']

# Expand to one row per EGID
expanded = expand_egid_to_rows(result, egid_col='EGID list')

print(f"Original rows: {len(result)}")
print(f"Expanded rows: {len(expanded)}")
```

---

## Example 6: Error Analysis

Analyze failed mappings to understand issues:

```python
import pandas as pd
from swiss_address_tools import get_egid_from_address

df = pd.read_csv('addresses.csv')

result = get_egid_from_address(df, col_house_no='house_no')

# Filter failed mappings
failed = result[result['EGID map'].str.endswith(':0')]

# Analyze failure reasons
print("Failure Analysis:")
print(failed[['address', 'EGID note']].to_string())

# Common issues:
# 1. Invalid or non-existent addresses
# 2. Formatting issues
# 3. House number mismatches
# 4. API connectivity problems
```

---

## Example 7: Batch Processing with Progress

Process large datasets with progress tracking:

```python
import pandas as pd
from swiss_address_tools import get_egid_from_address
import time

# Load large dataset
df = pd.read_csv('large_addresses.csv')

# Process in batches to avoid API rate limits
batch_size = 100
results = []

for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    
    print(f"Processing batch {i//batch_size + 1}/{len(df)//batch_size + 1}")
    
    batch_result = get_egid_from_address(batch, col_house_no='house_no')
    results.append(batch_result)
    
    # Add delay between batches
    time.sleep(1)

# Combine all results
df_final = pd.concat(results, ignore_index=True)
df_final.to_csv('all_results.csv', index=False)
```

---

## Example 8: Using Low-Level API Functions

For more control, use the low-level API functions directly:

```python
from swiss_address_tools import (
    get_bldg_attrs_from_address,
    get_egid_house_no_from_request
)

# Get raw API results
address = 'Bahnhofstrasse 10, 8001 Zürich'
results = get_bldg_attrs_from_address(address, lang='de', debug=True)

print(f"Found {len(results)} results")

# Extract EGID manually
for result in results:
    label = result['attrs']['label']
    egid = result['attrs']['featureId'].split('_')[0]
    print(f"Address: {label}, EGID: {egid}")

# Filter by house number
egids, house_nos, skipped = get_egid_house_no_from_request(
    results,
    target_house_no='10',
    target_address=address,
    exact_match=True
)

print(f"Matched EGIDs: {egids}")
print(f"House numbers: {house_nos}")
print(f"Skipped: {skipped}")
```

---

## Example 9: Integration with Other Tools

Combine with GeoPandas for spatial analysis:

```python
import pandas as pd
import geopandas as gpd
from swiss_address_tools import get_egid_from_address

# Map addresses to EGID
df = pd.read_csv('addresses.csv')
df_result = get_egid_from_address(df, col_house_no='house_no')

# Filter successful mappings
df_mapped = df_result[~df_result['EGID'].str.startswith('')]

# Now you can use EGID to join with building geometry data
# from Swiss Federal Geodata (e.g., GWR - Gebäude- und Wohnungsregister)
print(f"Successfully mapped {len(df_mapped)} addresses")
print("EGIDs can now be used to join with building geometry data")
```

---

## Example 10: Expanding House Number Ranges

Use the `expand_house_number_ranges` utility function to expand house number ranges:

```python
from swiss_address_tools import expand_house_number_ranges

# Expand simple range
result = expand_house_number_ranges("1-5")
print(result)
# Output: ['1', '2', '3', '4', '5']

# Expand multiple ranges with individual numbers
result = expand_house_number_ranges("10-12, 15, 20-22")
print(result)
# Output: ['10', '11', '12', '15', '20', '21', '22']

# Handle non-numeric house numbers
result = expand_house_number_ranges("10a, 12-14, 20b")
print(result)
# Output: ['10a', '12', '13', '14', '20b']

# Use with address processing
addresses_with_ranges = ["Hauptstrasse 10-14", "Bahnhofstrasse 1-3"]

for address in addresses_with_ranges:
    # Extract the range part
    house_range = address.split()[-1]
    expanded = expand_house_number_ranges(house_range, separator='-')
    print(f"{address} → {expanded}")
```

---

## Tips and Best Practices

```{tip}
**Optimization Tips:**
1. Clean your address data before processing
2. Use consistent address formatting
3. Process in batches for large datasets
4. Cache results to avoid redundant API calls
5. Check the EGID note column for debugging
```

```{warning}
**Common Pitfalls:**
- Not including postal codes in addresses
- Inconsistent house number formats
- Exceeding API rate limits
- Not handling missing or null values
```

---

## Next Steps

- Read the [API Reference](api.md) for detailed function documentation
- Check the [Usage Guide](usage.md) for more information
- Visit the [GitHub repository](https://github.com/BartonChenTW/swiss-building-tools) for the latest updates
