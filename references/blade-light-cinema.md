# 刃光電影語言：21:9 高速斬擊的完整寫法

> 蒸餾自一支 42.57 秒 / 2516×1080 / 30fps 的雪原夜戰參考片（68 鏡、67 切點）。
> 這支片的出處模型未知，是否單次生成**未證實**（H3 單段上限 15 秒，42 秒必為多段剪接或其他模型）。
> **在 H3 複製其切點密度：依模式決定每段鏡數（一般 3–9 鏡；ULTRA_SPEED 見 `ultra-speed.md`），其餘靠多段生成再剪接；不要把 60+ 鏡塞進單段。**

---

## 0. 一句話

**可複製的核心不是「特效多」，是四件事的組合：**

1. 模型自發的 **1.57 刀/秒**快切
2. **2 幀漫畫放射線衝擊格**（不是爆白）
3. **冰藍／紫羅蘭雙色分屬**（環境單色相 + 一個異物色）
4. **93% 剪影率的「低調天空 + 高調雪地」**夾擊構圖

---

## 1. 剪接密度

| 指標 | 值 |
|---|---|
| 切點 / 鏡數 | 67 / 68 |
| 間隔平均 | **0.592 s** |
| 間隔中位數 | **0.366 s** |
| 最短 / 最長 | 0.100 s / 3.131 s |
| **有效刀數** | **1.574 刀/秒** |
| 平均鏡長 | 0.626 s |
| 短鏡（<0.25s）佔比 | **37.3%** |

**主導節奏：0.10–0.50 秒一鏡（63% 的鏡）。**

> **最長的鏡（3.13s、2.93s、2.40s、2.13s）都是廣角交代空間；最碎的鏡（0.10s）幾乎都是特效插入格或形態突變。**
> 長鏡負責建立尺度，短鏡負責維持速度感——兩者比例約 4:1。

### 1.1 幀模式預算

| 模式 | 幀數 | 佔比 |
|---|---|---|
| COLOR（正常彩色） | 1187 | 92.9% |
| **BW（漫畫格）** | 37 | 2.9% |
| BLACK（純黑） | 9 | 0.7% |
| WHITE（爆白） | 45 | 3.5% |

> ⚠️ 結尾 33 幀（1.10 秒）全白淡出是**生成器溢出**，不是設計。**不該學。**

---

## 2. 構圖：低調天空 + 高調雪地

| 指標 | 值 |
|---|---|
| 主體為剪影（暗塊 ≥8% 畫面） | **93.2%** |
| 背光（暗塊外圍有亮邊） | **88.1%** |
| 高調地面（下 22% 比上 22% 亮 >30 階） | **66.1%** |
| 剪影暗塊面積中位數 | **31.3% 畫面** |

**上半是黑藍的樹林，下半是接近曝光的藍白雪面，角色永遠站在這條明暗交界線上。**

```text
The upper half is near-black tree line, the lower half is overexposed blue snow,
and the fighters travel along the boundary between them.
```

```text
The snow is so bright it has lost all detail, a glowing white field where the
fighters' shadows are the only dark shapes.
```

```text
No light falls on the fighters from the front; only the snow behind them draws
their outline.
```

> 最後一句是負面句（`No light falls...`）。**H3 沒有負面提示欄，必須改寫成正面句**：
> `The fighters receive no light from the front; only the snow behind them draws their outline.`

---

## 3. 色彩：單色環境 + 唯一異物

| 能量色 | 色相 | 高飽和像素佔比 |
|---|---|---|
| **冰藍 CYAN** | 210–230° | **97.6%** |
| **紫羅蘭 VIOLET** | 250–260° | **1.4%** |
| 琥珀（作為能量） | — | **0 幀** |

環境中間調 RGB = **(0, 74, 123)**，近乎單一藍綠。

**冰藍佔 97.6% → 它其實是「環境色」。紫羅蘭 1.4% → 它才是「異物色」。**

這與「主色給主角、對比色給環境」的常見做法**是反的**，但對夜戰更有效：觀眾的眼睛自動找唯一的異物。

```text
Violet is the only chromatic intruder in the teal frame, so the eye goes to it
the moment it appears.
```

### 3.1 顏色跟角色走，不跟畫面位置走

用**眼瞳／寶石**當錨點：

```text
The cold fighter's irises glow ice-blue; the warm fighter's irises are amber,
with a violet diamond set in her forehead.
```

