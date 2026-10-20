# 兩段接續（FL2VA Chain）

> 把一支超過 15 秒的打鬥拆成兩段生成，用末幀接續。
> **接續最容易壞的兩件事：接縫處速率掉下來、以及第二段的角色偷偷變了。**

---

## 0. 什麼時候要接續

| 總長 | 怎麼做 |
|---|---|
| ≤ 15 秒 | 單段。不要為了好玩切段。 |
| 16–30 秒 | **兩段**，各 15 秒，第 2 段用 FL2VA 接第 1 段末幀 |
| > 30 秒 | 依此類推，但**每多一段，身份漂移風險累加** |

**優先順序：先問能不能用 15 秒講完。** 15 秒 = 18–22 鏡，已經夠放完一整段交手。

---

## 1. 時長換算（最容易錯的一步）

FreeVideo 的 `frames` 量子是 **17n+5**，而且**送小數秒會向上取整**：

| 你想要的秒數 | ❌ 送 `seconds=15.0` 可能拿到 | ✅ 正確做法 |
|---|---|---|
| 15.000 秒 | 15.000 沒問題（剛好整除） | `frames = 360`（`seconds = 15.0`） |
| 11.542 秒 | 被推到 294 幀 = 12.25 秒 | 送 `277/24` |

**驗收**：送件後讀 `spec.frames`，必須等於預期值。
本輪實測：送 `seconds=15` → `frames=362`（不是 360），所以**一定要讀回來確認**。

> `362 / 24 = 15.083 秒`。多出來的 2 幀是安全邊際，剪輯時切掉。

---

## 2. 接續的三層

接續不是只有「把末幀餵進去」。有三層要同時成立：

### 第 1 層｜畫面接得上（末幀 → 首幀）

```bash
# 抽末幀（-sseof 比 -frames:v 1 可靠）
ffmpeg -y -sseof -0.5 -i segA.mp4 -update 1 -q:v 2 segA_last.png
```

**抽完一定要看那張圖。** 如果最後一幀是「兩人站定」或「糊成一團」，第二段會從一個爛起點出發。

### 第 2 層｜速率接得上（最重要）

**H3 在片段最後 1–2 秒會自動減速。** 所以第 1 段的尾巴本來就是慢的，
第 2 段如果直接從那裡起步，會被拖慢。

三個對策，**前兩個一定要做**：

| 對策 | 做法 |
|---|---|
| **① 第 1 段結尾寫成「動作中」而非「完成」** | 別寫 `settles into a low guard`；寫 `The lock breaks and she drives through, the blade clipping past and the camera still moving as the frame ends.` |
| **② 第 2 段首鏡立刻打破** | 首鏡前 0.5 秒內就要有動作：`The lock breaks within the first half-second: ... shoves through and drives ... back two steps.` |
| ③ 生成多要 0.5 秒再切 | 第 1 段切在動作轉折點，不切在末尾 |

**驗收**：兩段的 `末2s ÷ 中段` 與 `開場 0.8s ÷ 中段` 都要 ≥60%。
接縫在 15 秒處，所以要另外量「接縫附近」的運動（見 §5）。

### 第 3 層｜身份接得上（角色不能偷變）

FL2VA 沒有 `subject_definitions`，所以**第 2 段的身份全靠第 1 段末幀**。
但 15 秒的生成累積漂移已經不小，光靠末幀不夠。

**對策：在第 2 段的 `[Shot 1]` 用文字重述兩個角色的識別特徵。**

```text
[Shot 1] ... The shot begins inside the exact blade lock, framing, lighting and
profile composition established by <Picture 1>: Tieya, the tall northern warrior,
on frame left with her short black wolf-cut hair, three iron hoop earrings, the
scar under her right eye, her asymmetrical black iron armor and rust-red rope
sash, pressing her molten-orange-heated nodachi down; Bailu, the smaller
swordswoman, on frame right with her long black high ponytail, dark-gold hairpin,
ivory-white kimono and navy hakama, braced under the same lock with her
cold-blue katana ...
```

**這一段是「文字版的 identity lock」**——FL2VA 沒有六欄位，就用 `[Shot 1]` 的第一句補。

