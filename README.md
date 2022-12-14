# Example repository using [ifoam](https://github.com/iydon/of.yaml) library
## Dependency Management
| Tool                                              | File                                            |
| ------------------------------------------------- | ----------------------------------------------- |
| [pip](https://github.com/pypa/pip)                | [requirements.txt](config/pip/requirements.txt) |
| [pipenv](https://github.com/pypa/pipenv)          | [Pipfile](config/pipenv/Pipfile)                |
| [poetry](https://github.com/python-poetry/poetry) | [pyproject.toml](config/poetry/pyproject.toml)  |
| [pdm](https://github.com/pdm-project/pdm)         | [pyproject.toml](config/pdm/pyproject.toml)     |


## Available Script(s)
| File                                      | Description                                                                                                                                                                                                              |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [dam_break.py](script/dam_break.py)       | By changing the height of water in the [damBreak](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/multiphase/interFoam/laminar/damBreak/damBreak) case to find the corresponding centroid of water.         |
| [naca_airfoil.py](script/naca_airfoil.py) | By changing the angle of attack in the [nacaAirfoil](https://github.com/OpenFOAM/OpenFOAM-7/tree/master/tutorials/compressible/rhoPimpleFoam/RAS/nacaAirfoil) case to find the corresponding lift and drag coefficients. |


## Visualization Result(s)
### [damBreak](script/dam_break.py)
![](static/damBreak.png)

### [nacaAirfoil](script/naca_airfoil.py)
![](static/nacaAirfoil.png)
