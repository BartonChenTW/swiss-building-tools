"""Swiss Address to EGID mapping tools using GeoAdmin API."""

__version__ = "0.1.0"

from .mapping import (
    get_bldg_attrs_from_address,
    get_egid_from_address,
    get_egid_house_no_from_request
)
from .utils import li2str

__all__ = [
    'get_bldg_attrs_from_address',
    'get_egid_from_address',
    'get_egid_house_no_from_request',
    'li2str'
]