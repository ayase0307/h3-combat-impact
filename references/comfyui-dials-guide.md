# ComfyUI-Dials 武戲滑塊 Agent 獨家調控理論與實戰指南（v3.0 相位雙軌與幾何去耦體系）

> **核心定位**：MiniMax H3 是無 CFG 的引導蒸餾模型（負面提示詞完全無效），純文字對「速度倍率、重擊頓幀（Hit-Stop）、定樁防滑、光影張力」的控制存在物理上限。`ComfyUI-Dials` + `ComfyUI-MAINodes`（`MAIDialRack`）透過在 H3 `token_refiner` 輸出端（5376 維空間）直接注入 **~14 KB 無訓練方向向量（Steering Vectors）**，實現「每個潛空間幀（約 1/6 秒）雙分支精準混合」。
>
> **v3.0 核心突破**：徹底摒棄「全片掛單一靜態預設值」的粗放做法，建立基於 **5376 維實測向量內積幾何** 與 **`timecurve.py` 雙分支物理學** 的四大獨家定律，根除「跪姿貼地滑雪」、「萬花筒法陣吞人」、「近戰打太極」三大頑疾。

---

## 1. 四大底層物理與向量幾何定律（Agent 調參必讀內核）

### 定律一：5376 維範數不對稱與「共線運動洩漏律（Collinear Motion Leakage）」

直接解碼本機 19 顆 `.safetensors` 權重張量（`diffusion_model.token_refiner.dials_shift`, `dim=5376`），滑桿 `+1.0` 在不同轉盤上的真實歐幾里得推力 `||v||` 相差超過 **2.3 倍**，且多顆環境／特效盤與 `h3_motion` 存在強烈正相關共線投影：

| 轉盤名稱 | 向量範數 `\|\|v\|\|` | 與 `h3_motion` 餘弦 `cos` | 對 `h3_motion` 等效洩漏係數 | 實戰意義與踩坑機制 |
|---|---:|---:|---:|---|
| `h3_motion` | **65.03** | `+1.000` | **`+1.000`** | 全庫推力最強巨獸；淨等效超過 `+1.05` 即觸發場景重排（平地變斜坡、人物變形滑行） |
| `h3_storm` | **53.05** | **`+0.460`** | **`+0.375`** | 訓練對含 `wind whipping`，每開 `+1.0` 等於偷加 **`+0.375` 運動**！舊版 `motion 0.8 + storm 1.2` 真實運動高達 `+1.25` 必爆滑行 |
| `h3_evil_unhinged` | 59.36 | `+0.242` | `+0.221` | 狂亂撲衝，自帶前撲加速與尖叫 |
| `h3_space_warp` | 52.37 | `+0.247` | `+0.199` | 扭曲地平線並自帶鏡頭旋轉運動 |
| `h3_aura` | 42.92 | `+0.260` | `+0.172` | 爆氣光環，自帶推鏡與爆音（+18 LU） |
| `h3_evil_cold` | 41.59 | **`-0.195`** | **`-0.125`** | 冰冷凝視，自帶凍結屬性，開高會吃掉 12.5% 動作活力 |
| `h3_dramatic_light` | **28.01** | `+0.082` | `~0.000` | 範數最小、與運動幾乎正交，最純淨安全的武戲光影反差增幅器 |
| `h3_arcane_sigils` | **65.56** | `+0.041` | `~0.000` | 全庫最大範數外觀盤；長開必將人物與直線光砲扭成 2D 曼陀羅刺青／對稱日輪 |

> **等效運動總預算公式**：
> $$M_{\text{eff}}(t) = s_{\text{motion}}(t) + 0.375\,s_{\text{storm}} + 0.20\,s_{\text{warp}} + 0.17\,s_{\text{aura}} - 0.125\,s_{\text{cold}}$$
> - **地面紮實拆招／衝刺安全上限**：$M_{\text{eff}}(t) \in [+0.65, +0.98]$（嚴禁常駐破 `+1.05`）。
> - **定點跪姿／馬步蓄力／特寫鎖臉區間**：必須壓至 $M_{\text{eff}}(t) \in [-0.40, +0.05]$！若場景開了 `h3_storm +0.80`（洩漏 `+0.30`），定樁區段必須掛負向錨定軌 `h3_motion -0.30 ~ -0.65` 將洩漏徹底抵銷，否則角色維持跪姿時背景必偷跑成「貼地滑雪」！

