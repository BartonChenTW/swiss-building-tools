# Swiss Building Tools

Tools for processing Swiss building data, including mapping address to EGID.

## Documentation

Full documentation is available at: https://bartonchentw.github.io/swiss-building-tools/

## Installation

### From Git repository
```bash
pip install git+https://github.com/BartonChenTW/swiss-building-tools
```

## Usage

```python
import pandas as pd
from swiss_building_tools import get_egid_from_address

# Prepare your data
df = pd.DataFrame({
    'address': ['Bahnhofstrasse 10, 8001 Zürich', 'Bundesplatz 3, 3003 Bern'],
    'HausNr': ['10', '3']
})

# Map addresses to EGID
df_result = get_egid_from_address(df, col_house_no='HausNr')

# Note: The EGIDs are returned in column 'EGID list' (semicolon/comma-separated)
print(df_result[['address', 'EGID list', 'EGID map', 'EGID note']])
```

## Features

- **Address to EGID Mapping**: Map Swiss postal addresses to Federal Building Identifiers (EGID)
- **Multiple House Numbers**: Handle complex formats (e.g., "10/12", "10, 12", "1-5")
- **House Number Range Expansion**: Expand ranges like "1-5" into individual numbers [1, 2, 3, 4, 5]
- **Data Aggregation**: Group and aggregate building data by EGID with various statistics
- **Matching Options**: Support for exact and fuzzy matching
- **Detailed Logging**: Comprehensive mapping notes for troubleshooting

## Key Functions

- `get_egid_from_address()` - Map addresses to EGID using GeoAdmin API
- `expand_house_number_ranges()` - Expand house number ranges
- `process_expand_house_numbers()` - Process DataFrame with house number expansion
- `get_df_by_key()` - Aggregate data by key with sum, average, join, and more

### Tip: One EGID per row
If you need one row per EGID, use `expand_egid_to_rows(df_result)` to expand the `'EGID list'` column into separate rows.

## License

MIT License