# 衝擊幀與震屏：爆炸的時間設計

## 0. 核心命題

> **閃白打造爆發點，衝擊波輸出力量，震屏強化沉浸體驗。三者必須對齊在同一幀。**

「對齊」是最關鍵也最常被忽略的一環。三者差 2 幀，質感就散了。

---

## 1. 衝擊幀（Impact Frame）

### 1.1 四種形態

| 形態 | 視覺 | 適用 | 情緒 |
|---|---|---|---|
| **白閃** | 全畫面過曝至純白 | 能量釋放、爆炸、光束 | 爆發、擴張 |
| **黑閃／負片** | 全畫面轉黑或反色 | 吸收、重擊、破防、死亡 | 壓抑、終結 |
| **單色剪影** | 高對比純色剪影 + 速度線 | 招式命中、必殺 | 定格、儀式感 |
| **漫畫格** | 整幀去飽和成黑白 + 全 360° 放射線 | 高速斬擊、劍客對決 | 銳利、專業感 |

多數教學只教白閃。**黑閃是被低估的一招**——用在最後一擊或破盾時，比白閃更狠，因為它「收回」了光。

### 1.1.1 漫畫衝擊格：第四種裝置（實測蒸餾 + 實跑驗證）

**這是「風格跳轉」事件，不是「亮度」事件。** 兩者的模型行為完全不同，寫法也不同。

| 項目 | 漫畫衝擊格 | 爆白 |
|---|---|---|
| 發生的事 | 整幀去飽和 → 純黑白 | 整幀變亮 |
| 放射線 | **全 360° 放射**，非單方向拖尾 | 無 |
| 參考片幀數 | **2 幀（30fps 下 67 ms；24fps 取 2 幀＝83 ms）** | 1–2 幀 |
| 後接 | **1–3 幀純黑**（格間黑邊） | 直接回原畫面 |

實測（42.6 秒 / 1278 幀參考片）：10 個漫畫格中 **9 個剛好 2 幀**，全部 24/24 角度桶全滿（證明是全向放射線，不是拖尾）。

**三段式序列**（本片出現 7 次，是可寫成提示詞的固定節奏）：

```text
[Shot 3] At 00:01.600, the frame cuts to a black-and-white manga panel for two frames:
a solid white core at the point of contact with clean radial speed lines bursting in
every direction, the fighter crushed into a solid black silhouette, then one frame of
black, then the colour snaps back.
```

**關鍵：提示詞要明確寫「這格變黑白」，不能只寫「閃一下」。** 單色剪影與漫畫格是兩個不同的東西——前者保留單一彩度，後者是整幀去飽和。

#### ⚠️ 實跑驗證：裝置成立，但「2 幀」控不住

同一段提示詞實跑 8 秒（960×544、24fps、192 幀），量測每一幀的飽和度（`signalstats.SATAVG`）：

| 指標 | 未套用 skill | 套用 skill |
|---|---:|---:|
| 最低 SATAVG | 17.4 | **0.0**（完全去飽和） |
| SATAVG < 12 的幀數 | **0** | **44** |
| YAVG 動態範圍 | 82.4 – 124.8（**43 階**） | 16.0 – 193.7（**178 階**） |

**漫畫格確實生成了**，而且生成得很標準：整幀去飽和、純黑剪影、全向放射線。
**但幀數完全不受控**——寫 `for two frames`，實跑出 **23 幀（958 ms）與 21 幀（875 ms）**，
是指定值的 12 倍。同一個提示詞裡只寫了一次，卻在兩個不同時段各發生一次。

#### 兩條實務結論

**① 把漫畫格當成「一個獨立鏡頭」，不要當成「動作鏡頭裡的一個从句」。**

`for two frames` 這個寫法對**閃白**有效（既有實測），但對**整幀去飽和**無效——
模型把「cut to a black-and-white manga panel」理解成「切到一個黑白風格的鏡頭」，
所以給了整整一秒。把它寫成獨立的 `[Shot N]` 並給明確時間碼，語意才對得上。

**② 不寫「then one frame of black」。**

實跑的第二次發生，模型把整個場景去飽和了 **21 幀，而且角色完全不見**——
只剩一片灰白的雪林。`then one frame of black` 這句把「回彩色」的時機一起拖長了。

**想要 2 幀的精度，只能在後期剪。** H3 做不出 2 幀（約 70–83 ms）的漫畫格；
它能做出「一個 0.5–1 秒的黑白風格插入鏡頭」。寫提示詞時就該把它當成**一個鏡頭**來規劃，
而不是當成一個兩幀的插入格。

### 1.1.2 不爆白也能有衝擊感（3D CG 實測）

