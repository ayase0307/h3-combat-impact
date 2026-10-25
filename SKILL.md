---
name: h3-combat-impact
description: 綜合打鬥技能（MiniMax H3／海螺）：角色招式設計、交手編排、對打交換節拍、特效 VFX 分層、打鬥運鏡、表情、衝擊幀／閃白／漫畫格／hit stop、衝擊波與震屏、參考圖保真、接續生成、組裝變速與後製。凡 H3 提示詞含打鬥、對打、招式、必殺技／大招／絕招、秒殺、變身、法術爆炸、刀光劍氣、特效，或使用者說打擊感不夠、大招沒感覺、招式太慢、要毀天滅地，就載入；與 h3-video-prompting（通用 H3 提示詞）並用，打鬥／招式／特效／衝擊幀以本技能為準。Use for MiniMax H3 / Hailuo combat and action prompts - move design, fight choreography, exchange beats, VFX layering, fight camera, facial performance, impact frames (white flash, manga panel, burst strip), shockwave, screen shake, hit stop, blade light, one-hit kill, transformation, ultimate or special moves, reference identity lock, FL2VA chaining, speed-ramp assembly and compositing. Load together with h3-video-prompting whenever a prompt has fighting, moves or VFX; this skill wins on combat pacing, impact frames and shot-length exceptions.
agent_created: true
---

# H3 綜合打鬥技能

把「打得好看」拆成可設計、可寫、可驗收、可組裝的流程：**招式 → 編排 → 特效 → 運鏡 → 衝擊點 → 提示詞 → 驗證 → 後製**。適用 MiniMax H3（海螺）T2VA／I2VA／FL2VA／L2VA／Ref2VA。

衝擊幀是其中一條必經支線，不是全部：沒有好招式與交換，衝擊幀救不了；有好招式卻沒有衝擊點計畫，大招就沒感覺。

## 0. 與其他技能的分工

| 事項 | 以誰為準 |
|---|---|
| 欄位格式、對白、`<scenetrans>` 等通用語法 | 官方 schema（`references/output-format.md`）＞ h3-video-prompting |
| 打鬥節奏、招式、特效、衝擊幀、變速、**鏡長例外** | **本技能** |
| 鏡長 | 衝擊幀串段、打擊短鏡、ULTRA_SPEED 鏡可短於 2 s，不套用 h3-video-prompting 的「每鏡 ≥2 s」「鏡距 <2 s 警訊」 |
| 漫劇專案（ai-comic-drama） | 分鏡／segments 多填「衝擊幀計畫」；組裝階段照計畫做變速／合成 |

## 1. 直接做，還是給選項

| 使用者狀態 | 做法 |
|---|---|
| 有角色、場景、參考片或具體描述 | **直接做，不要問** |
| 給了參考圖但沒說要做什麼 | 先給建議，再給 3–5 個情境選項 |
| 什麼都沒有 | 給情境選項，用 T2VA（角色寫進提示詞） |

六個已實測情境：A 連續對轟、B 單鏡纏鬥、C 電影級大招、D 氣場覺醒、E 純氛圍、F 首幀延續。決策樹與話術見 `references/guided-mode.md`。

## 2. 必經流程（每次都走；每步標了必讀檔）

1. **角色招式設計**：每個角色定 3–5 招具名招式（位移／身體機制／物理結果／戰術目的四層）、一招一色、招牌符號。大招／必殺／秒殺／變身另寫「起勢 → 命中 → 後果」。
   → `references/move-library.md`；有大招、秒殺、變身：`references/ultimate-moves.md`
2. **交手編排**：選節奏模式（§4），排交換（弱勢方至少打中一次）、配額（刀路上限）、三招三高度、主導權換手、後果。
   → `references/choreography.md`；連續對轟 `continuous-brawl.md`；超高速 `ultra-speed.md`
3. **特效分層**：每擊最多三層（主體能量／接觸能量／環境反應），力場最多開三通道，配色三選一（§6.6）。
   → `references/vfx-vocabulary.md`、`references/force-field.md`
