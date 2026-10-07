#!/usr/bin/env python3
"""課本雙頁截圖 -> 講義用裁切圖 (Pillow)

用法:
    python scripts/crop_tex_figs.py --src 115contant/04ultrosoundpic --jobs jobs.json
    若不給 --jobs,則使用內建 CH4 超音波預設 (9 張).

jobs.json 格式:
    [
      {"src": "截圖 2026-10-02 上午8.53.14.png",
       "out": "04ultrosound_2.png",
       "box": [0.045, 0.135, 0.478, 0.815],
       "max_w": 1400},
      {"src": "a.png", "out": "b.png", "stack": [
         {"src": "a.png", "box": [...]},
         {"src": "a.png", "box": [...]} ] }
    ]
box = 相對座標 [x0,y0,x1,y1], 0~1, 左上原點.
stack = 同一來源多塊上下拼接 (如程式碼跨頁接續).
"""
import argparse, json, os
from PIL import Image

def crop_rel(im, box):
    w, h = im.size
    x0, y0, x1, y1 = box
    return im.crop((int(w*x0), int(h*y0), int(w*x1), int(h*y1)))

def fit_w(im, W):
    if im.width == W:
        return im
    return im.resize((W, int(im.height*W/im.width)), Image.LANCZOS)

def save(im, path, max_w=1400):
    if im.width > max_w:
        im = im.resize((max_w, int(im.height*max_w/im.width)), Image.LANCZOS)
    im.save(path, "PNG")
    print(f"saved {path} {im.size}")

DEFAULT_JOBS = [
    # 1: 單張模組照,直接複製
    {"src": "截圖 2026-10-02 上午8.21.14.png", "out": "04ultrosound_1.png",
     "box": [0, 0, 1, 1], "max_w": 1000},
    # 2: p62-63左頁 接線圖+對照表
    {"src": "截圖 2026-10-02 上午8.53.14.png", "out": "04ultrosound_2.png",
     "box": [0.045, 0.135, 0.478, 0.815]},
    # 3: p62-63右頁 程式01-16
    {"src": "截圖 2026-10-02 上午8.53.14.png", "out": "04ultrosound_3.png",
     "box": [0.535, 0.555, 0.985, 0.975]},
    # 4: p64-65左頁 code17-19+公式+序列監控
    {"src": "截圖 2026-10-02 上午8.53.22.png", "out": "04ultrosound_4.png",
     "box": [0.045, 0.075, 0.480, 0.625]},
    # 5: p64-65右頁 無源蜂鳴器外觀
    {"src": "截圖 2026-10-02 上午8.53.22.png", "out": "04ultrosound_5.png",
     "box": [0.595, 0.200, 0.960, 0.375], "max_w": 900},
    # 6: p64-65右頁 ESP32Servo安裝
    {"src": "截圖 2026-10-02 上午8.53.22.png", "out": "04ultrosound_6.png",
     "box": [0.545, 0.505, 0.985, 0.880]},
    # 7: p66-67左頁 頻率音階表+蜂鳴器接線
    {"src": "截圖 2026-10-02 上午8.53.52.png", "out": "04ultrosound_7.png",
     "box": [0.040, 0.320, 0.480, 0.975]},
    # 8: p66-67右頁 小蜜蜂程式
    {"src": "截圖 2026-10-02 上午8.53.52.png", "out": "04ultrosound_8.png",
     "box": [0.540, 0.140, 0.985, 0.700]},
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="截圖資料夾")
    ap.add_argument("--jobs", default=None, help="自訂 jobs.json")
    args = ap.parse_args()
    jobs = json.load(open(args.jobs)) if args.jobs else DEFAULT_JOBS
    # 9: p68-69 倒車雷達 01-30 + 31-33 上下拼接 (寫死,最常出錯處)
    src9 = os.path.join(args.src, "截圖 2026-10-02 上午8.54.00.png")
    if os.path.exists(src9) and args.jobs is None:
        base = Image.open(src9).convert("RGB")
        a = crop_rel(base, [0.040, 0.285, 0.480, 0.960])
        b = crop_rel(base, [0.545, 0.070, 0.985, 0.155])
        W = max(a.width, b.width)
        a, b = fit_w(a, W), fit_w(b, W)
        combo = Image.new("RGB", (W, a.height + b.height + 10), "white")
        combo.paste(a, (0, 0)); combo.paste(b, (0, a.height + 10))
        save(combo, os.path.join(args.src, "04ultrosound_9.png"))
    for j in jobs:
        im = Image.open(os.path.join(args.src, j["src"])).convert("RGB")
        out = crop_rel(im, j["box"])
        save(out, os.path.join(args.src, j["out"]), j.get("max_w", 1400))

if __name__ == "__main__":
    main()
