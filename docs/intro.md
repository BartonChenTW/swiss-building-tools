# Swiss Building Tools Documentation

Welcome to the Swiss Building Tools documentation! This package provides tools for mapping Swiss addresses to EGID (Federal Building Identifier) using the GeoAdmin API.

## Overview

Swiss Building Tools is a Python library that helps you:

- **Map Swiss postal addresses to EGID**: Convert addresses to Federal Building Identifiers
- **Handle complex address formats**: Support for multiple house numbers (e.g., "10/12" or "10, 12")
- **Flexible matching options**: Both exact and fuzzy matching capabilities
- **Detailed mapping notes**: Comprehensive feedback for troubleshooting
- **Rooftop PV analysis**: Work with Swiss rooftop photovoltaic data and solar irradiance profiles

## Modules

### swiss_building_tools
Core functionality for address mapping, data aggregation, and utilities.

### swiss_pv
Specialized tools for working with Swiss rooftop photovoltaic (PV) datasets, including:
- Classification of roof tilt and aspect angles
- Integration with hourly solar irradiance data
- Support for research datasets from EPFL and Zenodo

## Quick Start

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

print(df_result[['address', 'EGID list', 'EGID map', 'EGID note']])
```

## Key Features

```{admonition} What's New
:class: tip
- Support for batch address processing
- Enhanced error handling and logging
- Detailed mapping notes for each result
```

## Navigation

Use the sidebar to navigate through the documentation:

- **Installation**: How to install the package
- **Usage**: Detailed usage examples
- **API Reference**: Complete API documentation
- **Examples**: Real-world examples and use cases

## About

This project is maintained by [BartonChenTW](https://github.com/BartonChenTW) and is available under the MIT License.

```{tableofcontents}
```
