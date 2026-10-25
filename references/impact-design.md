# 打擊感設計：打擊結構、力度分級與材質反應

> 2026-10-26 改版：原「六拍」的第 3 拍「停 Hit Stop」在 H3 上不寫進提示詞（實測會被放大成 0.5–1 s 停頓，參考片命中後也幾乎不減速），改在組裝做。衝擊幀的形態與長度一律見 `impact-frame/forms.md`，路徑選擇見 `SKILL.md` §3。

## 0. 為什麼 AI 打鬥會「軟」

AI 影片模型傾向生成**平均化的中間狀態**：它會把「出拳」畫成一條平滑的插值曲線，於是缺少三件事——

1. **變速**（真實打擊是 0.4 秒蓄力 + 0.08 秒命中）
2. **停頓**（命中瞬間物理上必須有能量轉移的停滯）
3. **不對稱**（攻擊者過衝、受擊者延遲反應、布料晚半拍）

所以提示詞的任務不是「描述打鬥」，而是**強制插入變速與不對稱**；停頓交給組裝（複製幀，放在命中前或切鏡後）。

---

## 1. 打擊結構（原六拍；H3 版是五拍＋組裝停頓）

### 拍 1｜蓄 Anticipation
- **畫面**：反向預備動作（要往右打，先往左收）；重心壓到後腳；握把處指節泛白；衣襬與髮尾因急停而向前甩。
- **鏡頭**：`the camera pushes in with small amplitude at slow speed`，或反向緩推。**蓄力時鏡頭必須穩或反向**，任何同向運動都會洩掉張力。
- **不寫靜止詞**：`hangs poised`、`still for half a second` 在 H3 會變成 1–3.7 s 空等（EP03 實測）。蓄力用**動作與光**：能量在掌心聚集、碎石浮起、燈一片片滅、環境「預反應」（見 `ultimate-moves.md`）。
- **可寫**：`her weight sinks into the rear leg as the blade draws back behind her shoulder`
- **別寫**：`she prepares to attack`（太抽象，模型只會給一個站姿）

#### 攻擊必須寫成三段路徑（實測有效）

只寫「結果」模型不會動。要寫 **起始位置 → 軌跡 → 終點**：

| 寫法 | 結果 |
|---|---|
| ❌ `brings both blades down in a cross` | 他舉著刀不動（模型不知道刀從哪來） |
| ✅ `raises the right blade above his head and holds the left blade low, then drives the right blade down in a diagonal arc toward her left shoulder` | 完整抬刀 → 下劈 |

**雙武器要分別寫位置。** 只寫 `both blades` 模型會簡化成一把；「one high, one low」才會給兩把。

#### 眼神與姿態約束要放在鏡頭開頭

放在鏡頭**最後一句**的約束，權重會被後面的動作描述蓋過（實測：寫在結尾的 `her eyes stay on him` 完全失效，她整鏡低頭）。

```text
[Shot 5] At 00:05.600, ... She keeps her head turned toward him and her eyes fixed
on his mask the whole time. ...
```

第一句就鎖定，模型會把它當成整鏡的狀態。

### 拍 2｜觸 Contact（衝擊點）
- **畫面**：衝擊點。L1–L2 用局部星芒（P0）；L3 用同段亮度事件（P1）；L4 用衝擊幀串（P2）或分開合成（P3）——見 `SKILL.md` §3 決策卡。
- **鏡頭**：二選一——相機鎖死讓特效推開背景，或 `the frame jolts hard for a few frames on the impact and settles almost immediately`。
- **可寫（P1）**：`the frame blows out to white at the instant of contact as radial speed lines tear outward, then snaps straight back`
- **關鍵**：H3 不遵守幀數（`for two frames` 實測亮 11–45 幀）。寫「回來」（`then snaps straight back`），精準長度交給組裝。
- **形態**（白閃、黑閃／負片、單色剪影、漫畫格、背景翻色、曝光壓暗…）見 `impact-frame/forms.md`。

### （原拍 3｜停 Hit Stop → 移到組裝）
- 參考片 94 個強白事件，命中後減速只有 26%；Seedance 原提示詞寫 `two-frame hit-stop`，命中處 0 段重複幀；H3 寫 `near-freeze` 被放大成 0.5–1 s。
- **重量改由三件事給**：命中前微停（組裝時複製 2–10 幀，或寫成「頂住半拍」的畫面）、命中後切到下一鏡的 0.15–0.25 s reveal、命中後加速（`then the camera accelerates with the shockwave`）。見 `impact-frame/shake-and-timing.md` §2。

