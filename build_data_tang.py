# -*- coding: utf-8 -*-
"""《唐诗300首最应该背诵的300句》md -> entries.json + data.js（PWA 数据）
拼音全部来自 build_book_tang.py 的 PINYIN_OVERRIDE 人工核对表（300 条全覆盖）。
"""
import re, os, json
from pypinyin import pinyin as pinyin_fn, Style

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "唐诗300首最应该背诵的300句.md")
OUT_JSON = os.path.join(HERE, "entries.json")
OUT_JS = os.path.join(HERE, "data.js")
PINYIN_SRC = r"D:\WorkBuddy-CQ\build_book_tang.py"

# ---------- 提取 PINYIN_OVERRIDE（从 build_book_tang.py）----------
py_src = open(PINYIN_SRC, encoding="utf-8").read()
head = py_src.split("def get_pinyin", 1)[0]          # 取 get_pinyin 之前的全部内容
start = head.index("PINYIN_OVERRIDE = {")
tail = head[start:]
end = tail.rindex("}")                                # 取最后一个右大括号（表结束）
block = tail[:end + 1]
ns = {}
exec(block, ns)
PINYIN_OVERRIDE = ns["PINYIN_OVERRIDE"]
print("拼音表条目:", len(PINYIN_OVERRIDE))

# ---------- 解析 md ----------
text = open(SRC, encoding="utf-8").read()
lines = text.split("\n")

state = "lead"
cur_cat = None
cat_lead = []
entries = []   # 顺序保留，保证 id 连续
cat_order = []  # 分类出现顺序

entry_re = re.compile(r"^\*\*\s*【(\d+)】\s*(.+?)——(.+?)\s*\*\*\s*$")
cjk = re.compile(r"[一-鿿]")

for ln in lines:
    if ln.startswith("## "):
        # 标题形如：一、山水田园·一山一水总关情
        raw = ln[3:].strip()
        raw = re.sub(r"^[一二三四五六七八九十]+、", "", raw)     # 去序号
        cat = raw.split("·")[0].strip()                        # 取主题名（去副标题）
        cur_cat = cat
        if cat not in cat_order:
            cat_order.append(cat)
        cat_lead = []
        state = "lead"
        continue
    m = entry_re.match(ln)
    if m:
        term = m.group(2).strip()
        source = m.group(3).strip()
        entries.append({
            "n": int(m.group(1)),
            "term": term,
            "source": source,
            "category": cur_cat,
            "desc": "",
        })
        state = "desc"
        continue
    if state == "lead":
        if ln.strip():
            cat_lead.append(ln.strip())
    elif state == "desc":
        if not ln.strip():
            state = "gap"
        else:
            entries[-1]["desc"] += ln.strip() + " "

# 计算每条释义（strip 多余空格）
for e in entries:
    e["desc"] = e["desc"].strip()

# ---------- 拼音 ----------
def get_pinyin(s):
    if s in PINYIN_OVERRIDE:
        return PINYIN_OVERRIDE[s]
    return ' '.join(p[0] for p in pinyin_fn(s, style=Style.TONE))

# ---------- 组装 entries.json / data.js ----------
coll_id = "ty"
COLLECTIONS = [{"id": coll_id, "name": "唐诗三百首·最该背的300句"}]

missing_py = []
js_entries = []
for e in entries:
    term = e["term"]
    py = get_pinyin(term)
    if term not in PINYIN_OVERRIDE:
        missing_py.append(term)
    js_entries.append({
        "id": e["n"],
        "collection": coll_id,
        "term": term,
        "chars": len(cjk.findall(term)),
        "pinyin": py,
        "source": e["source"],
        "meaning": e["desc"],
        "category": e["category"],
        "easy": False,
    })

# 校验
ids = [e["id"] for e in js_entries]
assert ids == list(range(1, len(js_entries) + 1)), "id 不连续!"
# 交叉校验拼音表覆盖
md_terms = [e["term"] for e in js_entries]
not_covered = [t for t in md_terms if t not in PINYIN_OVERRIDE]
print("总条目:", len(js_entries))
print("id 连续:", ids == list(range(1, 301)))
print("分类数:", len(cat_order), cat_order)
print("拼音表未覆盖(走 pypinyin):", len(not_covered), not_covered[:5])

# 写 entries.json
json.dump(js_entries, open(OUT_JSON, "w", encoding="utf-8"),
          ensure_ascii=False, indent=0)
# 写 data.js
with open(OUT_JS, "w", encoding="utf-8") as f:
    f.write("// 自动生成，勿手改。前端通过 <script src=\"data.js\"> 引入。\n")
    f.write("window.COLLECTIONS = " + json.dumps(COLLECTIONS, ensure_ascii=False) + ";\n")
    f.write("window.ENTRIES = " + json.dumps(js_entries, ensure_ascii=False) + ";\n")

print("已生成:", OUT_JSON, "大小:", os.path.getsize(OUT_JSON) // 1024, "KB")
print("已生成:", OUT_JS, "大小:", os.path.getsize(OUT_JS) // 1024, "KB")
