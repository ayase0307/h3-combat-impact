---
name: h3-combat-impact
description: This skill should be used when writing, revising, or debugging MiniMax H3 / Hailuo (海螺) video prompts for action, combat, wuxia/xianxia, VFX-heavy or impact-driven shots — especially when the user asks for 打擊感 / 力度 / 拳拳到肉, 打鬥特效, 招式編排 / 動作設計 / 打鬥太單調沒感覺, 衝擊幀 / impact frame, 震屏 / 鏡頭震動, 力場 / 空氣扭曲 / 熱浪 / 衝擊波, 法術爆炸, 打鬥運鏡節奏, or wants to break down and recreate a fight or explosion reference video in H3 format. It provides the official H3 prompt schema, a six-beat impact design method, three structural principles (exchange / compression / consequence), a named-move library, a four-channel force-field model, impact-frame and screen-shake timings, bilingual camera and VFX vocabulary, fill-in prompt templates, and a post-generation QA checklist.
agent_created: true
---

# H3 打鬥與打擊感提示詞

把「打得好看」拆成可寫、可複製、可驗收的提示詞結構。適用於 MiniMax H3（Hailuo 海螺）的 T2VA / I2VA / FL2VA / L2VA / Ref2VA 全模式。

## 先決定：直接做，還是給選項

| 使用者的狀態 | 做法 |
|---|---|
| 已明確指定（有角色、有場景、有參考片、有具體描述） | **直接執行，不要問** |
| 給了參考圖但沒說要做什麼 | 依素材給 3–5 個情境選項，**先給建議再給選項** |
| 什麼都沒有 | 給情境選項，並用 **T2VA** 文生影片（角色寫進提示詞） |

六個已實測的情境：**A 連續對轟**、B 單鏡纏鬥、C 電影級大招、D 氣場覺醒、E 純氛圍、F 首幀延續。

完整決策樹、素材對應表、話術模板見 `references/guided-mode.md`。

**引導模式只用在「使用者不知道要什麼」的時候，不是每次都要走一遍。**

## 何時使用

- 撰寫或修改 H3 的動作、打鬥、仙俠、武俠、超能力、機甲、怪獸類提示詞。
- 使用者抱怨「動作軟」、「特效華麗但沒力量」、「像兩個木頭人」、「鏡頭亂轉」。
- 需要把參考影片（真人或 AI）拆解後用 H3 重現。
- 需要統一的打鬥分鏡節奏表、特效詞彙或驗收標準。

## 模式選擇：角色圖是「參考」還是「首幀」

| 你想要 | 模式 | 角色圖的角色 |
|---|---|---|
| 只要「長這個樣子」，人在畫面哪裡都行 | **Ref2VA** | `<Subject N>` 參考，**比例自由** |
| 從那張圖的構圖展開 | I2VA | `<Picture N>` 首幀，**比例被綁死** |

**只有當畫面比例必須與圖一致時才用 I2VA。** 想拍 16:9 就用 Ref2VA——用 I2VA 會把 9:16 的圖裁掉手腳或拉寬，改用 T2VA 則直接失去角色。

Ref2VA 的三個前提：
1. 提醒詞用六欄位（`subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music`）
2. 每個角色在 `subject_definitions` 裡定義成 `<Subject N>`，全篇沿用同一編號
3. `retention_analysis` 標 `fully_preserved`，並列出必須保留的特徵

**但這三點只是骨架，不足以保真。** 要讓生成結果「看起來就是參考圖裡那個人」，
必須照 `references/ref-identity-lock.md` 的 **9 類特徵清單**逐項列舉
（臉型／眼睛／疤／髮型／配件含數量／服裝結構／顏色綁衣物／剪影比例／武器型號＋相對長度），
外加 **3–4 個畫風材質錨**（`detailed_description` 首句與 `[Shot 1]` 首句兩處一致）。

> ⚠️ **畫風錨定不可膨脹**：超過 3 個形容詞會讓模型把參考圖當成「要重現的內容」，
> 整段變成靜止圖（實測運動量 0.49）。**保真與活力是互相拉扯的**，錨 3 個就夠。

## 節奏模式：三選一

| 模式 | 節奏單位 | 什麼時候用 | 規則 |
|---|---|---|---|
| **六拍** | 一次交手 | 單次重擊、有蓄力與收勢 | `references/impact-design.md` |
| **連續對轟** | 一次交換（0.8–1.5s） | 近身纏鬥、壓著打 | `references/continuous-brawl.md` |
| **ULTRA_SPEED** | **一個鏡頭（0.4–0.8s）** | **無人機高速跟拍、不間斷** | `references/ultra-speed.md` |

**ULTRA_SPEED** 是使用者明確要的模式：8 秒 10–14 鏡、每鏡 0.4–0.8 秒、
**不追求「攻→擋→反」的交換結構**，追求的是「鏡頭位置一直在換、動作一直在跑、周圍一直在壞」。
每鏡四件套：**鏡位 + 動作 + 運鏡 + 特效/周圍連動**。

