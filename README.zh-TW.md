<p align="center">
  <img src="assets/hero.jpg" alt="兩名武俠劍客在刀鋒相觸的瞬間：白熱火花、青綠與琥珀色衝擊波、衣袍被氣壓掀起" width="100%">
</p>

<h1 align="center">h3-combat-impact</h1>

<p align="center">
  <b>MiniMax H3 / 海螺的綜合打鬥 Agent Skill：角色招式設計、交手編排、特效分層、運鏡、表情、衝擊幀與震屏、參考圖保真、接續生成、組裝變速與後製。</b>
</p>

<p align="center">
  <a href="README.md">English</a> · <b>繁體中文</b>
</p>

<p align="center">
  <a href="LICENSE"><img alt="MIT" src="https://img.shields.io/badge/license-MIT-blue.svg"></a>
  <img alt="Agent Skill" src="https://img.shields.io/badge/agent-skill-8A2BE2">
  <img alt="MiniMax H3" src="https://img.shields.io/badge/MiniMax-H3%20%2F%20海螺-ff5a36">
  <img alt="提示詞類型" src="https://img.shields.io/badge/提示詞類型-11%20種實測-2ea44f">
  <img alt="腳本" src="https://img.shields.io/badge/scripts-stdlib%20%2B%20ffmpeg-0a7">
</p>

---

## 成品展示

下面每一支都是 MiniMax H3 在本機 RTX 4060 Ti（8 GB）上，用 [`examples/`](examples/) 裡的提示詞生成：固定種子、24 fps、`high` 畫質、1280×704（21:9 那支是 1280×544）。點標題可看完整 MP4。

<table>
  <tr>
    <td align="center" width="50%">
      <a href="assets/showcase/blade-light.mp4"><img src="assets/showcase/blade-light.gif" alt="21:9 夜間雪地：冰藍新月弧、X 形光、放射閃電、紫色刀光"></a><br>
      <b><a href="assets/showcase/blade-light.mp4">21:9 刃光電影</a></b><br>
      <sub>藍雪上的逆光剪影，唯一的紫色異物色 · <a href="examples/blade-light-21x9.txt">提示詞</a></sub>
    </td>
    <td align="center" width="50%">
      <a href="assets/showcase/ultra-speed.mp4"><img src="assets/showcase/ultra-speed.gif" alt="8 秒 12 鏡的庭院對決，機位在俯拍、貼地、升降之間切換"></a><br>
      <b><a href="assets/showcase/ultra-speed.mp4">超高速・無人機式運鏡</a></b><br>
      <sub>8 秒 12 鏡，每次切鏡都換機位 · <a href="examples/ultra-speed-drone.txt">提示詞</a></sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="assets/showcase/ink-wash.mp4"><img src="assets/showcase/ink-wash.gif" alt="老虎與持槍劍客，米黃紙色背景上的放射黑墨爆"></a><br>
      <b><a href="assets/showcase/ink-wash.mp4">水墨墨爆</a></b><br>
      <sub>用墨刺加 1 幀亮暗翻轉取代凍結 · <a href="examples/ink-wash.txt">提示詞</a></sub>
    </td>
    <td align="center">
      <a href="assets/showcase/six-beat.mp4"><img src="assets/showcase/six-beat.gif" alt="屋頂對決，刀鋒相觸瞬間出現 2 幀爆白"></a><br>
      <b><a href="assets/showcase/six-beat.mp4">六拍單次重擊</a></b><br>
      <sub>蓄力、爆白、衝擊波、被打飛 · <a href="examples/six-beat-single-hit.txt">提示詞</a>（2026-10 已依實測改寫，影片是舊版提示詞生成）</sub>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="assets/showcase/anime-30s.mp4"><img src="assets/showcase/anime-sakuga.gif" alt="空間站貨艙裡兩名改造人格鬥：衝擊閃光、火球、藍色反應堆、炸開的觀景窗"></a><br>
      <b><a href="assets/showcase/anime-30s.mp4">兩張參考圖生成的 30 秒 2D 動漫格鬥</a></b><br>
      <sub>2 × 15 秒 Ref2VA，角色保真 · <a href="examples/anime-ref2va-part1.txt">上半</a> · <a href="examples/anime-ref2va-part2.txt">下半</a></sub>
    </td>
    <td align="center">
      <a href="assets/showcase/face.mp4"><img src="assets/showcase/face.gif" alt="女劍客特寫：咬牙、眉頭擰緊、瞪大眼睛、低吼"></a><br>
      <b><a href="assets/showcase/face.mp4">臉部表演</a></b><br>
      <sub>寫肌肉動作，不寫形容詞 · <a href="examples/facial-performance.txt">提示詞</a></sub>
    </td>
  </tr>
  <tr>
    <td align="center" colspan="2">
      <a href="assets/showcase/impact-composite.mp4"><img src="assets/showcase/impact-composite.gif" alt="超高速片段，後製合成三階段漫畫衝擊序列" width="50%"></a><br>
      <b><a href="assets/showcase/impact-composite.mp4">後製加上衝擊幀</a></b><br>
      <sub>主片完全沒有衝擊幀；另外生成一支 H3 漫畫放射片，取 3 × 2 幀逐幀精準合成 · <a href="references/impact-frame/post.md">做法</a></sub>
    </td>
  </tr>
