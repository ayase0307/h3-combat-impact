# 衝擊幀後製（Impact Frame Post-Production）

> 當 H3 在同一段提示詞裡**做不出精準的 2 幀衝擊幀**時——
> 把它拆成兩條素材，再用 ffmpeg 合成。

---

## 0. 為什麼要拆

實測：在一支高速戰鬥片裡寫 `for two frames the frame cuts to a black-and-white
manga panel`，模型給的是 **23 幀（958 ms）**，而且第二次發生時角色直接消失。

| 同一段提示詞 | 結果 |
|---|---|
| 白閃 `for two frames` | ✅ 有效（既有實測） |
| **漫畫格 `for two frames`** | ❌ **失控 12 倍**（23 幀 / 21 幀） |
| 高速動作 + 衝擊幀寫在一起 | ❌ 動作被拖慢、角色消失 |

**根因**：整幀去飽和是一個「風格跳轉」，模型把它當成「切到一個黑白風格的鏡頭」，
不是「插入 2 幀」。在高速動作的上下文裡，它更傾向於佔滿整段。

**解法：分開生成，再合成。**

---

## 1. 三素材工作流

```
素材 A：主片        → 只有高速動作與運鏡，完全不寫衝擊幀
素材 B：衝擊幀片    → 單獨生成，幾秒，只要那一幀爆發
素材 C：放射線 PNG  → 素材 B 抽出來的那一幀
合成：   A + C 疊在指定時間點（2 幀 = 83 ms）
```

### 素材 A｜主片（8 秒）

**禁止**出現：`for two frames`、`manga panel`、`held impact frame`、`near-freeze`。
主片只負責：運鏡、戰鬥、特效、周圍連動。

```text
[Shot 8] At 00:07.100, a hard cut to a close three-quarter view of the blades
meeting: the oversized orange-heated nodachi meets the slender cold-blue katana,
a white-hot core at the exact metal contact, orange sparks and a narrow cold-blue
energy trace, both fighters' faces inches apart and lit by the flare. The camera
punches in with small amplitude at fast speed and shakes strongly.
```

> 注意：這裡寫的是「白色的核心」而不是「2 幀爆白」。
> 主片裡有爆發**內容**（讀者看得到），但沒有「幀數控制的插入格」。

### 素材 B｜衝擊幀片（3–4 秒）

單獨一支，只為了一兩幀。**這裡的幀數控制才會生效**——因為沒有高速動作在搶模型注意力。

```text
integrated_multimodal_description: [Shot 1] 3D CG, cinematic anime donghua, premium
painted CG materials, a moonlit ruined-stone courtyard with broken pillars, torn
red banners, wet reflective flagstones, burning braziers, cold moonlight and warm
firelight. A single frozen instant of extreme violence at the exact moment of
impact: an oversized molten-orange-heated nodachi and a slender cold-blue katana
collide head-on, the metal compressing between them. For two frames the entire
frame blows out to pure white at the exact point of contact, and a solid white
core with clean radial speed lines bursts outward from it in every direction. A
ring of orange sparks tears off the impact in a narrow cone, shattered flagstone
fragments and splashing water fly outward, and the torn red banners behind whip
violently. The two combatants are crushed into hard black silhouettes against the
white flare. The camera punches in with small amplitude at fast speed and shakes
strongly, and the image returns immediately with no glowing residue.
```

### 素材 C｜放射線 PNG

從素材 B 抽出要用的那一幀。

---

## 2. 合成

```bash
# 抽出衝擊幀片的那一幀
ffmpeg -y -i impact.mp4 -vf "select=eq(n\,12)" -fps_mode passthrough -frames:v 1 impact_frame.png

# 疊到主片的指定時間點
python scripts/impact_frame.py composite \
    --main main.mp4 --impact impact.mp4 \
    --at 6.8 --frame 12 --hold 0.083 --out final.mp4
```

`--hold` 決定覆蓋長度：

| hold | 幀數（24fps） | 效果 |
|---|---|---|
| 0.042 | 1 幀 | 太硬，像壞掉 |
| **0.083** | **2 幀（24fps 下 83 ms）** | **推薦**——參考片 30fps 的 2 幀為 67 ms，換算 ≈1.6 幀，取 2 幀；換算公式：24fps 幀數 = round(參考幀數 × 0.8)，最少 1 幀 |
| 0.125 | 3 幀 | 稍長 |
| 0.167 | 4 幀 | 開始像慢動作 |

---

### 2.1 多階段序列（白 → 黑白 → 主色）

一個高潮要 3 階段各 2 幀時，從素材 B 抽 3 幀，同一支主片連續疊 3 次，`--at` 每次加一個 hold：