另一支 3D CG 參考片（30.1 秒 / 723 幀）**全片零爆白幀**——逐幀亮度極值 35.3–198.1，沒有任何一幀接近純白，也沒有 1–2 幀插切。

它用三種東西取代爆白：

| 裝置 | 描述 | 佔比 |
|---|---|---|
| 接觸點局部星芒 | 只有撞擊點炸開，其餘畫面不動 | 最高頻 |
| 背景整體徑向拖影 | 整個背景被衝擊波推開 | 次高 |
| 橘→白→青綠三段色彩遞進 | 衝擊點的顏色變化歷程 | 常見 |

**所以「衝擊幀」不是只有閃白一條路。** 3D CG 風格可以完全不用爆白，改用「接觸點局部星芒 + 背景徑向拖影」。

> 但要小心：**背景徑向拖影容易被模型讀成「整個畫面在動」，主體反而糊掉。** 寫的時候要明確點名是背景：`the background behind them is pushed outward into radial streaks`。

### 1.1.3 破壞用「發光裂紋網」而不是碎塊飛散

同一支 3D CG 片裡，受力面（混凝土板）**不是碎散，而是沿受力點長出會發光的橘色裂紋網，交會處燒成白熱節點**，另有火星成串飄散。

```text
❌ the concrete slab shatters into flying chunks
✅ glowing orange cracks spread across the concrete slab from the point of impact,
   the intersections burning to white-hot nodes, and sparks trail off in strings
```

碎塊飛散是預設答案，模型最常給。裂紋網是「能量沿材質蔓延」，看起來更有技術含量。

### 1.1.4 多階段衝擊序列與墨爆（蒸餾自參考片；水墨已 H3 實跑，後製序列已實測，見下）

> 來源：斬擊光影打鬥 7.80s／39.00s、筆墨風格打鬥 0.6–4.3s（逐幀條目視；hit stop 為「無證據」，見下）。

**衝擊不是一格，是 3 階段 × 各 2 幀的序列**（30fps 參考片，約 200 ms；換成 H3 24fps＝6 幀≈250 ms）：

```text
白放射 2f → 黑白漫畫放射 2f → 主色（藍/金）放射 2f → 回常態
高潮版（39s）：漫畫放射 → 白 X 閃電 → 黑底能量剪影 3f → 暗場景 2f → 白色漫畫爆
```

- 黑底剪影那 3 幀不是靜止殘影，剪影形狀會變。H3 單段無法穩定控制 2 幀精度，**走後製**：`impact_frame.py composite` 連續呼叫 3 次，`--at` 每次加 0.083（見 `impact-frame-post.md` §2.1）。
- **實跑**：水墨 T2VA 的第二鏡確實出現放射墨爆（light 末段 71%、HQ 52%）；三階段序列走後製已驗證（`impact-frame-post.md` §2.1）。
- **hit stop 證據不足**：斬擊光影 mpdecimate 量得 1241/1278 幀為獨立幀，沒有重複幀；不要據此在提示詞裡硬寫「凍結」。

**水墨風用「墨爆」取代凍結**（筆墨風格打鬥）：

| 規則 | 數值 |
|---|---|
| 放射黑墨尖刺，尺度大於人物 | ≤0.4 s |
| 配 1–2 幀亮暗翻轉 | 約 80 ms（亮度 +48 → −43） |
| 頻率 | 每 1.0–1.5 s 一次；單段最多 2 次 |
| 結尾 | 可選：留 ≥0.5 s 墨散靜止（參考片如此）。⚠ 這會壓低「末 2s ÷ 中段」：H3 實跑水墨 HQ 只有 52%，要過 60% 就改成末鏡仍在動作中 |
| 重量來源 | 環境（石柱崩裂、碎石）＋紅綢甩出，不是凍結 |

```text
a radial burst of black ink spikes larger than the figures erupts from the point of impact for under half a second,
the frame flips to white then black for one frame each, and the ink disperses
```

### 1.2 幀數：唯一的硬規則

| 幀數 | 效果 |
|---|---|
| 1 幀 | 最銳利，像被電到 |
| 2 幀 | 標準，最通用 |
| 3–4 幀 | 開始像「閃光」，不再是「衝擊」 |
| 5 幀以上 | 變成燈光故障 |

**必須寫幀數。** 中文的「一瞬間」對模型沒有約束力，它會給 0.3–0.5 秒。

```text
for two frames the entire frame blows out to pure white
for one frame the image inverts to a black silhouette against white
```

### 1.2.1 強事件 vs 弱事件（實測修正）

`for two frames` **不是萬用藥**。它只在「強事件」上生效：

