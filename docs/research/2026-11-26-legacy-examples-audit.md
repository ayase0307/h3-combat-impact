# 2026-11-26 過往演示案例全面體檢與 v4.0 雙軌參數升級報告

> 範圍：`examples/` 下所有正式追蹤的 v1 基準展示集、`examples/v3-manju/` 旗艦漫劇集與 `scripts/render_v3_flagship.py` 的 JOBS 配置；同步升級 `scripts/validate_prompt.py` 的防動態破圖檢核。
> **驗證狀態聲明**：本報告的所有劇本結論都來自 validator 靜態檢核加人工導演審計。所有 Dial 配置都**只經過 `--dry` 建圖驗證**（圖可建、`[dial-physics]` 預算如下表），**尚未上 GPU 實測**；成片效果待第二波重跑（§7）確認。

---

## 1. 檢核方法

| 項目 | 指令／做法 |
|---|---|
| 格式與物理 | `python scripts/validate_prompt.py <檔> --duration <實際秒數>`；v3 雙語稿加 `--check-sync --strict-physics` |
| 被檔頭 profile 遮住的問題 | v3 六套另跑一次 `--profile fight`，看 `ultra`／`facial` 檔頭略過了哪些警告 |
| 人工導演審計 | 逐鏡對照中英稿：滑行詞（含 regex 沒抓到的 `glides`、`滑步`、`滑退`）、否定詞、表情過激詞、刀路單調、中英段落標題與切點一致性 |
| Dial 預算 | `python scripts/render_v3_flagship.py --dry <套件>`，讀 `[dial-physics]` 行（`summarize_motion_budget` 實算） |
| 回歸 | `python -m unittest discover -s tests -v`（27 項全過） |

**基線發現（修改前）**：
- `tests/test_validate.py` 原本就有 2 項失敗：Windows 管線的 stdout 預設 cp950，測試卻用 UTF-8 解碼，中文訊息比對永遠失敗。已在測試子程序統一注入 `PYTHONIOENCODING=utf-8` 修正。
- 先前的 v1 掃描沒有帶 `--duration`，所以末鏡占比與時間碼越界規則都沒有生效。本次全部改用實際秒數重跑。

---

## 2. v1 基準展示集

v1 是單語（純英文或純中文劇本式）基準稿，`--check-sync` 對它們不適用（會固定出現「未偵測到中文導演母稿」WARN），所以不列入計算。

| 檔案 | 時長 | 修改前 | 問題 | 修改內容 | 修改後 |
|---|---|---|---|---|---|
| `six-beat-single-hit.txt` | 8s | 0F／0W | — | 不動 | 0F／0W |
| `ultra-speed-drone.txt` | 8s | 0F／0W | — | 不動 | 0F／0W |
| `continuous-brawl.txt` | 8s | 0F／1W | 完全沒有摔投或擒拿，9 鏡都在同一個距離互砍 | Shot 7 的「推退三步」改成「揪住衣領、沉胯發力把他摔退三步」（`seizes his collar, loads her hips and hurls him backward three steps`），補一記有發力部位的摔投 | **0F／0W** |
| `blade-light-21x9.txt` | 8s | 0F／0W | — | 不動 | 0F／0W |
| `ink-wash.txt` | 5s | 0F／0W | — | 不動 | 0F／0W |
| `facial-performance.txt` | 5s | 0F／0W | — | 不動 | 0F／0W |
| `bloodmoon-ultimate-ref2va.txt` | 10s | 0F／2W | 單人招牌技能長稿：1281 詞超出 820 預算；沒有下盤動作 | 不動（取捨見 §6） | 0F／2W |
| `jade-rift-summon-ref2va.txt` | 10s | 0F／1W | 1293 詞超出預算 | 不動（取捨見 §6） | 0F／1W |
| `impact-frame-screenplay.txt` | 7s | **2F**／2W | 這是刻意採用的劇本式格式（`references/screenplay-format.md`），validator 卻拿 H3 官方欄位去檢查，判它「缺欄位、無 Shot」 | 檔案不動；validator 新增劇本式模式（§5.3），改檢查欄位順序、逐秒時間軸是否連續、聲音／連續性／硬約束是否寫齊 | **0F／0W** |
| `force-field-explosion.txt` | 5s | 0F／0W | — | 不動 | 0F／0W |
| `anime-ref2va-part1.txt` | 15s | 0F／0W | — | 不動 | 0F／0W |
| `anime-ref2va-part2.txt` | 15s | 0F／1W | 沒有下盤動作 | 不動（FL2VA 接續段，動作承接 part1） | 0F／1W |
| `impact-frame-inline.txt`（追加） | 8s | **1F**／1W | `<Picture 1>` 被引用卻沒有定義；3 處否定詞（`not a live-action photo, not flat 2D anime`、`no 3D depth`） | `subject_definitions` 補上 `<Picture 1>` 廢墟街定義；否定句改寫成正面描述（`Clearly a polished 3DCG render with game-cutscene depth…`、`on a paper-flat surface`） | **0F／0W** |

