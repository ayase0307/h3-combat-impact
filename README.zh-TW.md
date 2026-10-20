<p align="center">
  <img src="assets/hero.jpg" alt="兩名武俠劍客在刀鋒相觸的瞬間：白熱火花、青綠與琥珀色衝擊波、衣袍被氣壓掀起" width="100%">
</p>

<h1 align="center">h3-combat-impact</h1>

<p align="center">
  <b>讓 MiniMax H3 / 海螺的打鬥「真的有打到」的 Agent Skill：六拍打擊、具名招式、力場、衝擊幀、無人機式運鏡。</b>
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
      <sub>蓄力、爆白、衝擊波、被打飛 · <a href="examples/six-beat-single-hit.txt">提示詞</a></sub>
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
      <sub>主片完全沒有衝擊幀；另外生成一支 H3 漫畫放射片，取 3 × 2 幀逐幀精準合成 · <a href="references/impact-frame-post.md">做法</a></sub>
    </td>
  </tr>
</table>

30 秒格鬥是「重現」不是複製：它參考一支公開的 Seedance 2.5 展示片的結構（分鏡表、每次爆炸換色調、貨艙佈局），改寫成 H3 的格式與限制。參考角色圖不在此 repo。

## 為什麼需要這個 skill

AI 打鬥片的毛病都差不多：動作軟、特效像貼圖、兩個人像木頭人擺姿勢、臉像死人、鏡頭一直繞圈、最後兩秒站著不動。光寫「史詩爆炸」解決不了。

這個 skill 把「打得更有力」拆成能寫、能複製、**能量測**的結構：

- **六拍打擊**：蓄 → 觸 → 停 → 洩 → 退 → 收，每拍有時間佔比。
- **力場而非光效**：光／空氣／物質／粒子四通道；最便宜的力量證明，是衣襬或髮絲被推開。
- **具名招式**：16 招，每招四層，不再被平均成「揮、擋、退」。
- **三種節奏模式**：六拍、連續對轟、ULTRA_SPEED（8 秒 10–14 鏡，每次切鏡換機位）。
- **參考圖保真**：Ref2VA 的 9 類身份清單，讓角色保持「就是那一個」。
- **衝擊幀走後製**：H3 做不穩 2 幀閃光，所以分開生成、逐幀精準合成。
- **產出可直接貼上**：官方 H3 格式的單一 code block，附驗證器。
- **用數據驗收**：腳本對成品 MP4 量測運動、光事件、分鏡、接縫。

## 六拍結構

<p align="center">
  <img src="assets/six-beat.jpg" alt="一次揮劍拆成六格：蓄35%、觸5%、停15%、洩25%、退15%、收5%" width="92%"><br>
  <sub>一擊六拍與各自的時間佔比。沒有蓄力，就沒有重量。</sub>
</p>

| 拍 | 佔比 | 畫面要有 | 提示詞關鍵句 |
|---|---:|---|---|
| 1 蓄 | 35% | 反向預備、重心下沉、布料繃緊 | `weight sinks into the rear leg` |
| 2 觸 | 5% | **衝擊幀**：1–2 幀爆白／爆黑 | `for two frames the entire frame blows out to pure white` |
| 3 停 | 15% | 時間近乎凍結，塵與火花懸浮 | `decelerates to a near-freeze for two frames` |
| 4 洩 | 25% | 衝擊波、碎片、塵環、光影聯動 | `a ring of shockwave dust bursts outward` |
| 5 退 | 15% | 受擊者被打飛、衣髮延遲甩動、**震屏衰減** | `the shake decays within a third of a second` |
| 6 收 | 5% | 回到防禦姿勢、餘燼飄落、鏡頭回穩 | `settles into a low guard` |

蓄 ≥ 觸的 5 倍；一擊只給一個視覺高潮。「壓著打」用沒有凍結的四拍模式（[`continuous-brawl.md`](references/continuous-brawl.md)）；要「喘不過氣」的快切用 [`ultra-speed.md`](references/ultra-speed.md)。

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
| 六拍單次重擊 | [`six-beat-single-hit.txt`](examples/six-beat-single-hit.txt) | 110%；爆白幀有出現，開場偏慢 | HQ 73% | 過門檻；蓄力要短 |
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
> 「讓這個參考角色在太空站貨艙打 30 秒。」

## 工具

