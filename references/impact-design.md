# 打擊感設計：六拍、力度分級與材質反應

## 0. 為什麼 AI 打鬥會「軟」

AI 影片模型傾向生成**平均化的中間狀態**：它會把「出拳」畫成一條平滑的插值曲線，於是缺少三件事——

1. **變速**（真實打擊是 0.4 秒蓄力 + 0.08 秒命中）
2. **停頓**（命中瞬間物理上必須有能量轉移的停滯）
3. **不對稱**（攻擊者過衝、受擊者延遲反應、布料晚半拍）

所以提示詞的任務不是「描述打鬥」，而是**強制插入變速、停頓與不對稱**。

---

## 1. 六拍結構（HIT BEAT）

### 拍 1｜蓄 Anticipation
- **畫面**：反向預備動作（要往右打，先往左收）；重心壓到後腳；握把處指節泛白；衣襬與髮尾因急停而向前甩。
- **鏡頭**：`the camera holds a static shot` 或 `the camera pushes in with small amplitude at slow speed`。**蓄力時鏡頭必須穩或反向**，任何同向運動都會洩掉張力。
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

### 拍 2｜觸 Contact
- **畫面**：1–2 幀的爆白、爆黑或單色剪影；徑向速度線；畫面輕微徑向拉伸；色差（紅藍邊）。
- **鏡頭**：`the camera shakes strongly` 或 `the camera punches in with small amplitude at extreme speed`。
- **可寫**：`for two frames the frame blows out to white as radial speed lines tear outward from the point of contact`
- **關鍵**：一定要寫「幾幀」。H3 固定 24 fps，`two frames` ≈ 83 ms，模型對這個尺度有反應；寫 `briefly` 通常會給 0.5 秒的長閃，看起來像特效而不是打擊。
- **三種形態**（白閃＝爆發、黑閃＝終結、單色剪影＝儀式感）見 `impact-frame-and-shake.md`。

### 拍 3｜停 Hit Stop
- **畫面**：時間近乎凍結；只有塵埃、火花、碎屑還在慣性飄移；主角與受擊者姿勢鎖死。
- **鏡頭**：`the camera holds a static shot`（停頓期間鏡頭必須停，否則觀眾讀不到）。
- **可寫**：`the action decelerates to a near-freeze for a fraction of a second; only the sparks keep drifting`
- **關鍵**：這是最容易被模型忽略、也最有效的一拍。若一次生成常漏掉，把它獨立成一個 `[Shot N]`，用 0.5 秒單獨描述。

### 拍 4｜洩 Release
- **畫面**：衝擊波環、碎片、塵環、水幕、氣浪；方向必須與攻擊方向一致（橫掃 → 扇形，下劈 → 地面環）。
- **可寫**：`a ring of grey dust bursts outward along the ground`, `stone shards spray away from the impact point`, `water sprays up in a thin sheet`
- **關鍵**：**方向感**。寫 `explodes everywhere` 等於沒有方向，力量會散掉。
- **升級**：把「洩」展開成**力場四通道**（光／空氣／物質／粒子），見 `force-field.md`。只寫碎片與塵土，等於只開了物質通道——這是最常見的「貼圖感」來源。

### 拍 5｜退 Reaction
- **畫面**：受擊者被打飛／滑退／破防；頭髮與衣襬延遲半拍；攻擊者過衝半步。
- **可寫**：`he is hurled backward, boots gouging two lines in the wet stone`, `her ponytail whips a beat late`, `his follow-through carries him half a step past the strike`
- **關鍵**：**overlapping action**（延遲跟隨）是 AI 打鬥最缺的物理細節，一句就能補上。

### 拍 6｜收 Recovery
- **畫面**：回到 ready pose；殘留粒子飄落；鏡頭回穩。
- **可寫**：`she settles into a low guard as embers drift down through the lantern light`

---

## 2. 力度分級（選一級，不要混）

| 級別 | 適用 | 總長（24fps） | 停頓 | 鏡頭 | 特效預算 |
|---|---|---|---|---|---|
| **L1 輕** | 試探、格擋、擦身 | 5–8 幀 | 0–1 幀 | `shakes slightly` | 只有火花，不加衝擊波 |
| **L2 中** | 乾淨命中、破招 | 10–16 幀 | 2–3 幀 | `shakes strongly` | 火花 + 局部碎片 |
| **L3 重** | 擊退、破防、撞牆 | 20–32 幀 | 3–5 幀 | `shakes strongly` + 短暫失焦 | 衝擊波環 + 塵 + 環境物件晃動 |
| **L4 必殺** | 收尾、對撞、大絕 | 40–90 幀，**多鏡頭** | 5–8 幀 | 撞擊後 `pulls out with large amplitude` | 三段式：蓄能 → 對撞 → 環境毀壞 |

**L4 的標準結構**（不可壓縮成一個鏡頭）：
1. 蓄能（能量在武器/掌心聚集、地面碎石浮起、鏡頭緩推）
2. 對撞（兩股能量相接、畫面過曝、鏡頭強震）
3. 凍結（0.3 秒全畫面近白，聲音抽空）
4. 擴散（俯拍或大廣角，衝擊波以環狀掃過場景）
5. 餘韻（慢動作碎片落下、主角背影）

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

## 4. 時間預算（以 24 fps 換算）

| 節拍 | 秒 | 幀 |
|---|---|---|
| 蓄 | 0.30–0.45 | 7–11 |
| 觸 | 0.04–0.08 | 1–2 |
| 停 | 0.12–0.25 | 3–6 |
| 洩 | 0.20–0.30 | 5–7 |
| 退 | 0.15–0.20 | 4–5 |
| 收 | 0.05–0.10 | 1–2 |

一個 L2 命中 ≈ 0.9–1.2 秒。**7 秒片段 = 5–6 個 L1/L2 命中，或 1 個 L3 + 2 個 L1。** 超過這個密度，模型會把所有動作壓成模糊。

---

## 5. 節奏曲線（整段而非單擊）

一段 15 秒的打鬥，力度必須有起伏，否則觀眾 6 秒後就麻木：

```
L1 ─ L1 ─ L2 ─ L1 ─ L3 ──（靜 0.8s 對峙）── L4
```

- **每 3–4 擊必須插入一次「靜」**：對峙、呼吸、眼神、雨滴、燈火搖曳。靜是為了讓下一擊更響。
- **L4 之前必須有 0.5–1 秒的完全靜止**。這是所有動作片的共同語法。
- 一段只能有一個 L4。兩個大絕等於沒有大絕。

---

## 6. 爆炸類的專用結構（三段式）

純爆炸（法術、手雷、能量爆）不適用六拍，改用三段式：

```
① 爆發點（1–2 幀）     衝擊幀：全畫面閃白 + 爆心過曝
② 力量輸出（6–12 幀）   力場四通道：環形波 + 空氣折射 + 物質掀飛 + 光影聯動
③ 體感（0.3 秒衰減）    震屏：峰值 → 急速衰減 → 回穩
④ 餘韻（8–20 幀）       餘燼、煙塵、暗部緩慢恢復
```

**三者必須對齊在同一幀**（閃白、震屏峰值、衝擊波起始）。差 2 幀，質感就散了。

詳細的幀數、震屏衰減模型與 hitstop 參數見 `impact-frame-and-shake.md`。

**嵌套規則**：六拍的「洩」拍裡，可以放一個完整的三段式爆炸。但不要讓爆炸吃掉「退」與「收」——受擊者的反應與沉降才是重量感的收尾。

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
