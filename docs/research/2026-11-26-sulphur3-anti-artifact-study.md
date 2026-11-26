# Sulphur-3 抗動態破圖機制拆解與 PRISM 受控 A/B 實測（M1）

日期：2026-11-26｜硬體：RTX 5070 Ti 16GB＋i5-14600KF＋96GB RAM｜ComfyUI 本機 127.0.0.1:8188

> 範圍聲明：本研究**沒有**測 Sulphur-3 主模型 `s3.safetensors`／`s3_w4a8`（T2VA，不支援本專案 Ref2VA 多參考圖鎖臉）。
> 結論只涵蓋「把 Sulphur-3 的組件（corrector、Motion/STG 引導、校準 LoRA、Ref2VA 混合底模）嫁接到本專案 PRISM Ref2VA＋SelfLift 管線」的效果。
> 主實驗為單一 seed（5002）；n=1 不足以做統計結論，見〈侷限〉。

---

## 1. 推文主張 vs 倉庫實情

推文（@NFT_Chen，2026-11-25，經 fxtwitter API 鏡像讀取；x.com 直連回 402）主張：

| 推文主張 | 倉庫/原始碼實情 |
|---|---|
| 原版 H3 大動作會「融化崩壞」，Sulphur-3 經「完整微調」修好動態解剖，不再抽搐融化 | 官方 README 只寫「An uncensored video generation model based on MiniMax H3」，**沒有任何抗破圖宣稱或評測**。README 對 experimental 資料夾的建議是「I'd recommend ignoring them」 |
| 附帶「動作修正器」開箱即用，讓動作更穩 | `s3_corrector.safetensors` 確實存在。它是一個獨立的 2B 參數網路，用來修正**速度場殘差**，不是 LoRA，也不是針對動作的專用模組（見 §2）。原始碼 docstring 寫明「trained against one H3 checkpoint (S3)」；README 則寫「It also works with other H3 models」，但未附任何證據 |
| w4a8 版本 11.43GB，可在 16GB 卡上跑 | `quantized/s3_w4a8.safetensors` 大小為 11,433,462,056 bytes，與推文相符（本研究未實測） |
| 推薦設定 | 推文沒有給任何採樣參數。官方 Motion 範例工作流的設定是：s3_w4a8、SigmaShift 12/3、Euler simple 20 步、motion 1、STG 1、STG 層 20,21,22、until 0.25 |
| 多手多刃 | 推文沒有提到 |

推文另提及約 19 萬下載。這是熱度數字，不是品質證據。

---

## 2. 組件拆解

### 2.1 H3 Corrector（`S3_ComfyUI.zip` → `ComfyUI-H3-Corrector`）

**網路結構**（`corrector.py`）：
- 55 個 block 的時空 Transformer，width 1280、20 heads × 64，約 2B 參數；fp32 權重 8GB。
- 輸入是 concat(含噪潛空間 z, H3 速度 v) 共 48 通道，用 Conv3d 切成 (1,2,2) patch。
- 每個 block 依序做三件事：全片聯合自注意力（T/Y/X 三軸 RoPE，**所有幀所有位置一次看完**）、對 Qwen3-VL 原始 caption 隱狀態（5120 維）做交叉注意力、MLP。
- 每個 block 都受 (σ, σ_next, Δσ) 時間嵌入的 AdaLN 調變。

**採樣干預數學**（`__init__.py` 的 post-CFG 鉤子，每次模型評估後執行一次）：

```
v      = (x̂0 − z) / σ                       # H3 指向資料端的速度
r      = C(z, v, σ, σ_next, caption)          # 修正器預測的速度殘差
B      = budget × max(RMS(v), floor)          # 預算，budget 為訓練值 0.5
r̃      = r / sqrt(1 + RMS(r)² / B²)           # 平滑軟上限，RMS(r̃) < B
x̂0'    = x̂0 + σ · strength · r̃               # 只改影片切片，音訊原樣保留
```

