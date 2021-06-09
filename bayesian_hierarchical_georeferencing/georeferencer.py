from pathlib import Path

import numpy as np
import pandas as pd
import rasterio as rio

from bayesian_hierarchical_georeferencing.region_builder import RegionBuilder
from bayesian_hierarchical_georeferencing.region import Region


def georeference(
        name: str,
        data_dir: Path,
        original_map: np.ndarray,
        gcp: pd.DataFrame,
        regions: pd.DataFrame,
):
    full_map = Region.from_map(
        name=name,
        image=original_map,
        gcp=gcp,
    )
    region_builder = RegionBuilder(
        full_map,
        regions,
    )

    full_map.wld.to_wld(data_dir)


if __name__ == '__main__':
    data_dir = Path('../data')
    original_map = rio.open(data_dir / 'plan_1802.jpg').read()
    regions = pd.read_csv(data_dir / 'plan_1802.jpg.regions')
    points = pd.read_csv(data_dir / 'plan_1802.jpg.points')

    georeference(
        'plan_1802',
        data_dir,
        original_map,
        points,
        regions,
    )
