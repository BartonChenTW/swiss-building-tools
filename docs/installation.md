# Installation

## Requirements

- Python 3.7 or higher
- pandas >= 1.0.0
- requests >= 2.25.0

## Installation Methods

### Method 1: From PyPI (Recommended)

```bash
pip install swiss-address-tools
```

```{note}
This method is not yet available. The package is still in development.
```

### Method 2: From GitHub

Install directly from the GitHub repository:

```bash
pip install git+https://github.com/BartonChenTW/swiss-building-tools.git
```

### Method 3: Local Development Installation

For development or testing, clone the repository and install in editable mode:

```bash
# Clone the repository
git clone https://github.com/BartonChenTW/swiss-building-tools.git
cd swiss-building-tools

# Install in editable mode
pip install -e .
```

## Verifying the Installation

After installation, verify that the package is correctly installed:

```python
import swiss_address_tools
print(swiss_address_tools.__version__)
```

## Dependencies

The package will automatically install the following dependencies:

- **pandas**: For data manipulation and DataFrame handling
- **requests**: For making HTTP requests to the GeoAdmin API

## Troubleshooting

### Common Issues

#### Import Error

If you encounter import errors, make sure the package is installed in your current Python environment:

```bash
pip list | grep swiss-address-tools
```

#### API Connection Issues

If you have problems connecting to the GeoAdmin API:

- Check your internet connection
- Verify that the GeoAdmin API is accessible from your location
- Check if there are any firewall restrictions

### Getting Help

If you encounter any issues:

1. Check the [GitHub Issues](https://github.com/BartonChenTW/swiss-building-tools/issues)
2. Create a new issue with detailed information about your problem
3. Include your Python version, OS, and error messages