</table>

30 秒格鬥是「重現」不是複製：它參考一支公開的 Seedance 2.5 展示片的結構（分鏡表、每次爆炸換色調、貨艙佈局），改寫成 H3 的格式與限制。參考角色圖不在此 repo。

## 為什麼需要這個 skill

AI 打鬥片的毛病都差不多：動作軟、特效像貼圖、兩個人像木頭人擺姿勢、臉像死人、鏡頭一直繞圈、最後兩秒站著不動。光寫「史詩爆炸」解決不了。

這個 skill 把「打得好看」拆成一條**必經流程**，每一步都能寫、能複製、能量測：

**招式設計 → 交手編排 → 特效分層 → 運鏡 → 衝擊點清單與路徑 → 提示詞 → 驗證 → 後製／組裝指令**

- **它是綜合打鬥技能，不只是衝擊幀**：衝擊幀是其中一條必經支線；沒有好招式與交換，衝擊幀救不了。
- **與 h3-video-prompting 並用**：通用 H3 格式以官方 schema 為準；打鬥、招式、特效、衝擊幀、變速、鏡長例外以本技能為準。
- **打擊結構**：蓄 → 觸 → 洩 → 退 → 收；舊版的「停 Hit Stop」移到組裝（H3 會把 near-freeze 放大成 0.5–1 秒）。
- **力場而非光效**：光／空氣／物質／粒子四通道；最便宜的力量證明，是衣襬或髮絲被推開。
- **具名招式**：16 招，每招四層，不再被平均成「揮、擋、退」。
- **三種節奏模式**：六拍、連續對轟、ULTRA_SPEED（8 秒 10–14 鏡，每次切鏡換機位）。
- **參考圖保真**：Ref2VA 的 9 類身份清單，讓角色保持「就是那一個」。
- **衝擊幀決策卡（P0–P3）**：H3 不遵守幀數（`for two frames` 實測亮 11–45 幀），所以提示詞只生「可剪的素材」，幀數與速度在組裝決定；大招預設走「衝擊幀串＋5× 變速」。
- **交付三件**：可直接貼上的提示詞 code block、衝擊幀計畫表、組裝指令；驗證器會擋「有大招卻沒衝擊幀」「慢詞」「同段漫畫格」「閃白配持續震屏」。
- **用數據驗收**：腳本對成品 MP4 量測運動、光事件、分鏡、接縫。

## 打擊結構（原六拍，2026-10 改版）

<p align="center">
  <img src="assets/six-beat.jpg" alt="一次揮劍拆成六格：蓄、觸、停、洩、退、收" width="92%"><br>
  <sub>舊版六拍示意圖。第 3 拍「停」現在不寫進提示詞，改在組裝做（複製命中前的幀，或切鏡後 0.15–0.25 秒 reveal）。</sub>
</p>

| 拍 | 畫面要有 | 提示詞關鍵句 |
|---|---|---|
| 1 蓄 | 反向預備、能量聚集、碎石浮起（**不寫靜止詞**） | `weight sinks into the rear leg`、`the lights die one by one toward the target` |
| 2 觸 | **衝擊點**：依決策卡選 P0–P3 | `the frame blows out to white at the instant of contact, then snaps straight back` |
| 3 洩 | 衝擊波、碎片、塵環、光影聯動（力場最多三通道） | `a ring of shockwave dust bursts outward` |
| 4 退 | 受擊者在同一句被打飛、衣髮延遲甩動、震屏衰減 | `in the same unbroken moment he is hurled back` |
| 5 收 | 回到防禦姿勢、餘燼飄落、鏡頭回穩 | `settles into a low guard` |