---

### 定律二：同盤正負雙軌 `0..1` 推拉架構（Push-Pull Dual-Rail Architecture）

由 `ComfyUI-MAINodes/dials/timecurve.py` 源碼證實：時間曲線在每個潛空間幀執行雙分支線性內插 `v = v0 + M(t) * (v_dial - v0)`。
- **致命誤區**：只有在 **`M(t) ∈ [0.0, 1.0]`** 時才是真實強度；若在一列 `+1.0` 的 `h3_motion` 曲線上畫 `M = -2.0`，底層只是把正向預測反向線性外插，**實測完全無法凍結或定樁**（`LESSONS.md`：外插 `-2` 殘餘運動仍高達 `4.7`，疊加真實負列才降至 `1.0`）！
- **唯一正確解法 — 正負雙軌獨立列**：
  1. **錨定／頓幀負軌（Anchor & Hit-Stop Rail，`strength < 0`）**：
     - **定樁防滑（`--anchor t0:t1:-0.65`）**：用於單膝跪地開劍陣、站定集氣、臉部特寫，釘死腳底與岩石支點，吃掉風暴洩漏。
     - **重擊肉感頓幀（`--hitstop t0:t1:-1.80`）**：用於重拳入腹、雙扇夾死刀刃、重砸破地的 `0.25s` 瞬間，製造動畫級「卡肉頓幀（Hit-Stop）」並同步觸發衝擊閃幀！
  2. **爆發推進正軌（Burst Rail，`strength > 0`）**：
     - **高速交鋒／破空追拍（`--burst t0:t1:+0.65`）**：只在雙足蹬離突進、近身連打、飛彈追尾光束破空時將 `M(t)` 拉上 `1.0`！
  3. **同號多段合併省算力技巧**：`timecurve.py` 中每多一條不同 `points` 的曲線，每採樣步就多跑 1 次完整 DiT forward！`scripts/render_comfy.py` 的 `build_weighted_span_curve()` 會自動將所有負向區段（如 `-0.65` 定樁 ＋ `-0.30` 特寫 ＋ `-1.80` 頓幀）以最大絕對值為 `strength`、各段正規化為 `|s_i| / max_abs ∈ [0, 1]` **編譯成單一負軌曲線**，零外插失真且省下一半 GPU 步數耗時！

---

### 定律三：快切視覺盤 vs 慢變力場盤的時間慣性分流

| 類別 | 代表轉盤 | 潛空間響應速度 | 正確曲線畫法與鐵律 |
|---|---|---|---|
| **快切視覺盤**<br>(Fast-Look) | `h3_impact_frame`<br>`h3_colour_drain` | **極快（`0.1–0.2s`）**<br>跟隨率 `r = 0.93` | 只畫 **`0.25–0.35s` 窄脈衝**；Ref2VA 強度嚴守 **`+4.6 ~ +5.0`**（`≥+5.5` 易爆全黑裂紋吞沒角色或洩漏參考原圖）；必加 `"audio": "protect"` |
| **慢變力場盤**<br>(Slow-Field) | `h3_motion`, `h3_storm`<br>`h3_dramatic_light`, `h3_aura` | **慢慣性（`1.0–1.5s`）**<br>鄰區滲透約 20% | **嚴禁畫 `<0.5s` 碎拍**（會被時間注意力抹平）；必須按 **2–5 秒戰鬥相位區塊（蓄勢段／交鋒段／破空段）** 給包絡，且轉折提前 `0.25–0.35s` 起坡 |
| **奇觀法陣盤**<br>(Mandala Risk) | `h3_arcane_sigils`<br>`h3_space_warp`<br>`h3_psychedelic` | 高奪權性<br>（範數 `52–65`） | **嚴禁恆定開啟或尾端保持 `1.0`**（必導致末段退化成 2D 旋轉萬花筒／金紋爬滿臉，如 `rep05` 與 `rep04_v1`）；直線毀滅砲與實戰肉搏一律禁用，改走 **P7 / P8**！ |