| 事件類型 | 例子 | 2 幀爆閃 | 正確做法 |
|---|---|---|---|
| **強事件** | 爆炸、重擊、破防、撞牆 | ✅ 會生成 | 直接寫 `for two frames` |
| **弱事件** | 袖子擋刀、手掌發光、劍刃亮起、眼神變化 | ❌ 被平滑插值抹掉 | 改成**持續附著**或**獨立鏡頭** |

原因：模型的時序生成傾向平滑插值，一個孤立 2 幀的異常值會被當成噪聲抹平。強事件本身有物理衝擊支撐，異常值能被保留下來；弱事件沒有，就消失了。

**弱事件的兩種正確寫法：**

```text
// 持續附著：讓它成為場景裡唯一的光
a cold silver-blue light runs along the full length of the sleeve and stays lit,
the only cold light in the frame

// 獨立鏡頭：把 0.4 秒單獨給它，不要混在連續動作裡
[Shot 3] At 00:03.000, the camera cuts to a close-up. For two frames the frame blows out to white.
```

**診斷訊號**：如果生成結果裡完全找不到那一幀閃光，先問「這是強事件還是弱事件」，而不是加大形容詞。

### 1.2.2 能量色被場景吃掉

寫「冷色能量」但場景是暖光海（大量燭台、火把、日落）時，能量會消失——模型的照明優先級是場景既有光源。

三種解法，按效果排序：

1. **宣告唯一性**：`the only cold light in the frame`（最有效，一句話）
2. **拉長持續時間**：`stays lit` 取代 2 幀閃光
3. **提高面積**：從「一線」改成「整條袖子」「整把刀」

**不要**用「更亮的藍」來解決——亮度比不過場景主光，只會變成白色。

### 1.3 衝擊幀的完整結構（不只是閃白）

一個合格的衝擊幀鏡頭包含五件事：

| 元素 | 作用 | 寫法 |
|---|---|---|
| 時機 | 綁定在接觸幀 | `at the moment of impact` |
| 爆閃 | 爆發點 | `for two frames the frame blows out to white` |
| 迸發 | 方向與速度 | `the blast core bursts outward at extreme speed` |
| 波形 | 力量的形狀 | `the shockwave flattens into concentric rings racing outward` |
| 物質 | 環境證據 | `dust and gravel are ripped off the ground` |

---

## 2. 震屏（Screen Shake）

### 2.1 為什麼要「由強轉弱」

恆定震動看起來像相機壞了；**衰減震動**才像被撞了一下。

遊戲業界的標準做法（Squirrel Eiserloh, GDC）可以解釋這件事：

```
trauma ∈ [0, 1]                    // 衝擊量，可累加，上限 1
shake   = trauma²                   // 位移取平方 → 非線性
offset  = max_offset × shake × noise(t)   // 用噪聲，不用隨機
trauma -= decay × dt               // 線性衰減，decay ≈ 1.5–2.0 /s
```

**三個設計原理：**

1. **平方** — 小撞擊幾乎無感、大撞擊極其暴力。這就是「由強轉弱」的本質：不是等速變小，是**先急速下降再拖尾**。
2. **噪聲（Perlin）而非隨機** — 隨機會抖成電子雜訊；噪聲有連續性，看起來像「被震到」。
3. **可累加、上限 1** — 連續多次撞擊會疊加，但不會失控。

### 2.2 H3 的寫法

模型沒有 trauma 參數，只能用自然語言逼近。**必須交代三件事：峰值、衰減、回穩時間。**

```text
the camera shakes strongly at the moment of impact, the shake decays rapidly
in amplitude and settles back to steady within a third of a second
```

| 強度 | 寫法 | 適用 |
|---|---|---|
| 輕 | `the camera shakes slightly` | 腳步、擦身、輕擊 |
| 中 | `the camera shakes` | 一般命中 |
| 強 | `the camera shakes strongly` | 重擊、爆炸 |
| 極 | `the camera jolts violently, then decays within a quarter second` | 必殺、核級爆炸 |

**時長參考**：0.3 秒回穩是標準值；0.15 秒 = 極短促的重擊；0.5 秒 = 大規模災難。

### 2.3 三個不要

- 不要整段都 `shakes strongly`（觀眾暈、且失去層級）
- 不要寫 `the camera shakes continuously`（變成手持鏡頭）
- 不要讓震屏與主體動作同向（震動 + 主體運動 = 糊）

---

## 3. hitstop：衝擊幀的隱形搭檔

遊戲文獻的共識值：

- hitstop **0.05–0.15 秒**（超過 0.15 秒開始拖沓）
- 與震屏**同時觸發**，震屏峰值落在 hitstop 結束那一幀
- 慢動作放在 hitstop **之後**，不是之前

