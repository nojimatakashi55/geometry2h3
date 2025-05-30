# geometry2h3
Convert various geometry to H3 cells.

---

## 📦 Features

- 🧭 Convert GeoJSON, Shapely geometry, or WKT to H3 indexes
- 🧮 Supports arbitrary H3 resolutions
- 🔁 Output as set or list of H3 cells
- 📐 Easy integration with spatial analysis pipelines

---

## 🚀 Installation

Install via pip:

```bash
pip install geometry2h3
```

Or from source:
```bash
git clone https://github.com/nojima-t/geometry2h3.git
cd geometry2h3
pip install .
```

---

## 🛠️ Usage

Example: Convert GeoJSON Polygon

```python
from geometry2h3 import convert_geometry_to_h3

geojson = {
    "type": "Polygon",
    "coordinates": [[[138.0, 36.0], [138.1, 36.0], [138.1, 36.1], [138.0, 36.1], [138.0, 36.0]]]
}

hexes = convert_geometry_to_h3(geojson, resolution=8)
print(hexes)
```

---

## 🧪 Tests

```bash
pip install -r requirements.txt
pytest
```

---

## 📁 Project Structure

```
geometry2h3/
├── geometry2h3/         ← Core module
├── tests/               ← Unit tests
├── pyproject.toml       ← Project metadata
├── requirements.txt     ← Dev dependencies
├── LICENSE
├── README.md
```
