# 震屏、停頓與爆炸時序

> 什麼時候讀：有爆炸、法術轟擊、重擊要寫震屏；或要決定「停頓放哪」「三段式爆炸怎麼排」。
> 衝擊幀的形態與長度見 `forms.md`（本檔不再重複）。

---

## 0. 核心命題（修正版）

> **閃白打造爆發點，衝擊波輸出力量，震屏強化沉浸。**

舊版寫「三者必須對齊在同一幀」——這是 H3 寫法建議，**不是參考片實證**：2.mp4 教學示範的震屏（25.5 s 起約 10 幀，幅度 2→13→1）與閃白（24.6 s）不在同一幀；九尾最大衝擊那一下**不震**（相機鎖死）〔量測〕。

現在的規則：
- 寫在提示詞裡時，閃白與衝擊波放**同一句或相鄰句**（H3 才知道它們是同一事件）。
- **震屏二選一**：① 最大衝擊那一鏡相機鎖死，讓特效把背景推開；或 ② 回原鏡頭第一格猛震三下、一下比一下小、0.5 s 內停穩。**不要閃白配持續震屏**（validator 會擋）。

---

## 1. 震屏（Screen Shake）

### 1.1 為什麼要由強轉弱

恆定震動看起來像相機壞了；**衰減震動**才像被撞了一下。遊戲業界標準（Squirrel Eiserloh, GDC）：

```
trauma ∈ [0, 1]                    // 衝擊量，可累加，上限 1
shake   = trauma²                   // 位移取平方 → 非線性
offset  = max_offset × shake × noise(t)   // 用噪聲，不用隨機
trauma -= decay × dt               // 線性衰減，decay ≈ 1.5–2.0 /s
```

平方＝先急降再拖尾；噪聲＝像被震到而不是電子雜訊；可累加＝連打會疊但不失控。

### 1.2 兩種震法（參考片與教學片都有）

| 類型 | 長度 | 頻率 | 寫法 | 來源 |
|---|---|---|---|---|
| **短抖**（戰鬥片常態） | **2–5 幀**（0.07–0.17 s） | 每次接觸都給；參考動作片 0.56–1.36 次／秒 | `the frame jolts hard for a few frames on the impact and settles almost immediately` | 〔量測〕相對量測，信心中 |
| **計數衰減**（大招回原鏡頭） | 0.5 s 內停穩 | 一個大招一次 | `the camera jolts violently three times, each smaller than the last, settling within half a second` | 〔教學〕v6；〔H3 實測〕d17 |
| 教學示範值 | 0.3 s 回穩 | — | `the shake decays rapidly in amplitude and settles back to steady within a third of a second` | 教學片示範，不是戰鬥片常態 |

成品 37 號每段寫 5 次 `shakes strongly`，量到只有 0.24 次／秒（參考 0.56–1.36）；P01 寫 `one short camera jolt` → 0 次。**震屏要綁在單一接觸事件上、寫出峰值→衰減**，而不是整段 `strongly`。

### 1.3 三個不要

- 不要整段都 `shakes strongly`（暈，而且失去層級）。
- 不要寫 `shakes continuously`／`keeps shaking`（變成手持鏡頭）。
- 不要讓震屏與主體動作同向（震動＋主體運動＝糊）。

---

## 2. 停頓放哪（取代舊的「hitstop 是重量唯一來源」）

| 舊說法 | 量測／實測 | 現在 |
|---|---|---|
| 命中後 hitstop 0.05–0.15 s，寫 `decelerates to a near-freeze for two frames` | 參考片命中後減速只有 26%（中位 1.03）；Seedance 原提示詞寫 `two-frame hit-stop`，命中處 **0 段重複幀**；P01、V05 寫了都沒凍結（命中後運動 ×1.78、×5.9）；EP03 寫了反而被放大成 0.5–1 s | **提示詞不寫** |
| L4 前 0.5–1 s 完全靜止 | EP03 `hangs poised and still for half a second` → 命中前空等 1–3.7 s | 蓄力用動作與光，不寫靜止詞 |
| 慢動作放在 hitstop 之後 | — | 保留為剪輯建議 |

重量改由三件事給：
1. **命中前微停**（組裝時複製 2–10 幀；或寫成「頂住」的畫面，見 `../ultimate-moves.md`）。
2. **命中後切到下一鏡的 0.15–0.25 s reveal**（九尾、特效滿點）。
3. **命中後加速**：`then the camera accelerates with the shockwave`（Seedance 原提示詞；斬擊片衝擊後運動量是前段 1.3–3 倍）。