4. **運鏡**：景別與運鏡一起換、因果運鏡、幅度跳級、受力方鏡頭；最大衝擊鏡「鎖死」或「回來猛震三下」二選一。
   → `references/cinematic-camera.md`、`camera-grammar.md`；高速跟拍 `drone-camera.md`
5. **列衝擊點清單＋選路徑**：把每一次 L3 以上命中、大招、爆炸列成一行（時間碼／具名打擊點／力度 L1–L4），每行選 P0–P3（§3）。**清單是空的才能跳過，並在交付說明寫「本段無衝擊幀（理由）」。**
   → 選 P2 必讀 `references/impact-frame/burst-strip.md`；P3 必讀 `impact-frame/post.md`；寫實／半寫實或不確定形態 `impact-frame/forms.md`；爆炸與震屏 `impact-frame/shake-and-timing.md`
6. **寫提示詞**：套模板（大招用模板 F），守硬約束（§5）。主片只寫「可剪的素材」，不寫幀數控制、不寫慢詞。有參考圖必列九類身份特徵。
   → `references/prompt-templates.md`、`output-format.md`；有參考圖 `ref-identity-lock.md`；表情 `facial-performance.md`
7. **驗證**：`python scripts/validate_prompt.py prompt.txt --duration 8`。FAIL 全修；IMPACT 類 WARN 要修或在交付說明寫理由。再過一次 `references/qa-checklist.md`。
8. **交付＋後製／組裝指令**：提示詞 code block ＋ 衝擊幀計畫表 ＋ 組裝指令（P2 `ramp`、P3 `composite`）。超過 15 秒用 FL2VA 接續（`references/fl2va-chain.md`）。生成後照計畫組裝，再量測（§9）。

## 3. 衝擊幀決策卡（H3 實測，2026-10-26 版）

**原則：提示詞負責生出「夠長、可剪」的衝擊素材；幀數與速度一律在組裝決定。**
H3 不遵守幀數：`for two frames` 的白閃實際亮 11–45 幀，同段漫畫格 21–23 幀（角色會消失）。

| 路徑 | 什麼時候用 | 提示詞寫什麼 | 組裝做什麼 |
|---|---|---|---|
| **P0 不用全幀** | L1–L2、弱事件、3D CG 寫實質感 | 接觸點局部星芒＋背景徑向拖影（點名 background）＋色彩遞進 | 無 |
| **P1 同段亮度事件** | L3 單擊、不在乎精確幀數 | `the frame blows out to white at the instant of contact, then snaps straight back`；不寫 hold／freeze／幀數 | 可選：把過長的白段裁到 1–2 幀 |
| **P2 衝擊幀串＋變速（L4 大招／必殺／秒殺預設）** | 大招、毀天滅地、一招秒殺、變身 | 獨立一段 0.8–1.2 s：N 張（3–5）、每張約 0.2 s、同構圖、每張換底色與畫法、中間不插回正常畫面、一張比一張狠；回原鏡頭時特效已全開、第一格衝擊波環已外擴 | `impact_frame.py ramp`：衝擊幀段 5×、主特效 1.5× |
| **P3 分開生成＋合成** | 漫畫格、要對齊某一格、ULTRA_SPEED、多次衝擊、P2 失敗補救 | 主片不寫任何衝擊幀；另寫 3–4 s 衝擊片 | `impact_frame.py composite`（自動縮放、保留音軌、多組 `--insert`） |

**成品長度三級**（參考片量測）：短閃 **1–2 幀**（白閃、翻色）｜連續序列 **6–13 幀**（白→黑白→主色→剪影→反相→白→黑 3 幀）｜放射定格板 **9–12 幀**。形態表（14 種）見 `impact-frame/forms.md`。

**H3 禁用慢詞（大招段）**：`near-freeze`、`hangs poised`、`poised and still`、`still for half a second`、`like a meteor`、`for half a second`（閃光）、`swallows the whole frame`、`slowly`、`gradually`。

**停頓不寫進提示詞**：參考片命中後減速只有 26%，停頓真正在**命中前**或**切鏡後的 0.15–0.25 s reveal**；要停就在組裝時複製 1–3 幀。蓄力用動作與光（能量聚集、碎石浮起、燈一片片滅），不寫靜止詞。

