"""
Created By David Camelo on 03/09/2025
Helped by ChatGPT

Script to extract public Colombia geojson shape
wihtout directly downloading dependency
"""

import requests


class ArcGISDownloader:
    def __init__(self, url, outSR=4326, max_records=2000):
        self.url = url
        self.outSR = outSR
        self.max_records = max_records

    def download(self, where="1=1", as_geojson=True):
        # Implement API query template for filtering
        params = {
            "where": where,
            "outFields": "*",
            "outSR": self.outSR,
            "f": "geojson" if as_geojson else "json",
            "resultOffset": 0,
            "resultRecordCount": self.max_records,
        }

        # Review file structure
        features = []
        while True:
            r = requests.get(self.url, params=params)
            data = r.json()
            if "features" not in data or len(data["features"]) == 0:
                break
            features.extend(data["features"])
            params["resultOffset"] += params["resultRecordCount"]

        # Returnig file
        return {"type": "FeatureCollection", "features": features}
