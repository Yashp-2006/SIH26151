"""Error codes and structural constants for the Gwern/Grams adapter."""

# Structural errors (member-level, prevent normalization)
ENCODING_ERROR = "encoding_error"
HEADER_MISMATCH = "header_mismatch"
CSV_PARSE_ERROR = "csv_parse_error"
ROW_WIDTH_MISMATCH = "row_width_mismatch"
NONEMPTY_TRAILING_CELL = "nonempty_trailing_cell"
UNSUPPORTED_MEMBER_LAYOUT = "unsupported_member_layout"

# Field-level issues (row preserved, field marked)
INVALID_DECIMAL = "invalid_decimal"
INVALID_INTEGER = "invalid_integer"

# Expected CSV header — exact 11 cells including trailing empty
EXPECTED_HEADER = [
    "hash", "market_name", "item_link", "vendor_name", "price",
    "name", "description", "image_link", "add_time", "ship_from", ""
]

# Named header positions (1-based per spec section 4)
HEADER_POSITIONS = {
    "hash": 1,
    "market_name": 2,
    "item_link": 3,
    "vendor_name": 4,
    "price": 5,
    "name": 6,
    "description": 7,
    "image_link": 8,
    "add_time": 9,
    "ship_from": 10,
    "": 11,
}