**鏡頭密度統一表（優先級高於其他所有檔案）：**

| 模式 | 8 秒的鏡數 | 中位鏡長 | 短鏡占比 |
|---|---|---|---|
| 六拍 | 4–5 鏡 | 1.2–2.0s | ≤20% |
| 連續對轟 | 9–10 鏡 | 0.6–0.9s | ≥30% |
| **ULTRA_SPEED** | **10–14 鏡** | **0.4–0.8s** | **≥30%** |

## 硬約束：H3 提示詞規格（先記住，違反會直接掉品質）

| 項目 | 規格 |
|---|---|
| 單次時長 | 4–15 秒（超過 15 秒必須切段，用末幀接續） |
| 幀率 / 音訊 | 24 fps、32 kHz 原生立體聲 |
| 解析度 | 768p 基礎，2K 需 Regenerate |
| 比例 | 21:9 / 16:9 / 4:3 / 1:1 / 3:4 / 9:16 |
| 模式 | T2VA、I2VA、FL2VA、L2VA、Ref2VA |
| 對白語言 | 11 種，含中文：`<d>[Chinese] 台詞</d>` |

**輸出只有三個欄位**（T2VA / I2VA / FL2VA / L2VA）：

```text
integrated_multimodal_description: [Shot 1] <風格錨定> + <主體> + <動作> + <運鏡> + <特效> + <聲畫同步>
overall_soundscape: <環境音 + 物理音 + 非語言人聲，1–4 句>
non_diegetic_music: <只有觀眾聽得到的配樂，1–3 句，只寫樂器/速度/節奏/動態>
```

Ref2VA 另用六欄位：`subject_definitions` / `summary` / `retention_analysis` / `detailed_description` / `overall_soundscape` / `non_diegetic_music`。

**六條不可違反的寫作規則：**

1. `[Shot 1]` **不加時間碼**；後續鏡頭一律 `[Shot 2] At 00:03.500, the camera cuts to ...`，時間嚴格遞增且落在時長內。
2. 運鏡一律寫成**自然語句**：動作類型 + 幅度 + 速度（`the camera pushes in with large amplitude at fast speed`），不可在句尾堆標籤。
3. `[Shot 1]` 開頭必須有**風格錨定**（`3D CG, cinematic`、`live-action`、`2D-animated` 等）。
4. 主體動作與鏡頭運動**分開寫**，避免運動疊加糊成一團。
5. 對白只把語言標籤與台詞放進 `<d>`，說話者身分、語氣、動作放在外面。
6. **官方三欄位沒有負面提示欄**。所有「不要」都改寫成正面約束句，放在該鏡頭結尾（見下方「負面約束」）。

## 輸出契約：產出必須能直接貼進模型

**本 skill 的最終交付物是一個可直接貼上的提示詞，不是設計說明。**

### 交付形態

只給一個 code block，區塊內只有提示詞本體：

````text
```text
integrated_multimodal_description: [Shot 1] 3D CG, cinematic, ...
overall_soundscape: ...
non_diegetic_music: ...
```
````

區塊內**禁止**：標題、項目符號、粗體、編號清單、中文註解、分隔線。中文說明寫在 block 外面。

### 四個最常寫錯的語法（實測 7/7 全錯）

| 錯誤 | 正確 |
|---|---|
| 欄位名換行後才寫內容 | `integrated_multimodal_description: [Shot 1] ...`（**同一行**） |
| 標註 I2VA 卻沒寫對齊句 | 首行必須是 `For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.` |
| `[Shot 1]` 加了時間碼 | `[Shot 1]` 只有風格錨定與內容 |
| 用 `no` / `not` / `without` 表達禁止 | 改寫成正面動作 |

### 交付前必須跑檢查

```bash
python scripts/validate_prompt.py prompt.txt --duration 8
```

會檢查：欄位齊全與順序、對齊句、`[Shot 1]` 時間碼、時間碼遞增與否、末鏡長度 ≤30%、否定詞、Markdown 殘留、`<d>` 配對、標籤定義、字數預算。

**FAIL 必須修掉才能交付。**

完整格式規範（含對白、畫外音、`<scenetrans>`、畫面文字、Ref2VA 六欄位）見 `references/output-format.md`。

## 核心方法：六拍打擊結構（HIT BEAT）

### 先選節奏模式（三選一，不可混用）

| 模式 | 適用 | 節奏單位 | 關鍵差異 |
|---|---|---|---|
| **六拍**（預設） | 對決、單次交手、有蓄力與收勢 | 一次交手 | 有 4–6 幀凍結 |
| **連續對轟** | 近身纏鬥、誰都不退、壓著打 | 一次交換（0.8–1.5 秒） | 只有 2 幀衝擊幀 + 拖影，**沒有凍結** |
| **ULTRA_SPEED** | **無人機高速跟拍、不間斷** | **一個鏡頭（0.4–0.8 秒）** | **不追求交換結構**，靠換機位與連續連動 |

判斷訊號：
- 「不停」「連續」「沒有喘息」「壓著打」→ 用連續對轟（四拍）
- **「超高速」「一直打」「喘不過氣」「運鏡一直在動」→ ULTRA_SPEED**

