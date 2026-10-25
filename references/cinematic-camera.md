# 電影級運鏡（Cinematic Camera）

> 打鬥片的「電影感」不是來自機位多，而是來自**每個機位的幅度、速度、起始點都不同**，
> 並且**運鏡跟動作有因果關係**（因為他衝過來，所以鏡頭退）。

---

## 0. 診斷：為什麼「機位很多」還是看起來平

實測我自己寫的 20 個鏡頭，機位確實多樣（高空俯拍／貼地／鳥瞰／越肩／吊臂／遠景／特寫），
但**14 個鏡頭全部寫同一個幅度與速度**：

| 寫法 | 出現次數 |
|---|---|
| `with large amplitude at fast speed` | **14 / 20** |
| `with small amplitude at fast speed` | 4 / 20 |
| `holds a static shot` | 2 / 20 |

**結果：二十個鏡頭、二十種機位、同一個節奏。** 觀眾感受不到層次。

電影級運鏡的差別不在「用了幾個機位」，而在：

| 平面運鏡 | 電影級運鏡 |
|---|---|
| 每鏡一個機位、一個速度 | **幅度／速度／方向都有變化** |
| 運鏡是描述（鏡頭推近） | 運鏡是**因果**（因為他衝過來，所以鏡頭退） |
| 一鏡一動作 | 一鏡一動作 **＋ 起點與終點不同** |
| 全部 `fast speed` | 有快有慢，**慢的鏡用來對比更顯快** |

---

## 1. 三檔速度（不要全用 fast）

| 檔 | 寫法 | 什麼時候用 | 佔比 |
|---|---|---|---|
| **爆速** | `at extreme speed` | 命中、被打飛、崩塌 | 20% |
| **快** | `at fast speed` | 一般交手 | 45% |
| **慢** | `at slow speed` | 蓄力、凝視、餘韻 | 20% |
| **靜** | `holds a static shot` | 衝擊幀、極特寫 | 15% |

> **關鍵：慢是為了讓快更明顯。** 全片都是快的，等於全片都一樣快。

同一段裡至少要有 **1 個慢鏡 + 1 個靜鏡**。

---

## 2. 幅度要跳級，不要連續三鏡同幅度

幅度只有三級：`small` / 中（省略） / `large`。

```
❌ 大、大、大、大、大、大、大（等於沒幅度）
✅ 大 → 小 → 大 → 靜 → 大 → 小 → 大
```

**判斷訊號**：如果你連著寫了三個 `large amplitude`，第三個改成 `small`。

---

## 3. 運鏡要有因果（最重要的差別）

電影鏡頭的運動是**被動作推出來的**，不是自己決定要動。

| ❌ 描述式 | ✅ 因果式 |
|---|---|
| `The camera pushes in with large amplitude at fast speed.` | `He drives her back and the camera gives ground with them, pulling back at fast speed.` |
| `The camera trucks left.` | `She breaks left and the camera whips after her, lagging half a beat.` |
| `The camera holds a static shot.` | `The camera holds dead still as the impact lands and the whole frame shudders once.` |
| `The camera arcs around them.` | `The camera stays locked to her face as he circles behind — it does not follow him, it stays on her.` |

### 因果運鏡的五個句型

| 動作 | 對應的運鏡句 |
|---|---|
| 被擊退 | `the camera gives ground with her, pulling back at fast speed` |
| 衝過來 | `the camera holds its ground and lets him rush past it` |
| 破牆／撞柱 | `the camera gets shoved by the blast, shaking hard and settling` |
| 破空斬 | `the camera tracks the blade, snapping round with the swing` |
| 突然停手 | `the camera keeps drifting forward for a beat after she stops` |

**「鏡頭不跟」也是一種運鏡。** `the camera stays locked on her as he circles behind` 比
`arcs around them` 有戲得多——因為它表達了「誰在注意誰」。

---

## 4. 十個電影級機位（取代「繞圈」）

| # | 機位 | 為什麼有電影感 | H3 寫法 |
|---|---|---|---|
| 1 | **地面前置**（鏡頭貼地面，人在上面移動） | 地面質感成為前景，有壓迫 | `a camera lying flat on the wet stone, the fighters passing over it` |
| 2 | **前景遮擋穿越**（從柱子／布條後方滑出） | 產生景深與「偷偷看到」的視角 | `the camera slides out from behind a broken pillar` |
| 3 | **高度落體**（跟著人往上／往下） | 垂直運動比水平更少見 | `the camera drops with her from the colonnade as she falls` |
| 4 | **長焦壓縮**（遠處長焦，空間被壓扁） | 兩人像貼在一起，最有壓迫 | `a long lens from across the courtyard, the two fighters compressed into one plane` |
| 5 | **廣角貼臉**（極近距離、變形） | 呼吸感、攻擊感 | `the lens less than a hand's width from her face` |
| 6 | **鏡頭任人擺佈**（人從鏡頭前穿過） | 觀眾感覺「在現場差點被撞」 | `a fighter's shoulder sweeps past the lens` |
| 7 | **靜止不動**（關鍵時刻完全不動） | 對比之下最有力 | `the camera holds dead still and the frame shudders once` |
| 8 | **吊臂升降**（垂直大幅） | 建立尺度 | `the camera rises straight up above the rubble` |
| 9 | **甩到物件**（甩鏡停在物件上） | 節奏的「呼吸」 | `the camera whips to the falling brazier and stops on it` |
| 10 | **跟焦轉移**（焦點從 A 到 B） | 視線的轉移 | `the focus racks from her blade to his eyes` |