等價於把這一步的 Euler 速度從 v 改成 v + strength·r̃，且修正幅度永遠小於 0.5×速度 RMS。

**判讀**：修正器是一個「看得見整段影片時空」的小型去噪輔助網路。它的全片自注意力能拿某幀的軀幹與手位置去約束其他幀，理論上可修正幀間不一致（融化、肢體數漂移）。但它是對 S3 的速度分佈訓練的；PRISM＋DMAD 的速度場分佈不同，實際效果必須實測（§4）。

### 2.2 Motion/STG 引導（`experimental/H3_Corrector_Advanced_Motion_STG  .zip` → `guidance.py`）

只在前 `until` 比例的步數啟用，之後退回 CFG 1：

```
STG   : g = v_pos + stg   × (v_pos − v_skip)    # v_skip：同提示，但 H3 第 20,21,22 個 double_block 被跳過
Motion: g = g     + motion× (g     − v_still)   # v_still：「所有動作凍結」的靜止版提示
音訊   : 保留 v_pos；最後以 CFG 1 走 cfg_function，post-CFG（修正器）照常執行
```

- STG 就是 Spatiotemporal Skip Guidance：用「跳層後變弱的自己」當負向，推離結構崩壞方向。
- Motion 項推離「靜止版提示」的預測，用來放大真實運動、壓低「原地抖動」。
- 兩者串接，所以 STG 的有效係數是 stg×(1+motion)。
- 成本：啟用的步數每步要多跑 2 個 H3 分支（共 3 個）。

### 2.3 其他檔案

- `experimental/s3_raw_lora_calibrated.safetensors`：metadata 顯示為 rank 128、`minimax_h3_variant=fl2va`、`kind=joint_calibration`（bounded SPSA 校準）、reload strength 1.0。它是 S3_raw 對 FL2VA 底模的差分 LoRA，**不是**為 Ref2VA 訓練的。
- `experimental/Sulphur-3_Ref2VA-hybrid_mid_int8_convrot_keepB0-1-49.safetensors`（22.1GB）：從檔名推斷是「保留 block 0、1、49 原權重，其餘換成 S3」的 Ref2VA int8 混合底模。
- 本機 `Motion_Repair.safetensors`：metadata 名稱為「UFC」，由 ai-toolkit 訓練 1600 步，是格鬥動作 LoRA。專案內沒有既有的強度紀錄，本研究用 0.8。

### 2.4 與 SelfLiftH3Sampler／MAIDialRack 的協同

- **Corrector 可直接相容**：SelfLift 一採、二採各自呼叫 `comfy.samplers.sample`，CFGGuider 的 post-CFG 鉤子與 `sample_sigmas` 都會傳入（日誌已證實一採 6 步＋二採 8 步每步都有修正）。
  - 注意 `sample_sigmas` 是**分段切片**，`start_step/end_step` 在二採會從 0 重算。所以本專案用「掛在哪一段的 MODEL」來選段，不用 step 範圍。
- **Motion/STG 原生不相容**：官方節點輸出 GUIDER，只能接 SamplerCustomAdvanced，而 SelfLift 沒有 guider 輸入口。
  - 本專案新增 `comfy_nodes/ComfyUI-H3-SelfLift-MotionSTG`，把同一套數學改掛成 MODEL 上的 PREDICT_NOISE wrapper。
  - 靜止版提示放進 SelfLift 的 negative 槽：cfg=1 時一般步驟不會評估 negative，只有 wrapper 啟用的步驟會用到它。
  - 只掛一採骨架期，並強制二採走獨立模型尾端，避免引導漏進二採。
- **MAIDialRack（P9）不會被繞過**：Dials 是以 `patches_replace["dit"][("double_block", i)]` 的區塊替換生效，會隨 model_options 帶進 `calc_cond_batch`。
  - STG 弱分支在第 20–22 層會覆蓋該層的 Dial 位移。這只影響弱分支，屬預期行為。
