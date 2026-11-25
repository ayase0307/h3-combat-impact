# REMIX Pika 路线：從角色圖到 2K 定稿

> 本機 REMIX Studio（127.0.0.1:8190）agent API 的打鬥片完整路线。
> 來源：remix-studio guide.md／agent/connect.json（2026-11-19 讀取；時間數字是官方實測 measured）。
> 與直接 ComfyUI 出片（render_comfy.py）的差別：REMIX 管角色包、專案、分鏡表、身份檢查、超分與拼接。

## 0. 連線

```python
# scripts/remix_api.py（token 直接讀檔，不進 shell、不印出）
python scripts/remix_api.py POST /connect/hello '{"client":"Hermes"}'
python scripts/remix_api.py GET /status
python scripts/remix_api.py GET /projects
```

- base：`http://127.0.0.1:8190/remix/agent/v1`；Bearer token 路徑由環境變數 `REMIX_TOKEN_FILE` 指定（預設 `<REMIX_STUDIO_DIR>/agent/token`）；每請求帶 `X-Remix-Client`。
- **每次連線重讀 GET /guide**，功能會更新，不要依賴記憶。
- 送件前讀 `GET /scenarios` 拿該模式的 hardConstraints。

## 1. 專案與分鏡表（送單必帶 project）

```python
POST /projects {"name":"H3打戲實測R3"}          # 使用者要求才建
POST /projects/current {"project":"…"}
PUT  /projects/{p}/storyboard {"doc":{"chapters":[
  {"id":"R3","title":"…","events":[
    {"id":"R3-T1","title":"…","shots":[
      {"shot":"R3-T1-a","title_zh":"燼兆","seconds":8}]}]}]}}
```

- `POST /jobs` 沒帶 project → 400 project_required。角色包跨專案 → 400 project_mismatch。
- 分鏡表決定審片室的章節→事件分組；shot 代號同專案不可重複。
- 送片帶 `plan.title_zh`（≤60 字）、`storyboard_zh`、`start_state`／`end_state`。

## 2. 角色包：四視圖 sheet 自動裁切

```python
POST /packs {"name":"chiyuan","display_name":"赤鳶","kind":"actor",
             "sheet":"./assets/hero.png","project":"H3打戲實測R3"}
```

- **有四視圖設定圖（左臉部特寫＋右正／側／背）就帶 sheet**，伺服器自動切成 4 張，約 20 秒。
  不要自己切圖。沒有設定圖才用 images 走 Qwen 8 視角。
- 場景包：`kind:"scene"`（或 prop），帶 images；混合版下場景走參考圖不走 RefMod。
- 怪獸也是 actor pack（含生物），跨段身份一致。
- 建包後補角色卡：`POST /packs/{name}/meta {"intro":"…","appearance":"…"}`。
- **codex 生圖逐個跑**：並行會搶同一個產出資料夾（round2 measured 教訓）。

## 3. 送件：pika768 定稿規格

```python
POST /jobs {
  "prompt":"<六欄位 Ref2VA 提示詞>",
  "refmods":["chiyuan","r3_t1_scene"],     # 順序＝標籤順序
  "mode":"pika768", "seconds":8, "aspect":"16:9",
  "seed":3101, "realism":"3d",
  "project":"H3打戲實測R3", "shot":"R3-T1-a",
  "label":"r3-t1-a", "ref":"r3-20261119-t1a",
  "plan":{"title_zh":"燼兆","start_state":"…","end_state":"…"}
}
```

- 提示詞標籤照 `GET /packs` 每個資產的 tag：actor 寫 `<Subject N>`、場景寫 `<Picture N>`，
  依 refmods 順序各自從 1 編號；**送出後看回應 warning 確認圖號對應**。
- Pika 自动把角色標籤改 `<Subject N>`、場景改實際 `<Picture N>`。
- `realism:"3d"`＝3D 國漫，不掛寫實 LoRA（本 repo 風格預設）。
- `pika_steps` 預設 6（定稿）；`pika_sparse` 預設 first（第 1 步稠密）。
- **Pika 不收額外 LoRA**（motion_dial 例外）——h3-fight 的 BUNNY 配方不能搬。
- 秒數 2–15；幀數 17k+5：**8 秒＝192 幀＝整 8.000s**（唯一整秒網格，卡點首選）。
- 等待用 `GET /jobs/{id}?wait=25` 輪詢，不要長 sleep。
- 同一鏡頭重抽帶相同 shot；新請求給新 ref（含日期時間）。