```bash
# 貼進模型前先檢查格式（FAIL 必須修掉）
python scripts/validate_prompt.py prompt.txt --duration 8

# 量測生成影片的運動曲線（需要 ffmpeg 在 PATH）
python scripts/measure_motion.py --dir ./outputs
python scripts/measure_motion.py ref.mp4 --fps24            # 比較前先換算成 24fps

# 後製合成衝擊幀（逐幀精準：--at 請給 幀號/24）
python scripts/impact_frame.py composite --main main.mp4 --impact burst.mp4 \
    --at 3.875 --frame 3 --hold 0.083 --out out.mp4
```

| 指標 | 合格 |
|---|---|
| 開場 0.8s | ≥ 中段 50% |
| 末 2s ÷ 中段 | ≥ 60% |
| 最長低潮 | ≤ 0.8s |
| 峰值格 | ≥ 4 |

> 門檻以 24fps 素材校準。宣稱 60fps 的片可能其實是 24fps 加 pulldown，30fps 素材分數約低 20%；比較前請加 `--fps24`。

## 檔案一覽

| 檔案 | 內容 |
|---|---|
| [`SKILL.md`](SKILL.md) | 規格、六拍方法、力場、設計原則、工作流程 |
| [`references/output-format.md`](references/output-format.md) | 官方三／六欄位格式、對齊句、對白標籤 |
| [`references/impact-design.md`](references/impact-design.md) | 六拍細節、力度分級、材質反應 |
| [`references/move-library.md`](references/move-library.md) | 16 招具名動作、4 組串接、中英翻譯規則 |
| [`references/continuous-brawl.md`](references/continuous-brawl.md) | 連續對轟四拍模式 |
| [`references/ultra-speed.md`](references/ultra-speed.md) | ULTRA_SPEED：8 秒 10–14 鏡、每鏡一個光事件 |
| [`references/drone-camera.md`](references/drone-camera.md) | 無人機運鏡：8 種機位、五種尺度、禁止只繞圈 |
| [`references/blade-light-cinema.md`](references/blade-light-cinema.md) | 21:9 刃光電影語言、漫畫衝擊格、單色夜戰 |
| [`references/ref-identity-lock.md`](references/ref-identity-lock.md) | 參考圖保真：9 類身份特徵、畫風材質錨 |
| [`references/facial-performance.md`](references/facial-performance.md) | 用肌肉動作寫表情 |
| [`references/impact-frame-and-shake.md`](references/impact-frame-and-shake.md) | 衝擊幀形態與幀數、震屏衰減、墨爆 |
| [`references/impact-frame-post.md`](references/impact-frame-post.md) | 衝擊幀分開生成再後製合成 |
| [`references/fl2va-chain.md`](references/fl2va-chain.md) | 兩段接續、接縫、結尾規則 |
| [`references/force-field.md`](references/force-field.md) | 力場四通道、三種場型、句庫 |
| [`references/camera-grammar.md`](references/camera-grammar.md) | 官方運鏡詞彙、打鬥運鏡套路 |
| [`references/vfx-vocabulary.md`](references/vfx-vocabulary.md) | 中英特效詞彙庫、色彩腳本 |
| [`references/prompt-templates.md`](references/prompt-templates.md) | T2VA / FL2VA / Ref2VA 填空模板 |
| [`references/qa-checklist.md`](references/qa-checklist.md) | 生成前後檢查、失敗對應修法 |
| [`references/guided-mode.md`](references/guided-mode.md) | 引導模式：入口與情境選項 |
| [`references/case-wuxia-duel.md`](references/case-wuxia-duel.md) | 27.5 秒對決的拆解與重現 |
| [`examples/`](examples/) | 展示與上方實測表用到的十份提示詞 |
| [`scripts/`](scripts/) | `validate_prompt`、`measure_motion`、`measure_staging`、`measure_light_event`、`impact_frame`、`submit_ref2va`、`submit_chain`、`seam_check`、`submit_ab`、`poll_ab`、`compare_clips` |

## 誠實的限制

- 數據來自我自己在單一環境的實測，每種提示詞一個種子，是佐證，不是基準測試。
- 運動分數量的是畫面變化，不是主體運動；暗畫面或剪影片即使看起來對，分數也會偏低，仍要目視。
- 高畫質重跑與草稿是不同樣本，分數會變動，表格兩者都列。
- 力場類在高畫質下仍偏弱。
- 案例分析與 30 秒格鬥分析的是第三方參考片，影片與角色圖不包含在此 repo。
- H3 沒有負面提示欄；所有「不要」都改寫成正面約束句。

## 授權

MIT