- **解析度限制**：修正器以 2×2 patch 切潛空間，要求潛空間寬高為偶數，也就是像素寬高必須是 32 的倍數。
  - `draft480`（854×480 → 潛空間寬 53）會在二採報錯。本專案已在 CLI 加早期防呆。768p（1344×768）與 hd/fhd 不受影響。

---

## 3. 實驗設計

### 3.1 共同設定（所有組完全相同）

```
python scripts/render_comfy.py --engine selflift --dmad 0.8 --scheduler simple --steps 14 --transition 6 \
  --lowres-scale 0.6 --chunks 4 --hires-dials off --preset P9 \
  --prompt examples/v3-manju/caseA_manju_8s.txt \
  --ref assets/v3-manju/caseA/hero_feixue.png --ref assets/v3-manju/caseA/villain_shuangjue.png \
  --ref assets/v3-manju/caseA/scene_snow_peak.png \
  --seconds 8 --stage final --seed <5002|5003> --job s3ab_<組名>_s<seed> --out analysis/sulphur3_ab/<組名>_s<seed>.mp4 \
  <下表的組別參數>
```

- 768p（1344×768）、24fps、8 秒 = 192 幀；SelfLift 一採 6 步（0.6× 潛空間）＋二採 8 步。
- 每組結束後呼叫 ComfyUI `/free` 卸載模型，避免前一組殘留的顯存狀態影響耗時。
- 批次執行器與分析腳本已複製到 `analysis/sulphur3_ab/tools/`：`run_ab.py`、`strips.py`、`keyframes.py`、`consec.py`、`paired.py`、`cropgrid.py`、`parse_log.py`。注意：`analysis/` 在 `.gitignore` 內，這些腳本與所有成品**不會**進版控。以下是可完整重現的組別參數。

### 3.2 組別

| 組 | 組別參數（附加在共同設定之後） | 驗證「干預有生效」的證據 |
|---|---|---|
| A_base | `--unet Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors` | 對照組 |
| B1_corr_both | A＋`--corrector s3_corrector.safetensors --corrector-stage both`（fp32） | **中止**：一採正常完成（82 s），但二採第 1 步（日誌標示「includes setup」）跑了 765 秒，顯存 15.8GB、使用率 100%，之後手動中斷。推斷是 8GB fp32 修正器加上 H3 超出 16GB，退到共享記憶體。對照：同設定的 3 秒冒煙測試可以跑完（二採 135 s），所以卡住的是 8 秒 768p 的組合，不是 fp32 修正器在任何情況都不能用 |
| B1b_corr_both_bf16 | B1＋`--corrector-precision bf16`（改走 Advanced 節點並以 bf16 計算） | 日誌：一採 6/6、二採 8/8 步都有修正 |
| B2_corr_low | A＋`--corrector s3_corrector.safetensors --corrector-stage low`（fp32） | 日誌：一採 6/6 步有修正；與 A 的灰階幀差 MAD 46.5 |
| B3_stg_motion | A＋`--motion-stg --still-prompt examples/v3-manju/caseA_manju_8s_still.txt`（motion 1、stg 1、層 20,21,22、until 0.5） | 一採前 3 步每步約 12 秒，之後約 4 秒，代表 3 分支只在前 3 步啟用 |
| B4_corrlow_stg | B2＋B3 | 兩者證據都有；B4 啟用 STG 的 3 步修正比 0.47／0.46／0.42 偏高 |
| C1_s3rawlora_low | A＋`--lowres-lora s3_raw_lora_calibrated.safetensors:1.0` | 無「lora key not loaded」警告；與 A 的 MAD 67.5 |
| C2_motionrepair_low | A＋`--lowres-lora Motion_Repair.safetensors:0.8` | 無未匹配鍵警告；與 A 的 MAD 45.7 |
| D_hybrid | `--unet Sulphur-3_Ref2VA-hybrid_mid_int8_convrot_keepB0-1-49.safetensors`（**仍保留 DMAD 0.8 與 P9**） | 正常載入 |