**鏡頭二選一**：最大衝擊時相機鎖死讓特效推開背景，**或**回原鏡頭第一格猛震三下、一下比一下小、0.5 s 內停穩。不要閃白配持續震屏。

**命中不拍飛行**：`within a single frame … is already rammed into <具名部位>, with no visible travel`；受擊在同一句 `in the same unbroken moment` 被掀飛。

## 4. 節奏模式：三選一（不可混用）

| 模式 | 節奏單位 | 什麼時候用 | 8 秒鏡數 | 鏡長 | 必讀 |
|---|---|---|---|---|---|
| **打擊結構**（原六拍） | 一次交手 | 單次重擊、有蓄力與後果 | 4–5 鏡 | 中位 1.2–2.0 s | `impact-design.md` |
| **連續對轟** | 一次交換 0.8–1.5 s | 近身纏鬥、壓著打、「不停」「沒有喘息」 | 9–10 鏡 | 中位 0.6–0.9 s | `continuous-brawl.md` |
| **ULTRA_SPEED** | 一個鏡頭 | 無人機高速跟拍、「超高速」「一直打」「運鏡一直在動」 | 10–14 鏡 | **雙峰**：1–2 個 1.2–2.0 s 錨定鏡＋8–10 個 0.25–0.6 s＋2–3 個 ≤0.2 s 插入 | `ultra-speed.md` |

**鏡長要雙峰，不要節拍器**：參考片鏡長 CV 0.90–1.17；等距 0.7 s 一鏡（CV 0.3–0.5）就是單調。validator 對時間碼間隔 CV <0.4 給 WARN。本表優先於其他檔案的鏡數規則。

## 5. 硬約束與輸出契約

| 項目 | 規格 |
|---|---|
| 單次時長 | 4–15 秒（超過切段，FL2VA 接續） |
| 幀率／音訊 | 24 fps、32 kHz 原生立體聲（有聲生成，組裝時要保留音軌） |
| 比例 | 21:9／16:9／4:3／1:1／3:4／9:16 |
| 欄位 | 三欄位 `integrated_multimodal_description`／`overall_soundscape`／`non_diegetic_music`；Ref2VA 六欄位 |

**寫作規則**：
1. `[Shot 1]` 不加時間碼、開頭寫風格錨定；後續 `[Shot N] At 00:0X.XXX, …` 嚴格遞增、落在時長內，末鏡 ≤ 總長 30%。
2. 運鏡寫成自然語句：類型＋幅度＋速度；主體動作與鏡頭運動分開寫。
3. 沒有負面欄：「不要」改寫成正面約束句（`the blade stays perfectly straight and rigid`）。
4. 欄位名與內容同一行；I2VA／FL2VA 首行對齊句；對白 `<d>[Chinese] 台詞</d>`。
5. **字數預算**：4–8 秒 ≤520 字、9–15 秒 ≤700 字；Ref2VA 再 +300。超過砍形容詞，不砍動作；重要約束往前放。（validator 同一張表）
6. **時長與時間碼一致**；H3 最後 1–2 秒會自動減速 → 多生成 1.5 秒、剪掉。
7. 有參考圖：九類身份特徵逐項列、畫風錨 3–4 個材質特徵（超過 3 個形容詞會變靜止圖）。

**交付物（三件，缺一不可）**：
1. 提示詞 code block（區塊內只有提示詞，無註解、無 Markdown）。
2. **衝擊幀計畫表**（block 外）：`# | 時間碼 | 打擊點 | 力度 | 路徑 | 組裝`；無衝擊點寫一行「本段無衝擊幀（理由）」。格式見 `output-format.md` §1.1。
3. **組裝指令**：P2 的 `ramp --seg`、P3 的 `composite --insert`、接續的 concat；並註明「生成後先 `find-peak` 校正區間」。

## 6. 核心方法摘要（細節在 references）