> **第 3、6、10 項在 H3 特別有效**——它們不是「機位」，是「鏡頭行為」。

---

## 5. 一鏡的完整寫法（電影級）

四個元素都要有：

```text
[機位：高度＋距離] ＋ [主體動作] ＋ [運鏡：因果＋幅度＋速度] ＋ [一個鏡頭行為或環境反應]
```

實例：

```text
[Shot 7] At 00:04.200, the camera is lying flat on the wet stone at ankle height,
the fighters crossing above it. Bailu pivots on one heel and drives her katana
down; the tip bites the flagstone an inch from the lens and fractures it, chips
spitting past the glass. The camera does not move — the whole frame shudders
once and settles at slow speed.
```

拆解：

| 元素 | 內容 |
|---|---|
| 機位 | `lying flat on the wet stone at ankle height` |
| 動作 | `pivots on one heel and drives her katana down` |
| 運鏡（因果） | `does not move — the frame shudders once and settles` |
| 鏡頭行為 | `chips spitting past the glass` |

**「the camera does not move」＋「chips past the lens」＝ 電影感，不是特效感。**

---

## 6. 十五秒的運鏡節奏表

| 時間 | 運鏡檔位 | 機位類型 |
|---|---|---|
| 0–1s | 爆速／大 | 高空俯拍或貼地（定調） |
| 1–3s | 快／大→小 | 切貼地與越肩 |
| 3–5s | 快／小 | 中距離，換高度 |
| 5–6s | **慢或靜** | 極特寫（喘一口） |
| 6–9s | 爆速／大 | 命中最重的一擊，可靜可甩 |
| 9–12s | 快／中 | 追擊，長焦壓縮 |
| 12–15s | 快／大 → **慢** | 收尾，帶位移 |

**每一段都要有「一個慢或靜」的鏡。** 沒有停頓的連續快，觀眾會疲乏、反而覺得不刺激。

---

## 7. 檢查清單

- [ ] 全片 `arcs around` / `orbits` **≤1**，且只當轉接
- [ ] 速度分三檔以上（`extreme` / `fast` / `slow` / 靜），**不是全 `fast`**
- [ ] 幅度有跳級（大 → 小 → 大），**沒有連續三鏡 `large`**
- [ ] 至少 **3 個鏡頭的運鏡是因果句**（因為動作而動，`the camera gives ground` / `holds its ground`）
- [ ] 至少 **1 個「鏡頭不跟」**的鏡（`stays locked on her as he circles behind`）
- [ ] 至少 **1 個鏡頭行為**（貼地／穿前景／人掠過鏡頭／跟焦轉移）
- [ ] 至少 **1 慢 + 1 靜**用來做對比
- [ ] 沒有連續三鏡同高度

---

## 8. 常見失敗

| 症狀 | 根因 | 修法 |
|---|---|---|
| 機位很多但看起來一樣 | 幅度與速度全部同一檔 | 見 §1、§2 |
| 像 MV 或遊戲預告 | 每鏡都在推拉，沒有因果 | 改寫成因果句 |
| 感覺攝影機在炫技 | 沒有停頓 | 加慢鏡與靜鏡 |
| 看完記不住任何鏡頭 | 沒有「鏡頭行為」 | 加貼地／穿前景／焦點轉移 |
| 打鬥空間亂 | 機位高度沒跳 | 見 §6 節奏表 |
| 兩人像在跳華爾茲 | 一直在環繞 | 禁 orbit，改用十機位 |

## 9. 大招與收尾的鏡頭（2026-10-26 新增）

> 來源：1026 圖文提示詞（骨傘女 vs 劍女）、教學片 v6。**H3 未實測。**

### 9.1 Z 軸驟停觸發重擊

鏡頭沿 Z 軸跟著下墜的攻擊一起迅猛沉降，在命中那一刻**驟停**，用「停」把力量交給畫面：

```text
At 00:02.400, the camera plunges along the Z axis with her falling strike and stops dead at the moment the umbrella tip meets the rising sword point: the flagstones crack in a starburst, the puddles are blasted up into a towering wall of mist, and the camera sinks hard then rebounds.
```

### 9.2 瞳孔倒映來襲物

大招砸下前，0.1 s 推鏡切眼部極近特寫，瞳孔裡倒映來襲物；表情肌肉要寫（下眼瞼收緊、屏息），否則是死人臉。見 `ultimate-moves.md` §4。

### 9.3 吞沒鏡頭的收尾

貼地超廣角＋機位極速後拉，煙塵或光牆撲面吞沒鏡頭 → 黑屏或全白 → 靜：

```text
At 00:07.200, a ground-level ultra-wide shot as the camera pulls back with large amplitude at fast speed; the wall of dust rolls toward the lens and swallows the frame into darkness.
```

H3 的最後 1–2 秒會自動減速，這種「吞沒」正好可以吃掉那段減速；若要接下一段，用全白結尾，下一段第一格從滿屏白光中猛拉開（`fl2va-chain.md` §8）。

### 9.4 命中硬切特寫

命中瞬間硬切特寫看受力細節（甲冑凹陷、氣場碎裂）再切回倒飛。原文寫「0.5 s 強制升格」——升格在組裝做（`impact_frame.py ramp --seg a-b:0.5`），提示詞只寫硬切與細節。

### 9.5 荷蘭角繞轉

荷蘭角約 15°，貼地繞 90° 越轉越慢、傾斜慢慢回正（教學 v6）。注意全片繞圈 ≤1 次的規則（`drone-camera.md`）。