注意以下兩點與官方設定的差異：

- B3／B4 的 STG 設定為 until 0.5，作用於 SelfLift 一採的 3/6 步。官方範例是 until 0.25、跑 20 步單段採樣，兩者不可直接對照。
- B1b 的一採也是 bf16 修正器，但 B2 是 fp32。所以 B1b−B2 的差異同時包含「二採加掛修正器」與「一採精度不同」兩個因素，屬混雜變因。

### 3.3 量測與判讀方法

- 動態量：`measure_motion.py --fps24 --symmetry --footplant`（以 24fps 等效計的平均幀差、峰值節拍、靜止對稱、貼地滑行偵測）。
- 清晰度：`measure_sharpness.py`（全片均勻取 16 幀的 Laplacian 變異數，報 median 與 p10）。
  - 這個值會被構圖左右：遠景、刺繡密集的中景天生分數高，大特寫的皮膚天生分數低。
  - 因此另外算兩種**配對**清晰度：
    - B1b vs B2：兩者鏡頭結構、切點與機位相同，可逐幀比。但人物姿態不完全相同（見 `crop_s5002_b1b_vs_b2_f072.jpg`），所以這是「近似配對」。
    - f104–f110 臉部特寫窗：中央裁切後比較。
- 逐幀目檢（主要證據）。全部對照圖存於 `analysis/sulphur3_ab/`：
  - `strip_s5002_w*.jpg`：依劇本**事先**固定 5 個時間窗，每窗 6 幀。
  - `key_s5002_f*.jpg`：各組同幀號，640 寬放大。選幀時避開劇本切點（4.0／5.0／6.4 秒）前後至少 3 幀。
  - `consec_s5002_*.jpg`：連續逐幀，用來看抽搐、刀刃連續性與剪接混疊。
  - `zoom_D_f*.jpg`、`crop_s5002_*.jpg`：原解析度 1:1 局部，用於握持、肢體與細節軟化。
- 判讀原則：一組**有執行**該鏡劇本動作時，才判定破圖是否改善。動作量變少、或改成擺拍，使得「沒機會破圖」的情況，不算作修好。

## 4. 結果

### 4.1 指標總表

**seed 5002（全部 8 組）**

| 組 | 牆鐘時間 | ComfyUI 一採／二採 | 動態量（全程 24fps 等效）| 峰值節拍 | 清晰度 median／p10（全片 16 幀）| 特寫窗 f104–110 中央裁切 | 滑步／靜止對稱偵測 |
|---|---|---|---|---|---|---|---|
| A_base | 251 s | 51／163 s | 32.88 | 3 | 201.9／84.4 | 50.4 | 未觸發 |
| B1b_corr_both_bf16 | 481 s | 81／358 s | 28.13（−14%） | 3 | 104.9／53.7 | 27.4 | 未觸發 |
| B2_corr_low | 301 s | 83／169 s | 31.57（−4%） | 3 | 133.5／72.9 | 40.4 | 未觸發 |
| B3_stg_motion | 321 s | 104／161 s | 34.15（+4%） | 4 | 169.6／67.8 | 137.0 | 未觸發 |
| B4_corrlow_stg | 371 s | 137／169 s | 32.97（±0%） | 2 | 126.2／98.3 | 43.7 | 未觸發 |
| C1_s3rawlora_low | 261 s | 56／163 s | 29.93（−9%） | 3 | 206.6／140.4 | 324.0† | 未觸發 |
| C2_motionrepair_low | 261 s | 55／161 s | 32.75（±0%） | 1 | 222.0／109.0 | 73.5 | 未觸發 |
| D_hybrid | 272 s | 58／172 s | 21.11（−36%） | 6 | 386.1／254.3 | 473.1† | 未觸發 |

**seed 5003（複驗 5 組）**

