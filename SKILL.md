---
name: h3-combat-impact
description: Use when writing, revising, directing, or rendering MiniMax H3 / Hailuo (海螺) video prompts for action, combat, wuxia/xianxia, monster/mecha, VFX-heavy or impact-driven shots. v4.0 dual-track activation — Track A (silent auto-enhance, no menus) whenever a user asks to generate or edit a prompt or video involving 打鬥, 武俠仙俠, 刀劍兵刃, 怪獸機甲, 爆氣鬥氣, 力場衝擊波, 大招特效 or 高速追逐 and already gives clear characters / scene / action intent without naming the skill; Track B (interactive staged director with a mandatory timeline-outline review gate before any English prompt or GPU render) when the user names h3-combat-impact or asks to 用武戲技能設計, asks how the skill works or what it can do, or only gives reference images or a vague idea such as 幫我拍一段帥氣打鬥. Also when the user asks for 打擊感 / 力度 / 拳拳到肉, 打鬥特效, 招式編排 / 動作設計 / 高速打鬥, 衝擊幀 / impact frame, 震屏, 力場 / 空氣扭曲 / 衝擊波, ComfyUI-Dials / 武戲滑塊 / MAIDialRack / De-rope, or wants to reverse-engineer and recreate a fight reference video in H3 format.
agent_created: true
---

# H3 打鬥導演與武戲執行技能（v4.0 雙軌運作架構・相位雙軌與物理防滑版）

把「動作合乎真實步態力學、打得拳拳到肉、出片極致銳利且 100% 鎖美型顏值」整合成一條從**上游導演編排（姿態—位移相容律＋離散步態三拍）→ 雙語同步編譯與防滑閘門 → 中游 `PRISM + SelfLiftH3Sampler`（一採 `P7/P8` 相位正負雙軌 `MAIDialRack` ＋ 二採 `--hires-dials phase-motion` 解耦精修）→ 量化與貼地滑行驗收**的完整 Agent 工作流。

> **核心鐵律**：① 先導演戰鬥，再寫提示詞；接地靜態姿態（跪／蹲／馬步）嚴禁同鏡寫衝刺平移並必掛 `--anchor` 釘樁防滑，主動進攻嚴禁濫用 `slide/skid`；② 雙人實戰黃金鏡長 **`2.2–2.8s`（15 秒 5–6 鏡）**，留足幀數演完跨步與轉胯；③ 美型國漫／AI 漫劇特寫走 **A 檔冷靜微表情＋`--anchor`**；④ 出片主力走 **`--engine selflift --preset P7/P8 --hires-dials phase-motion`**，精準對沖 `h3_storm` 的 `+0.375` 共線運動洩漏。

---

## 第零階段：雙軌啟動路由（v4.0，收到訊息先判斷要不要停下來問）

完整話術、四大維度選項與《影片內容與時間軸主要動作概要》模板見 **`references/interactive-director-flow.md`**。

| 軌道 | 觸發條件 | 運作行為 |
|---|---|---|
| **軌道 A · 靜默自動增強** | 日常對話中要求生成／修改含打鬥、武俠仙俠、刀劍兵刃、怪獸機甲、爆氣鬥氣、力場衝擊波、大招特效、高速追逐的提示詞或影片，**已給明確角色／場景／動作意圖、未點名詢問技能** | 零打擾：不彈選單，內部套用姿態—位移防滑律、9 大載體路由、A 檔冷靜微表情、防動態破圖身體機制句法、雙語 1:1 切點同步與 `validate_prompt.py`，直接交付雙語提示詞與建議渲染指令（不主動啟動 GPU） |
| **軌道 B · 互動式分階段導演** | ① 點名本技能（`h3-combat-impact`、「用武戲技能幫我設計…」）② 詢問技能用法／功能 ③ 只丟參考圖或模糊想法（「幫我拍一段帥氣打鬥」） | 三階段閉環：**階段 1** 四大維度輕量選項（附推薦預設，可秒選）→ **階段 2**《影片內容與時間軸主要動作概要》**強制審閱閘門**，以「請問同意照這份分鏡概要推進，還是對哪幾秒的招式、鬥氣特效或勝負結果有調整建議？」停下 → **階段 3** 確認後才編譯雙語稿、跑 `validate_prompt.py --check-sync` 0 FAIL，再交付或呼叫 `render_comfy.py` |

