"""Swiss Address to EGID mapping tools using GeoAdmin API."""

__version__ = "0.1.3"

from .mapping import (
    get_bldg_attrs_from_address,
    get_egid_from_address,
    get_egid_house_no_from_request,
    expand_egid_to_rows
)
from .utils import li2str, expand_house_number_ranges, get_df_by_key, process_expand_house_numbers

__all__ = [
    'get_bldg_attrs_from_address',
    'get_egid_from_address',
    'get_egid_house_no_from_request',
    'expand_egid_to_rows',
    'li2str',
    'expand_house_number_ranges',
    'get_df_by_key',
    'process_expand_house_numbers',
]