| 組 | 牆鐘時間 | 動態量 | 清晰度 median／p10 | 特寫窗 |
|---|---|---|---|---|
| A_base | 261 s | 32.30 | 131.8／96.6 | 73.3 |
| B1b_corr_both_bf16 | 481 s | 28.00（−13%） | 71.8／43.3 | 34.5 |
| B2_corr_low | 301 s | 31.18（−3%） | 98.7／65.3 | 54.0 |
| C2_motionrepair_low | 261 s | 32.71（+1%） | 157.4／82.4 | 61.0 |
| D_hybrid | 271 s | 20.39（−37%） | 437.4／243.1 | — |

讀表注意：

- † C1、D 在 f104–110 不是同一個大特寫鏡，而是刺繡密集的中景，所以這一欄不可與其他組比較。
  - 已用 `key_s5002_f108.jpg` 確認 A／B1b／B2／B3／B4／C2 六組同為眉眼大特寫，可以互比。
  - seed 5003 用 `key_s5003_f108.jpg` 確認 A／B1b／B2／C2 同為大特寫，D 為中景。
  - 即使同鏡，髮絲與刺繡入鏡的比例仍不同（例如 B3 的髮絲較多），差距小於約 1.5 倍時不宜解讀。
- 全片清晰度受構圖支配。A 自己換 seed 就從 201.9 掉到 131.8（−35%），所以 ±35% 以內的全片清晰度差異都**分不出**是干預造成的。
- 最接近乾淨的清晰度比較是 B1b vs B2 的**逐幀配對**。兩者同機位、同切點，但人物姿態有差異，逐幀 MAD 約 27–28，所以是近似配對：

| seed | B1b／B2 逐幀清晰度比 median（p10–p90） | B1b 比 B2 軟的幀比例 | 逐幀灰階 MAD median |
|---|---|---|---|
| 5002 | 0.724（0.581–0.927） | 94.3% | 28.5 |
| 5003 | 0.687（0.531–0.891） | 95.8% | 26.8 |

  - 這代表二採加掛修正器（bf16）會讓畫面變軟約 30%，兩個 seed 都重現。
  - 由於一採精度也不同、姿態也有差，這個數字含有混雜變因。
  - 原解析度 `crop_s5002_b1b_vs_b2_f072.jpg` 可以看到，B1b 的碎石與袖口紋飾較平滑、細節較少。
- 動態量的雜訊底：A 換 seed 的差是 32.88 → 32.30（約 2%）。這只是單一對 seed 的估計，雜訊底本身並不可靠。
  - C2（±1%）、B4（±0%）落在雜訊底內，視為與 A 無法區分。
  - B2（−4%／−3%）在兩個 seed 都同方向下降，略大於這個粗估的雜訊底，但幅度太小、樣本太少，不足以下結論，只記為「可能略降」。
  - B1b（−13～−14%）與 D（−36～−37%）的下降在兩個 seed 都重現，幅度也遠大於雜訊底。
- 修正器的殘差／速度 RMS 比：
  - fp32 一採各步依序為 0.42、0.37、0.27、0.15、0.11、0.09。
  - bf16 二採 8 步的平均是 0.057（最大 0.076）。
  - B4 在 STG 啟用的前 3 步升到 0.47／0.46／0.42，接近 0.5 的預算上限，代表 STG 放大後的速度場更常被修正器「拉回」。
  - 這些比值沒有 S3 原生的參考值可以對照，因此**不**判定為「分佈不匹配」，只如實記錄。
- 「未觸發」只代表 `--footplant`／`--symmetry` 偵測器沒有報警，不等於確定沒有滑步。

### 4.2 逐幀目檢（主要證據）

判讀只在各組都執行同一段劇本動作、且離切點至少 3 幀的位置進行。