**裁決規則**：點名技能但需求已講清楚 → 仍走軌道 B，階段 1 預填成一行確認，**階段 2 閘門絕不跳過**（「你決定」也一樣）；只有使用者明確說「不用給我看概要，直接出」才改走軌道 A。軌道 B 閘門通過前，**嚴禁輸出長篇英文 Prompt 或啟動 GPU 算圖**。

> 名詞對照：軌道 A／B（要不要停下來問）≠ 模式 A／B（原創 vs 逆向，見 1.1）≠ A 檔／B 檔（表情分檔）；軌道 B 的選項寫成 `1-A … 4-B`，素材情境寫成 `S1 … S6`。

---

## 第一階段：入口與時長路由（先決定怎麼走，再動筆）

### 1.1 雙入口路由（原創 vs 逆向衍生）

| 使用者狀態 | 入口模式 | 做法 |
|---|---|---|
| 給了明確角色/場景/需求 | **模式 A · 原創導演** | 軌道 A 直接執行四階段漏斗，不問廢話（點名技能時走軌道 B 預填） |
| 給了參考圖但未說明方向 | **軌道 B 階段 1** | 依素材情境 S1–S6 換算推薦值，再問四大維度（見 `references/guided-mode.md`、`interactive-director-flow.md`） |
| 給了參考打鬥影片要求拆解或復刻 | **模式 B · 逆向＋衍生** | `ffprobe`/`ffmpeg` 抽幀與 `measure_motion.py --fps24` 拆解 → 補缺資產 → 產出 **1 復刻 + 2 衍生** 三方案並列一採抽卡（見 `references/reverse-and-remix.md`） |

### 1.2 時長優先路由（先於段落格式）

| 時長 | 結構 | 核心原則 |
|---|---|---|
| **約 15 秒（預設）** | **五段狀態接力** | `0–3s 即時搶攻 → 3–6s 變軸首中 → 6–10s 技術逆轉 → 10–13s 封鎖折返 → 13–15s 三拍終結` |
| **≤10 秒** | **四段短時長** | `即時搶攻 → 接觸後變線 → 持續追擊與攻守轉換 → 進行中的切出或指定結果`（**禁硬塞五段終局**） |
| **>15 秒多段拼接** | **三表先行** | 先交節拍表／狀態帳本／接縫表再逐段寫（見 `references/segment-continuity.md`） |

**可疊加開關 — 無停頓連續模式（No-Pause / ULTRA_SPEED）**：
需求含「無蓄力」「無停頓」「不停」「全程連打」「超高速」時，在任一時長結構上疊加：快慢只透過攻擊頻率、位移、切鏡密度與鏡頭速度表現；**嚴禁**角色停住、蓄力、站定、凝視、收勢、制動或靜態擺姿；每鏡結尾必須已觸發下一動作。

### 1.3 格式與參考圖模式選擇

| 需求 | 模式／格式 | 規則 |
|---|---|---|
| 只要保留角色與場景外觀、自由構圖與 16:9 畫幅 | **Ref2VA 六欄位**（預設） | `<Subject N>` 搭配 9 類特徵鎖定＋3 詞材質錨（見 `references/ref-identity-lock.md`） |
| 必須鎖死原圖構圖作為首幀或特效插入鏡 | **I2VA / FL2VA 三欄位** | 必寫官方首行對齊句（見 `references/output-format.md`） |
| 切點要準、要跑本機 ComfyUI 與 validator | **官方骨架**（預設） | `[Shot 1]` 無時間碼，後續 `[Shot N] At MM:SS.mmm,` 嚴格遞增（三派決策見 `references/formats.md`） |

---

## 第二階段：上游導演內核（絕不跳過，防止換皮套招）

完整條文見 **`references/fight-directing-contract.md`**，撰寫前必須在內部靜默完成三件事：

### 2.1 五級事實優先級與資產零推斷帳本
1. 衝突裁決順序：`使用者明確指定 → 參考圖可見事實 → 已確認角色習慣 → 維持連續性最小補全 → 導演原創`。
2. **武器與能力零推斷**：圖中沒有且未指定的武器、超自然能力不得新增；無武器角色全程徒手；雙方裝備與能量色嚴禁互相污染。
3. **單人圖補對手**：僅一張單人圖但要求雙人對打時，補一名「最小化輪廓徒手對手」並於中英文稿同步註明。
4. **參考圖職責鎖定**：動作起點圖不強迫復刻原構圖；角色圖不繼承原背景與站姿；場景圖只鎖建築／材質／光源／地形（不鎖死原始機位），**場景圖內嚴禁有人**。

