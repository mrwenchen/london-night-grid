# London // Night Grid

An interactive, cinematic 3D visualization of the City of London — 2,487 real building footprints extruded to their true heights over a glowing neon road network. Built in a single chat session with Claude (Fable 5), no 3D software required.

**[▶ Open the live demo](https://mrwenchen.github.io/london-night-grid/london_night_grid.html)** *(enable GitHub Pages: Settings → Pages → deploy from `main`)*

## What this is

A London answer to [Milan Janosov's "One Prompt, 46,000 Buildings" experiment](https://milanjanosov.substack.com) — his mega-prompt built Manhattan; this applies the same spec to the City of London's tower cluster: The Shard (310 m), 22 Bishopsgate (278 m), Heron Tower, the Cheesegrater, and the Gherkin, all at real-world heights from OpenStreetMap.

## Features

- **Real geometry** — OSM building footprints, heights from `height` / `building:levels` tags (log-scale color ramp, navy → pale cyan → white)
- **Neon-pink road network** with a radial "city pulse" wave
- **UnrealBloom glow**, floor scanlines, fresnel rim lighting
- **Full camera control** — drag to rotate, right-drag to pan, scroll to zoom
- **Control panel** — toggle bloom, scanlines, and pulse live
- **Compact data** — coordinates quantized to decimeters and delta-packed into base64 typed arrays (235 KB instead of ~5 MB of GeoJSON)

## Files

| File | Description |
|---|---|
| `london_night_grid.html` | Main visualization (open in any modern browser; loads three.js 0.147 from CDN) |
| `london_neon_3d.html` | Earlier v1 with a different aesthetic (Tron-style edges, cyan palette) |
| `template_nightgrid.html` | HTML/JS template before data injection |
| `payload.json` | Packed binary payload (base64 typed arrays) |
| `london_scene.json` | Intermediate simplified scene data |
| `fetch_osm.py` | Overpass API fetch script (buildings + roads → GeoJSON) |

## Reproduce it for your city

1. Get building footprints and roads from [overpass-turbo.eu](https://overpass-turbo.eu) for your bounding box (`way["building"]` / `way["highway"]`, export as GeoJSON)
2. Feed them to Claude with the mega-prompt from Milan's post
3. Share your city — that's the experiment

## Data & credits

- Map data © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors, licensed under [ODbL](https://opendatacommons.org/licenses/odbl/)
- Rendering: [three.js](https://threejs.org) r147
- Original experiment & mega-prompt: [Milan Janosov](https://substack.com/@milanjanosov)
- Built with [Claude](https://claude.com) (Fable 5) in Cowork mode
