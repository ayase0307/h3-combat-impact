# 打鬥運鏡語法（H3 官方詞彙 + 實戰套路）

## 0. 鐵律：每個鏡頭都要有運鏡（實測）

**沒有一個鏡頭可以是靜止的。**

實測原參考片（30 秒 / 40 刀）：0.0–0.375 持續推近、1.25–2.125 持續拉遠、2.25–2.875 再推近——**每一鏡都在推或拉**。

實測自己的三版：

| 版本 | 7 鏡裡有運鏡的 | ZOOM |
|---|---:|---:|
| A6 | 2 | 0 |
| D3 | 1 | 0 |
| D5 | 1 | 0 |

結果就是「完全沒有運鏡感」。

### 0.1 但有一個例外：最大衝擊可以鎖死相機（3D CG 實測推翻）

另一支 3D CG 參考片（30.1 秒 / 14 鏡）量到相反的結論：

- **43% 的鏡頭相機是鎖死的**（背景位移 < 1px）
- 而這 6 個靜止鏡頭裡，**有 4 個正是全片最重要的時刻**：臉部特寫、軍牌特寫、徑向爆點、最終引爆
- **全片最大衝擊（29.15 秒的放射爆點）相機完全鎖死**——位移平均 0.94px，18 幀中有 13 幀完全靜止，但銳度 1218 是全片最高

**為什麼？** 因為衝擊感來自「特效把背景推開」，不是來自「相機在抖」。相機不動，觀眾才有東西可以看；相機跟著一起動，整個畫面糊成一片。

| 情況 | 該怎麼寫 |
|---|---|
| 運動段落 | 每鏡一個運鏡（常規） |
| **最大衝擊那一鏡** | **相機鎖死，讓特效推開背景** |

```text
[Shot 5] At 00:06.400, the camera holds a static shot as the burst expands and the
background behind them is pushed outward into radial streaks.
```

**判斷訊號**：如果你要寫的是「全片最強的一擊」，那鏡**不該**有運鏡。前面的鋪陳鏡要動，這一鏡要靜——對比才成立。兩個都動就沒有高潮。

### 0.2 甩鏡要跟著主體甩，不是甩空景

實測：甩鏡時**中央位移 14.21px > 邊帶位移 9.74px**。差異代表鏡頭是跟著角色跑的，不是原地搖空景。

```text
❌ the camera pans right with large amplitude at fast speed
✅ the camera pans right with large amplitude at fast speed, following the fighter
```

沒有「跟著誰」的甩鏡，看起來就是鏡頭自己在亂動。

### 0.3 運鏡強度的可驗收下限

42.6 秒 / 68 鏡的參考片量測（背景帶相位相關）：

| 指標 | 值 |
|---|---|
| 有背景位移的鏡頭 | **86.8%**（53 鏡中 46 鏡） |
| 完全靜止的鏡頭 | 13.2% |
| 位移方向 | 水平 39 鏡、垂直 7 鏡 → **水平為主** |
| 中位背景位移 | 0.88 px/幀（160px 寬）= 原生 2516 寬約 **14 px/幀 ≈ 420 px/秒** |

**0.88 px/幀是「觀眾感覺得到鏡頭在動」的最低量。** 低於此值的運動等同靜止。驗收時：水平位移的鏡頭應占 **≥70%**，有位移的鏡頭應占 **≥85%**。

> 推近／拉遠（zoom）比例量不到——log-polar 與多尺度相關都會被內容變化淹沒。**不猜數字，改用視覺佐證。**

### 七鏡運鏡計畫（不重複）

| 鏡 | 運動 |
|---|---|
| 1 | push in（大幅快速） |
| 2 | 定格圖（不動） |
| 3 | truck right（大幅快速） |
| 4 | **zoom in**（大幅快速） |
| 5 | arc（小幅快速） |
| 6 | **zoom out**（大幅快速） |
| 7 | push in（小幅快速） |

**同一支片不要七個都 push in。** 推、拉、搖、移、環繞、變焦輪流用。

### 剪接密度：太慢的第一診斷

**「看起來像靜態畫」通常不是動作不夠強，是刀不夠多。**

