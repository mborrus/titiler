"""Custom colormaps for titiler application.

This module defines custom colormaps including the flood depth colormap
from the slate_lambda configuration.
"""

from rio_tiler.colormap import ColorMaps

# Flood Probability Depth colormap
# Based on slate_lambda config.yml lines 147-155
# Maps depth values (in cm) to RGB colors
# Note: The original ranges are [start, stop) where start is inclusive and stop is exclusive
flood_depth_intervals = [
    ((5, 16), (161, 211, 255, 255)),    # Light blue - shallow water (5-15 cm)
    ((16, 31), (88, 180, 255, 255)),    # Medium blue - moderate water (16-30 cm)
    ((31, 62), (38, 114, 222, 255)),    # Blue - deeper water (31-61 cm)
    ((62, 92), (34, 47, 191, 255)),     # Dark blue - deep water (62-91 cm)
    ((92, 257), (33, 36, 99, 255)),     # Very dark blue - very deep water (92+ cm)
]

# Flood Historic Event colormap (similar to probability depth but starts at 0)
# Based on slate_lambda config.yml lines 164-171
flood_historic_intervals = [
    ((0, 16), (161, 211, 255, 255)),    # Light blue
    ((16, 31), (88, 180, 255, 255)),    # Medium blue
    ((31, 62), (38, 114, 222, 255)),    # Blue
    ((62, 92), (34, 47, 191, 255)),     # Dark blue
    ((92, 257), (33, 36, 99, 255)),     # Very dark blue
]

# Create custom ColorMaps object with the flood colormaps
custom_colormaps = ColorMaps(
    data={
        "flood_depth": flood_depth_intervals,
        "flood_historic": flood_historic_intervals,
    }
)