> 更正：初看 f120 的關鍵幀時（該圖已依避開切點的原則刪除重產），A 的嚴重糊化像是「融化」，B2 看起來較乾淨。經 `consec_s5002_cut5s_f114-125.jpg` 逐幀確認，A 在 f117–f119 才從特寫切到動作鏡，f120 是剪接後第 1–2 幀的混疊；B2 則早已在動作鏡中段。兩者時間點不對等，**這個「B2 改善融化」的判讀已撤回**。

| 鏡次（幀） | A_base | B1b 兩段修正器 | B2 一採修正器 | B3 Motion/STG | B4 修正器+STG | C1 S3 校準 LoRA | C2 Motion_Repair | D Ref2VA 混合底模 |
|---|---|---|---|---|---|---|---|---|
| 鏡1 交鋒 f24–33（s5002） | 有執行低身突刺；f28–31 緋雪的劍刃消失在身體下；f33 出現兩道紅色斜線（劍或拖尾不明） | 有執行；f26 臉與持劍臂明顯糊化；f30 劍刃不見 | 有執行；f27–31 劍刃舉起可辨、握持清楚 | 有執行；劍刃全程清晰可辨；f33 紅色拖尾分裂成 3–4 道平行線 | 有執行；雙方劍刃被畫成貫穿半個畫面的直線光束（刃長失真）；f33 紅刃彎成弧形 | 改為緋雪中近景，突刺不完整 | 有執行；f26–31 劍刃淡弱；f33 長紅光束 | 姿態直立、正面擺拍；f30 雙方手中都看不到劍；動態最小 |
| 鏡1 交鋒（s5003） | 中度動態模糊，可辨 | f29–31 紅刃變成多道紅條 | 與 B1b 同機位，同樣出現多道紅條 | — | — | — | f29 交叉紅 X 光痕 | 遠景小人物，f30–31 大圈紅色弧形特效，近乎沒有實際交鋒 |
| 鏡3 特寫 f104–110（兩個 seed） | 五官完整 | 五官完整，皮膚與刺繡較軟 | 五官完整 | 五官完整 | 五官完整 | 中景（不同鏡） | 五官完整 | 中景（不同鏡）；s5003 改成持劍中景 |
| 鏡4 摔投 5.0–6.2 s（兩個 seed，`strip_s500*_w4`） | 兩個 seed 的 8 組都**沒有**清楚畫出擒腕＋髖摔。PRISM 組多為空中交錯接霜絕臉部近景；B1b f126–132、B4 f132 霜絕手臂有拖影；C1／D 是雙人站姿中景、刀刃交叉。不納入改善判讀 | ← | ← | ← | ← | ← | ← | ← |
| 鏡5 踢擊下半身 f160（s5002，`crop_s5002_legs_f160.jpg` 1:1） | 踢腿＋支撐腿，結構合理 | 踢腿被拉成一長條黑色塊，但沒有多腿 | 同 B1b，踢腿拉長，沒有多腿 | 支撐腿＋彎曲踢腿，沒有多腿 | **疑似三條深色褲腿**（左支撐、中彎膝、右上踢）；霜絕是白褲黑靴，所以較可能是緋雪多出一條腿 | （不同鏡，未檢） | 踢腿拉長，沒有多腿 | （站姿，沒有踢擊） |
| 鏡5 繳械 f168–187（s5002） | 霜絕跪地，f173–175 冰劍「憑空」回到手上（未繳械）；f186 握持良好 | 跪地空手；f186 雪地插著一把**黑色**劍（與冰藍劍色不一致） | 同 A，f173–175 冰劍回手；f186 冰劍落在地上 | f168–171 冰劍旋轉飛出，最接近劇本；f173–175 空中的劍變成黑柄 | f174–175 冰劍回手；f186 緋雪的**赤刃變成銀刃**（武器識別漂移） | 雙人中景互砍；f180 劍落地、霜絕空手（有繳械） | 霜絕全程持劍（未繳械）；f186 冰劍落地 | f180／f186：前景一把巨大冰劍飛出，**同時**霜絕手中還握著另一把冰劍（原解析度 `zoom_D_f180.jpg` 確認）＝**刀刃重複** |
| 鏡5 繳械（s5003） | f160 冰劍被擊飛（有繳械） | 踢擊時霜絕仍持劍 | f160 霜絕持冰劍，同時右上有一把黑劍飛出（兩把劍） | — | — | — | f160 霜絕空手、黑劍飛出（有繳械） | 雙方站姿持劍，沒有踢擊、沒有繳械 |

