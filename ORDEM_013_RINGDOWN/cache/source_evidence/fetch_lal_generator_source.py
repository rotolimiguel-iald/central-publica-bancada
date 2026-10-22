"""Read public generator source at the exact installed LAL commit, no build."""
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.parse import quote
import json
import argparse
import lalsimulation as lal
import source_evidence as se


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--origin", choices=["github", "gitlab"], default="github")
    parser.add_argument("--file", choices=["LALSimIMRSpinAlignedEOB.c", "LALSimInspiral.c", "LALSimInspiralGeneratorLegacy.c"], default="LALSimIMRSpinAlignedEOB.c")
    args = parser.parse_args()
    folder = se.ROOT/("lal_generator_source" if args.origin == "github" else "lal_generator_source_gitlab")
    if args.file != "LALSimIMRSpinAlignedEOB.c":
        folder = folder.with_name(folder.name+"_"+args.file[:-2])
    folder.mkdir(exist_ok=False)
    info = lal.SimulationVCSInfo
    commit = info.vcsId
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise ValueError("Installed commit is not a SHA1 identifier")
    name = args.file
    relative = "lalsimulation/lib/"+name
    prefix = ("https://raw.githubusercontent.com/lscsoft/lalsuite/" if args.origin == "github"
              else "https://git.ligo.org/lscsoft/lalsuite/-/raw/")
    url = prefix+quote(commit,safe="")+"/"+quote(relative,safe="/")
    record = dict(date_utc=datetime.now(timezone.utc).isoformat(), installed_version=lal.__version__,
                  installed_commit=commit, installed_tag=info.vcsTag, url=url,
                  scope="Read-only primary-source inspection; installed libraries unchanged")
    try:
        request = Request(url, headers={"User-Agent":"TGL-ringdown-numerical-audit/1.0"})
        with urlopen(request, timeout=30) as response:
            raw = response.read(2_000_000)
        expected = b"XLALSimIMRSpinAlignedEOBModes" if name == "LALSimIMRSpinAlignedEOB.c" else b"SimInspiral"
        if expected not in raw or len(raw)>=2_000_000:
            raise ValueError("Unexpected source response")
        temporary = folder/(name+".tmp")
        temporary.write_bytes(raw)
        if temporary.stat().st_size != len(raw):
            raise ValueError("Short public-source write")
        temporary.replace(folder/name)
        record.update(status="FETCHED_EXACT_INSTALLED_SOURCE", bytes=len(raw), sha256=se.sha(folder/name))
    except Exception as exc:
        record.update(status="PUBLIC_SOURCE_FETCH_FAILED", error=type(exc).__name__+": "+str(exc))
    se.write(folder/"PROVENANCE.json",record)
    print(json.dumps(record),flush=True)


if __name__=="__main__":
    main()
