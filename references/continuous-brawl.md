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

## 7. 提示詞骨架（7.5 秒單鏡）```text
integrated_multimodal_description: [Shot 1] <風格錨定>. <場景 + 錨點>. <兩人的位置與外觀>. <鏡頭第一個動作：從哪裡開始、往哪去>. <交換 1：命中 → 2 幀衝擊幀 → 拖影 → 回彈>. <交換 2：動作鏈接續>. <交換 3：動作鏈接續>. Every motion flows directly into the next strike, and both fighters stay sharp and anatomically correct throughout.

overall_soundscape: <環境底噪>. <三種物理音：拳套、鞋底、飾品>. <撞擊音>.

non_diegetic_music: <高速節拍>. <撞擊瞬間抽空>. <回來>.
```

**字數**：單鏡 7.5 秒約 400–520 字。超過就會壓縮動作。

---

## 8. 快切模式（實測結論）

如果參考片是**剪接驅動**（不是長鏡頭），改用快切而不是連續長鏡。判斷方法：數原片的剪點。

實測案例：30 秒動畫 40 個剪點（平均 0.75 秒一刀），前 7.5 秒 14 刀。

### 六條硬規則

| 規則 | 數據依據 |
|---|---|
| **7.5 秒最多 6 刀** | 寫 7 刀落地 5 刀；寫 8 刀反而落地 10 刀（模型自己在鏡頭內亂切） |
| **時間碼往前寫 0.2 秒** | 設 1.7s，實際剪在 1.875s（系統性延遲 0.15–0.3s） |
| **最後一鏡不要寫寬景 reset** | `wide shot ... both fighters reset and lunge` → 生成靜止對峙，尾端掉到 57% |
| **兩角色同框要防複製** | 動漫風寬景出現 3–4 個人影（應為 2 個）；寫 `exactly two figures` 有效 |
| **主語永遠是主角** | 寫「粉髮選手出拳」→ 2.5–5.5 秒全是對手的特寫，主角消失 |
| **但兩個角色都要有穩定標籤** | 只把對手改成「她／the other」→ 兩人融合、同臉、甚至打自己 |
| **特寫必須有內部運動** | 極特寫本身可動元素少，模型會讓它靜止 2 秒 |

### 標籤規則（雙人場景最容易犯的錯）

**鏡頭焦點是主角，但每個角色都必須有穩定、可視、互斥的標籤。標籤靠髮色／服裝，不靠代名詞。**

實測對照（同一個 7.5 秒打鬥）：

| 版本 | 對手標籤數 | `she/her` 數 | 結果 |
|---|---:|---:|---|
| A | 3 | 7 | 兩人清楚可辨 |
| A3 | **0** | **26** | 兩人融合、同臉、打自己 |

**兩個女性角色都叫「she／her」，模型只能猜。猜不出來時，最省事的解法就是把兩人畫成同一個人。**

| ❌ 錯（代名詞 / 懸空所有格） | ✅ 對（標籤 + 明確歸屬） |
|---|---|
| `She catches her uppercut on her forearm.` | `The black-haired fighter catches the pink-haired fighter's uppercut on a raised forearm.` |
| `the other guard` | `the pink-haired fighter's guard` |
| `letting the forearm drive into her own chin` | `the block jolts the black-haired fighter's head back` |

**`her own chin` 這種寫法會被字面執行成「她打自己」。** 身體部位一定要有明確歸屬。

標籤優先序（越好認越前面）：
1. **髮色**：`the black-haired fighter` / `the pink-haired fighter`（最強）
2. **手部**：`the black-gloved fighter` / `the bare-knuckled fighter`
3. **下身**：`the orange-pants fighter` / `the black-shorts fighter`

**主角的鏡頭份額靠景別與剪輯**（主角特寫 3 刀、對手最多 1 刀），不是靠刪掉對手的名字。

### 特寫的內部運動

```text
❌ an extreme close-up of her glove against the fence
✅ an extreme close-up of her glove as the fingers flex and the strap pulls tight against the fence
```

