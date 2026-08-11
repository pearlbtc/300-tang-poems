# 唐诗300首最应该背诵的300句 · 学习小工具

一个纯前端的唐诗名句学习 PWA（Progressive Web App）。参考「壹页格物」店铺的
《600个绝美的诗词成语》学习小工具产品线制作，作为独立仓库维护。

## 功能
- 📚 **唐诗名句库**：300 句按 8 类唐诗主题分卷（山水田园 / 边塞豪情 / 送别赠友 /
  思乡怀人 / 咏史怀古 / 情爱相思 / 人生哲理 / 四季时令），支持搜索与分类筛选。
- 📖 **每日一练**：分组学习，逐句过，可一键央视男声（edge-tts）朗读。
- ⭐ **收藏 / 自测**：收藏夹回顾、自测闯关、战绩统计，进度存 localStorage。
- 📱 **可安装**：支持添加到手机主屏，离线可用（Service Worker 缓存）。

## 数据
- `data.js` / `entries.json`：由 `唐诗300首最应该背诵的300句.md` 经
  `build_data_tang.py` 生成（拼音 300 句全部人工核对，多音字纠错表见
  `build_book_tang.py` 的 `PINYIN_OVERRIDE`）。
- `audio/*.mp3`：由 `gen_audio_tang.py`（edge-tts，zh-CN-YunyangNeural）生成。

## 本地运行
任意静态服务器即可，例如：
```bash
python -m http.server 8080
# 浏览器打开 http://localhost:8080/
```
> 注意：因 Service Worker 与音频加载，`file://` 直接双击打开可能受限，请用 http 方式访问。

## 重新生成
```bash
# 数据
python build_data_tang.py
# 音频（首次约 8-12 分钟，支持断点续传）
python gen_audio_tang.py
```

## 部署到 GitHub Pages
1. 推送到仓库 `pearlbtc/300-tang-poems`（main 分支根目录即站点）。
2. 仓库 Settings → Pages → Source 选择 **main** 分支 / **(root)** → Save。
3. 因含 `.nojekyll`，Pages 不会用 Jekyll 处理，站点即为本目录静态文件。

## 目录结构
```
index.html  app.js  styles.css  sw.js  manifest.webmanifest
data.js  entries.json  build_data_tang.py  gen_audio_tang.py
audio/  (300 个 <id>.mp3)
assets/ (cover.jpg + vol1-8.jpg 卷首图)
icons/  (icon-192 / icon-512 / icon-maskable-512)
唐诗300首最应该背诵的300句.md  (内容源)
```
