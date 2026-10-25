# 特效詞彙庫（中英對照）

寫特效的鐵則：**形狀 + 運動 + 顏色 + 與誰互動**。只寫顏色（`green energy`）模型會給一坨發光霧。

---

## 1. 能量本體（Shape of Energy）

| 形態 | 英文 | 適用 |
|---|---|---|
| 渦流球 | `spinning vortex orb` / `smoke-tailed orb` | 妖氣、念力、浮遊彈 |
| 絲帶 | `ribbon of energy` | 劍氣、追蹤攻擊 |
| 盤繞 | `coiling energy` / `helical coil` | 纏繞、鎖鏈、鞭 |
| 環 | `ring of energy` / `expanding halo` | 衝擊波、護盾、蓄力 |
| 錐 | `pressure cone` / `sonic cone` | 高速直衝、音爆 |
| 刃形 | `blade-shaped light` | 劍氣、斬擊 |
| 絲線 | `filaments of light` | 細膩、神經感、束縛 |
| 液態 | `liquid light` / `molten glow` | 火焰、岩漿、金術 |
| 霧態 | `rolling mist of energy` | 毒、瘴氣、亡靈 |

**組合寫法**：`eight spinning vortex orbs with long smoke tails orbit her in a slow ring`

---

## 2. 粒子與火花（Particles）

| 中文 | 英文 |
|---|---|
| 白熱火花 | `white-hot sparks` |
| 餘燼飄落 | `embers drift down` |
| 火星噴濺 | `sparks spray from the contact point` |
| 塵埃懸浮 | `dust motes hang in the light` |
| 金色碎屑 | `golden flecks` |
| 灰燼如雪 | `ash falls like snow` |
| 光斑（散景） | `out-of-focus bokeh lights` |
| 殘影 | `afterimages trail behind the blade` |

---

## 3. 破碎與衝擊（Destruction）

| 中文 | 英文 |
|---|---|
| 衝擊波環 | `a ring of shockwave dust bursts outward` |
| 碎石飛濺 | `stone shards spray away` |
| 地面龜裂 | `the flagstones crack in a starburst` |
| 瓦片震落 | `roof tiles rattle loose and fall` |
| 木屑爆開 | `splinters burst out` |
| 水幕 | `water sprays up in a thin sheet` |
| 氣浪推平布料 | `the silk is flattened by the pressure wave` |
| 空氣扭曲 | `the air ripples with heat distortion` |

---

## 4. 光與鏡頭光學（Light & Optics）

| 中文 | 英文 |
|---|---|
| 過曝爆白 | `the frame blows out to white` |
| 徑向速度線 | `radial speed lines tear outward` |
| 鏡頭光暈 | `anamorphic lens flare` |
| 體積光 | `volumetric god rays through the smoke` |
| 邊緣光 | `a hard rim light traces her silhouette` |
| 色差 | `slight chromatic aberration at the edges` |
| 失焦 | `the background falls into soft bokeh` |
| 高光溢出 | `highlights bloom and bleed` |

**爆白只給 1–2 幀。** 寫 `a flash` 而不指定幀數，模型通常給 0.5 秒，看起來像燈光故障。

---

## 5. 大氣與環境（Atmosphere）

| 中文 | 英文 |
|---|---|
| 濕地反光 | `wet flagstones mirror the lantern light` |
| 薄霧 | `low ground mist` |
| 細雨 | `fine rain streaks through the light` |
| 雨被氣壓推開 | `the rain is pushed into a radial sheet` |
| 燈火搖曳 | `lantern flames gutter in the shockwave` |
| 香灰/煙 | `incense smoke curls upward` |
| 樹影 | `the canopy sways overhead` |

---

## 6. 時間特效（Time）

H3 沒有 speed ramp 參數。**精準的變速、凍結、抽幀一律在組裝做**（`impact_frame.py ramp`／`composite`）；提示詞只給語意：

| 效果 | 英文寫法 | 注意 |
|---|---|---|
| ~~近乎凍結~~ | ~~`decelerates to a near-freeze`~~ | **已停用**：H3 放大成 0.5–1 s 停頓；參考片命中後也幾乎不減速。停頓在組裝做 |
| 突然恢復常速／加速 | `then snaps back to full speed`、`then the camera accelerates with the shockwave` | 命中後加速比減速更像參考片 |
| 慢動作 | `the moment stretches into slow motion` |
| 子彈時間 | `time slows as the camera arcs around the suspended shards` |
| 殘影疊加 | `three afterimages of the blade overlap in the same frame` |