**組裝端的時間曲線**（教學片 v5 的 Time Ramp 數字；H3 單段做不出，要用 `impact_frame.py ramp`）：接近 100%→250%，接觸瞬間降到 30% 或複製幀，隨即爆發到 300%；重擊後降到 30% **留半拍**給殘骸運動。〔教學，H3 未實測〕

---

## 3. 時序表（一次爆炸，24 fps）

| 時刻 | 幀 | 事件 | 通道 |
|---|---|---|---|
| T+0 | 0–1 | 亮度事件（白閃 P1，或衝擊幀串 P2 的第一張） | 衝擊幀 |
| T+0 | 0 | 震屏峰值（或相機鎖死） | 震屏 |
| T+1 | 1–2 | 環形衝擊波開始外擴 | 空氣 |
| T+2 | 2–8 | 塵土、碎石、玻璃被掀飛 | 物質 |
| T+3 | 3–10 | 熱浪與折射留下波紋 | 空氣 |
| T+0 → T+12 | 0–12 | 震動由強轉弱（短抖 2–5 幀；大招 0.5 s 內停穩） | 震屏 |
| T+8 | 8–20 | 餘燼飄落、煙塵沉降 | 粒子 |

---

## 4. 三段式爆炸配方

```
① 爆發點        衝擊幀（P0–P3 選一）
② 力量輸出      力場四通道：環形波 + 空氣折射 + 物質掀飛 + 光影聯動（最多三通道）
③ 體感          震屏：峰值 → 急速衰減 → 回穩（或鎖死）
④ 餘韻（可選）  餘燼、煙塵、暗部緩慢恢復；大爆後接一個「靜」的極近特寫
```

與打擊結構的關係：打擊結構是「一次交手」，三段式是「一次爆炸」；在「洩」裡放一個完整的三段式。不要讓爆炸吃掉受擊者的反應與沉降。

**大爆前先暗一下**〔教學 v6，H3 未實測〕：電先散掉、畫面暗約 0.3 s，再灌最粗的那一道。亮度反差比「更亮」更有效。

---

## 5. 完整範例（H3 三欄位，P1＋相機鎖死）

```text
integrated_multimodal_description: [Shot 1] 3D CG, cinematic. A low-angle wide shot frames a lone swordsman at the centre of a shattered stone courtyard. The air ahead of him compresses into visible layered sheets, and the background bends through them. [Shot 2] At 00:01.600, the blast core bursts outward at extreme speed and the frame blows out to white at the instant of contact, then snaps straight back; the camera holds a static shot while the shockwave flattens into a ring of concentric ripples racing outward across the courtyard and pushes the background away. Dust and gravel are ripped off the ground and thrown outward, the glass in the surrounding windows bows inward under the pressure, and shadows swing away from the blast. His robe is flattened against his body by the wind pressure, and his hair whips forward a beat late; then the camera accelerates with the shockwave.

overall_soundscape: A low pressure thump builds into a single deafening bass boom, followed by a tearing roar and the brittle crack of stone. Debris patters down across the courtyard as the wind dies.

non_diegetic_music: A single sustained low brass note that cuts to silence at the moment of the blast, then a slow taiko hit at half volume under the settling dust.
```

---

## 6. 常見錯誤

| 錯誤 | 後果 | 修正 |
|---|---|---|
| 只寫「一瞬間閃白」 | 長閃，像燈光故障 | `then snaps straight back`；精準幀數交給組裝 |
| 寫 `for two frames` 期待 2 幀 | 實際 11–45 幀 | 同上；或走 P2／P3 |
| 閃白＋整段持續震屏 | 手持晃動，衝擊被稀釋 | 震屏二選一（鎖死，或回來猛震三下） |
| 震屏沒有衰減 | 1 秒內適應，後面再大也沒感 | 寫峰值→衰減→回穩 |
| 整段都用整幀黑閃 | 壓抑到底 | 整幀黑只給終結／黑尾；壓暗可當標點 |
| 爆炸後立刻切鏡 | 沒有沉降，像斷電 | 加餘燼與煙塵；或切到 0.15–0.25 s reveal |
| 寫 near-freeze 當重量 | H3 放大成 0.5–1 s | 停頓放命中前或切鏡後，在組裝做 |
