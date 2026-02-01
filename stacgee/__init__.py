"""The init file of the package."""

__version__ = "0.0.1"
__author__ = "Pulakesh Pradhan"
__email__ = "pulakesh.mid@gmail.com"

from .catalog import EECatalog, STACCatalog, STACIndex
from .feature_collection import FeatureCollection as _FeatureCollection
from .image import Image as _Image
from .image_collection import ImageCollection as _ImageCollection

eecatalog = EECatalog()
stacindex = STACIndex()


def fromId(assetId: str):
    """Load a Catalog or Dataset from an ID."""
    assetId = assetId.replace("ee://", "")
    parts = assetId.split("/")
    if len(parts) == 1:
        try:
            return eecatalog.children.as_dict()[assetId]()
        except KeyError:
            # Maybe it's a dataset in the root catalog?
            # Browsing through catalogs
            for catalog_name in eecatalog.children.keys():
                cat = getattr(eecatalog, catalog_name)()
                if assetId in cat.children.keys():
                    return getattr(cat, assetId)()
            raise KeyError(f"Asset ID {assetId} not found in catalog.")
    else:
        try:
            catalog = eecatalog.children.as_dict()[parts[0]]()
            dataset_name = "_".join(parts[1:])
            # Handle some cases where the ID in STAC includes the catalog name again
            if dataset_name not in catalog.children.keys():
                full_name = "_".join(parts)
                if full_name in catalog.children.keys():
                    dataset_name = full_name
            return catalog.children.as_dict()[dataset_name]()
        except KeyError:
            # Fallback to searching all catalogs if the first part isn't a direct hit
            for catalog_name in eecatalog.children.keys():
                cat = getattr(eecatalog, catalog_name)()
                dataset_name = "_".join(parts)
                if dataset_name in cat.children.keys():
                    return getattr(cat, dataset_name)()
            raise KeyError(f"Asset ID {assetId} not found in catalog.")


def Image(assetId: str) -> _Image:
    """Load an Image from an ID."""
    obj = fromId(assetId)
    if not isinstance(obj, _Image):
        raise TypeError(f"Asset {assetId} is not an Image.")
    return obj


def ImageCollection(assetId: str) -> _ImageCollection:
    """Load an ImageCollection from an ID."""
    obj = fromId(assetId)
    if not isinstance(obj, _ImageCollection):
        raise TypeError(f"Asset {assetId} is not an ImageCollection.")
    return obj


def FeatureCollection(assetId: str) -> _FeatureCollection:
    """Load a FeatureCollection from an ID."""
    obj = fromId(assetId)
    if not isinstance(obj, _FeatureCollection):
        raise TypeError(f"Asset {assetId} is not a FeatureCollection.")
    return obj