⚠️ 不要寫 `time stops completely`——模型會真的把整段凍結，後面接不回來。

---

## 7. 色彩腳本

**配色規則三選一**（取代舊的「一段只能用一組」；2026-10-26 依參考片重分析）：

| 規則 | 什麼時候 | 例 |
|---|---|---|
| **互補雙色** | 兩人對打、各有能量色 | 青綠 vs 琥珀橙，A 只用冰藍、B 只用暖金 |
| **單色環境＋唯一異物色** | 夜戲、雪地、要刀光最亮 | 冰藍環境＋紫色異物（§7.1、`blade-light-cinema.md` §3） |
| **爆炸換調** | 長段、多次大爆炸 | 每次 L3 以上爆炸換一次全片色調：灰藍 → 橙 → 藍白 → 黑星空（Seedance 原提示詞 `each big blast rekeys the palette`；H3 未實測） |

不論哪種：**一技能（或一角色）鎖一顏色**，不要每擊換色。

以下是互補雙色的常用組合：

| 名稱 | 主色 | 對比色 | 氣質 |
|---|---|---|---|
| 仙俠青焰 | 青綠 `teal #2E8B7A` | 琥珀橙 `amber #E8892B` | 妖氣 vs 人間燈火（本案例） |
| 血月 | 暗紅 `crimson #8B1A1A` | 冷藍 `steel blue #3A5A78` | 殺伐、悲壯 |
| 金剛 | 金白 `gold #F2C14E` | 墨黑 `ink #101014` | 神聖、壓迫 |
| 雷獄 | 電紫 `violet #7A5CFF` | 鈉黃 `sodium #FFB347` | 科幻、暴烈 |
| 幽潭 | 冰藍 `ice #9FD8E8` | 深綠 `deep green #14342B` | 陰冷、詭異 |

**用法**：主色給主角的能量，對比色給環境光源（燈籠、火、城市）。兩色面積比約 3:7，讓主色成為視覺焦點。

### 7.1 夜戲的相反邏輯：把環境調成單一色相（實測蒸餾）

上面的色彩腳本是「主色給主角」。**但夜戰有另一套更有效的邏輯，而且與上面是反的。**

42.6 秒的雪原夜戰參考片量測結果：

| 項目 | 值 |
|---|---|
| 環境中間調 RGB | **(0, 74, 123)** —— 近乎單一的藍綠 |
| 冰藍能量佔高飽和像素 | **97.6%**（hue 210–230°） |
| 紫羅蘭能量佔高飽和像素 | **1.4%**（hue 250–260°） |
| 琥珀色作為能量 | **0 幀**（琥珀只出現在眼睛） |

**冰藍色佔了 97.6%——它其實是「環境色」。紫羅蘭只有 1.4%——它才是「異物色」。**

| 角色 | 作用 | 寫法 |
|---|---|---|
| **大量、低對比** | 環境色（幾乎等於背景） | `a single saturated teal-blue night` |
| **少量、高對比** | 異物色（觀眾的視線焦點） | `violet is the only chromatic intruder in the teal frame` |

**這種配色比互補色更適合夜戰**，因為觀眾的眼睛會自動找「唯一的異物」，不需要靠面積堆焦點。

### 7.2 能量色要用「眼瞳／寶石」當錨點

AI 生成時能量顏色會飄移。解法是把顏色綁到角色身上**看得見的固定特徵**：

```text
❌ one fighter has blue magic and the other has purple magic
✅ The cold fighter's irises glow ice-blue; the warm fighter's irises are amber,
   with a violet diamond set in her forehead.
```

量測佐證：片中的色彩歸屬**跟著角色走，不跟著畫面位置走**（左右互換時顏色不換邊）。眼睛與寶石是不會互換的錨點。

### 7.3 刃形光的四種形態

| 形態 | 描述 | 寫法 |
|---|---|---|
| **貼刃光邊** | 光沿刃口流動，不包住整把劍 | `a thin, sharp ice-blue glow clings to the blade's edge and flows along the cutting line` |
| **揮砍弧** | 軌跡凝成月牙，弧長＝揮砍半徑 | `the swing leaves a crescent of blade-light whose arc length equals the radius of her swing` |
| **離手光線** | 揮完不散，橫貫整幅、兩端出框 | `the light does not disperse; it stays as a hair-thin white thread crossing the entire frame and running off both edges` |
| **地面餘光帶** | 斬擊餘光沿地面拖出狹長光帶 | `the afterglow of the cut drags a long way along the snow, lighting the ground into a narrow luminous band` |