這解決了 AI 生成時的能量顏色飄移——眼睛和寶石是不會互換的。

---

## 4. 能量形態（8 種）

| # | 形態 | 說明 |
|---|---|---|
| 1 | **刃形光** | 貼在刃口流動的亮邊，長度與刀身相當 |
| 2 | **新月弧** | 揮砍軌跡的幾何化，弧的曲率＝揮砍半徑 |
| 3 | **橫貫全畫面的細光線** | 揮砍後**殘留**，長度超過畫幅、兩端出框 |
| 4 | **放射狀閃電分枝** | 命中點向外分叉，像玻璃裂紋 |
| 5 | **大型能量波／牆** | 一次重擊推出整面能量浪 |
| 6 | **X 形十字爆** | 交鋒點正面爆發，水平＋垂直兩條主軸 |
| 7 | **紫環／門戶環** | 環繞／包覆型（極少用） |
| 8 | **光之眼** | 能量內化到角色身上，不是武器 |

### 4.1 刃形與弧

```text
A thin, sharp ice-blue glow clings to the blade's edge and flows along the
cutting line instead of wrapping the whole sword.
```

```text
The swing leaves a crescent of blade-light whose arc length equals the radius
of her swing.
```

### 4.2 離手不散的光線（21:9 最好看，16:9 也可）

```text
After the blade leaves, the light does not disperse; it stays as a hair-thin
white thread crossing the entire frame and running off both edges.
```

```text
The light is straight, not curved, as if someone drew a single straight scar
across the image.
```

> **21:9 最好看**：兩位角色分踞左右三分之一、中央全空給光。舊版寫「21:9 限定」過窄——動作蒸餾參考片在 16:9 多次出現橫貫整幅的紅色細光線（5.8 s、21.7 s、28.5 s）。

### 4.3 爆發是 X 形，不是放射球

```text
The burst is not spherical; it is a cross of one horizontal and one vertical
axis, an X-shaped flare.
```

```text
At the moment of contact, ice-blue lightning branches outward from the point
of impact like cracks in glass.
```

### 4.4 能量與環境

```text
Snow is kicked up from underfoot into a radial spray that scatters along with
the light.
```

```text
Her hair and the hem of her coat follow the blade a half-beat late, whipping
out after the light has already passed.
```

---

## 5. 漫畫衝擊格（本片最值得學的裝置）

**「風格跳轉」事件，不是「亮度」事件。**

| 項目 | 漫畫衝擊格 | 爆白 |
|---|---|---|
| 發生的事 | 整幀去飽和 → 純黑白 | 整幀變亮 |
| 放射線 | **全 360° 放射**（量測 10/10 格角度佔用 24/24 桶全滿） | 無 |
| 幀數 | **2 幀（30fps 下 67 ms；換成 H3 24fps 取 2 幀＝83 ms）**，本片 10 格中 9 格剛好 2 幀 | 1–2 幀 |
| 後接 | **1–3 幀純黑**（格間黑邊） | 直接回原畫面 |

### 三段式序列（本片出現 7 次）

> ⚠️ **下面是參考片的描述，不可直接送 H3。** 同段寫漫畫格＋`then one frame of black`，H3 實測給 21–23 幀、第二次角色消失。送 H3 走 P3（另生衝擊片再 composite，`impact-frame/post.md`）或 P2（`impact-frame/burst-strip.md`）。另外本片實測的多階段序列不只三段：13.67 s 是 13 幀（白放射→黑白放射→紫放射→黑白剪影→反相→白→**黑 3 幀**），見 `impact-frame/forms.md` §0。

```text
[Shot 3] At 00:01.600, the frame cuts to a black-and-white manga panel for two
frames: a solid white core at the point of contact with clean radial speed
lines bursting in every direction, the fighter crushed into a solid black
silhouette, then one frame of black, then the colour snaps back.
```

```text
Inside the panel there are only two values, black and white, and the fighter is
crushed into a solid black silhouette.
```

```text
The centre of the burst is a solid white core ringed by clean radial lines with
no soft gradient between them.
```

> **提示詞要明確寫「這格變黑白」，不能只寫「閃一下」。**
> 單色剪影與漫畫格是兩個不同的東西——前者保留單一彩度，後者是整幀去飽和。

---

## 6. 尺度：用已知物比出來

**尺度不是靠「劍看起來很大」說的，是靠「劍跟人／跟倒木／跟樹幹比出來的」。**