## 衝擊幀決策卡

| 路徑 | 什麼時候 | 提示詞 | 組裝 |
|---|---|---|---|
| P0 不用全幀 | L1–L2、3D CG 寫實 | 局部星芒＋背景徑向拖影 | — |
| P1 同段亮度事件 | L3 單擊 | 閃白＋`then snaps straight back`，不寫幀數 | 可裁到 1–2 幀 |
| **P2 衝擊幀串＋變速** | **大招、必殺、秒殺（預設）** | 獨立一段 3–5 張、每張約 0.2 秒、同構圖換配色、一張比一張狠 | `impact_frame.py ramp`：5×／1.5× |
| P3 分開生成＋合成 | 漫畫格、對齊某一格、ULTRA_SPEED | 主片不寫，另生衝擊片 | `impact_frame.py composite` |

成品長度三級（參考片量測）：短閃 1–2 幀｜連續序列 6–13 幀｜放射定格板 9–12 幀。H3 禁用慢詞：`near-freeze`、`hangs poised`、`like a meteor`、`for half a second`…（[`burst-strip.md`](references/impact-frame/burst-strip.md)）。

一擊只給一個視覺高潮。「壓著打」用沒有凍結的四拍模式（[`continuous-brawl.md`](references/continuous-brawl.md)）；要「喘不過氣」的快切用 [`ultra-speed.md`](references/ultra-speed.md)。

## 力場：光效只是顏色，力場才是空氣

<p align="center">
  <img src="assets/force-field.jpg" alt="爆炸核心向外四個通道：光、空氣、物質、粒子" width="92%"><br>
  <sub>每擊最多同時開三個通道。優先順序：空氣 &gt; 物質 &gt; 光 &gt; 粒子。</sub>
</p>

```text
✗  epic explosion, glowing shockwave
✓  wind pressure flattens the silk against her body, the air ripples in a heat-haze ring,
   roof tiles rattle loose
```

## 每一種提示詞類型，都實測過

全部固定同一個種子。「末段÷中段」是片尾 2 秒運動量除以中段（[`measure_motion.py`](scripts/measure_motion.py)，合格 ≥ 60%）。數字預設為草稿（`light`）畫質，HQ 欄另標。

| 提示詞類型 | 範例 | 初版 | 修正後／高畫質 | 結論 |
|---|---|---|---|---|
| 六拍單次重擊 | [`six-beat-single-hit.txt`](examples/six-beat-single-hit.txt) | 110%；爆白幀有出現，開場偏慢 | HQ 73% | 過門檻；蓄力要短（數據是舊版提示詞，現行版已移除 near-freeze／for two frames，**待重跑**） |
| 連續對轟 | [`continuous-brawl.txt`](examples/continuous-brawl.txt) | 末段÷中段 118%，動作偏平靜 | – | 可用但平穩，不放展示 |
| ULTRA_SPEED＋無人機運鏡 | [`ultra-speed-drone.txt`](examples/ultra-speed-drone.txt) | 95% | HQ 80% | **強** |
| 21:9 刃光 | [`blade-light-21x9.txt`](examples/blade-light-21x9.txt) | 84% | HQ 67% | 過門檻（HQ 勉強）；暗畫面會壓低分數，要目視 |
| 力場爆炸 | [`force-field-explosion.txt`](examples/force-field-explosion.txt) | **28%**，主體凍住 | 改寫後 66%；HQ 43% | 弱，仍待改進 |
| 水墨墨爆 | [`ink-wash.txt`](examples/ink-wash.txt) | 71% | HQ 52%（尾端偏靜） | HQ 未過 60%；畫面對，結尾偏安靜 |
| 臉部表演 | [`facial-performance.txt`](examples/facial-performance.txt) | **40%** | 改寫後 133%；HQ 182% | 修正後強 |
| Ref2VA 角色保真 | [`anime-ref2va-part1.txt`](examples/anime-ref2va-part1.txt) | 94% | HQ 89% | **強** |
| Ref2VA 第二段 15 秒 | [`anime-ref2va-part2.txt`](examples/anime-ref2va-part2.txt) | **34%** | 改寫後 88%；HQ 93% | 修正後強 |
| I2VA 特效插入鏡 | [`SKILL.md`](SKILL.md) | 保住配色（鋼藍＋金）；首幀 PSNR ≈ 20 dB | – | 適合 1–4 秒插入鏡，運動偏低 |
| 後製衝擊幀 | [`impact-frame-source.txt`](examples/impact-frame-source.txt) | 6 幀連續，已驗證 | – | 24fps 主片可行，逐幀精準 |

