from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from bayesian_hierarchical_georeferencing.region_builder import RegionBuilder
from bayesian_hierarchical_georeferencing.region import Region


def georeference(
        name: str,
        suffix: str,
        data_dir: Path,
        original_map: np.ndarray,
        gcp: pd.DataFrame,
        regions: pd.DataFrame,
):
    full_map = Region.from_map(
        name=name,
        suffix=suffix,
        image=original_map,
        gcp=gcp,
    )
    region_builder = RegionBuilder(
        full_map,
        regions,
    )
    region_builder.split_map()

    full_map.wld.save(data_dir)


if __name__ == '__main__':
    data_dir = Path('../data')
    original_map = plt.imread(data_dir / 'plan_1802.jpg')
    regions = pd.read_csv(data_dir / 'plan_1802.jpg.regions', index_col=0)
    points = pd.read_csv(data_dir / 'plan_1802.jpg.points')

    georeference(
        'plan_1802',
        'jpg',
        data_dir,
        original_map,
        points,
        regions,
    )