### 6.1 打擊結構（H3 版）
蓄 → 觸 → 洩 → 退 → 收。**蓄**用反向預備與光（不寫靜止）；**觸**＝衝擊點（§3 路徑）；**洩**＝力場三通道，方向與攻擊一致；**退**＝受擊者被打飛、衣髮延遲半拍、攻擊者過衝；**收**＝回到架勢、粒子飄落。舊版的「停 Hit Stop」拍移到組裝。攻擊寫三段路徑（起始位置 → 軌跡 → 終點）。→ `impact-design.md`

### 6.2 三條設計原則（優先於節拍與特效）
**有交換**（弱勢方至少打中一次）、**空間壓小**（窄道／台階／貼牆）、**有後果**（撞斷、摔下、面具裂、刀脫手）。

### 6.3 招式
- **具名**：抽象動詞＝平均化動作；每招四層（位移／機制／結果／目的）。→ `move-library.md`
- **配額**：15 秒約 20 鏡，刀路**上限** 8，踢 ≥3、拳肘 ≥2、真摔 ≥2、下盤 ≥1、格擋 ≥3、身法 ≥3。→ `choreography.md`
- **每擊寫打哪**（下顎、膝、兩角之間），上中下輪換；動作前加速度詞（瞬間、蹬地、殘影），不寫「飛向」。
- **每秒最多 3 個具體動作**、一鏡 1–2 秒；只寫「高速打鬥」無效。
- **開局 0.5 秒內第一次接觸**：`First contact occurs within the opening half-second.`

### 6.4 特效
三層能量（主體能量／接觸能量／環境反應），環境層最能救打擊感。力場四通道（光、空氣、物質、粒子）一次最多三個，優先 空氣 ＞ 物質 ＞ 光 ＞ 粒子；最便宜的證明是**衣襬或頭髮被推**。特效寫「形態＋空間範圍＋與誰互動」，自創招名要翻成畫面。→ `vfx-vocabulary.md`、`force-field.md`

### 6.5 運鏡與表情
- 運鏡跟著因果走（被打飛才甩、衝擊波推才退），全片繞圈 ≤1 次，同一 15 秒內俯拍 ≤2 次且內容不同。→ `cinematic-camera.md`
- 表情是肌肉不是形容詞：`her jaw muscles bunch`、`her brows slam down`；四階段（緊繃／痛／狠／喘），兩人收放對比，呼吸／汗／吞嚥。→ `facial-performance.md`

### 6.6 配色與構圖
- **配色三選一**：互補雙色（兩人各一色）／單色環境＋唯一異物色（夜戲）／爆炸換調（每次 L3 以上爆炸換一次全片色調）。能量色錨在眼瞳或寶石上。
- **奇觀不放正後方、被角色掃出來、高潮要有位移**；高潮後 ≤1 s 的對稱 reveal 可以（靠次級運動撐住）。

## 7. 何時必讀哪份 reference

| 出現這個情況 | 必讀 |
|---|---|
| 大招、必殺、秒殺、變身、毀天滅地 | `references/ultimate-moves.md` ＋ `impact-frame/burst-strip.md` |
| 漫畫格、要對齊某一格、ULTRA_SPEED 的衝擊、P2 失敗 | `impact-frame/post.md` |
| 不確定衝擊幀長什麼樣、寫實／3D CG／水墨 | `impact-frame/forms.md` |
| 爆炸、法術轟擊、震屏 | `impact-frame/shake-and-timing.md` ＋ `force-field.md` |
| 單次重擊、力度分級 L1–L4、材質反應 | `impact-design.md` |
| 招式不夠、刀來刀去 | `move-library.md` ＋ `choreography.md` |
| 近身纏鬥、不停 | `continuous-brawl.md` |
| 超高速、無人機跟拍 | `ultra-speed.md` ＋ `drone-camera.md` |
| 運鏡平、鏡頭亂轉 | `cinematic-camera.md` ＋ `camera-grammar.md` |
| 刀光、劍氣、21:9 斬擊 | `blade-light-cinema.md` |
| 特效詞彙、配色、閃電、能量煙 | `vfx-vocabulary.md` |
| 臉是死的 | `facial-performance.md` |
| 有參考圖、要保真 | `ref-identity-lock.md` |
| 超過 15 秒、接續 | `fl2va-chain.md` |
| 輸出格式、計畫表 | `output-format.md` ＋ `prompt-templates.md` |
| 生成後驗收、量參考片、A/B | `lab-notes.md` ＋ `qa-checklist.md` |
| 完整案例 | `case-wuxia-duel.md` |
| 使用者不知道要什麼 | `guided-mode.md` |

