"""Bounded primary GWOSC metadata only. Never fetch strain/posterior bytes."""
import argparse
import hashlib
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIMIT = 5_000_000


def metadata_url(url):
    p = urllib.parse.urlsplit(url)
    if p.scheme != "https" or p.hostname not in ("gwosc.org", "www.gwosc.org") or p.username or p.password:
        raise ValueError("Only primary GWOSC HTTPS metadata")
    if any(x in p.path.lower() for x in (".hdf", ".h5", ".gwf", ".gz", ".npz", ".pkl", "posterior")):
        raise ValueError("Scientific data/archive endpoint prohibited")
    if not p.path.startswith(("/eventapi/", "/archive/links/", "/timeline/", "/data/", "/catalog/", "/GWTC", "/O4", "/about/", "/acknowledgments/", "/api/")):
        raise ValueError("Unreviewed metadata route")
    return url


class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, url):
        metadata_url(url)
        return super().redirect_request(request, fp, code, msg, headers, url)


def exclusive(path, raw):
    temporary = path.with_name(path.name + ".pending")
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.stat().st_size != len(raw):
        raise OSError("Incomplete metadata write")
    os.link(temporary, path)
    temporary.unlink()


def fetch(url, label):
    metadata_url(url)
    if not label.replace("_", "").replace("-", "").isalnum():
        raise ValueError("Unsafe label")
    folder = HERE / "metadata"
    folder.mkdir(exist_ok=True)
    receipt_path = folder / (label + ".receipt.json")
    body_path = folder / (label + ".body")
    if receipt_path.exists() or body_path.exists():
        raise FileExistsError("Preserve earlier metadata snapshot")
    receipt = {"url": url, "started_utc": datetime.now(timezone.utc).isoformat(), "method": "GET_METADATA_ONLY"}
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "IALD-E3-readiness-metadata/1", "Accept-Encoding": "identity"})
        with urllib.request.build_opener(Redirect()).open(request, timeout=25) as response:
            final = metadata_url(response.geturl())
            content_type = response.headers.get("Content-Type", "")
            if not any(t in content_type for t in ("json", "html", "text/plain")):
                raise ValueError("Non-metadata content type: " + content_type)
            raw = response.read(LIMIT + 1)
            if len(raw) > LIMIT:
                raise ValueError("Metadata size cap exceeded")
            receipt.update(status="METADATA_READ_NO_SCIENCE_BYTES", final_url=final,
                           content_type=content_type, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(),
                           HTTP_headers={key: response.headers.get(key) for key in ("Last-Modified", "ETag", "Content-Length")})
        exclusive(body_path, raw)
        receipt["body_relative_to_sidecar"] = str(body_path.relative_to(HERE))
    except Exception as error:
        receipt.update(status="METADATA_FETCH_FAILED", error=repr(error))
    receipt["finished_utc"] = datetime.now(timezone.utc).isoformat()
    receipt["script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    exclusive(receipt_path, (json.dumps(receipt, indent=2) + "\n").encode())
    print(json.dumps(receipt))
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("label")
    args = parser.parse_args()
    fetch(args.url, args.label)