### 2.2 九大戰鬥載體自動路由與非對稱攻防
依每個主體可見資產選唯一主載體（最多組合已具備之兩項），**嚴禁把不同載體寫成同一套劍法**：
- **刃器**（斬刺挑格滑刃）／**長柄**（中線壓迫、桿身慣性、被貼身不利）／**鈍器**（砸壓撞大幅擊退）／**遠程**（彈道、遮擋、掩體破壞）／**徒手**（拳掌肘膝摔投，**對持械禁裸手硬接鋒刃**）／**能力型**（必寫來源部位、方向、接觸與殘留，禁無源光球對轟）／**飛行生物**（振翼升力轉彎半徑）／**四足或巨獸**（蹬撲撕咬甩尾＋尺度參照，見 `references/monster-scale.md`）／**機械載具**（依可見推進器、關節與裝甲動作）。

### 2.3 三條結構鐵律＋九環因果鏈＋細節保真
1. **三條結構鐵律**（優先於一切特效）：① **必須有交換與逆轉**（弱勢方至少反打命中一次）② **把空間壓小**（柱廊／台階／斷崖逼出連續互動）③ **給出不可逆後果**（斷柱、裂地、甲碎、兵器脫手）。
2. **九環完整因果鏈**：每個關鍵攻防交換滿足 `起勢/重心 → 加速 → 明確攻擊線 → 接觸或險些命中 → 合理應對 → 形變/反震 → 沿力線位移 → 環境結果 → 下一動作觸發`。**每次切鏡至少繼承 4 項狀態**（位置／朝向／速度／高度／資產狀態／受擊狀態／環境餘波）。
3. **開局與收尾硬規則**：
   - 首接觸 ≤ 0.5 秒（拒絕站著對視開場；英文 `[Shot 1]` 可補 `First contact occurs within the opening half-second.`）。
   - H3 末尾 1–2 秒會自動減速：末鏡不超過總長 30%、選中景且保持進行中位移；實片剪輯時視需要裁掉尾端 1.0–1.5 秒。
4. **四項細節保真**：
   - **招式多樣性與三高度**（`references/choreography.md`、`move-library.md`）：15s 刀路上限 8 次，補踢擊／拳肘／真摔（非僵持 lock）／下盤；三招涵蓋上中下三高度，每招寫目標。
   - **肌肉微表情與顏值分檔**（`references/facial-performance.md`）：臉部特寫必選對分檔——**A 檔美型克制（國漫／AI 漫劇預設）**用「冷靜壓制詞」（`calm cold expression, smooth relaxed brows, softly closed lips`＋細汗／髮絲）壓住 H3 戰鬥先驗防齜牙醜臉；僅魔獸／粗獷反派用 **B 檔咆哮詞**。禁只寫 `eyes narrow` 或情緒形容詞。
   - **力場四通道**（`references/force-field.md`）：一次最多開三通道，優先序 `空氣折射 > 物質衣料碎石 > 全域光影 > 粒子`。
   - **奇觀不對稱構圖**（`references/ultimate-move.md`）：大招禁背景正中對稱奇觀，改為「偏軸掃出＋主體踏入奇觀位移」。

### 2.4 節奏模式速選表（三選一，不可混用）

| 模式 | 節奏單位 | 8 秒鏡數（中位鏡長） | 本地 Pika 6 步實測提示 |
|---|---|---|---|
| **六拍打擊**（重擊／單次交手） | 一次交手（蓄→觸→停→洩→退→收） | 4–5 鏡（1.2–2.0s） | 單鏡 2.3–2.9s 最能演完完整攻防弧線 |
| **連續對轟**（近身纏鬥） | 一次交換（2 幀衝擊→拖影→回彈→再入） | 5–10 鏡（0.6–1.5s） | 一刀三動（A 攻→B 擋→B 反）＋動作鏈動詞 |
| **ULTRA_SPEED**（無停頓高速） | 一個鏡頭（鏡位＋動作＋運鏡＋環境連動） | 10–14 鏡（0.4–0.8s） | 必須配 `ComfyUI-Dials`（P2/P3）＋ De-rope 防糊 |

---

## 第三階段：雙語同步交付與格式驗證

