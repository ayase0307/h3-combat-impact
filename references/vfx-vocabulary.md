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

H3 沒有 speed ramp 參數，只能用自然語言描述：

| 效果 | 英文寫法 |
|---|---|
| 近乎凍結 | `the action decelerates to a near-freeze for a fraction of a second` |
| 突然恢復常速 | `then snaps back to full speed` |
| 慢動作 | `the moment stretches into slow motion` |
| 子彈時間 | `time slows as the camera arcs around the suspended shards` |
| 殘影疊加 | `three afterimages of the blade overlap in the same frame` |

⚠️ 不要寫 `time stops completely`——模型會真的把整段凍結，後面接不回來。

---

## 7. 色彩腳本（一段只能用一組）

| 名稱 | 主色 | 對比色 | 氣質 |
|---|---|---|---|
| 仙俠青焰 | 青綠 `teal #2E8B7A` | 琥珀橙 `amber #E8892B` | 妖氣 vs 人間燈火（本案例） |
| 血月 | 暗紅 `crimson #8B1A1A` | 冷藍 `steel blue #3A5A78` | 殺伐、悲壯 |
| 金剛 | 金白 `gold #F2C14E` | 墨黑 `ink #101014` | 神聖、壓迫 |
| 雷獄 | 電紫 `violet #7A5CFF` | 鈉黃 `sodium #FFB347` | 科幻、暴烈 |
| 幽潭 | 冰藍 `ice #9FD8E8` | 深綠 `deep green #14342B` | 陰冷、詭異 |

**用法**：主色給主角的能量，對比色給環境光源（燈籠、火、城市）。兩色面積比約 3:7，讓主色成為視覺焦點。

---

## 8. 特效的三個禁用寫法

| 禁用 | 原因 | 改成 |
|---|---|---|
| `lots of particles everywhere` | 沒有方向與密度，變成雜訊 | `sparks spray in a narrow cone away from the impact` |
| `epic explosion` | 模型給通用火球，缺乏設計 | `a ring of white shockwave dust, then a low orange fireball` |
| `glowing aura` | 主體會被光暈吃掉 | `a thin teal rim of flame along the blade's edge` |