---

## 3. 第 2 段的首行對齊句（逐字）

```text
How the reference pictures align with the target video — <Picture 1> (from [Shot 1]) aligns with the 0.00-second mark of the target video.
```

第 2 段是**單一張圖**（只有首幀），所以**不要寫成 FL2VA 的兩張圖形式**。
寫成單圖形式，模型會把它當作 I2VA 式的起點延續。

首行之後**空一行**再接 `integrated_multimodal_description`。

---

## 4. 兩段的分工

| | 第 1 段 | 第 2 段 |
|---|---|---|
| 敘事 | 建立交手 → 第一次大碰撞 | 追擊 → 高潮 → 收 |
| 節奏 | 一路加速 | **開場就是最快**，中段稍喘，末尾拉回 |
| 鏡數 | 18–22 鏡（15 秒） | 18–22 鏡 |
| 結尾 | **動作中斷**（刀鎖住、人在空中） | **動作完成**（勝負分曉或定格） |
| 片頭 | 0.5 秒內接觸 | **0.5 秒內打破前一鏡的靜止** |

**第 2 段不是「第 1 段再來一次」。** 它要開得比第 1 段結尾快，
然後走向結局。

---

## 5. 接縫驗收

合成後要量的不是全片平均，而是**接縫前後各 2 秒**：

```bash
python scripts/measure_motion.py segA.mp4 segB.mp4 full_30s.mp4 --fps24
```

| 檢查 | 門檻 | 不合格的意義 |
|---|---|---|
| 第 1 段 `末2s ÷ 中段` | ≥60% | 第 1 段自己就爛尾了 |
| 第 2 段 `開場 0.8s ÷ 中段` | ≥60% | 第 2 段起步太慢 → 接縫掉速 |
| **接縫處逐幀差** | 接縫那一幀的差 **不低於前後 8 幀的中位數** | 接縫是一個「死格」 |
| 全片最長低潮 | ≤0.8s | 有頓點 |

### 量接縫的那一幀

```bash
# 把 30 秒片的逐幀差異印出來，看第 360–366 幀附近
ffmpeg -v error -i full_30s.mp4 -vf "tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-" -f null - | head -400 | tail -20
```

**接縫格的 YAVG 差應該跟鄰居差不多。** 如果它明顯偏低，代表兩段在那一格「對不上」
（姿態跳、鏡頭跳、光線跳），觀眾會看到一個頓點。

---

## 5.5 實測：接縫可以完美，但結尾會爛（2026-10-20）

兩段 15 秒（362 幀 ×2 = 724 幀 = 30.2 秒）的實測數據：

| | 全程運動 | 開場 | 末 2s ÷ 中段 | 旗標 |
|---|---:|---:|---:|---|
| 段 A | 24.69 | 25.66 | **87%** | 無 |
| 段 B | 22.17 | 34.57 | **50%** | **尾端停滯** |
| 合計 30.2s | 23.40 | 24.54 | 48% | 尾端停滯 |

**接縫本身是完美的**：接縫格 YAVG 差 14.54、前後 8 格中位數 16.86、比值 **86%**，
而且逐格看 360→368 那八格，刀鎖的構圖完全連續，看不出接點。

**但段 B 自己爛尾了（50%）。** 原因很明確：

> 段 B 的最後一鏡我寫了
> `Both fighters hold the lock as the frame ends, their faces turned toward each other.`
> ——**「hold the lock as the frame ends」就是在要求一個靜止結尾。**

這是自找的。`SKILL.md` 的收尾定格規則早就講過 H3 會自動減速，
結果我還在最後一鏡寫「維持不動」。

### 正確寫法

| ❌ 錯 | ✅ 對 |
|---|---|
| `Both fighters hold the lock as the frame ends.` | `The lock breaks and she drives through, the blade clipping past and the camera still moving as the frame ends.` |
| `settling into the final pose` | `still mid-step as the frame ends` |
| `they stand facing each other` | `she is already stepping in as the frame ends` |

**要「停在一個動作的過程中」，不是「停在一個姿勢上」。**

