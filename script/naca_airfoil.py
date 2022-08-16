import collections as c
import shutil
import typing as t
import pathlib as p

import matplotlib.pyplot as plt
import numpy as np

from foam import Foam


Path = t.Union[str, p.Path]


class Airfoil:
    def __init__(
        self,
        template: Path, directory: Path, time: float, velocity: float,
    ) -> None:
        self._foam = Foam.from_file(template)
        self._foam['foam']['system', 'controlDict', 'endTime'] = time
        self._directory = p.Path(directory)
        self._velocity = velocity

    @property
    def v(self) -> float:
        return self._velocity

    def forces(self, *thetas: float) -> t.Dict[str, t.List[float]]:
        data = c.defaultdict(list)
        for theta in thetas:
            forces = self._forces(theta)
            if forces is not None:
                data['theta'].append(theta)
                for name, force in forces.items():
                    data[name].append(force)
        return dict(data)

    def _forces(self, theta: float) -> t.Optional[t.Dict[str, float]]:
        path = self._directory / str(theta)
        if not path.exists():
            if not self._save_and_run(path, theta):
                return None
        keys = ('time', 'Cm', 'Cd', 'Cl', 'Cl(f)', 'Cl(r)')
        data = np.loadtxt(path/'postProcessing/forces/0/forceCoeffs.dat')
        return dict(zip(keys, data[-1]))

    def _save_and_run(self, path: p.Path, theta: float) -> bool:
        x = self._velocity * np.cos(theta)
        y = self._velocity * np.sin(theta)
        self._foam['foam']['0', 'U', 'internalField'] = f'uniform ({x} {y} 0)'
        self._foam['foam']['0', 'U', 'boundaryField', 'INLE1', 'UInf'] = f'({9*x} {9*y} 0)'
        self._foam['foam']['0', 'U', 'boundaryField', 'INLE1', 'value'] = f'uniform ({x} {y} 0)'
        self._foam['foam']['0', 'U', 'boundaryField', 'OUTL2', 'inletValue'] = f'uniform ({x} {y} 0)'
        self._foam['foam']['0', 'U', 'boundaryField', 'OUTL2', 'value'] = f'uniform ({x} {y} 0)'
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

    thetas = np.linspace(-np.pi/2, np.pi/2, 51)
    case = Airfoil(
        template='template/nacaAirfoil.yaml', directory='static/case',
        time=1e-5, velocity=340.29,
    )
    data = case.forces(*thetas)

    Figure(figsize=(12, 9)) \
        .plot(data['theta'], data['Cl'], label=r'Lift ($C_l$)') \
        .plot(data['theta'], data['Cd'], label=r'Drag ($C_d$)') \
        .set(
            title=fr'($C_l$/$C_d$) vs. $\alpha$ ($|v|$={case.v})',
            xlabel=r'Angle of Attack ($\alpha$)',
            ylabel=r'Coefficient ($C$)',
        ) \
        .save('static/nacaAirfoil.png', legend_ncol=1, grid=True, transparent=True)

    p.Path('static/nacaAirfoil.json').write_text(json.dumps(data))
