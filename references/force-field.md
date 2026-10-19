# 力場（Field）：讓特效擁有空氣

## 0. 核心命題

> **光效只是顏色，力場才是空氣。**

AI 生成爆炸的預設行為是「給你一顆發光火球」，但不會給你「世界被這顆火球影響」的證據。觀眾感覺「像煙霧彈」，不是因為特效不夠大，而是因為**場景沒有反應**。

三個典型失敗症狀（可直接用來診斷生成結果）：

| 症狀 | 技術含義 |
|---|---|
| 周圍物體一動不動 | 物質通道缺失 |
| 空氣沒有波瀾 | 空氣通道缺失 |
| 光影完全脫節 | 光通道缺失 |

---

## 1. 四通道模型

把「力場」拆成四個可獨立增減的通道。**這是本 Skill 的核心工具。**

```
場源（能量中心）
   ↓ 傳播（形狀 + 速度 + 方向）
   ├─ ① 光通道   → 亮度、色溫、陰影、暗部、反射
   ├─ ② 空氣通道 → 折射、熱浪、壓縮、色散、撕裂
   ├─ ③ 物質通道 → 布料、髮絲、玻璃、塵土、碎石
   └─ ④ 粒子通道 → 體積粒子、火星、煙塵、熱霧
```

**寫作公式：場源 → 傳播 → 四通道反應 → 全域聯動**

### 1.1 光通道

能量改變整個場景的照明，而不只是加一個發光體。

| 要寫什麼 | H3 寫法 |
|---|---|
| 全域光照聯動 | `the whole scene's lighting shifts in step with the energy` |
| 陰影被推開 | `shadows swing away from the blast and stretch across the ground` |
| 暗部被照亮 | `the shadowed side of the courtyard is lit for a moment` |
| 色溫偏移 | `the ambient light swings from cold blue to orange within the same beat` |
| 反射聯動 | `the wet flagstones flare with the same colour` |

**關鍵詞：`in step with`（同步）。** 沒有這個詞，模型會把爆炸光與環境光當成兩件事。

### 1.2 空氣通道

最容易被忽略、卻最能救「貼圖感」的一層。空氣是可見的介質。

| 要寫什麼 | H3 寫法 |
|---|---|
| 熱浪扭曲 | `heat haze warps the air above the ground` |
| 折射 | `light bends and splits into colour fringes as it passes through the field` |
| 壓縮成層 | `the air compresses into visible layered sheets` |
| 空間扭曲 | `the background bends through the distortion` |
| 撕裂 | `the air tears into layered sheets that drag the background with them` |
| 色散 | `hard light passing through the haze separates into red and cyan fringes` |

**這四個詞的差別（別混用）：**

- **折射 refraction** — 背景位移、輪廓錯位（最實用）
- **熱浪 heat haze** — 細密的向上抖動（火焰、沙漠）
- **壓縮 compression** — 層狀、同心、向前推（衝擊波前方）
- **色散 dispersion** — 邊緣出現紅藍彩邊（強光穿透）

### 1.3 物質通道

場景中的實體被力量推動。**這一層是「有沒有空氣」的證據。**

| 要寫什麼 | H3 寫法 |
|---|---|
| 布料被壓平 | `wind pressure flattens the silk against her body` |
| 髮絲被推 | `her hair whips forward a beat late` |
| 玻璃變形 | `the glass in the window bows inward under the pressure` |
| 塵土掀飛 | `dust and gravel are ripped off the ground and thrown outward` |
| 碎石浮起（蓄力） | `small stones lift off the ground and hover` |
| 瓦片震落 | `roof tiles rattle loose and fall from the eaves` |
| 水被推成扇 | `the rain is pushed into a radial sheet` |

### 1.4 粒子通道

體積粒子被流場帶動，而不是自己亂飛。

| 要寫什麼 | H3 寫法 |
|---|---|
| 被震波捲動 | `volumetric dust is dragged into curling spirals behind the wave` |
| 餘燼飄落 | `embers drift down through the lantern light` |
| 熱霧懸浮 | `suspended heat mist glows in the light` |
| 火星被拉長 | `sparks streak into long horizontal lines` |

**關鍵詞：`dragged into`（被帶動）。** 寫 `particles fly everywhere` 只會得到雜訊。

---

## 2. 三種場型（選一種，不要混）

### 2.1 一次性場（爆炸、衝擊、斬擊）

- 時態：**瞬間**（一幀觸發，隨後衰減）
- 四通道：全開
- 時間結構：爆發點 → 擴散 → 沉降

