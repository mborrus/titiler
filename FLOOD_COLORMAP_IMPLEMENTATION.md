# Flood Colormap Implementation for TiTiler

This document describes the implementation of the flood depth color scheme from `slate_lambda` into TiTiler.

## Overview

Two new colormaps have been added to TiTiler based on the flood color schemes defined in `../slate_lambda/config.yml` (lines 147-155 and 164-171):

1. **flood_depth** - Flood Probability Depth colormap (5-257 cm)
2. **flood_historic** - Flood Historic Event colormap (0-257 cm)

## Files Modified/Created

### 1. New File: `src/titiler/application/titiler/application/custom_colormaps.py`

This module defines the custom flood colormaps using rio-tiler's interval-based colormap format.

**Flood Depth Intervals:**
```python
flood_depth_intervals = [
    ((5, 16), (161, 211, 255, 255)),    # Light blue - 5-15 cm
    ((16, 31), (88, 180, 255, 255)),    # Medium blue - 16-30 cm
    ((31, 62), (38, 114, 222, 255)),    # Blue - 31-61 cm
    ((62, 92), (34, 47, 191, 255)),     # Dark blue - 62-91 cm
    ((92, 257), (33, 36, 99, 255)),     # Very dark blue - 92+ cm
]
```

**Flood Historic Intervals:**
```python
flood_historic_intervals = [
    ((0, 16), (161, 211, 255, 255)),    # Light blue - 0-15 cm
    ((16, 31), (88, 180, 255, 255)),    # Medium blue - 16-30 cm
    ((31, 62), (38, 114, 222, 255)),    # Blue - 31-61 cm
    ((62, 92), (34, 47, 191, 255)),     # Dark blue - 62-91 cm
    ((92, 257), (33, 36, 99, 255)),     # Very dark blue - 92+ cm
]
```

### 2. Modified File: `src/titiler/application/titiler/application/main.py`

The main application file was updated to:

1. Import the custom colormaps module
2. Import rio-tiler's default colormaps
3. Import the colormap dependency creator
4. Merge custom colormaps with default colormaps
5. Create a custom ColorMapParams dependency with merged colormaps
6. Pass the custom ColorMapParams to all tiler factories (COG, STAC, Mosaic)
7. Pass the merged colormap to the ColorMapFactory

**Key changes:**

```python
# Import custom colormaps
from rio_tiler.colormap import cmap as default_cmap
from titiler.application.custom_colormaps import custom_colormaps
from titiler.core.dependencies import create_colormap_dependency

# Merge colormaps
cmap = default_cmap.register(custom_colormaps.data)
ColorMapParams = create_colormap_dependency(cmap)

# Use in factories
cog = TilerFactory(
    ...,
    colormap_dependency=ColorMapParams,
    ...
)
```

## Usage

Once TiTiler is running, you can use the flood colormaps by adding the `colormap_name` parameter to your requests:

### Example 1: COG Tile with Flood Depth Colormap
```
GET /cog/tiles/{z}/{x}/{y}.png?url=https://example.com/flood_depth.tif&colormap_name=flood_depth
```

### Example 2: Preview with Flood Historic Colormap
```
GET /cog/preview.png?url=https://example.com/flood_event.tif&colormap_name=flood_historic
```

### Example 3: List All Available Colormaps
```
GET /colormaps
```

This will return a JSON response including the new flood colormaps:
```json
{
  "colormaps": [
    ...,
    "flood_depth",
    "flood_historic",
    ...
  ]
}
```

### Example 4: Get Specific Colormap Details
```
GET /colormaps/flood_depth
```

## Color Scheme Details

Both colormaps use a gradient from light blue (shallow water) to very dark blue (deep water):

| Depth Range (cm) | RGB Color | Description |
|-----------------|-----------|-------------|
| 5-15 (flood_depth) / 0-15 (flood_historic) | rgb(161, 211, 255) | Light blue - shallow water |
| 16-30 | rgb(88, 180, 255) | Medium blue - moderate water |
| 31-61 | rgb(38, 114, 222) | Blue - deeper water |
| 62-91 | rgb(34, 47, 191) | Dark blue - deep water |
| 92-257 | rgb(33, 36, 99) | Very dark blue - very deep water |

**Note:** The ranges are defined as [start, stop) where start is inclusive and stop is exclusive, matching the original slate_lambda configuration.

## Differences Between the Two Colormaps

1. **flood_depth**: Starts at 5 cm (for probability depth data)
2. **flood_historic**: Starts at 0 cm (for historic event data)

Otherwise, the color scales are identical.

## Integration with Existing Colormaps

The flood colormaps are merged with rio-tiler's default colormaps, so all standard colormaps (viridis, plasma, etc.) remain available alongside the new flood colormaps.

## Testing

To verify the implementation:

1. Start the TiTiler application:
   ```bash
   uvicorn titiler.application.main:app --reload
   ```

2. Check available colormaps:
   ```bash
   curl http://localhost:8000/colormaps
   ```

3. Test with a flood depth raster:
   ```bash
   curl "http://localhost:8000/cog/preview.png?url=YOUR_FLOOD_TIFF&colormap_name=flood_depth" -o test_flood.png
   ```

## Implementation Notes

- The colormaps use rio-tiler's interval-based format, which maps value ranges to specific colors
- The format is: `[((min_value, max_value), (R, G, B, A)), ...]`
- All color values are in the range 0-255
- Alpha channel is set to 255 (fully opaque) for all colors
- Values outside the defined ranges will not be colored

## Future Enhancements

Possible future improvements:

1. Add more flood-related colormaps (e.g., different hazard levels)
2. Support for custom color ramps via API parameters
3. Add interpolation between color stops for smoother gradients
4. Integration with other slate_lambda colormaps (fire, wind, etc.)