### 3.1 預設交付結構（雙語同步，免強制觸發詞）
除非使用者明確只要中文或只要英文，固定依序輸出：
1. **中文導演母稿**（15s 七段／≤10s 六段，段內標明實際切鏡時間點；不出現 `<Subject N>` 或英文 H3 欄位名）——供人 30 秒內審核動作因果與空間路線。
2. **English H3 Ref2VA Prompt**（單一 code block，區塊內禁任何 Markdown 標題／粗體／清單／中文註解）：
   - 六欄位嚴格依序：`subject_definitions:`、`summary:`、`retention_analysis:`、`detailed_description:`、`overall_soundscape:`、`non_diegetic_music:`（基礎模式用三欄位 `integrated_multimodal_description:` / `overall_soundscape:` / `non_diegetic_music:`）。
   - **時間線 1:1 同步**：中英文鏡頭數、順序、切鏡秒數、資產、勝負與餘波完全一致。
   - **不預設加 `BUNNY`**：僅在使用者明確指定特定 LoRA 觸發詞時才放首行；Pika H3 Flex＋Dials 路線不加額外 LoRA 觸發詞。
   - **無負面提示欄**：避開 `no / not / never / without / instead of / rather than`，全改寫為正面保持句（見 `references/output-format.md`）。
   - **字數預算**：T2VA ≤520 詞、Ref2VA 六欄位 ≤820 詞（長段重要約束前置）。
3. **建議 `ComfyUI-Dials` 執行指令**（附對應 `--preset` 與 `--hit` 秒數，可直接執行出片）。

### 3.2 交付前強制驗證
```bash
python scripts/validate_prompt.py prompt.txt --duration 15
python scripts/validate_prompt.py prompt.txt --duration 15 --check-sync   # 雙語檔額外驗證中英切點同步
python scripts/validate_prompt.py prompt.txt --duration 8 --profile ultra
```
**FAIL 必須全修掉才能交付或送出生成。**

---

## 第四階段：執行層路由（`ComfyUI-Dials` v3.0 相位雙軌 + `SelfLift` 二採解耦 + 防滑驗收）

完整 5376 維向量內積幾何、共線運動洩漏公式 $M_{\text{eff}}$、正負雙軌 `0..1` 推拉與 19 轉盤規格見 **`references/comfyui-dials-guide.md`**。

### 4.1 獨家 Dials 調控四定律（決定何時開什麼、怎麼調）
1. **共線運動洩漏補償（Motion Leakage Law）**：`h3_storm` 與 `h3_motion` 具 **`+0.460` 高度共線投影**（每 `+1.0` storm 偷加 `+0.375` 運動；`space_warp` 偷加 `+0.20`；`aura` 偷加 `+0.17`；`evil_cold` 抵銷 `-0.125`）。地面拆招總等效運動 $M_{\text{eff}}$ **嚴禁常駐超過 `+1.00`**（破 `+1.05` 即觸發平地變斜坡、人物貼地滑雪）。
2. **同盤正負雙軌 `0..1` 推拉（Push-Pull Dual-Rail）**：單列曲線填負值僅為線性外插（無法真定樁或頓幀）。必須以 **`--anchor t0:t1:-0.65`**（定樁防滑／特寫鎖臉）與 **`--hitstop t0:t1:-1.80`**（重擊 `0.25s` 卡肉頓幀＋`+4.8` 閃幀）建立獨立負軌，搭配 **`--burst t0:t1:+0.65`** 建立獨立正軌，各自在 `M ∈ [0, 1]` 精確混合。
3. **快慢雙通道慣性與奇觀盤禁令**：`h3_impact_frame` / `h3_colour_drain` 為 `0.1–0.2s` 快切盤（畫 `0.25–0.35s` 窄脈衝，`+4.6~+5.0`）；`h3_motion` / `h3_storm` / `h3_dramatic_light` 具 `1.0–1.5s` 注意力過渡慣性，須按 **2–5 秒戰鬥相位區段** 給包絡。直線毀滅砲與近身肉搏**嚴禁長開 `P5 (arcane_sigils)` / `P6 (space_warp)`**（防末段退化為 2D 萬花筒或金紋爬臉）。
4. **`SelfLift` 一採／二採解耦（`--hires-dials phase-motion`）**：一採（前 6 步）跑全量 `MAIDialRack` 塑形；二採（後 8 步 `model_hires`）僅繼承正負雙軌 `h3_motion`、拔除光影與風暴盤，同時實現**定樁零滑行＋特寫 100% 鎖顏值＋交鋒極速不打太極**。

### 4.2 主力武戲 Dial 配方速選（`--preset`）