### 時間預算（5070 Ti 16GB，measured 引自 guide）

| 規格 | 5s | 8s（外推 inferred） | 15s |
|---|---|---|---|
| pika480 4 步 | 48s | ~77s | 250s（6 步） |
| pika768 6 步 Sol-Attn | 99s | ~160–200s | 324s |
| pika1440 | 609s | ~1000s | ~2231s（inferred） |
| recavsr 2× 超分 | 10+6.6×秒數 ≈ 43s | ≈63s | ≈109s |

一次只跑一個 GPU 工作；送件排隊會依序跑。

## 4. 段間檢查（送下一鏡前）

```python
GET /jobs/{prev_id}/continuity    # 與前後鏡的銜接，特別是人物左右位置
GET /jobs/{id}/identity           # state=done 後檢查；fail 重抽，warn/no_face 人工確認
```

## 5. 超分定稿與拼接

```python
POST /jobs {"kind":"upscale","source":"<job id>","engine":"recavsr"}
# 768P→2K（2688×1536），固定 2×，保留音訊與幀率；完成掛回來源 result.hd
POST /stitch {"jobs":["id1","id2",…],"loudnorm":true}
```

- **選定版本後才超分**，不要對每個抽卡版超分。
- recavsr 是 768P→2K 主力；tessera 生成式精修只對定稿（5s 約 10 分，tessera_hero 不可關）。
- result.hd 只有一格，換引擎會蓋掉前一個。
- stitch 用各鏡頭選用版；若要用超分版拼接，下載 result.hd.url 後本地 ffmpeg concat
  （stitch 是否取 hd 未驗證，本輪實測後寫回）。
- 超分鏈禁止 SolAttnPatch（_morton_h3  fatal）——REMIX 已內建處理，自己組圖時注意。

## 6. 疑難排解（2026-11-19 實測踩坑）

| 症狀 | 根因 | 修法 |
|---|---|---|
| 所有 pika 工作 ComfyUI 400 `prompt_outputs_failed_validation`、`Invalid image file: remix_pika_<job>_N.png` | config.json 的 comfy_input/output 與運行中 ComfyUI 的實際目錄不一致（ComfyUI 升級會遷移目錄，例 Installs→Shared）；暫存圖寫進沒人讀的目錄 | 用 `/object_info/LoadImage` 檔案數對比 filesystem 確認實際目錄；修 config（留 .bak）→ 重啟 REMIX |
| 修路徑後 `POST /jobs` 400 `missing_refmod`「找不到視角圖資料夾」 | pack 視圖資料夾在 `<comfy_input>/remix_studio/pack_<name>`，舊包建在舊路徑 | 把舊 `input/remix_studio/pack_*` 复制到新路徑（非破壞性，舊專案的包一起救） |
| 送件有 job id 但全失敗 | **收件≠成功**；POST 只代表 queued | 一律 poll 執行狀態；`GET /jobs/{id}` 回 `{job:{...}}` 包裝；終態含 `succeeded`/`failed` |
| 重送同一 ref 拿到舊失敗工作 | ref 冪等 | 重送換新 ref（例 `-r2`） |
| measure_sharpness／seam_check 報 ModuleNotFoundError: cv2 | Hermes 內建 python 沒有 cv2 | 用 `py -3`（系統 Python，cv2 5.0.0）跑這兩支；measure_motion 內建 python 可跑 |

**批次送件前必做煙霧測試**：先送 1 件、確認 `status=running`（ComfyUI queue_running=1），再放其餘。

**驅動腳本版本管理（R3 踩坑）**：從舊版驱动复制改版時，grep 所有舊版名詞
（json 檔名、log 名、字串後綴）——docstring 改了但程式碼行漏改會讓新驅動讀寫舊帳本、
跳過已存在鍵。不同版本用獨立 jobs/results 檔；**運行中進程擁有的狀態檔不要手改**
（進程記憶體覆寫你的編輯）；要改先停進程，或讓它跑完再清理。

## 7. 本輪路線圖（R3）

```
codex 生圖（逐個）→ POST /packs（sheet 裁切）→ PUT storyboard
→ 每段：寫提示詞 → validate_prompt.py → POST /jobs pika768
→ wait → identity + continuity + measure_motion/sharpness + 接觸表
→ 失敗重抽（換 seed 記錄）→ 全段過 → recavsr 超分 → 拼接 → 交付
```