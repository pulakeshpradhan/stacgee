
Google Earth Engine STAC (stacgee)
##################################

.. |license| image:: https://img.shields.io/badge/License-MIT-yellow.svg?logo=opensourceinitiative&logoColor=white
    :target: LICENSE
    :alt: License: MIT

.. |commit| image:: https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg?logo=git&logoColor=white
   :target: https://conventionalcommits.org
   :alt: conventional commit

.. |ruff| image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
   :target: https://github.com/astral-sh/ruff
   :alt: ruff badge

.. |prettier| image:: https://img.shields.io/badge/code_style-prettier-ff69b4.svg?logo=prettier&logoColor=white
   :target: https://github.com/prettier/prettier
   :alt: prettier badge

.. |pre-commmit| image:: https://img.shields.io/badge/pre--commit-active-yellow?logo=pre-commit&logoColor=white
    :target: https://pre-commit.com/
    :alt: pre-commit

.. |pypi| image:: https://img.shields.io/pypi/v/stacgee?color=blue&logo=pypi&logoColor=white
    :target: https://pypi.org/project/stacgee/
    :alt: PyPI version

.. |build| image:: https://img.shields.io/github/actions/workflow/status/pulakeshpradhan/stacgee/unit.yaml?logo=github&logoColor=white
    :target: https://github.com/pulakeshpradhan/stacgee/actions/workflows/unit.yaml
    :alt: build

.. |coverage| image:: https://img.shields.io/codecov/c/github/pulakeshpradhan/stacgee?logo=codecov&logoColor=white
    :target: https://codecov.io/gh/pulakeshpradhan/stacgee
    :alt: Test Coverage

.. |docs| image:: https://img.shields.io/readthedocs/stacgee?logo=readthedocs&logoColor=white
    :target: https://stacgee.readthedocs.io/en/latest/
    :alt: Documentation Status

|license| |commit| |ruff| |prettier| |pre-commmit| |pypi| |build| |coverage| |docs|

Overview
--------

This packages provides an easy and straightforward way of getting Google Earth
Engine STAC information.

To take fully advantage of this package is recommended to use it in runtime
due to `lazy evaluation <https://en.wikipedia.org/wiki/Lazy_evaluation>`__

Installation
------------

.. code-block:: bash

    pip install stacgee

Usage
-----

**stacgee** provides a powerful way to interact with the Google Earth Engine STAC catalog. It can be used both to browse the catalog and to initialize GEE objects with rich metadata.

GEE-like Initialization
^^^^^^^^^^^^^^^^^^^^^^^

You can initialize datasets using their familiar GEE Asset IDs:

.. code-block:: python

    import stacgee
    import ee

    # Initialize ImageCollection (works like ee.ImageCollection but with STAC metadata)
    dw = stacgee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")

    # Access STAC-specific metadata
    print(dw.start_date)
    print(dw.status)  # e.g., "active" or "deprecated"

    # Access underlying GEE object for computation
    # stacgee objects proxy unknown methods to the underlying eeObject!
    filtered = dw.filterDate('2023-01-01', '2023-01-02')
    print(filtered.size().getInfo())

Accessing Rich Metadata
^^^^^^^^^^^^^^^^^^^^^^^

One of the main strengths of **stacgee** is accessing information often "hidden" or hard to reach in GEE:

**Class Information (Categorical Bands)**

.. code-block:: python

    # Get class names and colors for land cover datasets
    label_band = dw.bands.label
    for category in label_band.class_info:
        print(f"{category.value}: {category.description}")

**Bitmask Definitions (QA Bands)**

.. code-block:: python

    # Get human-readable bitmask definitions for quality bands
    s2 = stacgee.ImageCollection("COPERNICUS/S2_SR")
    qa_bits = s2.bands.QA60.bitmask.to_dict()

**Scaling and Offsets**

.. code-block:: python

    # Get physical unit conversion factors
    modis = stacgee.ImageCollection("MODIS/061/MOD11A1")
    lst_band = modis.bands.LST_Day_1km
    print(f"Scale: {lst_band.multiplier}, Offset: {lst_band.offset}")

Browsing the Catalog
^^^^^^^^^^^^^^^^^^^^

You can also browse the catalog as a tree:

.. code-block:: python

    from stacgee import eecatalog

    # Explore available Landsat datasets
    landsat = eecatalog.LANDSAT()
    print(landsat.children.keys())

    # Get a specific dataset
    l9 = landsat.LC09_C02_T1()

Credits
-------
Author: Pulakesh Pradhan

This package was created with `Copier <https://copier.readthedocs.io/en/latest/>`__ and the `@12rambau/pypackage <https://github.com/12rambau/pypackage>`__ 0.1.16 project template.