**v1 重跑挑選**：只有 `continuous-brawl.txt`（新增摔投）與 `impact-frame-inline.txt`（標籤與否定詞修正）的內容有變，值得重跑對照；其餘 v1 檔案沒有改，沿用既有成片即可。指令見 §7.2。

---

## 3. v3 旗艦漫劇集：劇本修正

六套升級對象都已經 0 FAIL，但其中 4 套靠 `#!profile: ultra`／`facial` 檔頭略過了招式檢查。改跑 `--profile fight --strict-physics` 才看得到被遮住的問題：

| 套件 | 修改前（fight 檢視） | 人工審計發現 | 劇本修改（中英同步） | 修改後 |
|---|---|---|---|---|
| `rep01_thunder_cleave` | 刀路 62% | 單人清場魔兵海加天劍，`ultra` profile 合理；第 3 鏡特寫是 A 檔冷顏 | 文字不動，只升級 Dial（§4） | 0F／0W（ultra）|
| `rep02_ink_flame_sea` | 刀路 **73%**、沒有摔投 | 雙人對決卻只剩刀劍互砍；Shot 2 寫 `spinning and sidestepping`；Shot 3 寫 `gliding into a smooth close-up`，「滑行」語意容易被讀成人在滑；中文段落標題寫「12—15 秒」，實際切點是 11.6s | Shot 2 改成「熾川踏住玄瀾刀背蹬開，扯住披風把他甩向水幕，兩人錯步分開」（踢擊＋擒拿＋摔投）；Shot 3 改成 `easing into`；Shot 5 補上 `pivots on his rear heel`（後腳跟擰轉發力）；中文標題改為「11.6—15 秒」 | **fight 檢視也 0F／0W** |
| `rep03_jade_hammer_dragon` | 刀路 67%、沒有摔投 | 中文「踩水滑步閃過龍顎」、英文 `skims across the spray`，正是溜冰步高危寫法；對百米巨龍寫摔投不合物理，維持 `ultra` | 改成「踏浪點水連續側步，一腳蹬開龍頜借力」／`bounds across the spray in quick planted steps … kicks off its jaw`（離散步態加踢擊） | 0F／0W（ultra）|
| `orig02_bamboo_lantern_umbrella_vs_spear` | 1W（`skidding`） | Shot 5 有 `glides half a step back` 與 `drops to one knee skidding in water` 兩處滑行（`glides` 沒有 `across`，regex 抓不到，是人工審計找到的）；中文 Shot 4 寫「翻身滑退」，而且漏寫英文已有的擒腕與過腰摔 | 英文改成 `takes half a step back on planted heels`、`drops to one knee in a short splash of water`；中文 Shot 4 補「擒腕提膝頂其側腹，轉胯一記過腰摔」，「滑退」改「後躍」 | **0F／0W** |
| `ult01_brush_seal_army` | 0W | 文字健康；風險在執行層：P5 長開 `arcane_sigils` 會讓墨圈爬臉、變成曼陀羅 | 文字不動，換 P8（§4） | 0F／0W |
| `ult02_lunar_prism_domain` | 0W | 文字健康；同樣是 P5 法陣盤的風險 | 文字不動，換 P8（§4） | 0F／0W |

另外 3 套已經是雙軌配置（`orig01_v13` P9、`rep04_v4` P8、`rep05` P7），文字與 Dial 都不動。`orig01_v13` 與 `rep04_v4` 已確認不會觸發新的防破圖 WARN（有專門測試鎖住）。

