import stacgee
import ee

# Initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='my-project')

def print_dataset_info(dataset):
    print(f"Dataset: {dataset.name}")
    print(f"Asset ID: {dataset.assetId}")
    print(f"Status: {dataset.status}")
    print(f"Start Date: {dataset.start_date}")
    print(f"Bands: {dataset.bands.keys()}")
    print("-" * 20)

# Example 1: Dynamic World V1
# Dynamic World is a near real-time 10m land use land cover dataset.
# The STAC metadata provides rich info about the classes.
print("--- Example 1: Dynamic World ---")
dw = stacgee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
print_dataset_info(dw)

# Accessing class information directly from STAC
label_band = dw.bands.label
print("Dynamic World Classes:")
for category in label_band.class_info:
    print(f"  {category.value}: {category.description} (Color: {category.color})")

# Example 2: Sentinel-2 Surface Reflectance
# Showing how to access bitmask definitions for Quality Assurance bands.
print("\n--- Example 2: Sentinel-2 SR ---")
s2 = stacgee.ImageCollection("COPERNICUS/S2_SR")
qa = s2.bands.QA60
if hasattr(qa, "bitmask"):
    print("Sentinel-2 QA60 Bitmask:")
    import json
    print(json.dumps(qa.bitmask.to_dict(), indent=2))

# Example 3: MODIS Land Surface Temperature
# Showing scaling and offset factors stored in STAC.
print("\n--- Example 3: MODIS LST ---")
modis = stacgee.ImageCollection("MODIS/061/MOD11A1")
lst_day = modis.bands.LST_Day_1km
print(f"Band: {lst_day.name}")
print(f"Description: {lst_day.description}")
print(f"Multiplied/Scale: {lst_day.multiplier}")
print(f"Offset: {lst_day.offset}")

# Example 4: Working like native Google Earth Engine
# Because we added delegation, you can call GEE methods directly.
print("\n--- Example 4: Mixed STAC/GEE usage ---")
# filterDate is a GEE method, not a STAC method.
# It works because stacgee proxies to the underlying ee.ImageCollection!
filtered = dw.filterDate('2023-01-01', '2023-01-02')
print(f"Filtered GEE Object Type: {type(filtered)}")
# Note: Computation returns native GEE objects.
count = filtered.size().getInfo()
print(f"Images found in range: {count}")
