# 輸出契約：讓產出的提示詞可以直接貼進 H3

本檔把官方 `base-en.txt` / `ref-en.txt` 的格式規則整理成可執行的交付標準。
**產出的提示詞必須通過 `scripts/validate_prompt.py`，才算完成。**

---

## 1. 交付形態

最終輸出**只有一個 code block**，區塊內只有提示詞本體。

````text
```text
integrated_multimodal_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: ...
```
````

**區塊內禁止出現**：標題、項目符號（`-` `*`）、粗體（`**`）、編號清單、中文註解、`#` 標記、表情符號、分隔線。
中文說明一律寫在 code block **外面**。

打鬥片段的交付物是**三件**：提示詞 code block ＋ 衝擊幀計畫表 ＋ 組裝指令（後兩件寫在 block 外）。

### 1.1 衝擊幀計畫表（有衝擊點就必附）

| # | 時間碼（生成片） | 打擊點 | 力度 | 路徑 | 組裝 |
|---|---|---|---|---|---|
| 1 | 01.00–02.00 | 蛇身中段 | L4 | P2（4 張） | 5× |
| 2 | 02.00–03.70 | — | — | 主特效 | 1.5× |
| 3 | 06.80 | 刀刃交擊 | L3 | P3 | `--insert 163:auto:2` |

- **時間碼**寫生成片（未變速）的秒數；P2 寫區間，P3 寫插入點。
- **路徑**：P0 不用全幀／P1 同段亮度事件／P2 衝擊幀串＋變速／P3 分開生成＋合成（`SKILL.md` §3）。
- 無衝擊點時寫一行：「本段無衝擊幀（理由：…）」。
- 這張表就是教學片的「出 N 秒，成片用 a–b 秒（X 倍速）」剪輯計畫；漫劇專案把它填進 segments 的 `impact_plan`。
- `validate_prompt.py` 看到 block 外有「衝擊幀計畫」字樣（或 `--impact-plan`），才不會對「有大招卻沒衝擊幀」報 WARN——P3 的主片本來就不寫衝擊幀。

### 1.2 組裝指令

```bash
# 生成後先校正：衝擊幀實際落在哪幾格（模型常提早或延後 0.3–0.6 s）
python scripts/impact_frame.py find-peak --in S04a.mp4
# P2：衝擊幀段 5×、主特效 1.5×（保留音軌）
python scripts/impact_frame.py ramp --in S04a.mp4 --seg 1.00-2.00:5 --seg 2.00-3.70:1.5 --out S04a.ramped.mp4
# P3：衝擊片自動挑最亮／最去飽和的格，疊到主片第 163 幀、停 2 幀
python scripts/impact_frame.py composite --main main.mp4 --impact impact.mp4 --insert 163:auto:2 --out final.mp4
```

---

## 2. 兩種模式，兩種欄位

### 基礎模式（T2VA / I2VA / FL2VA / L2VA）：三個欄位

```text
integrated_multimodal_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: ...
```

### 全參考模式（Ref2VA）：六個欄位

```text
subject_definitions: ...
summary: ...
retention_analysis: ...
detailed_description: ...
overall_soundscape: ...
non_diegetic_music: ...
```

**欄位名稱必須逐字一致**，不可翻譯、不可改寫、不可省略冒號。

---

## 3. 首行對齊句（關鍵幀模式必填）

| 模式 | 首行（逐字） |
|---|---|
| T2VA | 無 |
| I2VA | `For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.` |
| FL2VA | `How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.` |
| L2VA | `How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.` |

首行之後**空一行**再接欄位。

---

## 4. 排版細節（最常寫錯的地方）