### 拍 4｜洩 Release
- **畫面**：衝擊波環、碎片、塵環、水幕、氣浪；方向必須與攻擊方向一致（橫掃 → 扇形，下劈 → 地面環）。
- **可寫**：`a ring of grey dust bursts outward along the ground`, `stone shards spray away from the impact point`, `water sprays up in a thin sheet`
- **關鍵**：**方向感**。寫 `explodes everywhere` 等於沒有方向，力量會散掉。
- **升級**：把「洩」展開成**力場四通道**（光／空氣／物質／粒子），見 `force-field.md`。只寫碎片與塵土，等於只開了物質通道——這是最常見的「貼圖感」來源。

### 拍 5｜退 Reaction
- **畫面**：受擊者被打飛／滑退／破防；頭髮與衣襬延遲半拍；攻擊者過衝半步。
- **受擊不延遲**：重擊的命中 → 衝擊波 → 人被掀起，寫在同一句（`in the same unbroken moment`）；只有衣髮延遲，身體不延遲（EP03 實測：分開寫，模型讓人跪著等 1 秒才飛）。
- **可寫**：`he is hurled backward, boots gouging two lines in the wet stone`, `her ponytail whips a beat late`, `his follow-through carries him half a step past the strike`
- **關鍵**：**overlapping action**（延遲跟隨）是 AI 打鬥最缺的物理細節，一句就能補上。

### 拍 6｜收 Recovery
- **畫面**：回到 ready pose；殘留粒子飄落；鏡頭回穩。
- **可寫**：`she settles into a low guard as embers drift down through the lantern light`

---

## 2. 力度分級（選一級，不要混）

| 級別 | 適用 | 總長（24fps） | 衝擊點路徑 | 鏡頭 | 特效預算 |
|---|---|---|---|---|---|
| **L1 輕** | 試探、格擋、擦身 | 5–8 幀 | P0 局部星芒 | 短抖或不震 | 只有火花，不加衝擊波 |
| **L2 中** | 乾淨命中、破招 | 10–16 幀 | P0／P1 | 短抖 | 火花 + 局部碎片 |
| **L3 重** | 擊退、破防、撞牆 | 20–32 幀 | P1（要精準走 P3） | 短抖 + 短暫失焦 | 衝擊波環 + 塵 + 環境物件晃動 |
| **L4 必殺** | 收尾、對撞、大絕、秒殺 | 多鏡頭 | **P2**（或 P3） | 鎖死，或回來猛震三下 0.5 s 停穩 | 三拍：命中 → 衝擊幀串＋衝擊波 → 後果 |

「停頓幀數」欄已刪：停頓在組裝做（見上）。

**L4 的三拍結構**（取代舊五段版；舊版第 3 段「凍結 0.3 秒全畫面近白」在 H3 上會變長時間發光）：
1. **命中**（具名部位、寫明與被保護者的距離；命中不拍飛行：`within a single frame … is already rammed into …`）
2. **衝擊幀串＋衝擊波**（獨立一段，P2；回原鏡頭時特效已全開、第一格衝擊波環已外擴，隔一下再炸第二圈）
3. **後果**（受擊者在同一句被掀飛；傷害寫成命中當下的分解事件；下一段承接殘破）

蓄力可以放在命中前，但用動作與光蓄。完整寫法見 `impact-frame/burst-strip.md` 與 `ultimate-moves.md`。

### 2.1 三級碰撞體系（先定義、後文用代號觸發）

〔教學 v5 與 1026 圖文提示詞；H3 未實測。秒數類（抽幀、定格）在 H3 只會被理解成風格詞，精度要後製〕

在提示詞開頭（或交付說明）把碰撞特效**定義一次**，後面每次碰撞只寫「觸發輕／重碰撞」，省字數也讓每次碰撞一致：

| 級別 | 衝擊幀 | 負片範圍 | 鏡頭 | 粒子／物質 | 組裝端 |
|---|---|---|---|---|---|
| **輕碰撞** | 黑白水墨衝擊（局部） | 局部負片 | 沿軸向微甩 | 墨點、水珠、暗金粒子飛濺 | 複製 1 幀（約 0.05 s） |
| **重碰撞** | 放射水墨衝擊 | 中心負片 | 猛沉、猛甩回彈 | 前景潑墨／中層水片／後層石屑**三層爆開** | 複製 2 幀（約 0.1 s） |
| **大招** | 全屏黑白衝擊（P2） | 全屏負片後閃白 | 徑向劇烈震動＋中心魚眼 | 三層環形衝擊波 | 定格 3–4 幀（約 0.15 s）＋魚眼後製 |

