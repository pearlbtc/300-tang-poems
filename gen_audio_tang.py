# -*- coding: utf-8 -*-
"""读 entries.json，用 edge-tts 并发生成 audio/<id>.mp3（300 条）。
voice=zh-CN-YunyangNeural（央视/新闻主播男声）。
并发 Semaphore(8) 提速；已存在且 >500B 的会跳过（支持断点续传）。
"""
import asyncio, json, os
import edge_tts

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "entries.json"), encoding="utf-8"))
ents = d["entries"] if isinstance(d, dict) else d
OUT = os.path.join(HERE, "audio")
os.makedirs(OUT, exist_ok=True)
VOICE = "zh-CN-YunyangNeural"
SEM = asyncio.Semaphore(8)

async def gen_one(e):
    pid = str(e["id"])
    f = os.path.join(OUT, pid + ".mp3")
    if os.path.exists(f) and os.path.getsize(f) > 500:
        return 0
    async with SEM:
        try:
            tts = edge_tts.Communicate(e["term"], VOICE, rate="+0%")
            await tts.save(f)
            return 1
        except Exception as ex:
            print("ERR", pid, ex, flush=True)
            return 0

async def main():
    tasks = [gen_one(e) for e in ents]
    done = 0
    for coro in asyncio.as_completed(tasks):
        done += await coro
        if done % 20 == 0:
            print("generated", done, "files, ready=", len(os.listdir(OUT)), flush=True)
    print("AUDIO_DONE total_ready=", len(os.listdir(OUT)), flush=True)

asyncio.run(main())
