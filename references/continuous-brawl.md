# 連續對轟（CONTINUOUS_BRAWL）

## 0. 什麼時候用這個模式

| 模式 | 適用 | 節奏單位 |
|---|---|---|
| **六拍**（預設） | 對決、單次交手、有蓄力與收勢 | 一次交手 |
| **連續對轟** | 近身纏鬥、天台對打、誰都不退 | 一次交換（0.8–1.5 秒） |

**同一支片只能用一種。** 混用會兩邊都不成立——六拍需要停頓，四拍需要不停。

判斷訊號：如果需求裡出現「不停」「壓著打」「連續」「沒有喘息」，就用四拍。

---

## 1. 衝擊四拍

```
① 2 幀衝擊幀 → ② 長拖影 → ③ 彈性回彈 → ④ 立即再入
```

沒有蓄力、沒有凍結、沒有收勢。**因為它從不停止。**

| 拍 | 寫法 |
|---|---|
| ① 衝擊幀 | `for two frames the background flashes hot pink and radial speed lines burst from the contact` |
| ② 拖影 | `both bodies whip away in long smears` |
| ③ 回彈 | `land in a skid, and are already lunging again` |
| ④ 再入 | `she rides that snap into a one-two` |

對比六拍：六拍的「停」是 4–6 幀凍結；四拍的「停」只有 2 幀衝擊幀，緊接著就是拖影。**沒有凍結，只有拖影。**

---

## 2. 動作鏈（最核心的技法）

不要寫「動作清單」，要寫「動作鏈」——**上一個動作的殘餘動能，變成下一個動作的起點。**

| 清單式（錯） | 鏈式（對） |
|---|---|
| `She staggers back. Then she kicks.` | `One staggering step turns into a front kick.` |
| `He is bent over. Then he elbows.` | `An elbow whips out of the fold.` |
| `Her head snaps back. Then she punches.` | `She rides that snap into a one-two.` |
| `Her feet skid. Then she knees.` | `A knee drives out of the skid.` |

**句型模板**：`<上一個狀態> turns into / rides / drives out of / comes up out of <下一個動作>`

常用的四個動詞：`turns into`、`rides`、`drives out of`、`comes up out of`。

---

## 3. 深度錯位

```text
keeping one body nearer the lens and the other clearly behind it with air between them
```

兩人永遠一近一遠，中間有空氣。解決兩個問題：主體重疊看不清、兩人在同一平面比劃。

**不要寫** `both fighters in frame`——那會得到並排的兩根柱子。

---

## 4. 鏡頭參與

鏡頭是參戰者，有位置、有速度、有被撞的風險：

| 動作 | 寫法 |
|---|---|
| 從地面升起 | `the camera rises fast from floor level` |
| 從兩人之間穿過 | `passes between their bodies` |
| 鑽到踢腿下方 | `the camera drops under a spinning kick` |
| 擦過鏡頭 | `a punch skims past the lens within a hand's width` |
| 貼地疾馳 | `skims the floor` |

**「within a hand's width of the lens」比「close to camera」有效得多**——它給了具體距離。

---

## 5. 快速細節切

每 2–3 次交換後，插 0.2–0.4 秒的微觀鏡頭：瞇起的眼睛、收緊的拳套、甩動的飾品、填滿畫面的鞋底。

作用不是敘事，是**節奏呼吸**。在連續高速中插一個 0.3 秒近景，下一擊會顯得更大。

**H3 的寫法**：必須獨立成 `[Shot N]`，否則會被忽略。

```text
[Shot 2] At 00:04.200, the camera cuts to a half-second detail: her narrowed eyes, the glove tightening, the dog tags swinging.
[Shot 3] At 00:04.500, the camera cuts back to the fight as ...
```

⚠️ 這是一個高風險操作：0.3 秒的切點在 H3 上可能被吃掉或延長。要用就先做 A/B（見下）。

---

## 6. 空間錨點

給 2–3 個可互動的物件，讓動作有參照物：

| 錨點 | 用途 |
|---|---|
| 鐵絲網 | 蹬網反彈、撞網震顫 |
| 通風箱 | 踹凹、跳上、打滑 |
| 地面 | 滑步、擦痕、塵土 |

**沒有錨點的打鬥會飄。** 觀眾不知道誰在哪，也不知道力量從哪來。

---

## 7. 提示詞骨架（7.5 秒單鏡）

```text
integrated_multimodal_description: [Shot 1] <風格錨定>. <場景 + 錨點>. <兩人的位置與外觀>. <鏡頭第一個動作：從哪裡開始、往哪去>. <交換 1：命中 → 2 幀衝擊幀 → 拖影 → 回彈>. <交換 2：動作鏈接續>. <交換 3：動作鏈接續>. Every motion flows directly into the next strike, and both fighters stay sharp and anatomically correct throughout.

overall_soundscape: <環境底噪>. <三種物理音：拳套、鞋底、飾品>. <撞擊音>.

non_diegetic_music: <高速節拍>. <撞擊瞬間抽空>. <回來>.
```

**字數**：單鏡 7.5 秒約 400–520 字。超過就會壓縮動作。

---

## 8. 實驗建議（未驗證，需實測）

| 實驗 | 對照 | 想驗證什麼 |
|---|---|---|
| E1 | 單鏡到底 vs 加 0.3 秒細節插切 | 插切是加分還是破壞連續感 |
| E2 | 四拍 vs 六拍 | 7.5 秒內能放幾次可辨識命中 |
| E3 | 深度錯位 vs 並排 | 空間感 vs 兩人可辨性 |
| E4 | 鏡頭參與 vs 固定側拍 | 運動量 vs 可看性 |

**驗收門檻（比一般動作更嚴）**：最長低潮 ≤0.5 秒、末 2s÷中段 ≥70%、無「靜止對稱」、7.5 秒內 ≥3 次可辨識命中。

---

## 9. 常見失敗

| 症狀 | 原因 | 修法 |
|---|---|---|
| 打成一團看不清 | 兩人同深度、動作太密 | 加深度錯位；把交換數從 4 降到 3 |
| 每擊之間有停頓 | 用了六拍的凍結 | 刪掉 `near-freeze`，改成拖影 |
| 像在跳舞 | 沒有衝擊幀、沒有回彈 | 每擊都要有 `for two frames` + `smears` + `already lunging again` |
| 動作各自獨立 | 寫成清單 | 改用 `turns into` / `rides` / `drives out of` |
| 空間感消失 | 沒有錨點 | 給 2–3 個可互動物件 |
