
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

.. code-block:: python

    from stacgee import eecatalog

    # a lazy object does not contain the complete data but only the reference (name and url)
    landsat_lazy = eecatalog.LANDSAT

    # to fetch all data you need to call it
    landast = eecatalog.LANDSAT()

    # if you do this in runtime, the `landsat` object contains all datasets as attributes
    # if you don't do it in runtime you won't be able to see the datasets (attributes)

    # it works the same with datasets
    # lazy dataset
    l9_lazy = landsat.LC09_C02_T1
    # fetch L9 data
    l9 = landsat.LC09_C02_T1()


Credits
-------
Author: Pulakesh Pradhan

This package was created with `Copier <https://copier.readthedocs.io/en/latest/>`__ and the `@12rambau/pypackage <https://github.com/12rambau/pypackage>`__ 0.1.16 project template.
