# 特效編排：五點骨架與空間範圍

> 蒸餾來源：《特效寫法》80 秒（五點骨架＋「墨布切割」反例）、同片尾段的生產版提示詞
> （`【第N秒】`／`【复合运镜】`／`【节奏与声效】`／`【锁定特技对撞刻画】`／`【针对性约束】`／`【全局特效统一特性】`）。
> 可信度：**[實戰]** 作者自陳反覆測試；本 skill 轉錄方法論並改寫成 H3 三欄位。

## 核心診斷：作者自創的招，模型不知道長什麼樣

原片舉的例子是「主角使用**墨布切割**對敵人進行攻擊」。模型不懂三件事：

1. **墨布切割是什麼形狀**（一片布？一道線？一面牆？）
2. **敵人是哪個部位受到攻擊**（胸口？脖子？整個人？）
3. **敵人是怎麼沒的**（被切開？被蒸發？被壓扁？）

> 「AI 沒概念，自然也就沒法把控畫面。」

**這就是「特效沒感覺」的真正原因**——不是模型不會做特效，是**招式的物理不存在**。
`force-field.md` 講的是「力怎麼傳出去」，這篇講的是「**招長什麼樣、打在哪、留下什麼**」。

## 五點骨架

| # | 骨架 | 一句話 | 缺了會怎樣 |
|---|---|---|---|
| ① | **邏輯動線** | 按秒拆解，每個技能的時間軸都要交代 | 特效亂飛，沒有因果 |
| ② | **人物動作** | 明確寫出動作如何開展 | 模板式打鬥（揮、擋、退） |
| ③ | **空間特效** | 每個技能的**形態**＋**展示的空間範圍** | 特效只在角色身上，沒有尺度感 |
| ④ | **鏡頭語言** | 複合運鏡（一次寫兩種以上） | 畫面沒有張力、沒有帶入感 |
| ⑤ | **畫面風格** | 材質、色調、渲染方式，全局定調 | 每一鏡的特效長得不一樣 |

**③ 是原片明講「這點很關鍵」的一點，也是 AI 生成最常缺的一點。**

## ① 邏輯動線：秒級拆解

原片用 `【第1秒】【第2秒】…` 的秒級時間軸；H3 版就是 `[Shot N] At 00:0X.XXX` 的鏡頭時間碼，
但**多一個要求：每一鏡要能回答「這個技能現在走到哪一步」**。

| 階 | 內容 | 時間佔比 |
|---|---|---|
| 起手 | 招式被觸發的訊號（握拳、指訣、刀入鞘一半） | 15% |
| 成形 | 能量的形狀長出來（不是全畫面爆，是**先在一個地方成形**） | 35% |
| 推進 | 形狀往目標走，路徑上的環境被帶動 | 25% |
| 命中 | 目標的反應（變形、破口、位移） | 10% |
| 殘留 | 特效退去後留下的東西 | 15% |

**「成形」與「命中」一定要分成兩鏡或兩個明確的時間段。** 寫在一起，模型只會給一個大爆炸。

## ② 人物動作：寫「如何開展」，不要寫「攻擊」

```text
❌ 主角使用墨布切割對敵人進行攻擊
✅ 她反手把刀橫到腰後，重心沉進後腳，然後整個人向左擰出去，
   手腕在最高點翻轉，讓那條黑布離開刀身、像刀一樣甩出去
```

三個必寫元素：**起始姿勢**（手在哪）→ **發力機制**（哪個部位先動）→ **結束姿勢**（重心在哪）。

## ③ 空間特效：形態 + 空間範圍（最關鍵）

### 形態：給一個「物理等價物」

| 自創招 | 形態的物理等價物 | 關鍵形容 |
|---|---|---|
| 墨布切割 | 一片**薄而韌的布**，像刀刃一樣繃直 | `a ribbon of black cloth pulled taut and flat as a blade` |
| 劍氣 | 一道**壓縮的空氣楔** | `a wedge of compressed air` |
| 光砲 | 一根**實心光柱**，有直徑 | `a column of light two metres across` |
| 巨爪 | **五根手指的實體**，有指節 | `five fingers, each with two visible joints` |
| 領域展開 | 一個**有邊界的地面圓盤** | `a disc of white grid floor three metres across` |

### 空間範圍：四種標記法（至少寫兩種）

| 標記法 | 例 | 什麼時候用 |
|---|---|---|
| **絕對尺寸** | `three metres wide`, `a sixty-centimetre切口` | 單體大招 |
| **相對尺寸** | `twice her height`, `wider than his arm span` | 沒有絕對參照時最可靠 |
| **畫面佔比** | `filling the lower two thirds of frame` | 想要構圖效果 |
| **數量** | `seven strands`, `three concentric rings` | **最有效**：給數字模型就會照排 |

原片生產版提示詞裡就是這樣寫的：`七道粗密的外缘`、`三圈层`、`八道黑色粗墨柱`、`长戟十余道浓黑水条`。
**數字是特效有沒有「設計感」的分水嶺。**

### 命中結果：敵人是「怎麼沒的」