這幾支同時做了兩個修改，無法分開歸因：

- **最後一鏡寫成「動作進行中」**：`both fighters are still mid-motion as the frame ends` 讓力場片從 28% 到 66%、臉部片從 40% 到 133%、15 秒動漫下半從 34% 到 88%。末鏡寫「hold」「settle」，H3 就會把它凍住。
- **單鏡靜態場景改寫成 3–4 鏡**，每鏡有機位變化與環境反應。

提示詞格式 A/B（15 秒 Ref2VA、同參考圖同種子）：作者風格的中文提示詞、`[Shot 1]` 帶時間區間前綴，末段÷中段 108%；官方格式 113%，兩者都沒有停滯。驗證器仍以官方格式為準（[`fl2va-chain.md`](references/fl2va-chain.md) §5.6）。

## 安裝

```bash
git clone https://github.com/ayase0307/h3-combat-impact ~/.claude/skills/h3-combat-impact
```

任何讀 `SKILL.md` 的 agent 都能用（Claude Code、Codex 等）。Windows 請 clone 到 `%USERPROFILE%\.claude\skills\`。

然後直接用白話說：

> 「幫我寫一段 8 秒屋頂對決的 H3 提示詞，現在很飄，要有打擊感。」
> 「拆解這支打鬥參考片，用 H3 格式重現。」
> 「這個大招沒感覺，要毀天滅地。」
> 「幫兩個角色各設計三招，排一段 15 秒的對打。」
> 「讓這個參考角色在太空站貨艙打 30 秒。」

## 工具

```bash
# 貼進模型前先檢查格式（FAIL 必須修掉）
python scripts/validate_prompt.py prompt.txt --duration 8

# 量測生成影片的運動曲線（需要 ffmpeg 在 PATH）
python scripts/measure_motion.py --dir ./outputs
python scripts/measure_motion.py ref.mp4 --fps24            # 比較前先換算成 24fps

# 衝擊幀實際落在哪幾格？
python scripts/impact_frame.py find-peak --in clip.mp4

# P2：衝擊幀段 5×、主特效 1.5×（音軌一起變速）
python scripts/impact_frame.py ramp --in clip.mp4 --seg 1.40-2.21:5 --seg 2.21-3.96:1.5 --out clip.ramped.mp4

# P3：衝擊片自動挑最亮／最去飽和的一格，疊到主片第 93 幀、停 2 幀（自動縮放、保留音軌、印出驗收值）
python scripts/impact_frame.py composite --main main.mp4 --impact burst.mp4 \
    --insert 93:auto:2 --out out.mp4