六拍需要停頓，四拍需要不停，ULTRA_SPEED 需要每鏡都有光。**混用會兩邊都不成立。**

連續對轟的四拍公式、動作鏈句型、深度錯位、鏡頭參與、細節插切見 `references/continuous-brawl.md`。
ULTRA_SPEED 的四件套、每鏡光影事件、周圍連動清單見 `references/ultra-speed.md`。

### 衝擊幀做不到時：分開生成後製

**實測：在高速動作的同一段提示詞裡寫 `for two frames`，模型會給 23 幀（958 ms），
而且角色會整個消失。** 這是「風格跳轉」事件，模型把它當成一個黑白風格的鏡頭。

解法是拆成三個素材再合成：

```
素材 A：主片        → 只有高速動作與運鏡，完全不寫衝擊幀
素材 B：衝擊幀片    → 單獨生成，只要那一兩幀
素材 C：放射線 PNG  → 從素材 B 抽出來的那一幀
合成：   A + C 疊在指定時間點，hold 0.083s = 2 幀 = 67 ms
```

完整流程與驗收見 `references/impact-frame-post.md`。

> **後製路徑的價值：把不可控的東西變成可裁切。**
> 素材 B 生成 4 秒都無所謂，最後只會取用 2 幀。

### 六拍

每一個「命中」都拆成六拍。這是打擊感的骨架，缺拍就會軟。

| 拍 | 名稱 | 佔比 | 畫面該有什麼 | 提示詞關鍵詞 |
|---|---|---|---|---|
| 1 | 蓄 Anticipation | 35% | 反向預備、重心下沉、布料/肌肉繃緊、鏡頭微停或反向緩推 | `draws back`, `weight sinks into the rear leg`, `the camera holds a static shot`, `the blade trembles under tension` |
| 2 | 觸 Contact | 5% | **衝擊幀**：1–2 幀爆白/爆黑/單色剪影、徑向速度線、畫面微變形 | `for two frames the entire frame blows out to pure white` |
| 3 | 停 Hit Stop | 15% | 時間近乎凍結（hitstop 0.05–0.15s），塵埃與火花懸浮 | `the action decelerates to a near-freeze for two frames` |
| 4 | 洩 Release | 25% | **力場四通道**：衝擊波、碎片、塵環、水花、氣浪、光影聯動 | `a ring of shockwave dust bursts outward`, `the whole scene's lighting shifts in step` |
| 5 | 退 Reaction | 15% | 受擊者被打飛/滑退、衣物頭髮延遲甩動、**震屏衰減** | `is hurled backward`, `the shake decays within a third of a second` |
| 6 | 收 Recovery | 5% | 回到 ready pose、殘留粒子飄落、鏡頭回穩 | `settles into a low guard`, `embers drift down`, `the camera steadies` |

**三條比例鐵律：**

- 蓄 ≥ 觸的 5 倍長度。沒有蓄力，力量無從比較。
- 停（Hit Stop）是「重量」的唯一來源。寧可多 0.1 秒，不要沒有。
- 一擊只給一個視覺高潮。同時爆閃 + 大爆炸 + 慢動作 = 全部互相抵銷。

**爆炸類鏡頭另有一套結構**：爆發點（衝擊幀）→ 力量輸出（力場四通道）→ 體感（震屏衰減）→ 餘韻。見 `references/impact-frame-and-shake.md`。

## 核心方法二：力場四通道（特效為什麼不像貼圖）

> **光效只是顏色，力場才是空氣。**

AI 生成爆炸的預設行為是給一顆發光火球，但不會給「世界被影響」的證據。診斷三症狀：**周圍物體一動不動 / 空氣沒有波瀾 / 光影完全脫節**。

把「力場」拆成四個可獨立增減的通道：

```
場源 → 傳播（形狀+速度+方向）
        ├─ ① 光    全域亮度、色溫、陰影、暗部、反射
        ├─ ② 空氣  折射、熱浪、壓縮、色散、撕裂
        ├─ ③ 物質  布料、髮絲、玻璃、塵土、碎石
        └─ ④ 粒子  體積粒子、火星、煙塵、熱霧
```

**一次最多開三個通道。優先順序：空氣 > 物質 > 光 > 粒子。**

最便宜也最有效的力場證明：**主角的衣襬或頭髮被推。** 一句 `wind pressure flattens the silk against her body` 勝過十句 `epic explosion`。

完整句庫與三種場型（一次性／持續性／附著型）見 `references/force-field.md`。

## 核心方法三：打鬥的三條設計原則（比提示詞更重要）

提示詞寫得再好，設計錯了就是「優雅但沒感覺」。三個實測有效的結構原則：

### ① 必須有交換

**讓弱勢方至少打中一次。** 單向的攻防是「閃避示範」，不是戲。

- 失敗案例：7 秒裡主角 0 次命中，只有閃避與格擋 → 觀眾無感
- 成功做法：先被壓制 4 秒，第 5 秒逆轉一次 → 有勝負未卜的緊張

