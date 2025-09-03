# Scraping geo data

This folder contains scripts to extract geojson directly from official pages, allow extraction in short time without a need to download all the file if you just need extract and use the data over your static maps over notebooks

## Colombia geojson

The main source for Colombia geojson map is [MGN_MPIO_POLITICO DANE](https://www.arcgis.com/home/item.html?id=129f3fe8e3424cc7ba3fc19ff1522026) a detailed layer with political division offered by a public entity. This source is implemented by the script to extract all the country or just segments by "departamento" which plays a part of states of another foreing countrys in the region.

Those scrips are:

- [`full_import_geojson_Colombia.py`](./scraping_geodata/full_import_geojson_Colombia.py): Review all the web file, without downloading to reivew content.
- [`filtering_geojson_Colombia.py`](./scraping_geodata/filtering_geojson_Colombia.py): Works as a class to extract all data and be used by another script to filtering and manipulation.
- [`filter_departamento_geojson_COL.py`](./scraping_geodata/filter_departamento_geojson_COL.py): Is an semi interactive script to filtering the geojson file by "departamento" and saving the file. For now works by individual results.

## How to use this

By best practice clone the repository and execute in the command line the next line:

```bash
 python .\scraping_geodata\filter_departamento_geojson_COL.py --departamento NOMBRE_DEPARTAMENTO
```

All "departamento" names are writen in uppercase and include the correct Spanish accent marks (e.g., ANTIOQUÍA, CUNDINAMARCA, VALLE DEL CAUCA). This is important to ensure the script works properly.
