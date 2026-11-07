#!/usr/bin/env python3
"""Create a validated ZIP for manual Zenodo deposit, excluding Git history and local files."""
import argparse
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZipInfo
from build_catalog import ROOT, sha
from validate_archive import validate

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'dist/cnsm-2026-cfaip-archive.zip')
    args=parser.parse_args()
    output=args.output.resolve()
    if output.is_relative_to(ROOT) and not output.is_relative_to(ROOT/'dist'):
        parser.error('Inside this repository, package output must be under dist/.')
    files=validate()
    output.parent.mkdir(parents=True,exist_ok=True)
    # Fixed ZIP metadata makes identical repository files yield identical packages.
    with ZipFile(output,'w',compression=ZIP_DEFLATED,compresslevel=6) as z:
        for path in sorted(files):
            entry=ZipInfo('cnsm-2026-cfaip/'+path.relative_to(ROOT).as_posix(),date_time=(2026,11,6,0,0,0))
            entry.compress_type=ZIP_DEFLATED
            entry.external_attr=0o100644 << 16
            z.writestr(entry,path.read_bytes())
    with ZipFile(output) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(files)
    checksum=sha(output)
    output.with_suffix(output.suffix+'.sha256').write_text(f'{checksum}  {output.name}\n')
    print(f'Created {output} ({output.stat().st_size:,} bytes), {len(files)} files. SHA-256: {checksum}')

if __name__=='__main__':
    main()