| 條件 | 可容納刀數（7.5 秒） |
|---|---|
| 每刀一個動作 ＋ 一個運鏡 | **9–10 刀**（0.75–0.85 秒／刀） |
| 每刀只有描述、無動作 | 6 刀以下（再多會變靜態） |

實測對照：

| 版本 | 刀數 | 每刀內容 | 末段運動 |
|---|---:|---|---:|
| D5 | 5 | 有動作、運鏡少 | 9.55 |
| D6 | 5 | 有動作、每刀有運鏡 | 14.26 |
| A5 | 10 | 只有描述、無動作 | 全程 12.75 |
| **D7** | **9** | **一個動作 ＋ 一個運鏡** | **18.02** |

**刀多不是問題，刀多＋每刀空才是問題。**

原片基準：30 秒 40 刀 = 0.75 秒一刀。7.5 秒就是 10 刀。

### 衝擊是「切到定格圖」，不是「在動作裡凍結」

原片的做法：

```
0.50  切到極特寫（腳）
0.75  切到定格衝擊圖：命中姿勢 + 粉色放射線，停 4 格（0.37 秒）
1.25  切回廣角
```

**定格圖是一個獨立鏡頭**，畫面靜止、但有放射線撐住張力。它讀成「衝擊」，不是「慢動作」。

❌ 錯：`for two frames the action near-freezes`（在連續動作裡凍結 → 慢動作）
✅ 對：切一個新鏡頭，寫 `a held impact frame ... this frame holds for eight frames, then cuts away`

### 尺度要跳

廣角 → 極特寫 → 廣角。跳得越狠，節奏越強。連續三個中景就是平的。

## 1. 官方運鏡三維度

H3 只認這個結構：**動作類型 + 幅度 + 速度**，且必須寫成自然語句。

| 維度 | 可用表達 |
|---|---|
| 類型 | `Zoom In / Zoom Out`（變焦，機身不動） |
| 類型 | `Push In / Pull Out`（機身前後移動） |
| 類型 | `Pan Left / Pan Right`（原地水平搖） |
| 類型 | `Truck Left / Truck Right`（水平平移） |
| 類型 | `Tilt Up / Tilt Down`（原地垂直搖） |
| 類型 | `Pedestal Up / Pedestal Down`（整機升降） |
| 類型 | `Arc Shot`（繞主體弧線移動） |
| 類型 | `Tracking Shot`（跟隨移動物體） |
| 類型 | `Static Shot`（完全靜止） |
| 類型 | `Shake Slightly / Shake Strongly`（輕震／強震） |
| 類型 | `POV`（主觀視角） |
| 類型 | `Roll Clockwise / Roll Counterclockwise`（滾轉） |
| 幅度 | `with small amplitude` / `with large amplitude` |
| 速度 | `at slow speed` / `at fast speed` |

中等幅度與常速可省略。**不要**在句尾堆疊標籤：

- ✗ `close-up, dynamic, cinematic camera, shake, fast`
- ✓ `The camera pushes in with large amplitude at fast speed toward the point of contact.`

---

## 2. 打鬥專用套路（直接套用）

### 2.1 命中推鏡（Punch-In on Impact）
```text
As the blade connects, the camera punches in with small amplitude at fast speed and shakes strongly.
```
用途：所有 L2 以上命中。**推鏡 + 震動必須同時發生在同一個子句**，模型才會把它們綁在同一幀。

### 2.2 蓄力定鏡（Hold for Anticipation）
```text
The camera holds a static shot as her weight sinks into the rear leg and the blade draws back.
```
用途：蓄力拍。定鏡讓觀眾預期「要出事了」。

### 2.3 甩鏡轉場（Whip Pan Transition）
```text
The camera pans right with large amplitude at fast speed, the frame smearing into horizontal streaks, and settles on the male swordsman mid-stance.
```
用途：切換攻擊者。甩鏡比硬切更有連續感，且能掩蓋 AI 的接縫。

### 2.4 環繞對峙（Orbit Standoff）
```text
The camera arcs around the two figures with small amplitude at slow speed, keeping both silhouettes in frame.
```
用途：L4 之前的「靜」。慢速環繞能同時交代兩人距離與空間關係。