---

## 4. v3 旗艦漫劇集：`render_v3_flagship.py` 雙軌升級

設計規則：
- 慢變軌（`--anchor`／`--burst`／`--closeup`）的邊界放在切點前 `0.25–0.35s` 起坡。不在切點上的邊界，必須是劇本裡寫出的鏡內相位轉折（例如「特寫，然後彈射」），並登記在 `beats`。
- `--hitstop` 只畫 0.25s 窄脈衝，會自動附帶衝擊閃幀。
- 地面交鋒的峰值等效運動不得超過 `+0.98`。`+0.80` 正軌只用在騰空或破空段。
- P9 依左眼 5.0 實證維持 `--hires-dials off`，並用 `--closeup` 鎖臉，正軌上限 `+0.29`。P7／P8 一律用 `phase-motion`。
- 以上規則全部寫進 `tests/test_flagship_jobs.py`，變成會被檢查的事實。

| 套件 | 切點 | 舊配置 | 新配置 | `--dry` 預算（base／峰值） |
|---|---|---|---|---|
| rep01 | 0／3.2／6.2／9.0／10.6／12.6 | P3＋hits，二採 off | **P8** phase-motion；burst `0.0:2.9:0.65`、`2.9:5.9:0.80`（騰空）、`8.7:10.5:0.80`（天劍破空）；anchor `5.9:8.7:-0.65`（特寫）、`12.3:15.0:-0.30`（扛刀佇立）；hitstop `10.6:10.85`；hit `0.8:1.1` | +0.30／+1.10（只在騰空與破空段） |
| rep02 | 0／3.2／6.2／9.0／11.6 | P3＋hits，二採 off | **P9** off；closeup `6.0:9.0`；anchor `5.9:8.7:-0.30`（低弓馬步）；burst `0.0:5.9:0.25`、`11.3:15.0:0.25`；hitstop `9.0:9.25`（黑白衝擊幀）；hit `11.8:12.1` | +0.19（特寫段）／+0.94 |
| rep03 | 0／2.8／6.0／9.0／12.2 | P3＋hits，二採 off | **P7** phase-motion；burst `0.0:5.7:0.65`、`5.7:8.7:0.80`（騰空）；anchor `8.7:10.2:-0.55`（特寫，10.2s 轉側面重錘）、`11.9:15.0:-0.30`（落石輕喘）；hitstop `0.35:0.6`、`10.4:10.65`；beats `[10.2]` | +0.32／+1.12（只在騰空段） |
| orig02 | 0／3.2／6.2／9.1／12.0 | P3＋hits，二採 off | **P7** phase-motion；burst `0.0:5.9:0.65`、`8.8:12.8:0.65`；anchor `5.9:7.8:-0.55`（特寫，7.8s 紅絲彈射）、`13.3:15.0:-0.45`（寒戟單膝定樁）；hitstop `12.8:13.05`（奪槍）；hit `3.6:3.9`、`10.6:10.9`；beats `[7.8, 12.8, 13.3]` | +0.32／+0.97 |
| ult01 | 0／3.2／7.0／10.8 | P5＋hit，二採 off | **P8** phase-motion；burst `0.0:2.9:0.65`、`6.7:10.5:0.80`（墨龍俯衝）；anchor `2.9:5.0:-0.55`（特寫，5.0s 轉環繞揮毫）、`12.6:15.0:-0.30`（落關收筆）；hitstop `10.8:11.05`；beats `[5.0, 12.6]` | +0.30／+1.10（只在墨龍俯衝段） |
| ult02 | 0／4.0／7.8／11.0 | P5，二採 off | **P8** phase-motion；anchor `0.0:3.7:-0.30`（點湖）、`3.7:7.5:-0.65`（結印特寫）、`12.4:15.0:-0.30`（凌空定樁）；burst `7.5:12.4:0.55`（冰柱破湖到冰蓮綻放）；beats `[12.4]` | +0.30／+0.85 |

`[dial-physics]` 行裡的 `anchor_eff≈-1.5` 是負軌最大值，來自 0.25s 的 `--hitstop -1.8` 脈衝，不是常駐值。定樁段的實際值是 base 加 anchor，約 `-0.35 ~ 0.00`，落在 `[-0.40, +0.05]` 的定樁區間內。