特寫不給內部運動，就會變成兩秒的靜止畫面（實測：6.0–7.5 秒完全不動）。

### 角色元素混搭

兩個角色的服裝都寫得很詳細時，模型會把特徵交叉組合（實測：粉髮對手穿上了主角的綠條紋上衣）。

**解法：每一刀都點名主角的識別特徵**——`her black gloves`, `her green striped top`, `her orange graffiti pants`。讓它無法混淆。

### 剪點與動作的關係（最重要的一條）

**加剪點不會增加動作。**

實測：10 刀的版本（A5）全程運動 12.75，是三版裡最低的。因為每一刀都很短，刀內幾乎沒有動作——模型把「0.5 秒」理解成「一張圖停 0.5 秒」。

**動作必須寫在每一刀裡面。** 剪點只決定「什麼時候換畫面」，不決定「畫面裡有沒有事發生」。

### 細節插切 = 身份錨定（不只是節奏）

| | 角色一致性 |
|---|---|
| 有插切（每 2–3 刀插角色特寫） | 拳套、髮色、褲子紋樣全部保持 |
| 無插切 | 黑拳套變白、粉髮變紫 |

**每次特寫都在重新宣告角色設計。** 插切不只看起來有節奏，它同時是防止身份漂移的手段。

### 快切骨架

```text
[Shot 1] <風格錨定>. <首幀延續的動作>. for two frames <衝擊幀>. <拖影>.
[Shot 2] At 00:00.700, the camera cuts to an extreme close-up: <角色特徵物件>.
[Shot 3] At 00:01.500, the camera cuts to <景別>. <下一個交換>.
[Shot 4] At 00:02.300, the camera cuts to a half-second insert: <眼睛／飾品／鞋底>.
[Shot 5] At 00:03.100, ...
[Shot 6] At 00:03.900, ...
[Shot 7] At 00:05.000, the camera cuts to a tight close shot as she <動作中段>. The frame holds on the impact through the final frame.
```

**收尾用特寫或動作中段，不要用寬景。** 寬景在 H3 等於「停下來對看」。

---

## 9. 實驗紀錄（已驗證）

| 實驗 | 結果 |
|---|---|
| 快切 vs 單鏡（同角色、同首幀） | 快切版前 5 秒最接近原片；但尾端崩（57%）。單鏡版尾端穩（90%）但角色漂移 |
| 細節插切 | 有效。A 版插切後角色一致；B 版無插切，拳套變白、髮色變紫 |
| 8 刀 vs 實際 | 7 刀只落地 5 刀，且全部延遲 0.15–0.3s |
| 寬景兩人 | 出現 3–4 個人影 |

**結論：快切負責「風格」，特寫負責「收尾與身份」。兩者都要，但不能用寬景收尾。**

### 收尾定格（實測五版）

H3 在最後 1–2 秒會自動減速，五種寫法全部收斂到定格：

| 收尾寫法 | 末段絕對運動 |
|---|---:|
| 中景 + 全身往前走 | **15.45** |
| 寬景 + reset 再衝 | 11.49 |
| 貼身特寫 + 兩具身體鎖住 | 11.00 |
| 極特寫 + 手指收緊 | **8.70** |

**解法：生成時多要 1.5 秒，剪輯時切掉尾段。** 想留 6 秒就生成 7.5 秒。

**收尾用中景**，不要寬景（會變對峙）、不要極特寫（會變靜止）。

---

## 9. 常見失敗

| 症狀 | 原因 | 修法 |
|---|---|---|
| 打成一團看不清 | 兩人同深度、動作太密 | 加深度錯位；把交換數從 4 降到 3 |
| 每擊之間有停頓 | 用了六拍的凍結 | 刪掉 `near-freeze`，改成拖影 |
| 像在跳舞 | 沒有衝擊幀、沒有回彈 | 每擊都要有 `for two frames` + `smears` + `already lunging again` |
| 動作各自獨立 | 寫成清單 | 改用 `turns into` / `rides` / `drives out of` |
| 空間感消失 | 沒有錨點 | 給 2–3 個可互動物件 |