### ② 把空間壓小

**能貼身就不要分開。** 距離是打鬥的敵人。

| 空間 | 效果 |
|---|---|
| 大廳中央、四周空曠 | 畫面散、無壓迫、容易擺姿勢 |
| 柱廊窄道、台階、貼牆 | 無處可退、視線有落點、動作被迫連續 |

附帶好處：貼身時模型沒有空間擺姿勢，「優雅角色擺拍先驗」自動失效。

### ③ 給一個「後果」

撞斷欄杆、摔下台階、面具裂、刀脫手——**觀眾需要看見代價**。

沒有後果的打鬥 = 兩個人在跳舞。後果不必是血，但必須是不可逆的破壞。

> 這三條的優先級高於六拍與力場。先確定「有交換、有壓迫、有後果」，再談節拍與特效。

## 核心方法四：招式必須具名

**模型的預設行為是生成「平均化的打鬥」——揮、擋、退。它不會自己發明具體動作。**

寫 `he slashes at her` 只會得到最通用的版本。寫 `he flips his wrist and rips the blade upward from below in a reverse cut, the edge drawing a crescent of light` 才會得到「反手撩刀」。

**抽象動詞 = 平均化動作 = 單調。**

每一招必須包含四層：

| 層 | 內容 | 缺了會怎樣 |
|---|---|---|
| 1 位移 | 從哪到哪 | 沒有空間感 |
| 2 身體機制 | 哪個部位發力 | 沒有重量 |
| 3 物理結果 | 塵土、氣流、裂紋、火花 | 沒有打擊感 |
| 4 戰術目的 | 破站勢、破防、繞後 | 沒有方向 |

第 4 層最常被忽略，卻決定動作「有沒有意義」。

**串接規則**：三招一組 ≈ 1.2–1.5 秒，每招 0.4–0.5 秒，且必須涵蓋三個不同的空間層次（上／中／下）。三招都在同一高度 = 單調。

完整招式庫（16 招 + 4 組串接配方 + 中英翻譯規則）見 `references/move-library.md`。

### 開局：0.5 秒內必須有第一次接觸

**不要用「站著對視」開場。** 對峙是打鬥裡最無聊的部分，而模型的預設開場就是對峙。

```text
❌ 0.0–1.5s  兩人對視、風吹、衣襬飄動
✅ 0.0–0.5s  第一刀已經劈下來，或第一招已經衝出去
```

要交代距離與氣氛，用**動作中**的畫面交代（他走進來時已經在拔刀），不要用靜止的對視。

**最有效的做法是把它寫成獨立一句，放在 `[Shot 1]` 裡：**

```text
First contact occurs within the opening half-second.
```

實測：寫了這句的版本開場運動量 20.44，沒寫的只有 3.24（相差 6 倍）。

## 核心方法四之二：表情與表演（臉不能是死的）

**運鏡再炫、特效再華麗，只要角色的臉是死的，整段就是在看兩尊雕像打架。**

### 診斷：三種寫法一定失敗

| ❌ 寫法 | 為什麼無效 |
|---|---|
| `her amber irises narrow` | 這是**眼睛形狀**，不是臉部肌肉 |
| `pale gray eyes lit from below` | 這是**打光**，燈光打在死人臉上還是死人臉 |
| `a determined expression` | 這是**形容詞**，模型不知道對應哪塊肌肉 |

**三種都只碰到「眼睛」和「光」，沒有碰到「肌肉」。**

### 原理：表情是肌肉，不是形容詞

| ❌ 形容詞 | ✅ 肌肉動作 |
|---|---|
| `a determined expression` | `her jaw muscles bunch and her teeth clench` |
| `fierce eyes` | `her brows slam down into a hard knot above her nose` |
| `she looks shocked` | `her eyes fly wide and her lips part on a sharp intake of breath` |

**規則：每一句表情描述都必須有「可以動的部位 ＋ 一個動作」。**

可用部位：眉／上眼瞼／下眼瞼與眼周／鼻翼／下顎與咀嚼肌／齒／唇／頸與喉／太陽穴／汗淚／呼吸。

### 四階段表情（不是一個表情用到底）

| 階段 | 情緒 | 寫法 |
|---|---|---|
| 交手前 | 緊繃 | `her jaw locks and her brows pull together` |
| 吃到重擊 | 痛、失重 | `her eyes fly wide and her mouth wrenches open on a gasp` |
| 反擊 | 狠、決斷 | `her brows slam down and her lips peel back off clenched teeth` |
| 收尾 | 喘息 | `her chest heaves, a bead of sweat cutting through the dust on her cheek` |

### 兩人要有對比：收 vs 放

- **佔上風**：表情**收**（`her jaw locks, her mouth a flat line`）
- **處於下風**：表情**放**（`her brows climb, her lips part, a bead of sweat at her temple`）

**不用寫誰強誰弱，觀眾看臉就知道。**

### 三個不可省的生理反應

再快的打鬥人也會喘。沒有呼吸＝沒有力氣消耗＝看起來很輕。