| 手段 | 效果 |
|---|---|
| 失焦前景肩背佔 40% 畫面 | 一秒建立「劍很大、對手很遠」 |
| 橫貫畫面的倒木，人只到它一半高 | 用已知物做比例尺 |
| 垂直樹幹 | 連續的尺度提示 |
| 能量刃長度超過角色身高 | 直接說「劍很大」 |

```text
An out-of-focus black shoulder fills the left two-fifths of the frame while the
opponent stands far away as a small blue speck on the snow.
```

```text
A fallen trunk crosses the whole frame, the fighter reaching only half its
height, and the depth of the forest is established in one image.
```

---

## 7. 鏡頭語法

| 景別 | 鏡數 | 佔比 |
|---|---|---|
| 極特寫（只有眼／臉） | 2 | 2.9% |
| 特寫 | 8 | 11.8% |
| 中景 | 26 | 38.2% |
| 廣角／全景 | 15 | 22.1% |
| 大遠景／極遠景 | 3 | 4.4% |
| **無人物插入格** | **14** | **20.6%** |

**兩個反直覺的點：**

1. **近景 14.7%，其中 8 個是「臉」，兵器特寫 0 個。** 本片把特寫全用在臉上賣角色，尺度改用倒木／樹幹對比。
2. **20.6% 的鏡頭根本沒有可辨識人物**（漫畫格、純特效）。

### 運鏡

| 指標 | 值 |
|---|---|
| 有背景位移的鏡頭 | **86.8%**（53 鏡中 46 鏡） |
| 完全靜止 | 13.2% |
| 位移方向 | 水平 39 鏡、垂直 7 鏡（**水平為主**） |
| 中位背景位移 | 0.88 px/幀（160px 寬）= 原生約 **14 px/幀 ≈ 420 px/秒** |

```text
The camera trucks sideways along the snow, the background trunks smearing into
horizontal streaks while the fighter stays on the same side of the frame.
```

```text
The camera does not follow the fighter; it holds its position and lets them
rush across the frame.
```

---

## 8. 空間

- **幾乎全程貼地。** 68 鏡中只有約 4 鏡短暫躍起／騰空，單次不超過 0.5 秒。
- **兩位戰鬥者永遠分踞畫面左右兩側，中央留給能量。**
- 極少數置中對稱構圖（鏡 29，9.67s）。

```text
The two fighters hold the left and right thirds and the centre of the frame is
left entirely empty for the light.
```

---

## 9. 驗收門檻

| 門檻 | 建議值 |
|---|---|
| 切點密度 | 30fps 下 **≥1.5 刀/秒**（平均鏡長 ≤0.65s） |
| 短鏡佔比 | **≥30% 的鏡頭 ≤0.25s** |
| 漫畫衝擊格 | 每次重擊 **2 幀黑白放射線格 + 1–3 幀黑**（成品；走 P3 合成，不寫進主片） |
| 能量色彩集中度 | 單一能量色佔高飽和像素 **≥90%**，另一色 ≤2% |
| 插入格比例 | 全部鏡頭的 **≥15% 為無人物插入格** |
| 背景位移 | **≥85% 的鏡頭**有可量測的背景位移 |
| 運鏡方向 | 水平位移的鏡頭應占 **≥70%** |

> 本片（**非 H3 生成，出處模型未知**）的開場 0.8s 運動量只有中段的 **3.5%**，末 2s ÷ 中段只有 **15%**，且有 **2.07 秒低潮**。
> 原因：開場用了 2.13 秒的失焦前景大遠景；結尾 33 幀全白淡出。
> **這不代表它「不合格」**：參考片常刻意以靜止／淡出收尾。「末 2s ÷ 中段 ≥60%」只適用於要接下一段、或要求動態結尾的 H3 片段（`lab-notes.md` §0）。H3 上要接續時，別學它的開場與結尾。

---

## 10. 誠實限制

- 推近／拉遠（zoom）比例**量不到**（log-polar 與多尺度相關皆被內容變化淹沒），本文件不給數字。
- 景別分布是逐鏡目視判讀，**非演算法分類**。
- 無法區分 pan（原地搖）與 truck（平移），二者都產生背景水平位移。
- 主體運動 vs 特效運動**未能分離**。
- AI 生成的角色外觀會漂移，「A/B 角色」的對應在本片中不穩定，只有能量色歸屬可確認。
