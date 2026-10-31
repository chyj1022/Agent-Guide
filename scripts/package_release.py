"""Package curated source only. Output ZIP is outside the repository folder."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT.parent/'agent-design-guide.zip'
SKIP_PARTS={'.git','.venv','__pycache__','.agents','.codex'}
SKIP_SUFFIX={'.pyc','.pyo','.pdf','.png','.jpg','.jpeg','.zip'}
files=[p for p in ROOT.rglob('*') if p.is_file() and not any(x in SKIP_PARTS for x in p.relative_to(ROOT).parts)
       and p.suffix.lower() not in SKIP_SUFFIX and not p.name.startswith('.env')]
with ZipFile(DEST,'w',ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(files):z.write(p,Path(ROOT.name)/p.relative_to(ROOT))
with ZipFile(DEST) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)
    assert not any('__pycache__' in n or n.endswith('.pdf') for n in z.namelist())
manifest={'archive':DEST.name,'files':len(files),'bytes':DEST.stat().st_size,
          'sha256':hashlib.sha256(DEST.read_bytes()).hexdigest(),
          'excluded':['raw PDFs','raw OCR','source HTML archives','bytecode','environment files','git internals']}
(ROOT.parent/'agent-design-guide-release.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps(manifest,indent=2))
