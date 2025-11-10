"""Test script to verify the flood colormap implementation."""

import sys

# Test 1: Import the custom colormaps module
print("Test 1: Importing custom_colormaps module...")
try:
    from src.titiler.application.titiler.application.custom_colormaps import (
        custom_colormaps,
        flood_depth_intervals,
        flood_historic_intervals,
    )
    print("✓ Successfully imported custom_colormaps")
except Exception as e:
    print(f"✗ Failed to import: {e}")
    sys.exit(1)

# Test 2: Verify the colormaps are registered
print("\nTest 2: Verifying colormaps are registered...")
try:
    colormap_list = custom_colormaps.list()
    print(f"  Available custom colormaps: {colormap_list}")

    assert "flood_depth" in colormap_list, "flood_depth not in colormap list"
    assert "flood_historic" in colormap_list, "flood_historic not in colormap list"
    print("✓ Both flood colormaps are registered")
except Exception as e:
    print(f"✗ Colormap registration failed: {e}")
    sys.exit(1)

# Test 3: Verify the colormap structure
print("\nTest 3: Verifying colormap structure...")
try:
    flood_depth = custom_colormaps.get("flood_depth")
    print(f"  flood_depth colormap: {flood_depth}")

    # Check that it's a sequence (interval-based colormap)
    assert isinstance(flood_depth, list), "flood_depth should be a list"
    assert len(flood_depth) == 5, f"Expected 5 intervals, got {len(flood_depth)}"

    # Verify first interval
    first_interval = flood_depth[0]
    assert first_interval[0] == (5, 16), f"First interval should be (5, 16), got {first_interval[0]}"
    assert first_interval[1] == (161, 211, 255, 255), f"First color should be (161, 211, 255, 255), got {first_interval[1]}"

    print("✓ Colormap structure is correct")
except Exception as e:
    print(f"✗ Colormap structure verification failed: {e}")
    sys.exit(1)

# Test 4: Merge with default colormaps
print("\nTest 4: Testing merge with default colormaps...")
try:
    from rio_tiler.colormap import cmap as default_cmap

    merged_cmap = default_cmap.register(custom_colormaps.data)
    merged_list = merged_cmap.list()

    # Check that default colormaps are still there
    assert "viridis" in merged_list, "Default colormap 'viridis' should be present"

    # Check that custom colormaps are added
    assert "flood_depth" in merged_list, "Custom colormap 'flood_depth' should be present"
    assert "flood_historic" in merged_list, "Custom colormap 'flood_historic' should be present"

    print(f"✓ Successfully merged. Total colormaps: {len(merged_list)}")
except Exception as e:
    print(f"✗ Merge test failed: {e}")
    sys.exit(1)

# Test 5: Import main application
print("\nTest 5: Testing main application import...")
try:
    from src.titiler.application.titiler.application.main import app, cmap

    # Verify the app was created
    assert app is not None, "App should not be None"

    # Verify custom colormaps are available in the app's cmap
    app_cmap_list = cmap.list()
    assert "flood_depth" in app_cmap_list, "flood_depth not available in app"
    assert "flood_historic" in app_cmap_list, "flood_historic not available in app"

    print("✓ Application imported successfully with flood colormaps")
except Exception as e:
    print(f"✗ Application import failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("All tests passed! ✓")
print("=" * 60)
print("\nThe flood colormaps are now available in titiler:")
print("  - flood_depth: 5 intervals from 5-257 cm")
print("  - flood_historic: 5 intervals from 0-257 cm")
print("\nYou can use them by adding '&colormap_name=flood_depth'")
print("to your tile requests.")