**第三種「離手光線」在 21:9 最好看**（長度超過畫幅寬度）；16:9 也做得到——動作蒸餾參考片在 16:9 多次出現橫貫整幅的紅色細光線（5.8 s、21.7 s、28.5 s）。

### 7.4 爆發的主軸：X 形十字，不是放射球

```text
❌ a spherical burst radiating outward in every direction
✅ the burst is not spherical; it is a cross of one horizontal and one vertical axis,
   an X-shaped flare
```

X 形在 21:9 裡能同時佔滿寬度與高度；放射球只會變成一團。

---

## 8. 特效的三個禁用寫法

| 禁用 | 原因 | 改成 |
|---|---|---|
| `lots of particles everywhere` | 沒有方向與密度，變成雜訊 | `sparks spray in a narrow cone away from the impact` |
| `epic explosion` | 模型給通用火球，缺乏設計 | `a ring of white shockwave dust, then a low orange fireball` |
| `glowing aura` | 主體會被光暈吃掉 | `a thin teal rim of flame along the blade's edge` |

## 9. 特效寫法補充（2026-10-26 新增）

> 來源：老大的教學片 v5（特效寫法）、v6（衝擊幀教學片尾提示詞）。**以下除註明外 H3 未實測。**

### 9.1 特效五要素（v5）

特效沒感覺不是模型的錯，是提示詞沒有畫面感。每個技能交代：
1. **按秒拆動線**：每個技能幾秒起、幾秒到、幾秒散。
2. **人物動作**：動作怎麼展開，不要模板式打鬥。
3. **空間特效＝形態＋空間範圍**（最關鍵）：多大、到哪裡、佔畫面多少。
4. **鏡頭語言**：用什麼運鏡增加張力。
5. **畫面風格**：全局定調，控制 AI 不亂發揮。

每組可以用四欄：【複合運鏡】【極速動作】【錨定特效與環境反饋】【節奏與聲音】，全片頭寫一次【全招式統一特效】【攝影與聲場】（`impact-design.md` §2.1 三級碰撞體系就是「統一特效」的寫法）。

### 9.2 遞增曲線＝時間戳＋數量

「越來越多」對模型沒有約束力，寫成時間戳＋數量：

```text
At 2.0 seconds one or two bolts strike; by 2.8 seconds four or five; by 3.6 seconds six or seven; from 4.4 seconds eight to ten bolts burst every 0.3 seconds, each wave denser than the last, and even the darkest moment between waves holds at least as many bolts as the wave before.
```

### 9.3 真實閃電（照真閃電寫，不是一條光柱）

- 白熱芯＋色暈（`a white-hot core with a magenta glow`）。
- 到處尖銳折角、一路分叉、粗細長短方向都不同、不對稱、沒有直線。
- **同一路徑連閃 2–3 下（回擊）**，然後變細變暗散掉；下一陣從新路徑炸。
- 大中小三級：1–2 道主幹、2–3 道中等、幾十條髮絲細。

```text
Each bolt has a white-hot core wrapped in a magenta glow, bends at sharp jagged angles and forks again and again, every branch a different thickness and length; the same path flashes two or three times in quick return strokes, then thins, dims and dies, and the next burst tears down a new path: one or two main trunks, two or three medium branches and dozens of hair-thin filaments.
```

### 9.4 吸收型能量落點（反制模型預設的火花）

能量灌進角色時：落點不爆、不濺火星、沒有放射星芒，光順著皮膚和衣服往全身漫開（寫法見 `ultimate-moves.md` §5.4）。

### 9.5 魔法煙＝墨滴進水化開

黑色、像墨滴進水裡慢慢化開，只有被電照到的地方透出能量色，裡面有細電與上百顆火星：

```text
the magic smoke spreads like ink dropped into water, black except where the lightning lights it from inside in magenta, threaded with fine electricity and hundreds of tiny sparks
```

### 9.6 光源規則

畫面裡所有的光都由角色、道具、能量發出：**離光源越近越亮越飽和，越遠越暗越灰**；全畫面唯一飽和的顏色是能量色（`the only saturated colour in the frame is magenta`）。與 `impact-frame/forms.md` §5「宣告唯一性」同一招。

### 9.7 次要特效（主特效旁邊的小東西）

開炮除了主炮，還寫四周亂竄的電、往外擴的衝擊波環、熱浪扭曲、碎石滿地飛（v6 第 3 步）。對應 `force-field.md` 四通道。
