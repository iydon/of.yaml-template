import shutil
import typing as t
import pathlib as p

import matplotlib.pyplot as plt
import numpy as np

from foam import Foam


Array = t.List[float]
Path = t.Union[str, p.Path]


class DamBreak:
    def __init__(
        self,
        template: Path, directory: Path, time: float, interval: float,
    ) -> None:
        self._foam = Foam.from_file(template)
        self._foam['foam']['system', 'controlDict', 'endTime'] = time
        self._foam['foam']['system', 'controlDict', 'writeInterval'] = interval
        self._directory = p.Path(directory)

    def locations(self, width: float, *heights: float) -> t.Dict[float, t.Tuple[Array, Array]]:
        data = {}
        for height in heights:
            locations = self._locations(width, height)
            if locations is not None:
                data[height] = locations
        return data

    def _locations(self, width: float, height: float) -> t.Optional[t.Tuple[Array, Array]]:
        path = self._directory / f'{width},{height}'
        if not path.exists():
            if not self._save_and_run(path, width, height):
                return None
        else:
            self._foam._dest = path
        data = self._foam.post.centroid('alpha.water')
        self._foam._post = None
        xs, ys, _ = zip(*(data[key] for key in sorted(data)))
        return list(map(float, xs)), list(map(float, ys))

    def _save_and_run(self, path: p.Path, width: float, height: float) -> bool:
        self._foam['foam']['system', 'setFieldsDict', 'regions', 0, 'box'] = f'(0 0 -1) ({width} {height} 1)'
        self._foam.save(path)
        rets = self._foam.cmd.all_run(overwrite=False, parallel=False)
        if sum(rets) != 0:
            shutil.rmtree(path)
            return False
        else:
            return True


class Figure:
    Self = __qualname__

    def __init__(self, figsize: t.Optional[t.Tuple[int, int]] = None) -> None:
        self._fig, self._ax = plt.subplots(1, figsize=(figsize or (16, 9)))

    def plot(self, x: t.Any, y: t.Any, label: str, **kwargs) -> Self:
        kwargs = {
            'marker': 'o', 'markersize': 7, 'label': label,
            **kwargs,
        }
        self._ax.plot(x, y, **kwargs)
        return self

    def set(self, **kwargs) -> Self:
        self._ax.set(**kwargs)
        return self

    def save(self, path: str, legend_ncol: int = 0, grid: bool = True, transparent: bool = False) -> Self:
        if legend_ncol:
            self._ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0, ncol=legend_ncol)
        if grid:
            self._ax.grid()
        self._fig.savefig(path, bbox_inches='tight', transparent=transparent)
        return self


if __name__ == '__main__':
    import json

    width = 0.1461
    heights = np.linspace(0.1, 0.5, 5)
    case = DamBreak(
        template='template/damBreak.yaml', directory='static/case',
        time=3.0, interval=0.1,
    )
    data = case.locations(width, *heights)

    figure = Figure(figsize=(12, 9))
    for height, (xs, ys) in data.items():
        figure.plot(xs, ys, label=f'height={height:.01f}', markersize=3)
    figure \
        .set(
            title=f'Centroid of Water (width={width})',
            xlabel='X Coordinate',
            ylabel='Y Coordinate',
        ) \
        .save('static/damBreak.png', legend_ncol=1, grid=True, transparent=True)

    p.Path('static/damBreak.json').write_text(json.dumps(data))