- **呼吸**：`her chest heaves`（每 4–6 秒至少一次）
- **汗**：`sweat tracks down her temple`（中後段開始）
- **吞嚥**：`her throat works on a swallow`

完整部位清單、綁定寫法、失敗對照見 `references/facial-performance.md`。
## 核心方法五：奇觀構圖（避免「遊戲技能展示」感）

大招展示最容易掉進的坑：**背景巨型奇觀 + 主體居中 + 左右對稱 = 靜止的遊戲技能展示**。

這個構圖即使畫質升到 4K、加了次表面散射與景深，**依然是靜止的**。模板感不是畫質問題，是構圖問題。

實測：兩支「電影級重製版」的高潮段對稱殘差比全片平均低 20% 與 45%，同時出現 1.0 秒的運動死區——**最貴的兩秒，畫面最不動**。

### 三條規則

| 規則 | 錯 | 對 |
|---|---|---|
| **奇觀不放正後方** | `a lightning crown splits the darkness directly behind her` | `A branch of lightning tears down through the vault on her left, throwing her shadow across the floor to the right.` |
| **奇觀被她掃出來** | `The crown opens behind her.` | `She drags the filament sideways and the vault splits along its path.` |
| **高潮要有位移** | 她站在奇觀前面 | `She steps into the collapsing crown — one step, then a second — and the arcs bend around her as she passes through.` |

第三條最有效：**走進奇觀**同時解決主體運動、構圖不對稱（她不在中心）、尺度對照（走過去才知道多大）三件事。

### 判斷訊號

生成後跑 `measure_motion.py --symmetry`，若出現 `靜止對稱` 旗標，而且落在最高潮的鏡頭 → **改構圖，不要改光影**。

## 三層能量語言（特效不亂加）

打鬥特效不是裝飾，是「力的可視化」。每一擊最多同時存在三層，且必須分工：

1. **內層｜主體能量**：氣的顏色、形狀、附著位置（`teal spirit flame licking along the blade`）。
2. **中層｜武器/接觸能量**：撞擊點的產物（`a white-hot spark bloom at the point of contact`）。
3. **外層｜環境反應**：場景被推動的證據（`lanterns swing`, `roof tiles rattle loose`, `rain is pushed into a radial sheet`）。

**環境層是最常被忽略、卻最能救打擊感的一層。** 沒有環境反應，觀眾會覺得特效是貼上去的。

## 工作流程

1. **定節奏表**：先寫時間碼 / 景別 / 拍數，不寫形容詞。一個 7 秒片段放 4–5 個鏡頭。
2. **配能量色**：全片只允許一組互補色（例：青綠 vs 琥珀橙），並指定誰用哪一色。
3. **套模板**：從 `references/prompt-templates.md` 取 T2VA / FL2VA / Ref2VA 模板填空。
4. **寫三欄位**：`integrated_multimodal_description` 逐鏡頭寫；`overall_soundscape` 寫物理音；`non_diegetic_music` 只寫樂器與節奏。
5. **自檢**：跑 `references/qa-checklist.md`，逐項確認六拍、力場四通道、運鏡語法、時長預算。
6. **格式檢查**：跑 `scripts/validate_prompt.py`，FAIL 全修掉。
7. **交付**：只輸出一個 code block，區塊內不得有註解。
8. **接續生成**：超過 15 秒時，取上一段末幀當下一段 `<Picture 1>`，用 FL2VA 續接，並在提示詞第一行寫對齊句。

## 負面約束的正確寫法

官方沒有 negative prompt 欄位，把「不要」翻譯成「保持」：

| 想避免 | 寫成 |
|---|---|
| 臉部變形 | `her face stays sharp and anatomically correct throughout the motion` |
| 武器彎曲/融化 | `the blade stays perfectly straight and rigid` |
| 肢體穿模 | `the two bodies never intersect; contact happens only at the blade` |
| 鏡頭亂跳 | `the camera moves in one continuous take with no jump cuts` |
| 特效閃爍 | `the teal flame burns continuously without flicker` |
| 動作糊掉 | `each pose is clearly readable, with distinct silhouettes` |

## 可量測的四條硬規則（實測驗證）

這四條不是感覺，是可以檢查的。實測七版生成紀錄後補上。

### ① 時長必須與時間碼一致

**時間碼寫到幾秒，生成時長就要設幾秒。** 差 2 秒，最後一鏡會被拉長一倍，模型只能填「站著、粒子飄」。

| 症狀 | 原因 |
|---|---|
| 尾端停滯、人物站定不動 | 生成 10 秒但時間碼只寫到 8 秒 |

**檢查**：`最後一個剪點 + 最後一鏡設計長度 = 總時長`。末鏡不要超過總長的 30%。

### ② 動態結尾要分「主體」與「特效」

**畫面在動 ≠ 主體在動。** 銀河旋轉、光帶流動會讓運動量翻倍，但角色可能站著不動四秒。

達標的定義是**主體有位移或姿勢變化**：