| Preset | 適用場景 | 基底組合與雙軌搭配 |
|---|---|---|
| **P9（雙色刀弧作畫王牌）** | **番劇級雙人冷兵器高燃死鬥** | 實證五滑塊：`motion +0.50` + `ink_wash +0.50` + `storm +0.50` + `dramatic_light +0.90` + `h3_x_silentfilm_cyberpunk +0.40` + `impact_frame +0.35`；配純淨 `PRISM_int8` + `--hires-dials off`（禁掛 `blur_moving_edges_hook <= -1.0` 防 0.4s 鬼畜閃切） |
| **P7（徒手／混合戰）** | 雙人徒手／中近距實戰 | `dramatic_light +1.35` + `storm +0.85` + `evil_dread +0.45`；配 `--burst`（交鋒）、`--anchor`（特寫）、`--hitstop`（頓幀） |
| **P8（大招首選）** | 跪地／站樁開陣接超高速破空主砲 | `dramatic_light +1.40` + `storm +0.80` + `evil_dread +0.55`；開陣配 `--anchor 0:4:-0.65` 釘死防滑，破空配 `--burst 9:15:0.80` |
| **P1 / P2 / P3 / P4** | 純拆招 / 全程追逐 / 簡易重擊 / 慢重巨獸 | 已於 v3.0 校準 `storm` 洩漏（`P2` 淨 $M_{\text{eff}}=+0.925$，禁配跪蹲靜態詞） |
| **P5 / P6（限縮）** | 純結印圓陣 / 瞬時空間傳送 | 內建 75–80% 處強制歸零，禁止用於直線光砲或近戰 |

### 4.3 本機主力出片與量化防滑驗收流水線（`127.0.0.1:8188`）

```bash
# 1. 上游格式、雙語切點同步與防滑步態檢核（0 FAIL 才可送渲染）
python scripts/validate_prompt.py prompt.txt --duration 15 --check-sync

# 2. 主力 SelfLift 14 步 + P7/P8 相位雙軌渲染（一採全 Rack + 二採 phase-motion）
python scripts/render_comfy.py --engine selflift \
  --unet Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors --dmad 0.8 \
  --scheduler simple --steps 14 --transition 6 --lowres-scale 0.6 --chunks 4 --hires-dials phase-motion \
  --preset P7 --burst 0.0:2.5:0.65 --hitstop 2.5:2.8:-1.8 --anchor 7.5:9.0:-0.55 --burst 9.0:12.1:0.65 \
  --prompt prompt.txt --ref hero.png --ref villain.png --ref scene.png \
  --seconds 15 --seed 7101 --stage final --job fight_v3 --out out/fight_v3.mp4

# 3. 生成後運動節拍、靜止對稱、貼地滑行（--footplant）與清晰度驗收
python scripts/measure_motion.py out/fight_v3.mp4 --fps24 --symmetry --footplant
python scripts/measure_sharpness.py out/fight_v3.mp4
```

| 量化指標 | 合格門檻 | 說明 |
|---|---|---|
| 開場 0.8s 運動 | ≥ 中段的 50% | 低於此＝開場對峙過靜 |
| 末 2s ÷ 中段 | ≥ 60% | 低於此＝尾端減速停滯（裁尾 1.0–1.5s） |
| 最長低潮 | ≤ 0.8s | 超過＝無效等待 |
| 峰值格 | ≥ 4 | 跨版本比較最可靠的動作節拍指標 |
| 靜止對稱 | 不出現在高潮鏡 | 出現＝構圖退化為靜止技能展示 |

> **參考片幀率陷阱**：標示 60fps 的素材可能是 24fps 2:3 pulldown；逐幀分析務必加 `-fps_mode passthrough`，跨片比較一律用 `measure_motion.py --fps24`。

---

## 參考檔案與工具索引

### 新增核心（v2.0 – v4.0）
| 檔案 | 內容 |
|---|---|
| `references/interactive-director-flow.md` | v4.0 雙軌運作：軌道 A 靜默自動增強檢核表、軌道 B 三階段話術（四大維度選項→時間軸概要閘門→定稿出片）、《影片內容與時間軸主要動作概要》標準模板與完整對話範例 |
| `references/fight-directing-contract.md` | 上游導演合約：5 級事實優先級、零推斷帳本、9 大載體路由、6 種非對稱攻防、180° 軸線與雙色光軌、姿態—位移防滑律、雙語同步編譯 |
| `references/comfyui-dials-guide.md` | `ComfyUI-Dials` v3.0 完整調用指南：5376 維運動洩漏係數 $M_{\text{eff}}$、19 轉盤速查、P1–P9 配方、正負雙軌（`--anchor/--burst/--hitstop`）、`SelfLift` 一採二採解耦與 De-rope |
| `references/reverse-and-remix.md` | 雙入口工作流：模式 A 原創導演、模式 B 參考片逆向＋1 復刻 2 衍生並列抽卡、一採→二採→三採流水線 |