---

## 5. `validate_prompt.py` v4.0 升級

### 5.1 空泛打鬥句（WARN）
逐鏡比對 `attacks fiercely`、`fights intensely`、`epic battle`、`trade blows`、`engage in combat` 這類**片語**（不比對單字 `epic`，所以 `epic ultra-wide low shot` 不會誤報）。只有在**同一鏡**完全沒有身體機制詞（重心、腳跟、轉胯、肩肘腕膝、拳掌等）時才發 WARN。

### 5.2 短鏡翻轉堆疊（WARN）
單鏡時長 `< 1.5s`，且 `spins／flips／somersaults／whirls／cartwheels／twists mid-air` 系列詞合計 `≥ 4` 個 → 防肢體融化 WARN。邊界值（3 個詞、恰好 1.5s）有測試鎖住，不會發 WARN。

### 5.3 劇本式模式
同時有 `[參考鎖]`、`[本段]`，且沒有 H3 官方欄位時，改用劇本式契約檢查：
- 六欄位齊全且順序正確 → 否則 FAIL
- `[本段]` 的逐秒時間軸連續、沒有倒退 → 否則 FAIL
- 時間軸結束點不超出 `--duration` → 否則 FAIL
- 單段超過 8s → WARN
- `[聲音]` 沒寫「有沒有人說話」 → WARN
- `[連續性]` 缺首態或尾態 → WARN
- `[硬約束]` 沒寫無字幕 → WARN

劇本式依設計把禁止項集中在 `[硬約束]`，所以這個模式不跑否定詞檢查。

### 5.4 誤殺檢查
新規則對所有正式追蹤的 examples 都沒有誤報；`orig01_v13`、`rep04_v4` 有專門測試鎖住「不得觸發任一新 WARN」。

---

## 6. 已知取捨（保留的 WARN）

| 檔案 | WARN | 為什麼不修 |
|---|---|---|
| `bloodmoon-ultimate-ref2va.txt` | 字數 1281＞820；沒有下盤動作 | 單人招牌技能（`character-signature-skill.md`）長稿，靠逐項外觀鎖定換取身份保真，已有成片佐證；沒有對手，下盤規則不適用。砍 460 詞等於重寫，應另開任務並重新出片比對 |
| `jade-rift-summon-ref2va.txt` | 字數 1293＞820 | 同上 |
| `anime-ref2va-part2.txt` | 沒有下盤動作 | FL2VA 接續段，下盤招式在 part1 |
| `impact-frame-source.txt` | 1 處否定詞 | 素材類（`material` profile）原始卡片描述，沿用既有預算 |
| `rep01`、`rep03`（fight 檢視） | 刀路偏高 | 單人清場、以小打大巨龍，維持 `ultra` profile |

---

## 7. 第二波 GPU 重跑指令清單

> 前置條件：本 worktree 沒有 `assets/v3-manju/`（已被 gitignore）。請在有素材的主 checkout 執行，或先把素材資料夾複製過來。ComfyUI 需在 `127.0.0.1:8188` 上線。

### 7.1 v3 旗艦六套

```bash
# 0. 先保留舊的 P3/P5 成片做 A/B（--force 會覆蓋同名 mp4）
mkdir -p analysis/v3-manju/flagship/legacy_v3
for k in rep01 rep02 rep03 orig02 ult01 ult02; do
  mv analysis/v3-manju/flagship/${k}_15s_prism14.mp4 analysis/v3-manju/flagship/legacy_v3/ 2>/dev/null
done

# 1. 劇本 0 FAIL 閘門
for f in rep01_thunder_cleave rep02_ink_flame_sea rep03_jade_hammer_dragon \
         orig02_bamboo_lantern_umbrella_vs_spear ult01_brush_seal_army ult02_lunar_prism_domain; do
  python scripts/validate_prompt.py examples/v3-manju/$f.txt --duration 15 --check-sync --strict-physics
done

# 2. 只建圖核對 Dial 預算（不送 GPU）
python scripts/render_v3_flagship.py --dry rep01 rep02 rep03 orig02 ult01 ult02

# 3. 正式出片（每套約 SelfLift 14 步 15 秒；腳本跑完會自動做 measure_motion / measure_sharpness）
python scripts/render_v3_flagship.py --force rep01 rep02 rep03 orig02 ult01 ult02

# 4. 防滑與靜止對稱驗收
python scripts/measure_motion.py analysis/v3-manju/flagship/{rep01,rep02,rep03,orig02,ult01,ult02}_15s_prism14.mp4 --fps24 --symmetry --footplant

# 5.（選用）新舊並排對照
python scripts/compare_clips.py --before analysis/v3-manju/flagship/legacy_v3/rep01_15s_prism14.mp4 \
  --after analysis/v3-manju/flagship/rep01_15s_prism14.mp4 --label-before "v3 P3" --label-after "v4 P8" \
  --out analysis/v3-manju/flagship/rep01_v3_vs_v4.gif
```