| 消失方式 | 寫法 | 殘留物（一定要寫） |
|---|---|---|
| 切開 | `cut clean through at the waist` | 整齊的截面、向內翻捲的邊緣 |
| 蒸發 | `boiled away from the contact point outward` | 白煙、炭化的輪廓 |
| 壓碎 | `flattened under the palm` | 碎屑向外放射、地面凹陷 |
| 吸走 | `drawn into the vortex in a spiral` | 盤旋的碎片、被拉長的殘影 |
| 釘住 | `pinned to the pillar, still moving` | 裂紋網、仍在震動的肢體 |

**只寫「被打中」＝沒有結果。** 觀眾需要看到「不可逆的改變」。

## ④ 鏡頭語言：一鏡兩運鏡

原片要求「合理運用不同的鏡頭運鏡」，生產版一句裡常出現兩種以上：

```text
【复合运镜】FPV 死咬后的后背冲入破碎巨浪，摄影机人体 270 度，
钻过两道水交缠叠起，再实空变向折回到接油之轮
```

H3 的寫法（官方格式只允許**一個**官方運鏡詞在頭句）：

```text
[Shot 3] At 00:02.400, the shot cuts to a tracking shot at shoulder height behind her,
as the camera trucks alongside at fast speed.
Camera: 50mm from two metres at shoulder height, moving with her for 1.2 s,
ending with the wave face filling frame-left.
```

**「複合」在 H3 要拆成「頭句一個官方詞 + 五小節描述」**，不能堆兩三個官方詞——堆了會被平均成一個。

## ⑤ 畫面風格：全局定調

原片的 `【全局特效统一特性】` 一欄寫的是：`全局墨瀑、水珠爆裂、硬底质感水浪、金边`。
翻成 H3 的做法：**寫在 `[Shot 1]` 的風格錨定裡，全段只寫一次。**

```text
[Shot 1] 3D CG, cinematic, ink-wash fluid simulation with hard-edged water sheets
and gold rim light on every energy edge, high-contrast black-and-white core with one accent hue.
```

三個錨就夠（見 `ref-identity-lock.md` 的警告：超過 3 個形容詞會把畫面壓成靜止圖）。

## 未知招式的三步翻譯法（本 skill 的延伸）

拿到一個作者自創、模型不可能懂的招式，照這三步翻：

| 步 | 動作 | 「墨布切割」的答案 |
|---|---|---|
| 1 | **拆成物理名詞**：它是什麼材質、什麼形狀、怎麼動 | 薄布、繃直、像刀一樣甩 |
| 2 | **指定起點→路徑→終點** | 從她腰後 → 由左下斜掃到右上 → 停在敵人肩線上方 |
| 3 | **指定命中結果＋殘留物** | 敵人胸口一道平整切口，邊緣向內翻捲，黑煙從切口滲出 |

```text
[Shot 4] At 00:03.200, the shot cuts to a medium shot of the cloaked figure as the camera whips
sideways at fast speed. Camera: 40mm from four metres at chest height, whipping right at fast
speed with large amplitude over 0.8 s. Motion: First she drags the blade back to her hip, then
her weight sinks into the rear leg, and the whole torso twists left as the wrist snaps over at
the top. The black cloth leaves the blade and goes taut and flat, a two-metre ribbon cutting
the air. Light: The ribbon's leading edge catches a single hard white highlight while the rest
stays matte black, and the rain it passes through is pushed into a thin sheet. Sound: Cloth
snaps taut at 0.3 s then hisses through the air, with a wet cut at 0.7 s.
```

## 生產版區塊 → H3 三欄位的對照表

| 原片區塊 | H3 放哪裡 |
|---|---|
| `【第N秒】` | `[Shot N] At 00:0X.XXX` |
| `【复合运镜】` | 頭句的官方運鏡詞＋Camera 小節 |
| `【节奏与声效】`（`250%~300% 常速贯穿`） | `overall_soundscape` ＋ 各鏡 Sound 小節 |
| `【锁定特技对撞刻画】` | Motion ＋ Light 小節 |
| `【针对性约束】`（`全片只有她一个人`） | `[Shot 1]` 的第一句（重要約束往前放） |
| `【全局特效统一特性】` | `[Shot 1]` 的風格錨定（≤3 個錨） |

## 自檢（交付前逐項）

- [ ] 每一招都有：**材質／形狀**、**起點→終點**、**空間範圍（含數字）**、**命中結果**、**殘留物**
- [ ] 「成形」與「命中」不在同一句
- [ ] 每鏡至少兩種空間標記法
- [ ] 全局只有一組主色＋一個點綴色（`vfx-vocabulary.md` 的色彩腳本）
- [ ] 風格錨 ≤3 個，寫在 `[Shot 1]`
- [ ] 逐鏡的 Sound 有秒數，且與命中時刻對齊

## 反模式

1. **只寫招式名。** 「墨布切割」「天罡劍氣」——模型只能給通用光效。
2. **只寫亮度。** 「發光、強光、爆閃」——沒有形狀就沒有辨識度。
3. **全部都在主角身上。** 沒有環境尺度的特效＝貼圖（見 SKILL.md 三層能量語言的「外層」）。
4. **每一鏡都換特效形狀。** 一個技能從頭到尾只有一種形狀，才叫「招式」。
5. **寫「敵人被擊中」。** 要寫敵人的哪個部位、變成什麼、留下什麼。
