A small utility that takes a set of CityGML input files
collects all their buildings and gathers them in a single
CityGML resulting file.

## Installation
```bash
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```

## Usages
* With input files:
```bash
(venv)$ python CityGMLBuildingBlender.py --inputFiles filename_1.gml filename_2.gml <...filename_n.gml...> --output output.gml
```

* With input folder:
```bash
(venv)$ python CityGMLBuildingBlender.py --inputFolder ./CityGMLFiles --output output.gml
```

* Mixing input files and folder:
```bash
(venv)$ python CityGMLBuildingBlender.py --inputFiles filename_1.gml filename_2.gml <...filename_n.gml...> --inputFolder ./CityGMLFiles --output output.gml
```