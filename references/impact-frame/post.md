# P3｜衝擊幀分開生成，再合成到主片

> 什麼時候讀：選了 P3——漫畫格／放射線格、要對齊到某一格、ULTRA_SPEED（主片禁寫衝擊幀）、一段裡要多次衝擊、或 P2 生成失敗要補救。
> 核心觀念：**把不可控的東西變成可裁切。** 衝擊片生成 4 秒、裡面亂成什麼樣都無所謂，最後只取 1–13 幀。

---

## 0. 為什麼要拆

| 同一段提示詞裡 | H3 實測 |
|---|---|
| 白閃 `for two frames` | 會亮，但亮 **11–45 幀**（EP03 d10–d15）；只能保證「有亮」 |
| 漫畫格 `for two frames` | **21–23 幀**，第二次角色消失 |
| 高速動作＋衝擊幀寫在一起 | 動作被拖慢、角色消失 |

整幀去飽和是「風格跳轉」，模型把它當成「切到一個黑白風格的鏡頭」，不是「插入 2 幀」。

---

## 1. 三素材工作流

```
素材 A：主片        → 只有動作、運鏡、特效、周圍連動；完全不寫衝擊幀
素材 B：衝擊片      → 單獨生成 3–4 秒，只寫衝擊那一刻（構圖要對得上主片）
合成：   從 B 挑幀（可自動挑亮度峰／飽和度谷），疊到 A 的指定幀，hold 1–13 幀
```

### 素材 A｜主片

**禁止**：`for two frames`、`manga panel`、`held impact frame`、`near-freeze`。主片裡可以有爆發**內容**（白熱核心、火花），但沒有「幀數控制的插入格」。

```text
[Shot 8] At 00:07.100, a hard cut to a close three-quarter view of the blades meeting: the oversized orange-heated nodachi meets the slender cold-blue katana, a white-hot core at the exact metal contact, orange sparks and a narrow cold-blue energy trace, both fighters' faces inches apart and lit by the flare. The camera punches in with small amplitude at fast speed and jolts hard for a few frames, settling almost immediately.
```

### 素材 B｜衝擊片（3–4 秒）

沒有高速動作搶注意力，衝擊的**形態**比較守得住（幀數仍然不守，沒關係）。環境光、材質、色調要逼近主片，否則合成會像貼圖。

```text
integrated_multimodal_description: [Shot 1] 3D CG, cinematic anime donghua, premium painted CG materials, a moonlit ruined-stone courtyard with broken pillars, torn red banners, wet reflective flagstones, burning braziers, cold moonlight and warm firelight. A single frozen instant of extreme violence at the exact moment of impact: an oversized molten-orange-heated nodachi and a slender cold-blue katana collide head-on, the metal compressing between them. The entire frame blows out to pure white at the exact point of contact, and a solid white core with clean radial speed lines bursts outward from it in every direction. A ring of orange sparks tears off the impact in a narrow cone, shattered flagstone fragments and splashing water fly outward, and the torn red banners behind whip violently. The two combatants are crushed into hard black silhouettes against the white flare. The camera punches in with small amplitude at fast speed, and the image snaps straight back to the clean colour frame.
overall_soundscape: A single sharp metallic crack and a deep bass boom.
non_diegetic_music: N/A
```

驗證衝擊片本身要加 `--impact-clip`（豁免漫畫格與表情規則）：`python scripts/validate_prompt.py impact.txt --duration 4 --impact-clip`。

---

## 2. 合成

```bash
# 先看衝擊片裡哪幾格最像衝擊（亮度峰／飽和度谷）
python scripts/impact_frame.py find-peak --in impact.mp4 --top 5

# 單點：主片第 163 幀起，疊衝擊片第 12 幀，停 2 幀
python scripts/impact_frame.py composite --main main.mp4 --impact impact.mp4 \
    --insert 163:12:2 --out final.mp4

# 讓腳本自己挑衝擊片裡最亮／最去飽和的那一格
python scripts/impact_frame.py composite --main main.mp4 --impact impact.mp4 \
    --insert 163:auto:2 --out final.mp4
```

- 衝擊片解析度與主片不同時，**自動縮放＋置中裁切**到主片大小。
- **主片音軌原樣保留**（H3 是有聲生成，衝擊音都在主片裡）。
- 舊語法 `--at 秒 --frame N --hold 秒` 仍可用；`--at-frame` 直接收幀號。

`hold` 對照（成品 24fps）：

| hold | 用途 |
|---|---|
| 1 幀 | 最銳利；黑白交替鏈裡每張 1 幀 |
| **2 幀** | 白閃、翻色、單張漫畫格的預設 |
| 3 幀 | 黑尾、黑底能量剪影（F11） |
| 9–12 幀 | 放射定格板（F 長度級「放射定格板」） |