### 2.5 低角度英雄鏡（Low-Angle Hero）
```text
The camera tilts up with small amplitude at slow speed from the cracked flagstones to her face.
```
用途：開場、收尾、氣勢建立。低角度 + 上搖 = 壓迫感。

### 2.6 俯拍衝擊波（Top-Down Shockwave）
```text
The camera pedestals up with large amplitude at fast speed into a top-down view as the shockwave ring races outward across the courtyard.
```
用途：L4 的擴散拍。俯拍是唯一能拍出「衝擊波規模」的角度。

### 2.7 跟拍位移（Tracking the Knockback）
```text
The camera trucks right with large amplitude at fast speed, keeping pace with him as he is hurled backward.
```
用途：擊退。跟拍讓觀眾感覺「自己被推著走」。

### 2.8 主觀受擊（POV Impact）
```text
The camera drops to a POV as the fist fills the frame, then rolls counterclockwise and shakes strongly.
```
用途：偶爾用一次，代入感極強。**整段只能用一次**。

---

## 3. 主體動作與鏡頭運動必須分離

這是官方明列的規則，也是 AI 打鬥最容易糊掉的原因。

- ✗ `The camera spins around her as she spins and slashes`（兩個旋轉疊加 → 畫面全糊）
- ✓ `She spins once on her heel and slashes horizontally while the camera holds a static shot.`

原則：**主體動得快，鏡頭就穩；主體不動，鏡頭才動。**

---

## 3.3 電影級運鏡：幅度與速度要有變化

**機位多 ≠ 有電影感。** 實測我自己寫的 20 個鏡頭，機位確實多樣
（高空俯拍／貼地／鳥瞰／越肩／吊臂／遠景／特寫），
但 **14 個鏡頭全部寫 `with large amplitude at fast speed`** ——
二十種機位、同一個節奏。

### 三檔速度（不要全用 fast）

| 檔 | 寫法 | 佔比 |
|---|---|---|
| 爆速 | `at extreme speed` | 20% |
| 快 | `at fast speed` | 45% |
| 慢 | `at slow speed` | 20% |
| 靜 | `holds a static shot` | 15% |

**慢是為了讓快更明顯。** 全片都快的，等於全片都一樣快。
同一段至少要有 1 個慢鏡 + 1 個靜鏡。

### 幅度要跳級

`large` → `small` → `large` → 靜 → `large`。
**連著寫三個 `large amplitude`，第三個改成 `small`。**

### 運鏡要有因果（最重要的差別）

| ❌ 描述式 | ✅ 因果式 |
|---|---|
| `The camera pushes in with large amplitude.` | `He drives her back and the camera gives ground with them, pulling back.` |
| `The camera trucks left.` | `She breaks left and the camera whips after her, lagging half a beat.` |
| `The camera holds a static shot.` | `The camera holds dead still as the impact lands and the frame shudders once.` |

**「鏡頭不跟」也是一種運鏡。**
`the camera stays locked on her as he circles behind` 比 `arcs around them` 有戲得多。

十個電影級機位（地面前置／前景穿越／高度落體／長焦壓縮／廣角貼臉／
人掠過鏡頭／完全靜止／吊臂升降／甩到物件／跟焦轉移）
見 `references/cinematic-camera.md`。

---
## 3.4 ⛔ 禁止「繞著人物轉圈圈」

**`arcs around` / `orbits` 全片最多 1 個，而且只能當「轉接鏡」**（用來從一個位置接到下一個位置）。

早期這份 skill 唯一主推的套路就是 Arc Shot，結果每一鏡都在繞同一個人轉——
觀眾感受到的是「攝影機繞著模特兒轉」，不是「無人機在拍一場戰鬥」。

| | 繞圈圈（arc / orbit） | 無人機式 |
|---|---|---|
| 機位變化 | 繞同一個中心，距離不變 | 每鏡換一個**完全不同**的位置與高度 |
| 焦段 | 主角一直同樣大小 | 主角時大時小，時而佔滿畫面、時而是小點 |
| 觀感 | 展示角色 | **觀看一場戰鬥** |
| 空間 | 平面，看不出深度 | 有高、有低、有遠、有近 |

**要無人機式運鏡（8 個機位、五種尺度、穿前景、大遠景）→ 見 `references/drone-camera.md`。**