---

### 定律四：`SelfLiftH3Sampler` 一採／二採階段解耦律（`--hires-dials phase-motion`）

本機冠軍管線（`PRISM_int8 + DMAD 0.8 + SelfLift 14步, transition=6, lowres=0.6`）分為兩個物理階段：
1. **一採（Steps 0–5，`0.6x` 低解析骨架期）**：掛載完整 `MAIDialRack`（含 `dramatic_light`、`storm`、`evil_dread`、雙軌 `motion`、`impact_frame`，所有曲線 `steps: 6` 精準跑完一採即停，不浪費算力）。
2. **二採（Steps 6–13，`1.0x` 原生高解析精修期 `model_hires`）**：
   - 若設 `keep`：`storm` + `dramatic_light` + `impact_frame` 在高解析細化期持續猛推，會把人臉推成猙獰鬼臉。
   - 若設 `off`：雖然 100% 鎖住絕美顏值，但近身快打會被無 Dial 的二採「修平速度」而略顯溫吞。
   - **v3.0 終極預設 `--hires-dials phase-motion`**：二採 `model_hires` **僅精準繼承「正向 Burst 軌 ＋ 負向 Anchor/Hit-Stop 軌」兩列 `h3_motion`，且將二採曲線 `steps` 鎖定為 `2`**（因 `SelfLiftH3Sampler` 傳入切片後之 `sigmas[transition_step:]`，二採僅剛抬升完的前 2 步需雙分支鎖定動態邊界，後 6 步微紋理期自動退回 `1×` 單次 DiT 呼叫，每支 15s 成片現省 ~470 秒）！實測同時達成：**定樁段零滑行 ＋ 特寫段 100% 絕美鎖臉 ＋ 交鋒破空段極速銳利 ＋ 算力減半**！

---

## 2. 八組武戲 Dial 預設配方與何時選用決策表

