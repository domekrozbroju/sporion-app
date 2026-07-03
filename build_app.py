#!/usr/bin/env python3
"""Sestaví sporion_app.html ze tří zdrojových témat.
Každý zdroj se zakóduje base64 a vloží jako data-URL do <iframe>.
Spuštění:  python3 build_app.py
"""
import base64, os

HERE = os.path.dirname(os.path.abspath(__file__))

FRAMES = [
    ("frame-minimal", "sporion_minimal_spa2.html", True),   # výchozí aktivní
    ("frame-pixel",   "sporion_pixel_spa.html",    False),
    ("frame-noir",    "sporion_noir3.html",        False),
]

def b64(path):
    with open(os.path.join(HERE, path), "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

iframes = "\n".join(
    '<iframe id="{id}"{active} src="data:text/html;base64,{data}"></iframe>'.format(
        id=fid,
        active=' class="active"' if active else "",
        data=b64(src),
    )
    for fid, src, active in FRAMES
)

html = """<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sporion</title>
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{ width: 100%; height: 100%; overflow: hidden; }}
iframe {{ width: 100%; height: 100%; border: none; display: none; background: #fff; }}
iframe.active {{ display: block; }}
</style>
</head>
<body>
{iframes}
<script>
function switchTheme(t){{document.querySelectorAll('iframe').forEach(f=>f.classList.remove('active'));const x=document.getElementById('frame-'+t);if(x){{x.classList.add('active');if(x.contentWindow)x.contentWindow.postMessage({{sporion:'shown'}},'*');}}}}
// Sdílený stav potů napříč tématy (data-URL iframy nesdílí localStorage)
var _master=null;
function _postState(win){{ if(win&&_master) win.postMessage({{sporion:'state',pots:_master.pots,archive:_master.archive}},'*'); }}
function _broadcast(except){{ document.querySelectorAll('iframe').forEach(function(f){{ if(f.contentWindow&&f.contentWindow!==except) _postState(f.contentWindow); }}); }}
window.addEventListener('message',function(e){{
  var d=e.data; if(!d) return;
  if(d.theme){{ switchTheme(d.theme); return; }}
  if(d.sporion==='hello'){{ if(!_master) _master={{pots:d.pots||[],archive:d.archive||[]}}; _postState(e.source); return; }}
  if(d.sporion==='sync'){{ _master={{pots:d.pots||[],archive:d.archive||[]}}; _broadcast(e.source); return; }}
  if(d.sporion==='view'){{ document.querySelectorAll('iframe').forEach(function(f){{ if(f.contentWindow&&f.contentWindow!==e.source) f.contentWindow.postMessage(d,'*'); }}); return; }}
  if(d.sporion==='lang'){{ document.querySelectorAll('iframe').forEach(function(f){{ if(f.contentWindow&&f.contentWindow!==e.source) f.contentWindow.postMessage(d,'*'); }}); if(window.parent && window.parent!==window && e.source!==window.parent) window.parent.postMessage(d,'*'); return; }}
}});
</script>
</body>
</html>
""".format(iframes=iframes)

out = os.path.join(HERE, "sporion_app.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)

print("OK -> sporion_app.html ({:,} bytes)".format(os.path.getsize(out)))