---
## 3.5 「運鏡感」的三個條件（2026-10-19 實測補完）

**「每個鏡頭都要有運鏡」只說了必要條件，沒有說充分條件。**
實跑三版之後量測，發現寫了運鏡 ≠ 有運鏡感。真正決定觀眾感覺「鏡頭在動」的是下面三件事。

### 條件一｜每鏡的取景必須不一樣（不要主體在同一位置）

只寫 `the camera trucks right` 不夠。**如果每一鏡的主體都在畫面同一個位置、同一個大小**，
觀眾感受到的是「同一個鏡頭在微調」，不是「運鏡」。

| 做法 | 效果 |
|---|---|
| 每鏡換一個機位（低角／俯角／極特寫／跟拍／越肩） | 有運鏡感 |
| 每鏡只換運鏡方向，機位不變 | 像同一鏡頭在晃 |

實測對照（同一顆種子、同一場景）：

| 版本 | 寫法 | 中位鏡長 | 短鏡% | 觀感 |
|---|---|---:|---:|---|
| B | 每鏡一個運鏡，但全是廣角／中景 | 0.73s | 30% | **單調** |
| C | 每鏡換景別＋運鏡 | 0.50s | 60% | 明顯改善 |
| D | 再加每鏡一個光影事件 | 0.375s | 73% | 接近參考片 |

**寫法要點：景別詞與運鏡詞一起改變。** 只寫運鏡不寫景別，模型會給你十個一樣的廣角。

### 條件二｜鏡長要短，而且要「雙峰」

參考片（42.6 秒 / 68 鏡）：**中位鏡長 0.20 秒**，68.8% 的鏡短於 0.5 秒，但仍有 18.8% 的鏡長於 1 秒。

這是**雙峰分布**：幾個長鏡交代空間與動作，大量短鏡負責衝擊與特效插入。
均勻的 0.7 秒一鏡 = 節奏單調。

> **長鏡與短鏡的比例 ≈ 1:4。** 8 秒裡大約 2 個長鏡（1.5–2.5 秒）＋ 8–10 個短鏡。

### 條件三｜每一鏡都要有光影事件，不只有「命中」那一鏡

量測指標「鏡內是否有亮度急遽變化」：

| 版本 | 有光事件的鏡% | 亮度擺幅中位 |
|---|---:|---:|
| 參考片 | **71.4%** | **85.7** |
| 我的實跑版 | 40–50% | 17–32 |

**參考片幾乎每一鏡都有一個光影事件**——能量浪、X 形爆、放射線漫畫格、光刃。
只有「命中」才給光的版本，會有半片是暗的。

> **規則：一個 8 秒片段裡，至少 7 成的鏡要有光影事件。**
> 寫法：每一鏡都指定一個光源（核心爆點／放射線／能量浪／光刃／白熱節點），
> 不要只寫在「命中」那一鏡。

### 三個條件的寫法模板

```text
[Shot 1] ... chest to chest, filling the frame from the waist up ...
          the instant they meet, a white-hot core bursts at the contact point
          and ice-blue lightning branches outward from it ...
          The camera arcs around the locked pair with large amplitude at fast speed.

[Shot 2] At 00:01.900, the camera cuts to an extreme close-up of the two blades
          crossed at the contact point, a white-hot core where they grind,
          a violet halo closing around the crossing steel, and sparks tearing
          off the impact in a narrow cone. The camera pushes in with large
          amplitude at fast speed.

[Shot 3] At 00:03.700, the frame cuts to a black-and-white manga panel:
          a solid white core at the point of contact with clean radial speed
          lines bursting in every direction ...
```

**三樣東西每一鏡都要有：新的景別、新的運鏡、新的光。**

---

## 4. 打鬥分鏡的景別節奏

一段 15 秒的打鬥，景別必須有呼吸：

| 順序 | 景別 | 功能 | 停留 |
|---|---|---|---|
| 1 | 大廣角 / 低角度全景 | 交代空間與人數 | 1.5–2.5s |
| 2 | 中景 | 動作主體 | 0.8–1.2s |
| 3 | 特寫（手、眼、兵器） | 蓄力與意圖 | 0.5–0.8s |
| 4 | 中景 / 跟拍 | 命中 | 0.3–0.5s |
| 5 | 特寫（撞擊點） | 衝擊幀 | 0.1–0.2s |
| 6 | 大廣角 | 衝擊波與環境 | 1.0–2.0s |