| 規則 | 正確 | 錯誤 |
|---|---|---|
| 欄位名後直接接內容 | `integrated_multimodal_description: [Shot 1] Cinematic...` | 欄位名換行後才寫 `[Shot 1]` |
| 欄位之間空一行 | 欄位間有一個空行 | 全部黏在一起 |
| `[Shot 1]` 不加時間碼 | `[Shot 1] Cinematic, a wide shot...` | `[Shot 1] At 00:00.000, ...` |
| 後續鏡頭加遞增時間碼 | `[Shot 2] At 00:01.400, the camera cuts to...` | `[Shot 2] Then we see...` |
| 時間碼格式 | `At 00:03.500`（分:秒.毫秒） | `At 3.5s`、`At 00:3.5` |
| 切鏡動詞 | `the camera cuts to` / `the shot cuts to` / `transitions to` / `changes to` / `switches to` | `next shot`、`cut`、`→` |

---

## 5. 內容規則

| 項目 | 規則 |
|---|---|
| 語言 | 正文一律英文；對白、歌詞、畫面可見文字保留原文 |
| 風格錨定 | `[Shot 1]` 開頭必須有（`Cinematic`、`live-action`、`3D CG`、`2D-animated` 等） |
| 運鏡 | 動作類型 + 幅度 + 速度，寫成自然語句，不可堆標籤 |
| 主體／鏡頭 | 主體動作與鏡頭運動分開寫，避免同向疊加 |
| 對白 | `<d>[Chinese] 台詞</d>`；台詞逐字保留，不翻譯、不改標點 |
| 畫外音 | `says in an off-screen voiceover`，並緊接一句「嘴唇保持閉合」 |
| 跨切點台詞 | `<scenetrans>`；被截斷用 `<cutoff>` |
| 畫面文字 | 用英文雙引號包住原文：`A sign reading "营业中" glows above the door.` |
| 聲景 | 1–4 句連續段落，寫環境音＋物理音＋非語言人聲，不重複對白 |
| 配樂 | 1–3 句，只寫樂器／速度／節奏／動態；不要抽象情緒詞；無配樂寫 `N/A` |
| 時長 | 時間碼全部落在實際時長內；最後一鏡不超過總長 30% |
| 負面約束 | **不使用** `no` / `not` / `never` / `without` / `instead of` / `rather than`，改寫成正面動作 |

### 負面約束的改寫法

| 不要寫 | 改寫成 |
|---|---|
| `no static ending` | `She advances two steps as the storm closes behind her.` |
| `does not look at him` | `Her eyes stay fixed on his mask.` |
| `instead of standing still` | `She drives off her rear leg into the swing.` |
| `without slowing` | `Her speed keeps climbing through the final frame.` |

---

## 6. Ref2VA 專屬規則

| 項目 | 規則 |
|---|---|
| 標籤 | `<Subject N>`（可重用內容）、`<Picture N>`（畫面錨點）、`<Video N>`（整段影片）、`<Audio N>`（音訊） |
| 一致性 | 標籤一旦定義，後續所有段落必須沿用同一編號與含義 |
| 只定義角色時 | 不要另開 `<Picture N>` 條目，改在 `<Subject N>` 內註明來源圖 |
| 保留等級 | 只有三種：`fully_preserved` / `partially_copy` / `reference` |
| `summary` 前綴 | 方括號標註任務類型，如 `[reference generation]`、`[video editing + audio reuse]` |
| 上限 | 圖 ≤9、影片 ≤3（每段 2–15 秒、總計 ≤15 秒）、音訊 ≤3，合計 ≤12 檔 |

---

## 7. 交付前自檢

```bash
python scripts/validate_prompt.py prompt.txt --duration 8
```

檢查項目：

- 欄位齊全且順序正確
- 關鍵幀模式的首行對齊句存在
- `[Shot 1]` 沒有時間碼
- 時間碼嚴格遞增且在時長內
- 最後一鏡長度 ≤ 總長 30%
- 無負面約束詞
- 無 Markdown 殘留
- 對白 `<d>...</d>` 成對
- 引用標籤皆有定義
- 字數在預算內（4–8 秒 ≤520、9–15 秒 ≤700；Ref2VA 再 +300——與 `SKILL.md` §5 同一張表）
- 衝擊幀：大招有衝擊幀或計畫、無 H3 慢詞、主片無同段漫畫格、閃白不配持續震屏、震屏有衰減

**FAIL 的項目必須修掉；WARN 的項目要能說明為什麼保留。**