### 2.1 多階段序列（一次濾鏡完成，不反覆重編碼）

斬擊光影實測的 13 幀序列（白放射 2 → 黑白放射 2 → 主色放射 2 → 黑白剪影 2 → 反相 1 → 白 1 → **黑 3**），從衝擊片挑對應的幀，連續疊：

```bash
python scripts/impact_frame.py composite --main main.mp4 --impact B.mp4 \
    --insert 163:3:2 --insert 165:9:2 --insert 167:15:2 --insert 169:21:2 \
    --insert 171:auto:1 --black 172:3 --out final.mp4
```

`--black 幀號:長度` 直接插純黑幀（多階段序列的黑尾）。

**舊實測（2026-10-21）**：主片＝超高速 1280×704，衝擊素材＝H3 生成的 4 秒漫畫放射片，三段各 2 幀連續疊，第 93–98 幀 YAVG＝62.5, 62.8, 115, 115, 117, 127，6 幀連續無交錯。兩張漫畫放射亮度差不明顯，不要期待肉眼分得出三個平台——**換配色**（白／黑白／主色）才分得出來。

---

## 3. 合成後的驗收（兩段式門檻，取代舊的自相矛盾版本）

舊版同時要求「衝擊幀處 YAVG 要有明顯尖峰」與「衝擊幀前後 YAVG 差 <8 階」——兩者不可能同時成立。36 號實驗用「量測幾乎不變」當成功證據，目視才發現插進去的是一張全彩月夜遠景（Y83，與前後同亮度），**衝擊幀根本沒被看見**。

| 檢查 | 門檻 | 怎麼量 |
|---|---|---|
| ① 插入幀本身**看得見** | 插入幀與鄰幀 YAVG 差 **≥40 階**，或 SATAVG 降到 **<15**（黑白格），或換成平塗異色（翻色） | `composite` 結束時自動印出插入區與前後 3 幀的 Y／S |
| ② 插入區**以外**接得順 | 插入區前 3 幀 vs 後 3 幀 YAVG 差 **<8 階**（主片自身的亮度跳動不算合成錯誤） | 同上 |
| ③ 音軌還在 | 輸出有 audio stream | `ffprobe -show_streams final.mp4` |
| ④ 整體節奏 | 末 2s÷中段 ≥60%、最長低潮 ≤0.8 s（要接下一段時才硬性要求） | `measure_motion.py final.mp4` |

①不過：換一格（`find-peak` 的下一個候選），或衝擊片重寫成更極端的亮度／去飽和。②不過：改衝擊片的環境描述逼近主片，或把 hold 縮短。

---

## 4. 什麼時候不要走 P3

| 情況 | 改走 |
|---|---|
| 只要一個白色爆點、不在乎精確幀數 | P1（同段亮度事件），組裝時裁短 |
| 大招、毀天滅地、要 3–5 張遞進衝擊幀 | P2（`burst-strip.md`）——一次生成、組裝變速，比挑幀省事 |
| L1–L2、3D CG 寫實質感 | P0（局部星芒＋背景徑向拖影） |

---

## 5. ULTRA_SPEED 與 FL2VA 接續：後製是必經步驟

37／38 號成品走 ULTRA_SPEED、主片不寫衝擊幀，但流程裡沒有後製這一步 → 成品 **0 去飽和、0 黑幀、0 翻色**，Y 只到 32–182（參考片 0–253）。規則鏈斷了，成品就沒有衝擊幀。

**所以**：選了 ULTRA_SPEED 或接續鏈，衝擊幀計畫表裡每一個 P3 衝擊點都要有一行 `composite` 指令；`submit_chain.py` 跑完 concat 後，**再跑 composite**，最後才量測。

---

## 6. 完整工作流

```bash
# 1. 主片（不含衝擊幀）與衝擊片各自生成（本機 FreeVideo；Hark 雲端不能跑 gen）
python scripts/impact_frame.py gen --prompt impact_prompt.txt --out impact.mp4 \
    --width 960 --height 544 --seconds 4 --api http://127.0.0.1:8189/freevideo/agent/v1 --token-file /path/to/token
# 2. 挑幀
python scripts/impact_frame.py find-peak --in impact.mp4
# 3. 合成（印出驗收數值）
python scripts/impact_frame.py composite --main main.mp4 --impact impact.mp4 --insert 163:auto:2 --out final.mp4
# 4. 重新量測
python scripts/measure_motion.py final.mp4 --symmetry
```

---

## 7. 待做

- [ ] `--bloom N`：把衝擊幀的光暈延伸到前後 N 幀（補「同鏡內亮度擺幅」，36 §八 3），尚未實作。
- [ ] `submit_chain.py --impact-at`：接續鏈自動接 composite，尚未實作（目前手動跑 §6）。
