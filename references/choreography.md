# 招式編排（Fight Choreography）

> `move-library.md` 有 16 招，但**寫的時候還是會滑回「砍、擋、退」**。
> 這份文件解決的是「**怎麼逼自己用上多樣招式**」，不是增加招式數量。

---

## 0. 診斷：招式庫有 16 招，實際只用了 2 招

實測我自己寫的兩段 15 秒（各 20 鏡），統計動詞：

| 類別 | 段 A | 段 B | 8 秒版 |
|---|---:|---:|---:|
| **刀路／斬擊** | **36** | **32** | **17** |
| 踢擊 | 1 | 0 | 1 |
| 拳肘 | 1 | 0 | 1 |
| 摔投／擒拿 | 8* | 9* | 0 |
| **下盤／絆** | **0** | **0** | **0** |
| 格擋／卸力 | 2 | 4 | 1 |
| 位移／身法 | 4 | 2 | 1 |

\* 其中大半是 `lock` / `hold the lock`（刀鎖住），**不是真的摔投**。

**結論：刀路動詞是其他所有類別的 20 倍以上。整支片就是「刀來刀去」。**

### 根因不是招式不夠，而是**沒有配額**

我寫的時候是「逐鏡想一個動作」，所以自然滑向最熟的動詞（cut / strike / drive）。
**沒有任何機制強迫我換類別。**

---

## 1. 解法：配額制

### 一段 15 秒（約 20 鏡）的招式配額

| 類別 | 最少 | 說明 |
|---|---:|---|
| **刀路／斬擊** | — | **上限 8 次**（不是最少，是上限） |
| **踢擊**（腿／膝） | **3** | 近身必備 |
| **拳肘**（拳／肘／掌） | **2** | 破防用 |
| **摔投／擒拿**（真的摔，不是 lock） | **2** | 距離變化來源 |
| **下盤／絆** | **1** | 改變水平面 |
| **格擋／卸力**（有反應的擋） | **3** | 讓對方看起來難打 |
| **位移／身法** | **3** | 空間感 |

**刀路上限 8 次**這條最重要。沒有上限，其他類別永遠長不出來。

### 8 秒（10–14 鏡）的配額

| 類別 | 最少 |
|---|---:|
| 刀路上限 | **5** |
| 踢擊 | 1 |
| 拳肘 | 1 |
| 摔投 | 1 |
| 下盤 | 0–1 |
| 格擋 | 2 |
| 位移 | 2 |

---

## 2. 「真的摔」與「假摔」的差別

`lock` / `hold the lock` **不是摔投**，它只是兩人僵持。兩段的數據就是被這個騙了。

| ❌ 僵持（不算摔） | ✅ 真的摔 |
|---|---|
| `their blades lock` | `she hooks her ankle and dumps her over her hip` |
| `hold the lock as the frame ends` | `she gets an underhook and throws her across the flagstones` |
| `they brace against each other` | `she takes his wrist and whips him past her into the pillar` |

**判斷標準：有沒有一個人離開地面，或被迫移動超過一步。** 沒有的就是僵持。

---

## 3. 每個鏡頭的動作要寫「目標」，不只是「動作」

只寫動作，模型會給你一個孤立的姿勢。寫目標，動作才有方向。

| 只有動作 | 加了目標 |
|---|---|
| `she kicks` | `she snaps a low kick at the front knee to take her base` |
| `she punches` | `she fires a short hook into the ribs to open the guard` |
| `he slashes` | `he rips a reverse cut upward to break her stance` |
| `she throws her` | `she hip-throws her into the pillar to end the exchange` |

**目標決定動作的形狀。** 「踢膝蓋」和「踢頭」是完全不同的動作。

---

## 4. 三招一組，涵蓋三個高度

連續三招必須打三個不同高度，否則看起來是「一直在同一個地方揮手」。

| 組型 | 配方 |
|---|---|
| **上→下→中** | 高踢／斬頭 → 掃腿絆倒 → 膝撞腹部 |
| **近→遠→近** | 肘擊 → 甩開 → 追進來摔 |
| **虛→實→收** | 虛踢 → 肘擊打實 → 退步卸力 |