H3 寫法：開頭一句 `Every light clash triggers a small black-and-white ink flash at the contact point and a sideways jolt along the camera axis; every heavy clash triggers a radial ink burst at the centre of the frame, the camera sinking hard then rebounding, with ink, water and stone bursting out in three layers.` 後面就寫 `triggering a light clash`／`triggering a heavy clash`。

---

## 3. 材質反應對照表（寫對材質，力量才落地）

| 被擊材質 | 該出現的反應 | 英文寫法 |
|---|---|---|
| 濕石板 | 水膜飛濺、石屑、回彈聲 | `water sprays off the wet flagstones`, `chips of stone skip away` |
| 木頭／屋瓦 | 木屑、瓦片震落、粉塵 | `roof tiles rattle loose and fall`, `splinters burst out` |
| 金屬 | 白熱火花、金屬尖鳴、凹痕 | `white-hot sparks spray from the contact point` |
| 布料 | 撕裂、褶皺被氣壓推平 | `the silk is flattened by the pressure wave` |
| 血肉 | 無血漿特寫，用**受力變形 + 汗/塵** | `his cheek deforms under the blow, sweat spraying` |
| 能量護盾 | 環形波紋、裂紋、折射 | `concentric ripples race across the barrier, then crack` |
| 空氣 | 音爆錐、氣浪、雨被推開 | `a visible pressure cone forms`, `the rain is pushed into a radial sheet` |
| 地面整體 | 龜裂、下陷、揚塵 | `the flagstones crack in a starburst and sink slightly` |

---

## 4. 時間預算（以 24 fps 換算，成品時間軸）

| 節拍 | 秒 | 幀 |
|---|---|---|
| 蓄 | 0.30–0.45 | 7–11 |
| 觸 | 0.04–0.08 | 1–2（成品；生成端不寫幀數） |
| （命中前微停，組裝） | 0.08–0.4 | 2–10 |
| 洩 | 0.20–0.30 | 5–7 |
| 退 | 0.15–0.20 | 4–5 |
| 收 | 0.05–0.10 | 1–2 |

一個 L2 命中 ≈ 0.8–1.1 秒。**7 秒片段 = 5–6 個 L1/L2 命中，或 1 個 L3 + 2 個 L1。** 超過這個密度，模型會把所有動作壓成模糊。

---

## 5. 節奏曲線（整段而非單擊）

一段 15 秒的打鬥，力度必須有起伏，否則觀眾 6 秒後就麻木：

```
L1 ─ L1 ─ L2 ─ L1 ─ L3 ──（靜 0.8s 對峙）── L4
```

- **每 3–4 擊插入一次「靜」**：呼吸、眼神、雨滴、燈火搖曳。靜是為了讓下一擊更響。**大爆之後**最適合放一個「靜」的極近特寫（嘴唇、只有道具光、幾乎無聲）。
- **L4 之前不寫完全靜止**（舊規則「0.5–1 秒完全靜止」在 H3 會被放大成 1–3.7 s 空等）。要「靜→爆」的對比：用**眼部極近特寫＋瞳孔倒映來襲物**、**大爆前先暗一下**、**聲音驟窄**，或在組裝時複製命中前 2–10 幀。
- 一段只能有一個 L4。兩個大絕等於沒有大絕。

**整段節奏曲線一句寫死**（v7 原提示詞；H3 未實測，但這句不花幾個字）：把運鏡／速度版本的曲線寫在 `[Shot 1]` 或交付說明裡，例如「開場慢、第一次交鋒快、近距離碰撞短暫停頓、中段追逐快、瞬斬前凝神、瞬斬極快、收劍慢、最後終極爆發突然放大規模」。英文：`The pacing runs slow at the open, fast at the first clash, a brief hold at the close-quarters lock, fast through the chase, a held breath before the flash cut, the flash cut itself instant, slow on the sheathing, then the final burst suddenly blows the scale wide open.`

---

## 6. 爆炸類的專用結構（三段式）

純爆炸（法術、手雷、能量爆）不適用打擊結構，改用三段式：

```
① 爆發點        衝擊幀（P0–P3 選一）
② 力量輸出      力場：環形波 + 空氣折射 + 物質掀飛 + 光影聯動（最多三通道）
③ 體感          震屏：峰值 → 急速衰減 → 回穩（或相機鎖死）
④ 餘韻（8–20 幀）餘燼、煙塵、暗部緩慢恢復
```