| 代號 | 適用戰鬥場景 | 基底常駐盤 | 時間曲線軌道搭配（建議 CLI） |
|---|---|---|---|
| **P9（番劇刀劍首選）**<br>**左眼 5.0 雙色刀弧盤** | **頂級雙人冷兵器高速對決、清晰刀弧軌跡、破防重斬** | `motion +0.50`, `ink_wash +0.50`（強化凌厲刀弧筆觸）<br>`storm +0.50` ($M_{\text{eff}}=+0.69$), `dramatic_light +0.90`<br>`experimental/h3_x_silentfilm_cyberpunk +0.40`（微開強化紅藍冷暖反差，禁超 +0.8）<br>`impact_frame +0.35` | 搭配純淨 `PRISM_int8 + DMAD 0.8` 與二採 `--hires-dials off`（清晰度達 `200+`）＋ `--closeup` 鎖特寫。<br>**【實測紅線】**：嚴禁掛 `h3_blur_moving_edges_hook <= -1.0`（實測 `-1.40` 會在 15s 內撕裂出 25 次 0.4s 鬼畜硬切！），亦不掛舊底模 `Bunny_weapon_combatV1`（會注入雙銅鐔夾手與雙臂桶出上框髒特徵） |
| **P7（近戰通用）**<br>**相位雙軌實戰盤** | **雙人徒手／混合近戰、多高度拆招、重擊砸場** | `dramatic_light +1.35`<br>`storm +0.85` (洩漏 `+0.32`)<br>`evil_dread +0.45` | 交鋒段 `--burst t0:t1:0.65`（$M_{\text{eff}}=+0.97$）<br>特寫段 `--anchor t0:t1:-0.55`（$M_{\text{eff}}=-0.23$）<br>鎖刃點 `--hitstop t0:t1:-1.2` |
| **P8（大招首選）**<br>**定樁蓄勢破空盤** | **仙俠萬劍歸宗、站樁／跪地集氣接直線毀滅主砲、巨獸俯衝轟擊** | `dramatic_light +1.40`<br>`storm +0.80` (洩漏 `+0.30`)<br>`evil_dread +0.55` | 跪地／開陣段 `--anchor 0:4.2:-0.65`（$M_{\text{eff}}=-0.35$ 釘死地面防滑）<br>出拳特寫段 `--anchor 4.2:9.0:-0.30`（$M_{\text{eff}}=0.00$ 穩臉）<br>破空光束段 `--burst 9.0:15.0:0.70`（$M_{\text{eff}}=+1.00$） |
| **P1** | 寫實武俠純拆招、含對白過招 | `motion +0.50`, `dramatic_light +1.00` | 無需曲線或僅特寫加 `--closeup` |
| **P2（v3 校準）** | 全程無停頓追逐／無人機穿梭（無跪蹲靜態鏡） | `motion +0.55`, `storm +1.00`, `dramatic_light +1.10` | 常駐 $M_{\text{eff}}=+0.925$（嚴禁配跪蹲靜態詞） |
| **P3（v3 校準）** | 傳統重擊硬碰（簡易單軌版） | `motion +0.45`, `dramatic_light +1.60`, `storm +1.00` | 配 `--hit t0:t1` |
| **P4** | 慢重巨物壓場、重錘 Boss 沉重步伐 | `motion -0.35`, `dramatic_light +1.80`, `evil_dread +0.80` | 沉重遲滯物理感 |
| **P5（限縮脈衝）** | 純結印召喚符文圓陣（非直線砲） | `dramatic_light +1.20`, `evil_dread +0.60` | 內建 `arcane_sigils +1.40` 蓄力後於 80% 處強制歸零防萬花筒 |
| **P6（限縮脈衝）** | 瞬時空間扭曲傳送（非長尾對轟） | `dramatic_light +1.40`, `evil_dread +0.60` | 內建 `space_warp +1.50` 於 75% 處強制歸零 |

---

## 3. 本機 19 顆已安裝轉盤完整實測規格速查

路徑：`<ComfyUI>/models/loras/dials/`（API 填 `dials/<檔名>`）。

1. **動量與物理環境（3 顆）**：
   - `h3_motion.safetensors`（`||v||=65.03`）：靜止凍結 ↔ 狂奔跳躍；雙軌控制核心，避免混掛 `h3_motion_lora.safetensors`（pre-refiner 舊相容檔，不支援時間曲線與 `hold`）。
   - `h3_storm.safetensors`（`||v||=53.05`）：無風平靜 ↔ 狂風飛沙能量弧；帶 `+0.375` 運動洩漏與風聲增益，建議 `0.8–1.0`。
2. **光影與瞬切衝擊（3 顆）**：
   - `h3_dramatic_light.safetensors`（`||v||=28.01`）：平光低反差 ↔ 單一硬主光深影；武戲最穩清晰度與立體感來源，建議 `1.1–1.8`。
   - `h3_impact_frame.safetensors`（`||v||=48.58`）：正常色彩 ↔ 黑白反相粗墨線閃幀；僅限 `0.25–0.35s` 短脈衝，`+4.6~+5.0`（`audio: protect`）。
   - `h3_colour_drain.safetensors`（`||v||=42.35`）：全彩 ↔ 灰階抽色；時停或致命一擊前 `0.3s` 瞬切 `+4.0`（`interp: "step"`）。
3. **奇觀與畫風（5 顆，高奪權性慎用）**：
   - `h3_aura.safetensors`（`||v||=42.92`）：爆氣光環，必開 `audio: protect`，強度 `≤1.8` 防推鏡改臉。
   - `h3_arcane_sigils.safetensors`（`||v||=65.56`）、`h3_space_warp.safetensors`（`||v||=52.37`）、`h3_psychedelic.safetensors`（`||v||=53.71`）：僅限中段短時蓄力後歸零，嚴禁配直線光束或長尾保持。
   - `h3_ink_wash.safetensors`（`||v||=57.88`）：T2VA 水墨有效，Ref2VA 會被彩色設定圖壓回。
