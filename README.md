# Swiss Address Tools

Tools for mapping Swiss addresses to EGID (Federal Building Identifier) using the GeoAdmin API.

## Installation

### From local directory (development)
```bash
pip install -e /path/to/swiss-address-tools
```

### From Git repository
```bash
pip install git+https://github.com/yourusername/swiss-address-tools.git
```

## Usage

```python
import pandas as pd
from swiss_address_tools import get_egid_from_address

# Prepare your data
df = pd.DataFrame({
    'address': ['Bahnhofstrasse 10, 8001 Zürich', 'Bundesplatz 3, 3003 Bern'],
    'HausNr': ['10', '3']
})

# Map addresses to EGID
df_result = get_egid_from_address(df, col_house_no='HausNr')

print(df_result[['address', 'EGID', 'EGID map', 'EGID note']])
```

## Features

- Map Swiss postal addresses to EGID
- Handle multiple house numbers (e.g., "10/12" or "10, 12")
- Exact and fuzzy matching options
- Detailed mapping notes for troubleshooting

## License

MIT License