# 測試
python -m unittest discover -s tests
```

| 指標 | 合格 |
|---|---|
| 開場 0.8s | ≥ 中段 50% |
| 末 2s ÷ 中段 | ≥ 60%（要接下一段或要求動態結尾時） |
| 最長低潮 | ≤ 0.8s |
| 峰值格 | ≥ 4 |

> 門檻以 24fps 素材校準。宣稱 60fps 的片可能其實是 24fps 加 pulldown，30fps 素材分數約低 20%；比較前請加 `--fps24`。

## 檔案一覽

| 檔案 | 內容 |
|---|---|
| [`SKILL.md`](SKILL.md) | 核心：分工、八步必經流程、衝擊幀決策卡、節奏模式、硬約束與交付物、何時必讀哪份 reference |
| [`references/output-format.md`](references/output-format.md) | 官方三／六欄位格式、對齊句、對白標籤、**衝擊幀計畫表與組裝指令** |
| [`references/ultimate-moves.md`](references/ultimate-moves.md) | 大招、必殺、一招秒殺（三鏡三邏輯）、變身、延遲命中、頂住半拍、後果寫法 |
| [`references/impact-frame/forms.md`](references/impact-frame/forms.md) | 衝擊幀唯一形態表（14 種）、三級長度、寫實配方、變身鏈、已推翻寫法對照 |
| [`references/impact-frame/burst-strip.md`](references/impact-frame/burst-strip.md) | P2 衝擊幀串段＋組裝變速（大招預設）、H3 禁用慢詞 |
| [`references/impact-frame/post.md`](references/impact-frame/post.md) | P3 分開生成再合成、兩段式驗收 |
| [`references/impact-frame/shake-and-timing.md`](references/impact-frame/shake-and-timing.md) | 震屏（短抖／計數衰減）、停頓放哪、三段式爆炸時序 |
| [`references/impact-design.md`](references/impact-design.md) | 打擊結構細節、力度分級 L1–L4、三級碰撞體系、材質反應 |
| [`references/move-library.md`](references/move-library.md) | 16 招具名動作、4 組串接、中英翻譯規則 |
| [`references/choreography.md`](references/choreography.md) | 招式編排：配額制、真摔與僵持、三招三高度、提速排名、強約束句 |
| [`references/cinematic-camera.md`](references/cinematic-camera.md) | 電影級運鏡：三檔速度、因果運鏡、十機位、Z 軸驟停、吞沒鏡頭收尾 |
| [`references/continuous-brawl.md`](references/continuous-brawl.md) | 連續對轟四拍模式 |
| [`references/ultra-speed.md`](references/ultra-speed.md) | ULTRA_SPEED：8 秒 10–14 鏡、雙峰鏡長、後製必經 |
| [`references/drone-camera.md`](references/drone-camera.md) | 無人機運鏡：8 種機位、五種尺度、俯拍去重 |
| [`references/blade-light-cinema.md`](references/blade-light-cinema.md) | 刃光電影語言、漫畫衝擊格、單色夜戰 |
| [`references/ref-identity-lock.md`](references/ref-identity-lock.md) | 參考圖保真：9 類身份特徵、畫風材質錨 |
| [`references/facial-performance.md`](references/facial-performance.md) | 用肌肉動作寫表情 |
| [`references/fl2va-chain.md`](references/fl2va-chain.md) | 兩段接續、接縫、白色接縫、每段剪輯計畫 |
| [`references/force-field.md`](references/force-field.md) | 力場四通道、三種場型、句庫 |
| [`references/camera-grammar.md`](references/camera-grammar.md) | 官方運鏡詞彙、打鬥運鏡套路 |
| [`references/vfx-vocabulary.md`](references/vfx-vocabulary.md) | 中英特效詞彙庫、配色三選一、閃電／能量煙／吸收型落點 |
| [`references/prompt-templates.md`](references/prompt-templates.md) | T2VA / FL2VA / Ref2VA 填空模板、**模板 F 大招** |
| [`references/qa-checklist.md`](references/qa-checklist.md) | 生成前後檢查、失敗對應修法 |
| [`references/lab-notes.md`](references/lab-notes.md) | 量測規則、工具、A/B 對照實驗紀錄 |
| [`references/guided-mode.md`](references/guided-mode.md) | 引導模式：入口與情境選項 |
| [`references/case-wuxia-duel.md`](references/case-wuxia-duel.md) | 27.5 秒對決的拆解與重現 |
| [`examples/`](examples/) | 展示與上方實測表用到的十份提示詞 |
| [`scripts/`](scripts/) | `validate_prompt`、`impact_frame`（find-peak／ramp／composite／gen）、`measure_motion`、`measure_staging`、`measure_light_event`、`submit_ref2va`、`submit_chain`、`seam_check`、`submit_ab`、`poll_ab`、`compare_clips` |
| [`tests/`](tests/) | validator 樣本與 `impact_frame.py` 端到端測試：`python -m unittest discover -s tests` |

## 誠實的限制

- 數據來自我自己在單一環境的實測，每種提示詞一個種子，是佐證，不是基準測試。
- 運動分數量的是畫面變化，不是主體運動；暗畫面或剪影片即使看起來對，分數也會偏低，仍要目視。
- 高畫質重跑與草稿是不同樣本，分數會變動，表格兩者都列。
- 力場類在高畫質下仍偏弱。
- 案例分析與 30 秒格鬥分析的是第三方參考片，影片與角色圖不包含在此 repo。
- H3 沒有負面提示欄；所有「不要」都改寫成正面約束句。
- 2026-10 改版收進的新教學規則多數是**H3 未實測**（在檔案裡逐條標註）；P2 衝擊幀串只有一次 H3 實跑（EP03 S04-a d17），張數、防分格句、負片寫法仍待固定 seed 驗證。

## 授權

MIT