4. **反派氣場包 Villainy Pack（8 顆）**：
   - **武戲百搭首選**：`h3_evil_dread`（`+0.4~+0.8`，純環境山雨欲來壓迫感，零傷臉零傷音）。
   - **特定角色氣質**：`h3_evil_sinister`（暗影壓迫，開高傷語音）、`h3_evil_cold`（冰冷無情，帶 `-0.125` 運動抑制）、`h3_evil_unhinged`（狂暴撲擊，帶 `+0.221` 運動推進，`≤0.6`）、`h3_evil_corrupted`（場景腐化做舊）、`h3_evil_creepy`、`h3_evil_seductive`、`h3_evil_impish`。

---

## 4. 標準 Agent 一鍵調用範例（v3.0 雙軌命令）

```bash
# 範例 A：定樁開萬劍 → 正面直拳流星劍雨 → 超音速螺旋主砲破山（P8 + 定樁/爆發雙軌）
python scripts/render_comfy.py --engine selflift \
  --unet Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors --dmad 0.8 \
  --scheduler simple --steps 14 --transition 6 --lowres-scale 0.6 --chunks 4 --hires-dials phase-motion \
  --preset P8 --anchor 0.0:4.2:-0.65 --anchor 4.2:9.0:-0.30 --burst 9.0:15.0:0.70 --hit 9.0:9.3 \
  --prompt examples/v3-manju/rep04_v3_myriad_swords_cannon.txt \
  --ref assets/v3-manju/rep04/taixuan.png --ref assets/v3-manju/rep04/bg_pine_cliff.png \
  --seconds 15 --seed 6401 --stage final --job rep04_v3 --out analysis/v3-manju/dial_lab/rep04_v3_15s.mp4

# 範例 B：雙人近身兵刃高速實戰（P7 + 交鋒 Burst + 重擊 Hit-Stop 頓幀 + 特寫 Anchor）
python scripts/render_comfy.py --engine selflift \
  --unet Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors --dmad 0.8 \
  --scheduler simple --steps 14 --transition 6 --lowres-scale 0.6 --chunks 4 --hires-dials phase-motion \
  --preset P7 --burst 0.0:2.5:0.65 --hitstop 2.5:2.8:-1.8 --burst 2.8:7.5:0.60 \
  --anchor 7.5:9.0:-0.55 --burst 9.0:12.1:0.65 --hitstop 12.1:12.4:-1.8 --burst 12.4:15.0:0.45 \
  --prompt examples/v3-manju/orig01_v3_clocktower_duel.txt \
  --ref assets/v3-manju/orig01/jinyuan.png --ref assets/v3-manju/orig01/heming.png --ref assets/v3-manju/orig01/bg_clocktower.png \
  --seconds 15 --seed 7101 --stage final --job orig01_v3 --out analysis/v3-manju/dial_lab/orig01_v3_15s.mp4
```

---

## 5. 進階機構：何時使用串聯 `hold: true` 或自製 `MAIDialMake`

1. **串聯 Rack 的 `hold: true` 正交剔除**：`MAIDialRack` 支援在列上設 `"hold": true`（從同 Rack 其他 post-refiner 列中正交投影移除該方向），但**同一節點內 `hold` 列不可與 `time` 曲線列共存**。若需對常駐基底做正交去耦，應在圖中先接第一個無曲線 `MAIDialRack`（含 `hold: true`），再串聯第二個掛載 `time` 曲線的 `MAIDialRack`。日常武戲直接用 `render_comfy.py` 的 `--anchor` 負軌即可精準抵銷運動洩漏。
2. **自製 14 KB 專屬轉盤（`DialsMakeDial`）**：僅在 19 顆內建盤無法表達特定材質／筆觸時使用。撰寫 4–8 組除目標特質外**逐字相同**的 `A ||| B` 句子（嚴禁在外觀盤混入 `running / whipping / raging` 等動作詞以免污染運動軸），確認 `pair_agreement_cos > 0.60` 後存檔即刻可用。