**連續兩個同景別 = 剪輯死亡。** 每次切換景別，至少要跳一級（廣角→特寫，或特寫→廣角）。

---

## 5. 速度感的四個開關（按順序開）

1. **前景掠過**：`lanterns whip past the lens`（前景快速劃過 = 速度）
2. **運動模糊**：`the blade smears into a horizontal streak`（只給兵器，不給人）
3. **塵/水/雨被推開**：`rain is pushed into a radial sheet`（環境反應）
4. **鏡頭震動**：`shakes strongly`（最後才加，加了就別再加大幅度）

四個全開會變成災難。**一次最多開三個。**

---

## 6. 常見運鏡錯誤

| 錯誤寫法 | 問題 | 修正 |
|---|---|---|
| `360-degree rotating camera` | H3 會生成一整圈模糊 | 改成 `arcs around with small amplitude at slow speed` |
| `fast zoom` | 容易整個畫面失焦 | `pushes in with small amplitude at fast speed` |
| `camera follows the fight` | 沒有方向與幅度 | 指定 `tracks left / trucks right` + 幅度 |
| 每個鏡頭都 `shakes strongly` | 觀眾暈、且失去層級 | 只有 L3 以上才用 `strongly` |
| 一個鏡頭內切三次景別 | 模型會融成一團 | 一次鏡頭只給一個機位 |
| 甩鏡不指定跟隨對象 | 看起來像鏡頭自己在亂動 | 加 `following the fighter`（甩鏡要跟主體甩） |
| 最大的衝擊也給大幅度運鏡 | 畫面整個糊掉，沒有焦點 | 那一鏡鎖死相機，讓特效推開背景 |

---

## 7. 參考片量測的兩個陷阱（實測，會讓你得出錯的結論）

### 7.1 「60fps」可能不是 60fps——先驗證再換算

一支標示 `r_frame_rate=60` 的參考片，實測：

| 項目 | 值 |
|---|---|
| 封裝宣告 | 60/1 |
| **實際封裝數** | **723 幀 / 30.1417s = 24.06fps** |
| 幀間隔分布 | 0.050s × 364 幀、0.0333s × 356 幀 |
| 真相 | **24fps 母版的 2:3 pulldown**（交錯重複幀） |

**H3 是 24fps，所以這類素材「幀數 1:1 對應」，根本不需要任何 60→24 換算。**

驗證指令：

```bash
ffprobe -v error -select_streams v:0 -show_entries "packet=pts_time" -of csv=p=0 clip.mp4
```

看相鄰時間差有幾種值：只有一種 → 固定幀率；兩種且交錯 → pulldown。

> **踩坑警告**：逐幀分析時不加 `-fps_mode passthrough`，ffmpeg 會重抽成 CFR60，幀數 723→1809，差異中位數歸零，自適應門檻失效——實測炸出 **618 個假切點**。

### 7.2 跨片比運動量，必須先統一幀率

`measure_motion.py` 取的是「每幀平均差異」。同樣的實際運動：

- 24fps 每幀差異 = 1.00
- 30fps 每幀差異 = **0.80**（位移被攤薄到更多幀）
- 60fps 每幀差異 = **0.50**

實測差 2.5 倍。**30fps 素材的運動分數系統性偏低約 20%。**

真實案例：兩支參考片原生分數 16.51 vs 14.06，看起來前者活躍 17%；**正規化到 24fps 後是 15.94 vs 16.06，幾乎相同**。那 17% 是幀率造成的假象。

| 指標 | 幀率敏感度 |
|---|---|
| `overall` / `opening` / `mid` / `ending` | **偏低**（30fps −20%、60fps −50%） |
| `peaks`（峰值格） | **偏高**（30fps +25%，因為幀數多） |
| 靜止對稱 | 相對判定，仍有效 |

**規則：引用絕對值時乘 1.25 折回 24fps（30fps 素材）；跨片比較前先統一幀率。**