```text
❌ 星系繼續旋轉，光帶繼續流動（特效在動，人沒動）
✅ She advances two steps into the storm, her heels cracking the marble, stole whipping behind her.
```

### ③ 字數預算

| 時長 | 上限 | 超過就砍 |
|---|---|---|
| 4–8 秒（不論幾鏡） | 520 字 | 形容詞、同義疊加 |
| 9–15 秒 | 700 字 | 形容詞、同義疊加 |

**不要砍動作。** 砍掉一個動作，比砍掉十個形容詞損失更大。

實測：七版從 525 字膨脹到 1022 字（+95%），最長的那版反而最好——所以長度不是絕對。真正的風險是**超過 520 字後，寫在最後的約束會失效**。重要約束一律往前放，不要放在最後一段。

### ④ 人物佔比

主體要在畫面裡夠大，特效才不會吃掉它。明寫一句：

```text
She remains the dominant subject, occupying approximately 65–80% of the frame height.
```

沒寫這句的版本，主角會被巨大的特效環、星門、法陣擠成畫面中央的一個小點。

### ⑤ 收尾定格：多要 1.5 秒，剪輯時切掉

**H3 在片段最後 1–2 秒會自動減速。** 實測五版、四種收尾寫法（寬景 reset／貼身特寫／極特寫／中景前進）、三種景別，**全部收斂到同一個結果：定格**。

末段絕對運動：中景 15.45 ＞ 寬景 11.49 ＞ 貼身特寫 11.00 ＞ 極特寫 8.70。

這不是提示詞寫得不夠。**解法是剪輯，不是改字。**

| 想要的長度 | 生成時長 | 取用 |
|---|---|---|
| 5 秒 | 6.5 秒 | 0–5.0 |
| 6 秒 | 7.5 秒 | 0–6.0 |
| 8 秒 | 9.5 秒 | 0–8.0 |

多要的 1.5 秒是**安全邊界**，不是內容。切在「動作剛完成、下一擊還沒出」的瞬間，張力最大。

**收尾景別選中景**：全身可見（有位移空間）＋主體夠大（不會變小點）＋有環境可參照。極特寫最差，可動元素太少。

---

## 量測工具

`scripts/measure_motion.py` 對任何生成好的 mp4 輸出運動曲線與旗標：

```bash
python scripts/measure_motion.py --dir ./outputs
python scripts/measure_motion.py --dir ./outputs --symmetry   # 額外偵測「靜止對稱」
python scripts/measure_motion.py ref.mp4 --fps24              # 折回 24fps 等效值（跨幀率比較）
```

輸出欄位：全程／開場 0.8s／中段／末 2s／末÷中／最長低潮／峰值格，並自動標記 `開場過靜`、`尾端停滯`、`低潮 Xs`、`節拍過少`。

**`--fps24` 會先偵測實際幀率再折回 24fps 等效值**，並標記 `pulldown(...)`（幀間隔交替的偽幀率素材）。跨幀率比較時一定要用這個模式。

**判讀門檻：**

| 指標 | 合格 | 說明 |
|---|---|---|
| 開場 0.8s | ≥ 中段的 50% | 低於此 = 開場過靜 |
| 末 2s ÷ 中段 | ≥ 60% | 低於此 = 尾端停滯 |
| 最長低潮 | ≤ 0.8s | 超過就是無效等待 |
| 峰值格 | ≥ 4 | 太少 = 動作節拍不足 |
| 靜止對稱（`--symmetry`） | 不出現在高潮鏡頭 | 出現 = 構圖正在變成技能展示 |

**限制**：這是「畫面變化」不是「主體運動」，特效大幅運動會拉高分數。分數達標仍要目視確認主體有動。

### 量測參考片之前的兩個必查（會讓你得出錯的結論）

**① 封裝宣告的幀率可能是假的。**

一支標示 `r_frame_rate=60` 的參考片，實測只有 723 幀 / 30.14s = **24.06fps**——幀間隔嚴格在 0.050s 與 0.0333s 之間交替，是 **24fps 母版的 2:3 pulldown**。

**H3 是 24fps，所以這類素材「幀數 1:1 對應」，不需要任何 60→24 換算。**

```bash
ffprobe -v error -select_streams v:0 -show_entries "packet=pts_time" -of csv=p=0 clip.mp4
```

看相鄰時間差有幾種值：只有一種 → 固定幀率；兩種且交錯 → pulldown。

> 逐幀分析時**必須加 `-fps_mode passthrough`**，否則 ffmpeg 會重抽成 CFR60，差異中位數歸零、自適應門檻失效——實測炸出 618 個假切點。

**② 跨片比運動量必須先統一幀率。**

`measure_motion.py` 取的是「每幀平均差異」，同樣的實際運動：24fps = 1.00、30fps = **0.80**、60fps = **0.50**。**30fps 素材的運動分數系統性偏低約 20%。**

真實案例：兩支參考片原生分數 16.51 vs 14.06 看似前者活躍 17%；**正規化到 24fps 後是 15.94 vs 16.06，幾乎相同**。