### 打擊感、編排與保真（既有精華）
| 檔案 | 內容 |
|---|---|
| `references/ref-identity-lock.md` | 參考圖保真：9 類特徵清單、3 詞材質錨、乾淨 3D CG 設定圖規範（避厚塗糊化） |
| `references/impact-design.md` | 六拍細節、力度分級、材質反應、優雅角色姿勢先驗 |
| `references/continuous-brawl.md` | 連續對轟四拍、動作鏈句型、深度錯位、一刀三動、細節插切 |
| `references/ultra-speed.md` | ULTRA_SPEED 模式：四件套、周圍連動清單、鏡頭密度統一表 |
| `references/choreography.md` / `move-library.md` | 招式配額制（刀路上限）、真摔判準、三高度串接、16 招具名庫 |
| `references/facial-performance.md` | 肌肉微表情部位清單、四階段表情、收放對比、生理反應 |
| `references/force-field.md` | 力場四通道模型、三種場型、中英句庫 |
| `references/impact-frame-and-shake.md` / `impact-frame-post.md` / `impact-frame-inline.md` | 衝擊幀四路徑（Dial 脈衝／內嵌多卡閃切／後製合成／爆白）、震屏衰減數學、hitstop |
| `references/shot-five-part-combat.md` / `speed-acceleration.md` / `vfx-choreography.md` / `character-signature-skill.md` | 每鏡五小節（含重心參數）、提速八級與動作密度、特效空間範圍五點骨架、角色×專屬技能重現系統 |
| `references/camera-grammar.md` / `cinematic-camera.md` / `drone-camera.md` | 官方運鏡自然語句、三檔速度與幅度跳級、無人機 8 機位 |
| `references/blade-light-cinema.md` / `ultimate-move.md` / `vfx-vocabulary.md` | 21:9 刃光電影語言、大招不對稱奇觀構圖、中英特效與色彩腳本 |
| `references/segment-continuity.md` / `monster-scale.md` / `fl2va-chain.md` | 多段三表工程、場景破壞換圖、以小打大巨獸尺度、兩段接縫檢查 |
| `references/formats.md` / `output-format.md` / `prompt-templates.md` / `guided-mode.md` / `qa-checklist.md` / `screenplay-format.md` / `remix-pika-route.md` | 三格式決策表、官方欄位契約、模板、引導樹、QA 檢核、REMIX Studio 路線 |

### 執行與驗證腳本
| 腳本 | 用途 |
|---|---|
| `scripts/render_comfy.py` | 本機 ComfyUI 出片引擎：支援 `PRISM + SelfLiftH3Sampler`（14 步）與 Pika 6 步、`MAIDialRack`（P1–P9／`--anchor/--burst/--hitstop`）、`--hires-dials` 解耦、De-rope 與 `ReCaVSR 2x` 2K 超分 |
| `scripts/validate_prompt.py` | 驗證官方格式、時間碼、否定詞、表情肌肉與美型臉防過激（`--face-style`）、招式多樣性、防滑閘門、雙語切點同步（`--check-sync`）；v4.0 加防動態破圖 WARN（空泛打鬥句缺身體機制、`<1.5s` 短鏡堆疊 ≥4 個翻轉旋轉詞）與劇本式（`[參考鎖]…[硬約束]`）檢核 |
| `scripts/render_v3_flagship.py` | 9 套 v3 旗艦漫劇批次渲染（全部 P7/P8/P9 正負雙軌；`--dry` 只看 Dial 運動預算、`--force` 覆蓋重跑） |
| `scripts/measure_motion.py` / `measure_sharpness.py` / `measure_staging.py` / `measure_light_event.py` | 24fps 歸一化運動曲線、靜止對稱（`--symmetry`）、貼地滑行檢測（`--footplant`）、拉普拉斯清晰度、鏡長與光影事件量測 |
| `scripts/compare_clips.py` / `impact_frame.py` / `seam_check.py` | 固定 seed 並排動態圖與運動對照、後製 2 幀衝擊幀合成、接縫死格檢測 |