整體觀察：

1. **沒有任何一組明顯消除了融化或多刃。**
   - 鏡1 的劍刃消失與拖尾分裂，在 A 和各干預組都會出現。
   - 刀刃重複與武器顏色漂移分別出現在 A（s5003）、B2（s5003）、B4、D 等組，不是某個干預專屬的問題。
   - 在檢查過的幀中，肢體融化或多手多腿只在 B4 的 f160 看到一例疑似多腿。
   - 由於 A 與各干預組的構圖本來就不同，這些觀察只能說「看不到改善」，無法推論修正器在哪個階段失效。
2. **修正器的主要可見效果是「變軟」，不是「變穩」。** 二採加掛時配對清晰度 ×0.69–0.72，1:1 局部（`crop_s5002_b1b_vs_b2_f072.jpg`）可以看到紋飾與碎石細節被抹平。
3. **D 混合底模的「乾淨」來自動得少。** 兩個 seed 的動態量都下降 36–37%，鏡頭偏遠景擺拍，踢擊、摔投、繳械等劇本動作大量沒有執行；繳械段還出現刀刃重複。依 §3.3 的判讀原則，這**不**算修好破圖。
4. **B3 Motion/STG 是唯一在單一 seed 上同時保住動態量（+4%）、劍刃可辨度與劇本繳械動作的組。** 但它只跑了 seed 5002，n=1，在 §5 列為「待複驗候選」，不是推薦。

## 5. 工程結論：何時開、何時不開

### 5.1 推文主張的實測結論

- 「Sulphur-3 修好融化抽搐」：本研究無法驗證，因為主模型是 T2VA，沒有測。
  - 能測的是它的 Ref2VA 混合底模（D）。在 8 秒劍鬥劇本上，它的做法是把動態量降低約 37%、改成擺拍構圖，而且仍出現刀刃重複。對本專案「高動態＋鎖臉」的目標來說，這是**負面**交換。
- 「附帶修正器讓動作更穩」：在 PRISM＋DMAD＋SelfLift 管線上**看不到**穩定性改善，只看到構圖改變、畫面變軟和額外耗時。
  - 修正器的 docstring 寫明它是對 S3 訓練的。換到 PRISM 底模後效果不佳，與這點一致。不過本研究只能說「沒效」，無法區分是「底模不匹配」還是「修正器本身就沒效」。

### 5.2 開關建議

| 組件 | 建議 | 理由 |
|---|---|---|
| `--corrector`（兩段，bf16） | **不開** | 耗時 +92%（251→481 s）；配對清晰度 ×0.7，兩個 seed 都重現；動態量 −13%；沒有可見的破圖改善 |
| `--corrector`（兩段，fp32） | **16GB 卡跑 8 秒 768p 時不要用** | 8 秒 768p 卡在二採第 1 步 765 秒後被中斷；3 秒短片可以跑完。需要兩段時改用 `--corrector-precision bf16`，但見上一列 |
| `--corrector --corrector-stage low` | 預設不開 | 耗時 +20%；構圖改變（與 A 的 MAD 46.5）；看不到破圖改善。動態量（−3～−4%）與全片清晰度在兩個 seed 都略低於 A，方向一致，但都在雜訊範圍內，不足以下「變軟」的結論 |
| `--motion-stg`（until 0.5） | 預設不開；**列為下一輪複驗候選** | 耗時 +28%；單一 seed 上動態量 +4%，劍刃可辨，繳械動作最貼近劇本；但 n=1，而且需要手寫靜止版劇本 |
| 修正器＋STG（B4） | 不開 | 耗時 +48%；劍刃被拉成貫穿光束、武器顏色漂移、f160 疑似多腿；STG 啟用步的修正比貼近預算上限，顯示兩者作用方向可能衝突（推測，未驗證） |
| `--lowres-lora s3_raw_lora_calibrated` | 不開 | 這是 FL2VA 的校準差分，不是 Ref2VA 用的；構圖改變大（MAD 67.5），動態量 −9%，看不到破圖改善 |
| `--lowres-lora Motion_Repair:0.8` | 可開可不開（無害、無益） | 零額外耗時，兩個 seed 的動態量與清晰度都與 A 無法區分 |
| Sulphur-3 Ref2VA 混合底模 | **戰鬥鏡不用** | 動態 −37%（兩個 seed 都重現）、擺拍化、刀刃重複。如果是低動態的文戲、需要更銳利的遠景，可以另外評估 |

