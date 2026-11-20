python3 - <<'PY'
m=open('/home/claude/pipe/manifest.json').read()
s=open('/home/claude/pipe/index.src.html').read().replace('__MANIFEST__',m)
open('/home/claude/bastion/index.html','w').write(s)
PY
python3 -I /home/claude/pipe/webp.py >/dev/null