閃白與衝擊波寫在同一句或相鄰句；震屏與閃白不必同幀（參考片並不同幀），但不要閃白配持續震屏。

震屏寫法與時序表見 `impact-frame/shake-and-timing.md`。

**嵌套規則**：打擊結構的「洩」拍裡，可以放一個完整的三段式爆炸。但不要讓爆炸吃掉「退」與「收」——受擊者的反應與沉降才是重量感的收尾。

---

## 7. 優雅角色的姿勢先驗（實測結論）

模型對「優雅／美貌型角色」有一套強烈的**擺拍先驗**：低眉、側臉、含蓄、手部姿態柔美。角色越靜止，這套先驗越強；角色越在動作中，真實感越高。

**三次實測的結果：**

| 寫法 | 結果 |
|---|---|
| 靜止鏡頭 + `settles into a low guard, weight on the back foot` | 只取「手抬起」，丟掉「低架」與「後腳承重」→ 變成舞蹈姿 |
| 靜止鏡頭 + `her eyes stay on him`（放結尾） | 完全失效，全程低頭 |
| 靜止鏡頭 + `her head stays turned toward him`（放第一句） | 仍失效 |

**結論：不要用文字對抗先驗，要用結構繞過它。**

### 三條對策

1. **不給靜止的英雄姿勢鏡頭。** 想要戰意，就讓她一直在動——退、擋、轉、撐。移動中模型來不及套用擺拍模板。
2. **視線用動作驅動，不用凝視指令。**
   ```text
   ❌ she looks at him
   ✅ Her eyes drop to his blade as it comes, then snap back to his mask as she parries.
   ```
   有了物理原因（刀來了 → 看刀 → 擋住 → 看他），模型才不會把她拉回低眉狀態。
3. **用對手的存在逼出視線。** 雙人同框時，只要對手在做威脅性動作，她的視線自然會被拉過去；單人特寫最容易擺拍。

### 判斷訊號

如果生成結果裡她的姿態「漂亮但沒有威脅感」，不要加更多形容詞（`fierce`, `battle-ready` 這類詞無效），直接改結構：**讓她動起來，或讓對手壓過來。**

## 8. 每次接觸都要有物理後果

只有光沒有物理 = 貼圖。每一擊至少一件：

| 擊法 | 環境反應 |
|---|---|
| 肘／拳 | 腳下石板裂開星芒、塵土上衝 |
| 膝 | 石板被壓裂抬起、對方滑退 |
| 踢 | 每次轉身踩裂地面 |
| 摔 | 石板碎裂、石塊與塵土往外炸 |

平面／抽象背景用**背景翻色、角色保留原色**表達衝擊（`impact-frame/forms.md` F5）。參考片（打鬥蒸餾）翻色持續 **3–12 幀**；舊規則「只翻一幀」在 H3 會被時序平滑抹掉：

```text
the flat background slam-changes colour from coral to hot pink with radial speed lines, while both fighters keep their own colours, then snaps back to coral
```

**打擊點與被保護者的距離要寫**：打離主角遠的部位、寫明中間空地（`two big steps to his right, with clear open ground between it and him`），否則命中會波及主角。

## 9. 受力方鏡頭（爽感來源）

觀眾要看的是**被打的那一方**，不是出招的那一方。每段至少一刀：

| 鏡頭 | 拍什麼 |
|---|---|
| 受力臉部特寫 | 頭被打偏、頭髮甩過臉、眼睛閉上、飾品盪起 |
| 受力部位特寫 | 手套鎖住對方手臂、指節泛白、束帶繃緊 |
| 受力全身 | 被打飛、滑退、膝蓋彎曲、腳離地 |

只拍出招方 → 像打沙包；拍受力方 → 有打擊感。

## 10. 不同比例的兩段式變拍（Ref2VA 不可靠）

**要在不同比例下保留角色，不要改生成模式，要改首幀比例：**

```
角色圖 9:16，要拍 16:9：

① image 任務（people）→ 16:9 雙人首幀
   people: [{image: 珊瑚圖, x: 0.32, height: 0.55, feet: 0.92},
            {image: 海沫圖, x: 0.68, height: 0.55, feet: 0.92}]
② generate（media.first = 那張首幀）→ I2VA 16:9
```

| 做法 | 結果 |
|---|---|
| I2VA 直接用 9:16 圖 | 比例被綁死 |
| 16:9 + T2VA | 角色完全走樣 |
| 16:9 + Ref2VA(media.references) | **模型把圖當內容重現，整段變靜止圖**（實測運動量 0.49） |
| **image(people) 做首幀 + I2VA** | **角色與比例都對** |