| 指標 | 幀率敏感度 |
|---|---|
| `overall` / `opening` / `mid` / `ending` | 偏低（30fps −20%、60fps −50%） |
| `peaks`（峰值格） | 偏高（30fps +25%，幀數多） |
| 靜止對稱 | 相對判定，仍有效 |

**引用絕對值時乘 1.25 折回 24fps；跨片比較前先統一幀率。**

> `measure_motion.py --fps24` 會自動完成這件事（先偵測實際幀率，再折回 24fps 等效值），
> 並把 pulldown 素材標出來。**跨片比時直接用 `--fps24`，不要手動換算。**

### 跨版本比較的禁忌

**運動分數不能跨比例、跨景別比較。**

16:9 廣角裡兩人只佔畫面一小塊，動作再大，像素變化也有限；9:16 近景人物填滿畫面，一點動作就是大幅變化。

實測：編排最好的一版（9 種招式、主導權換手 3 次、峰值 35）運動分數 14.64，反而低於動作單調的一版（21.89）。

| 指標 | 可否跨版本比 |
|---|---|
| **峰值格** | ✅ 可以（動作節拍數量，最可靠） |
| 開場／末段絕對值 | ⚠️ 僅同比例同景別可比 |
| 末2s÷中段 | ⚠️ 僅同比例可比 |
| 全程運動 | ❌ 不可比 |

## 產出前後對照圖（每次改版都要做）

**技能改版之後，必須實跑「技能使用前」與「技能使用後」兩版提示詞，把結果做成並排動態圖放回 repo。**

這是這個 skill 唯一的「成果證明」。沒有對照圖的規則更新，只是主張。

```bash
# 1. 兩版提示詞各存成一份 .txt（同一個場景、同一顆 seed，只有寫法不同）
# 2. 送本機 H3 實跑
python scripts/submit_ab.py --before before.txt --after after.txt \
    --label-before "A · 技能使用前" --label-after "B · 套用技能後" \
    --width 960 --height 544 --seconds 8 --quality light --seed 20261019

# 3. 等生成完成並下載（可續跑，已下載的會跳過）
python scripts/poll_ab.py --jobs analysis/ab/jobs.json

# 4. 量測 + 做成並排動態圖
python scripts/compare_clips.py --before analysis/ab/before.mp4 --after analysis/ab/after.mp4 \
    --out compare.gif --label-before "A · 技能使用前" --label-after "B · 套用技能後" \
    --width 240 --fps 8 --colors 64 --dither-scale 3
```

`compare_clips.py` 會同時輸出兩片的運動量對照表（全程／開場／末÷中／低潮／峰值），把數字寫進 README 就是證據。

**設計要點：**

| 項目 | 要求 |
|---|---|
| 變因 | **只有提示詞不同**——同 seed、同解析度、同時長、同首幀（`--seed` 必須固定） |
| 「前」版 | 用**沒有 skill 時的直覺寫法**，不是故意寫壞 |
| 「後」版 | 套用全部規則的版本 |
| 尺寸 | 單片寬 240、8fps、64 色 → 4–5 MB，適合放 repo |
| 標籤 | 一定要有，否則看圖的人不知道哪邊是哪邊 |

> **種子沒固定就會得到假對照。** repo 裡的 `assets/demo-ab-skill.gif` 用的是兩支隨機種子不同的實跑，
> 它是「構圖對齊的比較」而不是嚴格單變因實驗——新的流程用 `--seed` 固定種子才是嚴格受控的。

### 受控對照的實測結果（2026-10-19）

同種子（20261019）、同 960×544、同 8 秒、同 light 品質、同採樣步數，**唯一變因是提示詞**：

| 指標 | 未套用 skill | 套用 skill |
|---|---:|---:|
| 字數 / 鏡數 | 122 / 1 | 631 / 10 |
| 全程運動 | 13.79 | **20.46** |
| 末 2s ÷ 中段 | 97% | **210%** |
| 末 2s | 13.30 | **33.75** |
| 峰值格 | 24 | **30** |
| 完全去飽和幀數 | **0** | **44**（漫畫衝擊格） |
| 亮度動態範圍 | 43 階 | **178 階** |

**「套用規則」不只是分數變高，是換成另一種畫面語言**：快切、逆光剪影、
黑白漫畫衝擊格、橫貫整幅的刀光、能量色錨在眼睛與寶石上。

量測飽和度與亮度的指令（`signalstats`）：

```bash
ffmpeg -v error -i clip.mp4 -vf "signalstats,metadata=print:key=lavfi.signalstats.SATAVG:file=-" -f null -
```

> **漫畫格的幀數控不住**：寫 `for two frames`，實跑出 23 幀（958 ms）與 21 幀（875 ms）。
> 詳見 `references/impact-frame-and-shake.md` §1.1.1。

## 參考檔案

