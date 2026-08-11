# -*- coding: utf-8 -*-
"""生成唐诗 PWA 图标(3张) + 把 images_tang 的水墨图转成 assets/cover.jpg + vol1-8.jpg"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_IMG = r"D:\WorkBuddy-CQ\images_tang"
FONT = r"C:\Windows\Fonts\simkai.ttf"   # 楷体

# ---------- 图标 ----------
def make_icon(size, safe):
    img = Image.new("RGB", (size, size), (122, 82, 44))   # 主题棕 #7a5230
    d = ImageDraw.Draw(img)
    # 内描边
    inset = int(size * 0.04)
    d.rectangle([inset, inset, size - inset, size - inset], outline=(243, 233, 210), width=max(2, int(size * 0.012)))
    fsize = int(size * (0.62 if not safe else 0.5))
    font = ImageFont.truetype(FONT, fsize)
    txt = "唐"
    bbox = d.textbbox((0, 0), txt, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1]
    # 印章红底 + 白字
    d.text((x, y), txt, font=font, fill=(243, 233, 210))
    return img

icon512 = make_icon(512, safe=False)
icon512.save(os.path.join(HERE, "icons", "icon-512.png"))
make_icon(192, safe=False).save(os.path.join(HERE, "icons", "icon-192.png"))
make_icon(512, safe=True).save(os.path.join(HERE, "icons", "icon-maskable-512.png"))
print("图标已生成: icon-192 / icon-512 / icon-maskable-512")

# ---------- 卷首图 ----------
mapping = [
    ("cover.png", "cover.jpg"),
    ("01_shanshui.png", "vol1.jpg"),
    ("02_biansai.png", "vol2.jpg"),
    ("03_songbie.png", "vol3.jpg"),
    ("04_sixiang.png", "vol4.jpg"),
    ("05_huaigu.png", "vol5.jpg"),
    ("06_qingai.png", "vol6.jpg"),
    ("07_zheli.png", "vol7.jpg"),
    ("08_siji.png", "vol8.jpg"),
]
for src, dst in mapping:
    im = Image.open(os.path.join(SRC_IMG, src)).convert("RGB")
    im.save(os.path.join(HERE, "assets", dst), "JPEG", quality=88)
print("卷首图已生成:", len(mapping), "张 -> assets/")
