import base64, pathlib

# 把内联字体的 base64 填进源文件，产出一份可独立打开的 index.html
d = pathlib.Path(__file__).resolve().parent
src = (d / "圣诞树.src.html").read_text(encoding="utf-8")
font = (d / "great-vibes-latin.woff2").read_bytes()
uri = "data:font/woff2;base64," + base64.b64encode(font).decode("ascii")

out = src.replace("__FONT_URI__", uri)
assert "__FONT_URI__" not in out
(d / "index.html").write_text(out, encoding="utf-8")
print("ok", len(out))