實例：

```text
[Shot 5] She snaps a high kick at Bailu's head to force her guard up.
[Shot 6] Bailu ducks under it and sweeps at the planted ankle to take her legs out.
[Shot 7] As Tieya stumbles, Bailu drives a knee into her ribs to finish the entry.
```

**三鏡、三個高度、三種部位。**

---

## 5. 主導權必須換手

一段 15 秒至少要換手 **2 次**。

| 時間 | 誰在主導 |
|---|---|
| 0–5s | A 壓著打 |
| 5–6s | **A 被反制**（換手點） |
| 6–11s | B 壓著打 |
| 11–12s | **B 被反制**（換手點） |
| 12–15s | 對衝，未定 |

**換手的那一鏡要寫清楚「怎麼換的」**——是格擋後反打、是躲開後抓到空檔、還是抓住武器。

---

## 6. 完整配方：15 秒的招式表

| # | 時間 | 招式 | 類別 | 高度 |
|---|---|---|---|---|
| 1 | 0.0 | 踏空縱躍，從上方壓下來 | 位移＋刀路 | 上 |
| 2 | 0.8 | 抬刀橫架，火花爆開 | 格擋 | 上 |
| 3 | 1.6 | 低掃腿絆腳 | **下盤** | 下 |
| 4 | 2.2 | 跳起避開，順勢膝撞 | **踢擊** | 中 |
| 5 | 2.9 | 手肘硬擋，順勢推開 | 格擋＋**拳肘** | 中 |
| 6 | 3.6 | 反手撩刀上挑 | 刀路 | 上 |
| 7 | 4.3 | 貼地翻滾躲開 | 位移 | 下 |
| 8 | 5.0 | 抓起手腕往柱子甩 | **摔投** | 中 |
| 9 | 5.8 | 撞上柱子，碎石落下 | （反應） | 中 |
| 10 | 6.5 | 回身背拳打肋 | **拳肘** | 中 |
| 11 | 7.2 | 短刀突刺 | 刀路 | 中 |
| 12 | 7.9 | 側身閃過，手刀劈腕 | 格擋＋**拳肘** | 中 |
| 13 | 8.6 | 掃堂腿放倒 | **下盤** | 下 |
| 14 | 9.3 | 翻身壓制，肘擊落下 | 摔投＋**拳肘** | 中 |
| 15 | 10.0 | 頂膝掙脫 | **踢擊** | 中 |
| 16 | 10.8 | 蹬柱變向，繞到背後 | 位移＋環境 | — |
| 17 | 11.5 | 背後勒頸拖倒 | **擒拿** | 中 |
| 18 | 12.3 | 反手肘擊脫困 | **拳肘** | 中 |
| 19 | 13.1 | 對衝，雙刀相撞 | 刀路 | 上 |
| 20 | 13.9 | 踢腿把對方踹開 | **踢擊** | 中 |

**統計**：刀路 5、踢擊 3、拳肘 5、摔投 2、下盤 2、擒拿 1、格擋 3、位移 3。

---

## 7. 檢查清單

- [ ] 刀路動詞 **≤8 次**（15 秒）／**≤5 次**（8 秒）
- [ ] 踢擊 ≥3、拳肘 ≥2、摔投 ≥2、下盤 ≥1、格擋 ≥3、位移 ≥3（15 秒）
- [ ] **沒有把 `lock` / `hold` 當成摔投算**
- [ ] 每個動作都寫了「目標」（`to take her base` / `to open the guard`）
- [ ] 每三招涵蓋三個不同高度
- [ ] 主導權換手 ≥2 次，且寫清楚「怎麼換的」
- [ ] 每一招都具名（不是 `slashes` / `strikes`）

---

## 8. 常見失敗