```text
the blast core bursts outward; for two frames the frame blows out to white.
The shockwave flattens into concentric rings racing outward. The whole scene's
lighting shifts in step with the energy, dust and gravel are ripped off the
ground, and the air tears into layered sheets that bend the background.
```

### 2.2 持續性場（熱浪、瘴氣、結界、能量護罩）

- 時態：**進行式**（持續存在，強度起伏）
- 四通道：以「空氣 + 光」為主，「物質」只做微幅，「粒子」做緩慢循環
- 關鍵詞：`continuously`, `keeps rippling`, `pulses slowly`

```text
the ground keeps radiating a low field; the air above it ripples continuously
and bends the outline of the far rooftops. The light pulses slowly in time
with the heat, and suspended mist drifts through it.
```

**一次性 vs 持續性最常被寫錯的地方**：把熱浪寫成爆炸。熱浪是「一直在抖」，不是「炸一下」。

### 2.3 附著型場（武器附魔、身體氣場）

- 時態：**貼附於主體**，隨主體運動
- 四通道：以「光 + 粒子」為主，「空氣」只在邊緣做薄薄一層折射
- 關鍵詞：`a thin rim of`, `hugging the blade`, `trailing`

```text
a thin teal flame hugs the blade's edge and trails behind it as it moves,
bending the air immediately around the steel
```

---

## 3. 三種題材的完整範例（中英對照）

### 3.1 魔法能量場（紫／青）

```text
A magic energy field expands outward from her palm. The whole scene's lighting
shifts in step with the glow, shadows swing away from the source, heat haze
warps the air, and the airflow rolls outward. Wind pressure flattens the silk
of her sleeves and pushes her hair back. Light bends and splits into colour
fringes as it passes through the field, and volumetric dust is dragged into
curling spirals behind the wave.
```

### 3.2 高溫熱浪（沙漠、熔岩）

```text
The ground keeps radiating a steady field. The whole scene's lighting follows the
intensity of the heat, the air near the ground ripples and shivers continuously,
and heat currents roll upward. The air refracts and distorts the outline of the
nearby rocks; light passing through the hot air shifts and separates into colour
fringes. Suspended heat mist drifts through the frame, and the light and shadow
ripple with the airflow.
```

> 中文版可直接用：「地面產生持續力場擾動，全域燈光跟隨熱浪強度聯動，近地面空氣持續扭曲震顫，熱氣流向上翻滾，空氣折射扭曲近景輪廓，光線穿透熱空氣發生偏移，撕裂空氣色散，懸浮熱霧，光影隨氣流起伏動態變化。」

### 3.3 科幻爆炸衝擊波

```text
Strong air compression distorts the space. The shockwave's wind pressure pushes
the air forward, and nearby glass and fabric are crushed and deformed by the
pressure. The air tears into layered curved sheets that warp the space. Hard
light punches through and overexposes the air, producing dispersion. Volumetric
sand and dust churn, and the light and shadow tremble in sync with the shockwave.
```

---

## 4. 使用規則

1. **一次最多開三個通道。** 四通道全開會讓模型把注意力分散到粒子，主體糊掉。
2. **優先順序**：空氣 > 物質 > 光 > 粒子。空氣最有效、粒子最廉價。
3. **必須有一個「反向證據」**：主角的衣襬或頭髮被推。這是最便宜也最有效的力場證明。
4. **持續性場要寫「強度起伏」**，否則會變成一張靜態濾鏡。
5. **不要用術語代替描述。** `Field 力場擾動模擬` 對以英文結構化語料訓練的模型（如 H3）可能是噪音；把它拆成四通道的具體句子。

---

## 5. 診斷表：生成後對照

| 看到的問題 | 缺哪個通道 | 補什麼句子 |
|---|---|---|
| 爆炸像發光球 | 全部 | 先補空氣通道的折射 |
| 特效邊緣很乾淨 | 空氣 | `the air tears into layered sheets` |
| 主角像貼在背景上 | 物質 | `wind pressure flattens the silk against her body` |
| 場景亮度沒變 | 光 | `the whole scene's lighting shifts in step with the energy` |
| 煙塵像貼圖 | 粒子 | `volumetric dust is dragged into curling spirals` |
| 爆炸沒有「推進感」 | 空氣（壓縮） | `the air compresses into visible layered sheets pushing forward` |
| 熱浪看起來像靜止濾鏡 | 持續性 | 加 `keeps rippling` + 強度起伏 |
