"""Collect only URL listings and DQ intervals for the five fixed metadata targets."""
import json
from pathlib import Path
from fetch_metadata_v2 import fetch

HERE = Path(__file__).resolve().parent
TARGETS = ["GW230919_215712", "GW241111_111552", "GW240513_183302", "GW240920_073424", "GW250118_170523"]


def main():
    for event in TARGETS:
        label = event + ("_retry" if event == "GW230919_215712" else "")
        entry = next(iter(json.loads((HERE / "metadata" / (label + ".body")).read_bytes())["events"].values()))
        streams = [item for item in entry["strain"] if item["detector"] in ("H1", "L1")
                   and item["format"] == "hdf5" and item["sampling_rate"] == 4096]
        if len(streams) != 2:
            raise ValueError("Expected one H1 and one L1 file")
        start = min(item["GPSstart"] for item in streams) - 4096
        end = max(item["GPSstart"] + item["duration"] for item in streams)
        run = "O4a" if event.startswith("GW23") else "O4b"
        for detector in ("H1", "L1"):
            if event == "GW230919_215712" and detector == "H1":
                continue  # Already archived in this task; never repeat it.
            fetch(f"https://gwosc.org/archive/links/{run}_4KHZ_R1/{detector}/{start}/{end}/json/",
                  f"archive_{detector}_{event}")
        if event != "GW230919_215712":
            fetch(f"https://gwosc.org/timeline/segments/all/{run}/{start}/{end-start}/", "timeline_" + event)


if __name__ == "__main__":
    main()