### 另一個發現：第 2 段開場反而最強（34.57）

段 B 的開場運動量 34.57 遠高於段 A 的 25.66。
**證明「第 2 段首鏡 0.5 秒內打破」這條規則有效**——
接續段的起步不但沒有掉速，還比第 1 段更快。

**所以問題只在結尾，不在接縫。**

### 5.6 15 秒單段的結尾（2026-10-21，E1 實測：結論是看末鏡寫法，不是 15 秒本身）

另兩支 15 秒 Ref2VA（同參考圖、同 seed 20261019、7 個事件，唯一變因＝提示詞格式），末鏡都寫成
`both fighters are still mid-motion as the frame ends`：

| 版本 | 全程 | 開場 | 末 2s ÷ 中段 | 旗標 |
|---|---:|---:|---:|---|
| A 作者格式（中文、`[Shot1] At 00:00.00, 0–2.0s｜…`） | 18.11 | 9.70 | **108%** | 無 |
| B skill 格式（英文、`[Shot 1]` 無時間碼） | 19.62 | 14.18 | **113%** | 無 |

兩支都沒有爛尾，目視最後一鏡仍是兩人對撞、光爆。**所以 §5.5 的爛尾很可能來自「hold the lock」這句，而不是 15 秒長度。**
單 seed、單組圖，樣本小；結論只用來降級「15 秒必爛」的印象，不當作保證。


### 修正後的檢查

- [ ] 最後一鏡**不要**出現 `hold` / `settling` / `stand` / `facing each other`
- [ ] 最後一鏡要有位移或姿態變化（`drives through` / `still mid-step`）
- [ ] 生成多要 0.5–1 秒，剪輯切掉尾巴
## 6. 常見失敗

| 症狀 | 根因 | 修法 |
|---|---|---|
| 接縫處明顯頓一下 | 第 1 段結尾是「站定」，第 2 段從靜止起步 | 第 1 段結尾寫動作中；第 2 段首鏡 0.5 秒內打破 |
| 第 2 段角色變了 | FL2VA 只靠末幀，15 秒漂移已累積 | 第 2 段 `[Shot 1]` 用文字重述身份特徵 |
| 第 2 段的刀變短了 | 沒寫武器相對長度 | 在 `[Shot 1]` 寫 `her oversized nodachi`、`her slender katana` |
| 第 2 段畫風變了 | 沒寫材質錨 | 第 2 段 `[Shot 1]` 首句照抄第 1 段的畫風句 |
| 第 2 段變成慢節奏 | 第 1 段結尾太慢，模型沿用了那個節奏 | 見 §2 第 2 層 |
| 總長少於 30 秒 | `seconds` 被捨去 | 讀回 `spec.frames` 確認 |
| 兩段接起來有色差 | 光線描述不同 | 兩段用同一組光源描述（同一句照抄） |

---

## 7. 完整流程

```bash
# 1. 送第 1 段（Ref2VA，15 秒）
python scripts/submit_ref2va.py --prompt segA.txt \
    --image char1.png --image char2.png --image scene.png \
    --label "A · 第1段 15s" --seconds 15 --seed 20261019 --outdir analysis/chain

# 2. 抽末幀（先看一眼那張圖）
ffmpeg -y -sseof -0.5 -i analysis/chain/after.mp4 -update 1 -q:v 2 analysis/chain/segA_last.png

# 3. 送第 2 段（FL2VA，首幀 = 第 1 段末幀，15 秒）
python scripts/submit_ref2va.py --prompt segB.txt \
    --first analysis/chain/segA_last.png \
    --label "B · 第2段 15s 續接" --seconds 15 --seed 20261019 --outdir analysis/chain

# 4. 接成 30 秒
printf "file '%s'\nfile '%s'\n" "$PWD/analysis/chain/segA.mp4" "$PWD/analysis/chain/segB.mp4" > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy analysis/chain/full_30s.mp4

# 5. 量測（含接縫）
python scripts/measure_motion.py analysis/chain/segA.mp4 analysis/chain/segB.mp4 analysis/chain/full_30s.mp4 --fps24
```