換算 24 fps：0.05–0.15 秒 = **1.2–3.6 幀**。

**所以 `for two frames` 是精準的，`for a moment` 是模糊的。**

在 H3 中的對應寫法：

```text
the action decelerates to a near-freeze for two frames, then snaps back to full speed
```

---

## 4. 時序表（一次爆炸的完整節拍）

以 24 fps 計：

| 時刻 | 幀 | 事件 | 通道 |
|---|---|---|---|
| T+0 | 0–1 | 全畫面閃白，爆心過曝 | 衝擊幀 |
| T+0 | 0 | 鏡頭開始劇烈震動（峰值） | 震屏 |
| T+1 | 1–2 | 環形衝擊波開始外擴 | 空氣 |
| T+2 | 2–8 | 塵土、碎石、玻璃被掀飛 | 物質 |
| T+3 | 3–10 | 熱浪與折射留下波紋 | 空氣 |
| T+0 → T+7 | 0–7 | 震動幅度由強轉弱（0.3 秒衰減） | 震屏 |
| T+8 | 8–20 | 餘燼飄落、煙塵沉降 | 粒子 |

**注意**：衝擊幀只有 1–2 幀，但它決定了整個爆炸的「有沒有張力」。這 80 毫秒是性價比最高的 80 毫秒。

---

## 5. 三段式爆炸配方

```
① 爆發點（1–2 幀）     衝擊幀：全畫面閃白 + 爆心過曝
② 力量輸出（6–12 幀）   力場四通道：環形波 + 空氣折射 + 物質掀飛 + 光影聯動
③ 體感（0.3 秒衰減）    震屏：峰值 → 急速衰減 → 回穩
④ 餘韻（可選）          餘燼、煙塵、暗部緩慢恢復
```

### 與六拍結構的關係

| 六拍 | 三段式 | 說明 |
|---|---|---|
| 蓄 | — | 三段式不管蓄力，只管爆炸本體 |
| 觸 | ① 爆發點 | 完全對應 |
| 停 | ① 尾端 | 衝擊幀就是 hitstop 的視覺化 |
| 洩 | ② 力量輸出 | 力場四通道是「洩」的完整版 |
| 退 | ③ 體感 | 震屏衰減對應受擊者延遲反應 |
| 收 | ④ 餘韻 | 對應 |

**六拍是「一次交手」的結構，三段式是「一次爆炸」的結構。** 兩者可嵌套：在六拍的「洩」拍裡，放一個完整的三段式爆炸。

---

## 6. 完整範例（H3 三欄位）

```text
integrated_multimodal_description: [Shot 1] 3D CG, cinematic. A low-angle wide shot frames a lone swordsman at the centre of a shattered stone courtyard. The air ahead of him compresses into visible layered sheets, and the background bends through them. [Shot 2] At 00:01.600, the blast core bursts outward at extreme speed. For two frames the entire frame blows out to pure white; the camera shakes strongly at the moment of impact, the shake decays rapidly in amplitude and settles back to steady within a third of a second. The shockwave flattens into a ring of concentric ripples racing outward across the courtyard. Dust and gravel are ripped off the ground and thrown outward, the glass in the surrounding windows bows inward under the pressure, and the whole scene's lighting shifts in step with the energy as shadows swing away from the blast. Volumetric dust is dragged into curling spirals behind the wave. His robe is flattened against his body by the wind pressure, and his hair whips forward a beat late.

overall_soundscape: A low pressure thump builds into a single deafening bass boom, followed by a tearing roar and the brittle crack of stone. Debris patters down across the courtyard for several seconds as the wind dies.

non_diegetic_music: A single sustained low brass note that cuts to silence at the moment of the blast, then a slow taiko hit at half volume under the settling dust.
```

---

## 7. 常見錯誤

| 錯誤 | 後果 | 修正 |
|---|---|---|
| 只寫「一瞬間閃白」 | 模型給 0.5 秒長閃，像燈光故障 | 寫 `for two frames` |
| 閃白與震屏分在不同鏡頭 | 兩者不對齊，質感散掉 | 放同一鏡頭同一子句 |
| 震屏沒有衰減 | 觀眾 1 秒內適應，後面再大也沒感 | 加 `decays ... within a third of a second` |
| 整段都用黑閃 | 情緒壓抑到底，失去起伏 | 黑閃只留給最後一擊 |
| 爆炸後立刻切鏡 | 沒有沉降，像斷電 | 加 8–20 幀的餘燼與煙塵 |
| 慢動作放在 hitstop 之前 | 節奏倒錯，力量被提前洩掉 | 慢動作永遠在 hitstop 之後 |
