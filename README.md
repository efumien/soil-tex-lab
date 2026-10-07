# soil-tex-lab

課本截圖 → TeX 實驗講義 + 自動裁圖技能（高中資訊科技，SOIL 導向）。

適用於 [opencode](https://opencode.ai) 的 skill（`SKILL.md`），也可當作流程文件直接照著做。

![流程圖](./assets/flow.png)

## 用法（opencode）

```sh
# 全域安裝
mkdir -p ~/.config/opencode/skills/soil-tex-lab
cp -r SKILL.md scripts references assets ~/.config/opencode/skills/soil-tex-lab/
# 然後重開 opencode
```

之後直接說：

> 把 04 超音波課本截圖轉成 tex 講義，對齊 01-03 格式，高中學生、要 SOIL

就會自動產出：講義 `.txt` + 裁切圖 `*_1..9.png` + SOIL 檢核。

## 輸入 / 產出

| 項目 | 說明 |
| --- | --- |
| 輸入 | 章節主題、截圖資料夾（`截圖*.png`）、參考格式 `01~03.txt` |
| 產出 | `<章節>.txt`（`\input` 片段）、`<前綴>_1..N.png`（寬≤1400） |

## Python 套件

| 套件 | 功能 |
| --- | --- |
| `Pillow` | `open/crop/resize/paste/save`：相對座標裁切 + 跨頁拼接 + 流程圖繪製 |
| `argparse/json/os` | 標準庫，處理 `--src/--jobs` 參數 |

```sh
pip install pillow
python scripts/crop_tex_figs.py --src 115contant/04ultrosoundpic
```

詳細流程、SOIL 模板、檢查清單見 [`SKILL.md`](./SKILL.md)。

## License

MIT