### 5.3 推薦 CLI

維持現行基線，也就是本研究的 A 組，不掛任何 Sulphur-3 組件：

```
python scripts/render_comfy.py --engine selflift \
  --unet Minimax-h3_Singularity_x_10Eros-Max_PRISM_int8.safetensors --dmad 0.8 \
  --scheduler simple --steps 14 --transition 6 --lowres-scale 0.6 --chunks 4 --hires-dials off --preset P9 \
  --prompt <劇本> --ref <主角> --ref <對手> --ref <場景> --seconds 8 --seed <seed> --stage final \
  --job <job> --out <out.mp4>
```

下一輪若要複驗 Motion/STG，在上面這條命令後加：

```
  --motion-stg --still-prompt <同劇本的靜止版> --stg-until 0.5
```

建議至少跑 3 個 seed，並與官方的 until 0.25 做對照。

## 6. 侷限

- **樣本數**：主實驗 n=1（seed 5002）；複驗 seed 5003 只涵蓋 A／B1b／B2／C2／D。B3、B4、C1 只有單一 seed，結論強度相應較弱。
- **未測 Sulphur-3 主模型**：T2VA 不支援本專案的多參考圖鎖臉，所以 §5.1 對推文「主模型修好融化」的主張不作判定。
- **B1b 的精度混雜**：B1b 一採用 bf16 修正器，B2 用 fp32，所以 B1b−B2 的差異同時含「二採加掛」與「一採精度」兩個因素；兩者人物姿態也不完全相同。
- **D 組不是純底模比較**：D 沿用了為 PRISM 調校的 DMAD 0.8 LoRA 與 P9 Dials。它的動態下降與擺拍化，不能全部歸因於 Sulphur-3 混合底模本身；換用適合它的 LoRA／Dials 設定後結果可能不同。
- **STG 設定**：本研究用 until 0.5、作用在 SelfLift 一採的 3/6 步，與官方 until 0.25／20 步單段不同。靜止版劇本 `caseA_manju_8s_still.txt` 為手寫，也會影響 Motion 項。
- **目檢解析度與覆蓋率**：逐幀對照多為 225–640 px 寬的縮圖，原解析度 1:1 只檢查了 `zoom_D_f*.jpg`、`crop_s5002_legs_f160.jpg` 與 `crop_s5002_b1b_vs_b2_f072.jpg`。手指層級的握持細節判讀可信度有限，肢體融化檢查也只覆蓋 f160 一個踢擊幀。
- **清晰度指標**：全片 16 幀取樣受構圖支配，跨組比較以配對指標與目檢為準。
- **偵測器**：滑步與靜止對稱偵測「未觸發」不等於不存在。
- **流程**：任務簡報禁止再派子代理，所以使用者全域設定中的 checker／reviewer 子代理審查**沒有**執行；改以非回歸腳本（16 組預設圖逐位元一致、修正器 3 段與 Motion/STG 192 組接線）與 `tests/test_validate.py`（9 項通過）自驗。