## 8. 腳本速查（輸入 → 輸出）

| 腳本 | 用途 | 一行範例 | 在哪跑 |
|---|---|---|---|
| `validate_prompt.py` | 格式＋招式＋衝擊幀檢查 | `python scripts/validate_prompt.py p.txt --duration 8`（衝擊片加 `--impact-clip`） | 任何地方 |
| `impact_frame.py find-peak` | 找衝擊幀實際落在哪幾格 | `python scripts/impact_frame.py find-peak --in clip.mp4` | 任何地方（需 ffmpeg） |
| `impact_frame.py ramp` | P2 分段變速（含音軌） | `python scripts/impact_frame.py ramp --in a.mp4 --seg 1.40-2.21:5 --seg 2.21-3.96:1.5 --out a.ramped.mp4` | 任何地方 |
| `impact_frame.py composite` | P3 疊衝擊幀（縮放、保留音軌、印驗收值） | `python scripts/impact_frame.py composite --main m.mp4 --impact i.mp4 --insert 163:auto:2 --out f.mp4` | 任何地方 |
| `impact_frame.py gen` | 生成衝擊片 | `--api URL --token-file F`（或環境變數 `H3_API_BASE`／`H3_TOKEN_FILE`） | 需本機 FreeVideo |
| `measure_motion.py` | 運動曲線與旗標 | `python scripts/measure_motion.py out.mp4 --fps24 --symmetry` | 任何地方 |
| `measure_staging.py`／`measure_light_event.py` | 鏡長分布／每鏡光影事件 | 見 `lab-notes.md` | 任何地方 |
| `submit_ab.py`／`poll_ab.py`／`compare_clips.py` | 技能前後 A/B 對照 | 見 `lab-notes.md` §3 | 送件需本機 |
| `submit_ref2va.py`／`submit_chain.py`／`seam_check.py` | Ref2VA 送件／接續鏈／接縫檢查 | 見 `fl2va-chain.md` | 送件需本機 |

## 9. 量測門檻速查（細節 → `lab-notes.md`）

| 指標 | 合格 | 備註 |
|---|---|---|
| 開場 0.8 s | ≥ 中段 50% | — |
| 末 2 s ÷ 中段 | ≥ 60% | 只在要接下一段或要求動態結尾時硬性要求 |
| 最長低潮 | ≤ 0.8 s | L4 前刻意蓄力可豁免（先目視） |
| 峰值格 | ≥ 4 | 唯一可跨版本比的指標 |
| 衝擊幀可見 | 插入幀與鄰幀 YAVG 差 ≥40 或 SATAVG <15 | composite 自動印出 |
| 音軌 | 組裝後仍在 | `ffprobe` |

參考片先驗幀率（標 60 可能是 24 pulldown），跨片比用 `--fps24`。

## 10. 最常見的錯

1. **有大招卻沒有衝擊幀計畫**（validator：IMPACT WARN）。
2. **寫 near-freeze／poised／still 當重量**，H3 放大成 0.5–3.7 s 空等。
3. **光束寫成流星**（`like a meteor`），畫出飛行全程。
4. **同段寫漫畫格**，21–23 幀、角色消失 → P3。
5. **閃白配持續震屏**，或震屏沒有衰減。
6. **刀來刀去**：刀路沒有上限、每擊沒寫打哪、三招同高度。
7. **臉是死的**：用眼睛形狀／打光代替肌肉。
8. **鏡長節拍器**：等距 0.7 s 一鏡。
9. **選了 P2／P3 卻沒附組裝指令**，成品就沒有衝擊幀（37／38 號的教訓）。
10. **只用術語**（`沖擊幀`、`Field 力場擾動`）不寫物理描述；這些術語在 H3 是否有效**未經 A/B 驗證**，送進模型的一律寫具體句子。