| 檔案 | 內容 |
|---|---|
| `references/impact-design.md` | 六拍細節、力度分級（輕/中/重/必殺）、材質反應對照表、節奏時間預算、優雅角色的姿勢先驗 |
| `references/move-library.md` | 16 招具名動作（突進/下盤/拳掌/兵器/落地/防守）、四層結構、4 組三招串接配方、中英翻譯規則 |
| `references/continuous-brawl.md` | 連續對轟模式：衝擊四拍、動作鏈句型、深度錯位、鏡頭參與、細節插切、實驗設計 |
| `references/blade-light-cinema.md` | 21:9 高速斬擊電影語言：1.57 刀/秒、漫畫衝擊格、單色環境+異物色、剪影構圖、尺度手法 |
| `references/ref-identity-lock.md` | 參考圖保真：9 類身份特徵列舉、畫風材質錨、環境參考只鎖建築 |
| `references/drone-camera.md` | 無人機運鏡：8 個機位、五種尺度、穿前景、禁止繞圈圈 |
| `references/facial-performance.md` | 表情與表演：肌肉動作為主、四階段表情、收放對比、生理反應、特寫必配表情 |
| `references/ultra-speed.md` | ULTRA_SPEED 模式：8 秒 10–14 鏡、每鏡四件套、周圍連動清單、鏡頭密度統一表 |
| `references/impact-frame-post.md` | 衝擊幀分開生成再後製：三素材工作流、hold 0.083s、接縫亮度檢查 |
| `references/fl2va-chain.md` | 兩段接續：幀數換算、接縫三層（畫面／速率／身份）、接縫驗收 |
| `references/force-field.md` | 力場四通道模型、三種場型、中英句庫、診斷表 |
| `references/impact-frame-and-shake.md` | 衝擊幀四形態與幀數、漫畫格三段式、震屏 trauma 數學、hitstop 參數、三段式爆炸時序 |
| `references/camera-grammar.md` | H3 官方運鏡詞彙表、打鬥運鏡套路、主體/鏡頭分離寫法、最大衝擊可鎖死相機、幀率陷阱 |
| `references/vfx-vocabulary.md` | 中英特效詞彙庫（能量、粒子、破碎、光、大氣）、色彩腳本、夜戲單色環境邏輯、刃光四形態 |
| `references/prompt-templates.md` | 可直接填空的 T2VA / FL2VA / Ref2VA 模板 + 完整範例 |
| `references/qa-checklist.md` | 生成前自檢、生成後驗收、常見失敗與對應修法 |
| `references/case-wuxia-duel.md` | 完整實例：27.5 秒仙俠對決的拆解與四段式重現 |
| `references/output-format.md` | 官方輸出格式契約：三／六欄位、首行對齊句、對白與標籤語法、常見錯誤對照 |
| `references/guided-mode.md` | 引導模式：三種進入路徑、六個情境選項、素材對應、話術模板、無圖時的 T2VA 寫法 |
| `scripts/validate_prompt.py` | 檢查提示詞是否符合官方格式、能否直接貼進模型 |
| `scripts/measure_motion.py` | 量測生成影片的運動曲線，自動標記開場過靜／尾端停滯／低潮過長 |
| `scripts/compare_clips.py` | 把兩支影片做成並排動態圖 + 運動量對照表（改版後的成果證明） |
| `scripts/submit_ab.py` | 把技能前/後兩版提示詞以固定種子送出本機 H3 |
| `scripts/poll_ab.py` | 等生成完成並下載（可續跑） |
| `scripts/submit_ref2va.py` | 上傳多張參考圖並送出 Ref2VA 生成工作 |
| `scripts/impact_frame.py` | 衝擊幀分開生成，再後製合成到主片 |
| `scripts/measure_staging.py` | 量測取景變化與鏡長分布（運鏡感的客觀指標） |
| `scripts/measure_light_event.py` | 量測每一鏡有沒有光影事件（光影華麗度的客觀指標） |

## 最常被寫錯的三件事

1. **寫「一瞬間閃白」而不寫幀數。** 模型會給 0.3–0.5 秒的長閃，看起來像燈光故障。永遠寫 `for two frames`。
2. **震屏沒有衰減。** 恆定震動 = 相機壞了。必須寫 `decays rapidly and settles back to steady within a third of a second`。
3. **只用術語不用描述。** `Field 力場擾動模擬`、`沖擊幀`、`震屏` 這類術語在中文模型上有效，但 H3 要的是結構化物理描述。術語留給自己記索引，送進模型的必須是具體句子。

## 新增的三個最容易漏掉的點

4. **最大的衝擊那一鏡，相機應該是鎖死的。** 43% 的 3D CG 參考片鏡頭相機不動，而且鎖死的正是關鍵時刻——衝擊感來自「特效把背景推開」，不是相機在抖。前面的鏡頭要動，這一鏡要靜。
5. **衝擊幀不只有爆白。** 「漫畫放射線格」（整幀去飽和成黑白 + 全 360° 放射線，2 幀 + 1 幀黑）是另一種裝置，而且更適合高速斬擊。
6. **參考片標示的幀率可能是假的。** 標 60fps 可能是 24fps 的 pulldown；而且 30fps 素材的運動分數系統性偏低 20%。**先驗證再換算。**
