#!/usr/bin/env python3
"""Fetch City of London buildings or roads from Overpass API -> compact GeoJSON."""
import json, sys, urllib.request

# bbox: south, west, north, east — City of London cluster + Shard
BBOX = "51.503,-0.095,51.520,-0.070"
OUT_DIR = "/sessions/sleepy-dreamy-brahmagupta/mnt/outputs"

QUERIES = {
    "buildings": f'[out:json][timeout:35];way["building"]({BBOX});out geom;',
    "roads": f'[out:json][timeout:35];way["highway"~"^(motorway|trunk|primary|secondary|tertiary|residential|unclassified|pedestrian)$"]({BBOX});out geom;',
}

def parse_height(tags):
    h = tags.get("height") or tags.get("building:height")
    if h:
        try:
            return float(str(h).replace("m", "").strip())
        except ValueError:
            pass
    lv = tags.get("building:levels")
    if lv:
        try:
            return float(lv) * 3.2
        except ValueError:
            pass
    return None

def main(kind):
    q = QUERIES[kind]
    req = urllib.request.Request(
        "https://overpass-api.de/api/interpreter",
        data=("data=" + urllib.parse.quote(q)).encode(),
        headers={"User-Agent": "claude-cowork-viz/1.0"},
    )
    with urllib.request.urlopen(req, timeout=40) as r:
        data = json.load(r)
    feats = []
    for el in data.get("elements", []):
        if el.get("type") != "way" or "geometry" not in el:
            continue
        coords = [[round(p["lon"], 6), round(p["lat"], 6)] for p in el["geometry"]]
        tags = el.get("tags", {})
        if kind == "buildings":
            if len(coords) < 4 or coords[0] != coords[-1]:
                continue
            props = {"h": parse_height(tags)}
            if tags.get("name"):
                props["name"] = tags["name"]
            geom = {"type": "Polygon", "coordinates": [coords]}
        else:
            if len(coords) < 2:
                continue
            props = {"hw": tags.get("highway")}
            geom = {"type": "LineString", "coordinates": coords}
        feats.append({"type": "Feature", "properties": props, "geometry": geom})
    fc = {"type": "FeatureCollection", "features": feats}
    path = f"{OUT_DIR}/london_{kind}.geojson"
    with open(path, "w") as f:
        json.dump(fc, f, separators=(",", ":"))
    named = sum(1 for f_ in feats if f_["properties"].get("name"))
    withh = sum(1 for f_ in feats if f_["properties"].get("h"))
    print(json.dumps({"kind": kind, "features": len(feats), "with_height": withh, "named": named, "path": path}))

if __name__ == "__main__":
    main(sys.argv[1])