| 症狀 | 根因 | 修法 |
|---|---|---|
| 整片都在揮刀 | 沒有配額，習慣滑向最熟的動詞 | 刀路上限 8 次 |
| 招式多但看起來一樣 | 都在同一個高度 | 三招三高度 |
| 像打沙包，對面只會擋 | 沒有換手 | 加 2 個換手點 |
| 動作有但沒氣勢 | 沒寫目標 | 每個動作加 `to ...` |
| 摔投看不出是摔 | 寫成 `lock` / `brace` | 要有人離地或被推超過一步 |
| 兩人黏在一起不動 | 全程近身，沒有位移 | 位移 ≥3，距離要有變化 |
| 招式中斷不連貫 | 每招獨立寫 | 用動作鏈：上一招的殘餘動能當下一招起點 |

## 9. 速度、可見性與強約束（2026-10-26 新增）

> 來源：老大的教學片 v2（打鬥特效）、v3（提高打鬥的方法）、v7（雙女劍鬥原提示詞）、1026 圖文提示詞。**以下全部 H3 未實測**，但都是提示詞層技巧，成本低。

### 9.1 提速方法排名（v3 作者經大量測試的 tier list）

| 排名 | 方法 | 結論 |
|---|---|---|
| 最差 | 只寫「高速打鬥」「急速打鬥」 | 堆再多次都沒用，慢得像打太極 |
| 低 | 0.2 秒一個動作（每秒 5 招） | 不慢，但 AI 跑不動（超載） |
| 低 | 速度形容詞（閃電般出拳） | 特定幀有用，整體提速有限 |
| 低 | 負面提示詞 | 加比不加好，差距不大 |
| 中 | 節奏鐵律（告訴 AI 這是快速打鬥）、高速鏡頭參數 | 只能快，出不了極限速度 |
| **頂級** | **身法特效＋動態模糊殘影** | 速度加權非常高 |
| **頂級** | **分鏡拆成 1–2 秒、每秒 3 個具體動作** | 極限速度方法 |

**規則**：一鏡 1–1.5 秒、三個具名動作、加 `motion blur`／`afterimage`，不寫 `high-speed fight`。

```text
[Shot 2] At 00:01.000, a low tracking shot with heavy directional motion blur: in one second she sidesteps his thrust, traps his wrist under her arm, and drives her elbow into his jaw, leaving a smeared afterimage behind each move.
```

### 9.2 速度詞

✅ `kicks off the ground`、`instantly`、`at blinding speed`、`leaving an afterimage`、`blinks`
❌ `flies toward`（「機甲飛向巨龍」→ 軟綿綿）

### 9.3 每擊寫打哪，上下左右換著打（v2）

「只寫『機甲攻擊巨龍』→ 每下都一樣」。四刀四位置：額頭橫切、由下往上挑下顎、低位撞前腿、斜劈兩角之間。與 §3「寫目標」、§4「三招三高度」同一件事，大型對手也適用。

### 9.4 ACT 追尾與換位（1026 圖文）

- 「3A 第三人稱 ACT 追尾機位」：鏡頭死咬攻擊者後肩。
- **無站樁、無隔空對波**：全程近身兵刃纏鬥；兩人站著各自放波＝最無聊的打法。
- **人物每 0.2–0.3 秒完成一次換位**（成品時間軸；生成時可寫慢一點再加速）。
- **重擊命中必觸發擊飛，攻擊者瞬間追擊**。
- **三連輕擊**：`a 0.1-second blink across half the frame, triggering three light clashes in a row`。

### 9.5 強約束句（v7 原提示詞翻譯，可直接搬）

```text
Sparks appear only at the exact point where the blades touch.
Every leap has a clear take-off, arc and landing.
Every movement carries weight and momentum; both fighters keep their feet on the ground between leaps.
Each fighter moves in a clear direction through one continuous space.
Fast shots keep directional motion blur, but faces, hands and blade contact stay readable.
The camera serves the action and steadies between strikes.
The effects frame the fighters and leave their faces and hands visible.
```

對應的負面版本（v7 原文「不要全程亂閃白光、不要過曝、不要特效完全遮擋人物、不要無意義旋轉、不要動作重複循環」）要改寫成上面的正面句。**「不要全程亂閃白光」**特別重要：閃白只給衝擊點清單裡的那幾下。
