# Flood Colormap Mapping: slate_lambda → TiTiler

This document shows the exact mapping from the slate_lambda configuration to the TiTiler implementation.

## Source: slate_lambda config.yml

### Flood Probability Depth (lines 147-155)

```yaml
flood:
  probability:
    depth:
      color:
        [
          { "range": [5, 16], "rgb": [161, 211, 255] },
          { "range": [16, 31], "rgb": [88, 180, 255] },
          { "range": [31, 62], "rgb": [38, 114, 222] },
          { "range": [62, 92], "rgb": [34, 47, 191] },
          { "range": [92, 257], "rgb": [33, 36, 99] },
        ]
```

## Target: TiTiler custom_colormaps.py

### Implementation

```python
flood_depth_intervals = [
    ((5, 16), (161, 211, 255, 255)),    # Light blue - shallow water (5-15 cm)
    ((16, 31), (88, 180, 255, 255)),    # Medium blue - moderate water (16-30 cm)
    ((31, 62), (38, 114, 222, 255)),    # Blue - deeper water (31-61 cm)
    ((62, 92), (34, 47, 191, 255)),     # Dark blue - deep water (62-91 cm)
    ((92, 257), (33, 36, 99, 255)),     # Very dark blue - very deep water (92+ cm)
]
```

## Transformation Details

| Source Format | Target Format | Notes |
|---------------|---------------|-------|
| `{"range": [5, 16], "rgb": [161, 211, 255]}` | `((5, 16), (161, 211, 255, 255))` | Added alpha channel (255) |
| JSON object with "range" and "rgb" keys | Python tuple of (range_tuple, rgba_tuple) | Rio-tiler interval format |
| RGB values (3 components) | RGBA values (4 components) | Alpha = 255 (fully opaque) |

## Color Comparison

Let's verify each color is correctly mapped:

### Color 1: Light Blue (Shallow Water)
- **Source**: `{ "range": [5, 16], "rgb": [161, 211, 255] }`
- **Target**: `((5, 16), (161, 211, 255, 255))`
- ✓ **Match**: Range [5-16), RGB values identical, alpha added

### Color 2: Medium Blue (Moderate Water)
- **Source**: `{ "range": [16, 31], "rgb": [88, 180, 255] }`
- **Target**: `((16, 31), (88, 180, 255, 255))`
- ✓ **Match**: Range [16-31), RGB values identical, alpha added

### Color 3: Blue (Deeper Water)
- **Source**: `{ "range": [31, 62], "rgb": [38, 114, 222] }`
- **Target**: `((31, 62), (38, 114, 222, 255))`
- ✓ **Match**: Range [31-62), RGB values identical, alpha added

### Color 4: Dark Blue (Deep Water)
- **Source**: `{ "range": [62, 92], "rgb": [34, 47, 191] }`
- **Target**: `((62, 92), (34, 47, 191, 255))`
- ✓ **Match**: Range [62-92), RGB values identical, alpha added

### Color 5: Very Dark Blue (Very Deep Water)
- **Source**: `{ "range": [92, 257], "rgb": [33, 36, 99] }`
- **Target**: `((92, 257), (33, 36, 99, 255))`
- ✓ **Match**: Range [92-257), RGB values identical, alpha added

## Visual Color Gradient

```
5cm                                                                    257cm
├──────────┬──────────┬──────────┬──────────┬──────────────────────────┤
│  Light   │  Medium  │   Blue   │   Dark   │     Very Dark Blue       │
│   Blue   │   Blue   │          │   Blue   │                          │
│ (161,211 │ (88,180, │ (38,114, │ (34,47,  │      (33,36,99)         │
│  ,255)   │  255)    │  222)    │  191)    │                          │
└──────────┴──────────┴──────────┴──────────┴──────────────────────────┘
```

## Integration Points in TiTiler

The flood colormaps are registered and made available through:

1. **ColorMapParams dependency** - Used by all tiler endpoints to accept `colormap_name` parameter
2. **ColorMapFactory** - Provides `/colormaps` endpoints to list and view colormaps
3. **All Tiler factories** - COG, STAC, and Mosaic endpoints all support the flood colormaps

## Usage Examples

### Basic Tile Request
```bash
curl "http://localhost:8000/cog/tiles/10/163/395.png?url=s3://bucket/flood.tif&colormap_name=flood_depth"
```

### With Rescaling
```bash
curl "http://localhost:8000/cog/tiles/10/163/395.png?url=s3://bucket/flood.tif&colormap_name=flood_depth&rescale=5,257"
```

### Preview Image
```bash
curl "http://localhost:8000/cog/preview.png?url=s3://bucket/flood.tif&colormap_name=flood_depth" -o flood_preview.png
```

### List All Colormaps (including flood)
```bash
curl "http://localhost:8000/colormaps"
```

### Get Flood Colormap Details
```bash
curl "http://localhost:8000/colormaps/flood_depth"
```

## Verification

Both Python files compile successfully:
- ✓ `custom_colormaps.py` - Syntax valid
- ✓ `main.py` - Syntax valid, integrates custom colormaps

The implementation is complete and ready for use!