驗收重點：
- 特寫段（rep01 6.2–9.0、rep02 6.2–9.0、rep03 9.0–10.2、orig02 6.2–7.8、ult01 3.2–5.0、ult02 4.0–7.8）沒有齜牙或臉部變形
- orig02 13.3s 後的單膝與 ult02 全片沒有貼地滑行（`--footplant`）
- ult01、ult02 末段沒有曼陀羅法陣爬臉

### 7.2 v1 重跑兩檔

```bash
COMMON="--engine selflift --unet Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors --dmad 0.8 \
  --scheduler simple --steps 14 --transition 6 --lowres-scale 0.6 --chunks 4 --hires-dials phase-motion --stage final"

# continuous-brawl（8s T2VA，新增 Shot 7 摔投；全程交鋒正軌，Shot 8 肘擊入顎頓幀）
python scripts/validate_prompt.py examples/continuous-brawl.txt --duration 8
python scripts/render_comfy.py $COMMON --preset P7 --burst 0.0:8.0:0.65 --hitstop 5.3:5.55:-1.8 \
  --prompt examples/continuous-brawl.txt --seconds 8 --seed 5101 --job v4_brawl --out out/v4_continuous_brawl.mp4

# impact-frame-inline（8s Ref2VA；2.4s 踏地閃幀、4.2s 出拳頓幀；--ref 順序請與原出片一致：街景＝<Picture 1>）
python scripts/validate_prompt.py examples/impact-frame-inline.txt --duration 8
python scripts/render_comfy.py $COMMON --preset P7 --hit 2.4:2.7 --hitstop 4.2:4.45:-1.8 \
  --prompt examples/impact-frame-inline.txt --ref <街景圖>.png --ref <人物圖>.png \
  --seconds 8 --seed 5201 --job v4_inline --out out/v4_impact_inline.mp4

python scripts/measure_motion.py out/v4_continuous_brawl.mp4 out/v4_impact_inline.mp4 --fps24 --footplant
```

上面兩條 `render_comfy.py` 都已用 `--dry` 驗證可建圖：brawl 預算 base `+0.32`、峰值 `+0.97`；inline 預算 base `+0.32`。

---

## 8. 變更檔案一覽

| 檔案 | 變更 |
|---|---|
| `SKILL.md` | v4.0 雙軌：frontmatter 觸發詞、第零階段雙軌路由與裁決規則、索引 |
| `references/interactive-director-flow.md` | 新增：雙軌判定、軌道 A 檢核表、軌道 B 三階段話術、時間軸概要模板、完整對話範例 |
| `references/guided-mode.md` | 情境改名 S1–S6，加上與四大維度的對照，修正「何時不出選單」的軌道裁決 |
| `scripts/validate_prompt.py` | 空泛打鬥句與短鏡翻轉堆疊 WARN、劇本式模式 |
| `scripts/render_v3_flagship.py` | 六套升級到 P7/P8/P9 雙軌、`beats`、`--dry` |
| `tests/test_validate.py` | UTF-8 子程序環境、v1 全集與 v3 九套 0 FAIL、新規則邊界測試、劇本式測試 |
| `tests/test_flagship_jobs.py` | 新增：JOBS preset、區段範圍、切點對齊、特寫負軌、P9 正軌上限 |
| `examples/continuous-brawl.txt`、`examples/impact-frame-inline.txt` | §2 |
| `examples/v3-manju/rep02`、`rep03`、`orig02` | §3 |
