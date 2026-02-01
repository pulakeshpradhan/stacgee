"""Earth Engine STAC Catalog."""

import re
from typing import Union

import requests

from .custom_types import ListNamespace
from .dataset import Dataset
from .feature_collection import FeatureCollection
from .image import Image
from .image_collection import ImageCollection
from .stac import STAC


class LazyDataset(STAC):
    def __init__(self, href: str, name: str, parent):
        """Catalog."""
        super(LazyDataset, self).__init__(href, name, parent)
        self.data = {}

    def __call__(self):
        """Fetch data and return the corresponding object."""
        super(LazyDataset, self).__call__()
        eetype = self.data.get("gee:type")
        if eetype == "image":
            # fetch data here
            ds = Image(self.href, self.name, self.parent)()
        elif eetype == "image_collection":
            ds = ImageCollection(self.href, self.name, self.parent)()
        elif eetype == "table":
            ds = FeatureCollection(self.href, self.name, self.parent)()
        else:
            ds = Dataset(self.href, self.name, self.parent)()
        return ds


class Catalog(STAC):
    def __init__(self, href: str, name: str, parent=None):
        """Catalog."""
        super(Catalog, self).__init__(href, name, parent)
        self.data = {}
        self.children: ListNamespace[Union["Catalog", Dataset, LazyDataset]] = ListNamespace(
            key="name"
        )

    def __call__(self):
        """Fetch data."""
        if self.is_lazy():
            self.data = requests.get(self.href).json()
            self._parse_contents()
            self._lazy = False
        return self

    def _parse_contents(self):
        """Parse contents (links) of the catalog."""
        for link in self.data.get("links", []):
            if link["rel"] == "child":
                href = link["href"]
                # Try to get a title, fallback to id or filename
                title = link.get("title") or link.get("id") or href.split("/")[-1].split(".")[0]
                name = title.replace("-", "_").replace(" ", "_")

                # Remove parent name prefix if exists
                if self.name and re.match(f"^{self.name}", name):
                    clean_name = name.replace(f"{self.name}_", "")
                    if clean_name:
                        name = clean_name

                # Determine if it's a sub-catalog or a dataset
                # This is a bit tricky without fetching, so we use LazyDataset
                # which will decide upon being called.
                item = LazyDataset(href, name, self)
                self.children._append(item)
                try:
                    self.__setattr__(name, item)
                except AttributeError:
                    # In case of name collisions or invalid names
                    pass


class STACCatalog(Catalog):
    """A generic STAC Catalog that can be initialized from any STAC URL."""

    def __init__(self, href: str, name: str | None = None):
        if name is None:
            name = href.split("/")[-1].split(".")[0]
        super(STACCatalog, self).__init__(href, name)


class EECatalog(Catalog):
    """Earth Engine STAC Catalog.

    This Catalog contains a set of Catalogs accessible via attributes.

    This is always the root for all children.
    """

    base_url = "https://earthengine-stac.storage.googleapis.com/catalog/catalog.json"

    def __init__(self):
        """Earth Engine STAC Catalog."""
        super(EECatalog, self).__init__(self.base_url, "EECatalog")
        self.__call__()


class STACIndex(STAC):
    """STAC Index Catalog.

    Fetches all public catalogs listed on stacindex.org.
    """

    api_url = "https://stacindex.org/api/catalogs"

    def __init__(self):
        """STAC Index."""
        super(STACIndex, self).__init__(self.api_url, "STACIndex")
        self.children = ListNamespace(key="name")
        self.data = requests.get(self.api_url).json()
        self._get_catalogs()

    def _get_catalogs(self):
        """Parse catalogs from STAC Index API."""
        for entry in self.data:
            title = entry.get("title") or entry.get("slug")
            name = title.replace("-", "_").replace(" ", "_").replace(".", "_")
            href = entry.get("url")

            if not href:
                continue

            # Create a generic STAC Catalog for each entry
            catalog = Catalog(href, name, self)
            self.children._append(catalog)
            try:
                self.__setattr__(name, catalog)
            except AttributeError:
                pass