```bash
IN=main.mp4; F0=163   # 起始幀號（主片 24fps；163/24 ≈ 6.79s）
for i in 0 1 2; do
  python scripts/impact_frame.py composite --main $IN --impact B.mp4     --at $(python -c "print(($F0+2*$i)/24)") --frame $((12+i*3)) --hold 0.083 --out step$i.mp4
  IN=step$i.mp4
done
```

驗收：逐幀 YAVG 序列看得出插入的 6 幀連續即可；整體驗收照 §3。

**實測（2026-10-21）**：主片＝超高速 1280×704 高畫質片，衝擊素材＝H3 生成的 4 秒漫畫放射片，`--at` 取 24fps 的整數幀（93/24、95/24、97/24）、`--hold 0.083`、`--frame 3/9/15`。第 93–98 幀 YAVG＝62.5, 62.8, 115, 115, 117, 127，連續 6 幀無交錯；插入點前 66.5 → 後 81.7（落差 15 階，是剪接點本身的亮度跳動，不是合成錯誤）。第 2、3 段（兩張漫畫放射）亮度差不明顯，不要期待肉眼分得出三個平台。
**注意**：`impact_frame.py` 舊版用 `between(t, start, start+dur)` 以時間開關，浮點邊界會讓 2 幀變 1 幀、多次疊加時與主片交錯；現已改成 `between(n, 首幀, 末幀)` 以幀序號開關，`--at` 請直接給 `幀號/幀率`（腳本會讀主片自己的幀率換算幀號；舊語意取 ceil，新版取 round，同一組參數可能提早 1 幀）。

## 3. 合成後的驗收

**後製會破壞原本的量測數字，所以必須重跑。**

```bash
python scripts/measure_motion.py final.mp4 --symmetry
```

| 檢查 | 門檻 |
|---|---|
| 末 2s ÷ 中段 | ≥ 60% |
| 最長低潮 | ≤ 0.8s |
| 峰值格 | ≥ 4 |
| 衝擊幀處的 YAVG 跳躍 | 應有一個明顯的尖峰 |

**亮度接縫檢查**：合成前後各取衝擊幀前後 3 幀，YAVG 差應該 < 8 階。
差太多表示素材 B 的環境亮度跟素材 A 對不上，合成會像貼一張圖上去。

```bash
# 取合成前後的亮度值比較
ffmpeg -v error -ss 6.6 -i final.mp4 -frames:v 6 -vf "signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -f null -
```

**如果對不上**：改素材 B 的環境描述（光源、材質、色調）去逼近素材 A，
或把 `--hold` 縮短到 1–2 幀（接縫的視覺權重就小了）。

---

## 4. 什麼時候**不要**走後製

| 情況 | 建議 |
|---|---|
| 只是要一個白色爆點 | **直接寫在主片裡**（白閃的幀數控制有效） |
| 漫畫格／放射線插入格 | **走後製**（同段生成會失控 12 倍） |
| 衝擊幀要跟動作完全對齊 | 走後製，但要挑到動作匹配的幀 |
| 一次要很多個衝擊幀 | 走後製，一個素材 B 產多幀，合成多次 |

---

## 5. 完整工作流

```bash
# 1. 產生主片（不含衝擊幀）
python scripts/submit_ab.py --before main_prompt.txt --after main_prompt.txt \
    --label "主片" --width 960 --height 544 --seconds 8 --seed 20261019 \
    --outdir analysis/impact

# 2. 產生衝擊幀片
python scripts/impact_frame.py gen --prompt impact_prompt.txt \
    --out analysis/impact/impact.mp4 --width 960 --height 544 --seconds 4

# 3. 合成
python scripts/impact_frame.py composite \
    --main analysis/impact/before.mp4 --impact analysis/impact/impact.mp4 \
    --at 6.8 --frame 12 --hold 0.083 --out analysis/impact/final.mp4

# 4. 重新量測
python scripts/measure_motion.py analysis/impact/final.mp4 --symmetry
```

---

## 6. 既有規則的例外條款

| 規則 | 在後製路徑下的例外 |
|---|---|
| `impact-frame-and-shake.md` §1.2「衝擊幀要寫在同一個鏡頭裡」 | **後製路徑例外**：素材 A 不寫衝擊幀，素材 B 單獨寫 |
| `impact-frame-and-shake.md` §1.2.1「強事件 vs 弱事件」 | 素材 B 因為是獨立的短片，**弱事件也可以用 2 幀**（沒有高速動作干擾） |
| `impact-frame-and-shake.md` §1.1.1「漫畫格幀數控不住（實跑 23 幀）」 | **後製路徑下用 `--hold` 精確控制**，素材 B 本身多長都不影響最終時長 |
| `SKILL.md`「衝擊幀只給一幀」 | 同上，後製下由 `--hold` 決定 |

**核心觀念：素材 B 失控是無關緊要的，因為最終只會取用 1–2 幀。**
這就是後製路徑的價值——把不可控的東西變成可裁切。
