# 打鬥運鏡語法（H3 官方詞彙 + 實戰套路）

## 0. 鐵律：每個鏡頭都要有運鏡（實測）

**沒有一個鏡頭可以是靜止的。**

實測原參考片（30 秒 / 40 刀）：0.0–0.375 持續推近、1.25–2.125 持續拉遠、2.25–2.875 再推近——**每一鏡都在推或拉**。

實測自己的三版：

| 版本 | 7 鏡裡有運鏡的 | ZOOM |
|---|---:|---:|
| A6 | 2 | 0 |
| D3 | 1 | 0 |
| D5 | 1 | 0 |

結果就是「完全沒有運鏡感」。

### 七鏡運鏡計畫（不重複）

| 鏡 | 運動 |
|---|---|
| 1 | push in（大幅快速） |
| 2 | 定格圖（不動） |
| 3 | truck right（大幅快速） |
| 4 | **zoom in**（大幅快速） |
| 5 | arc（小幅快速） |
| 6 | **zoom out**（大幅快速） |
| 7 | push in（小幅快速） |

**同一支片不要七個都 push in。** 推、拉、搖、移、環繞、變焦輪流用。

### 剪接密度：太慢的第一診斷

**「看起來像靜態畫」通常不是動作不夠強，是刀不夠多。**

| 條件 | 可容納刀數（7.5 秒） |
|---|---|
| 每刀一個動作 ＋ 一個運鏡 | **9–10 刀**（0.75–0.85 秒／刀） |
| 每刀只有描述、無動作 | 6 刀以下（再多會變靜態） |

實測對照：

| 版本 | 刀數 | 每刀內容 | 末段運動 |
|---|---:|---|---:|
| D5 | 5 | 有動作、運鏡少 | 9.55 |
| D6 | 5 | 有動作、每刀有運鏡 | 14.26 |
| A5 | 10 | 只有描述、無動作 | 全程 12.75 |
| **D7** | **9** | **一個動作 ＋ 一個運鏡** | **18.02** |

**刀多不是問題，刀多＋每刀空才是問題。**

原片基準：30 秒 40 刀 = 0.75 秒一刀。7.5 秒就是 10 刀。

### 衝擊是「切到定格圖」，不是「在動作裡凍結」

原片的做法：

```
0.50  切到極特寫（腳）
0.75  切到定格衝擊圖：命中姿勢 + 粉色放射線，停 4 格（0.37 秒）
1.25  切回廣角
```

**定格圖是一個獨立鏡頭**，畫面靜止、但有放射線撐住張力。它讀成「衝擊」，不是「慢動作」。

❌ 錯：`for two frames the action near-freezes`（在連續動作裡凍結 → 慢動作）
✅ 對：切一個新鏡頭，寫 `a held impact frame ... this frame holds for eight frames, then cuts away`

### 尺度要跳

廣角 → 極特寫 → 廣角。跳得越狠，節奏越強。連續三個中景就是平的。

## 1. 官方運鏡三維度

H3 只認這個結構：**動作類型 + 幅度 + 速度**，且必須寫成自然語句。

| 維度 | 可用表達 |
|---|---|
| 類型 | `Zoom In / Zoom Out`（變焦，機身不動） |
| 類型 | `Push In / Pull Out`（機身前後移動） |
| 類型 | `Pan Left / Pan Right`（原地水平搖） |
| 類型 | `Truck Left / Truck Right`（水平平移） |
| 類型 | `Tilt Up / Tilt Down`（原地垂直搖） |
| 類型 | `Pedestal Up / Pedestal Down`（整機升降） |
| 類型 | `Arc Shot`（繞主體弧線移動） |
| 類型 | `Tracking Shot`（跟隨移動物體） |
| 類型 | `Static Shot`（完全靜止） |
| 類型 | `Shake Slightly / Shake Strongly`（輕震／強震） |
| 類型 | `POV`（主觀視角） |
| 類型 | `Roll Clockwise / Roll Counterclockwise`（滾轉） |
| 幅度 | `with small amplitude` / `with large amplitude` |
| 速度 | `at slow speed` / `at fast speed` |

中等幅度與常速可省略。**不要**在句尾堆疊標籤：

- ✗ `close-up, dynamic, cinematic camera, shake, fast`
- ✓ `The camera pushes in with large amplitude at fast speed toward the point of contact.`

---

## 2. 打鬥專用套路（直接套用）

### 2.1 命中推鏡（Punch-In on Impact）
```text
As the blade connects, the camera punches in with small amplitude at fast speed and shakes strongly.
```
用途：所有 L2 以上命中。**推鏡 + 震動必須同時發生在同一個子句**，模型才會把它們綁在同一幀。

### 2.2 蓄力定鏡（Hold for Anticipation）
```text
The camera holds a static shot as her weight sinks into the rear leg and the blade draws back.
```
用途：蓄力拍。定鏡讓觀眾預期「要出事了」。

### 2.3 甩鏡轉場（Whip Pan Transition）
```text
The camera pans right with large amplitude at fast speed, the frame smearing into horizontal streaks, and settles on the male swordsman mid-stance.
```
用途：切換攻擊者。甩鏡比硬切更有連續感，且能掩蓋 AI 的接縫。

### 2.4 環繞對峙（Orbit Standoff）
```text
The camera arcs around the two figures with small amplitude at slow speed, keeping both silhouettes in frame.
```
用途：L4 之前的「靜」。慢速環繞能同時交代兩人距離與空間關係。

### 2.5 低角度英雄鏡（Low-Angle Hero）
```text
The camera tilts up with small amplitude at slow speed from the cracked flagstones to her face.
```
用途：開場、收尾、氣勢建立。低角度 + 上搖 = 壓迫感。

### 2.6 俯拍衝擊波（Top-Down Shockwave）
```text
The camera pedestals up with large amplitude at fast speed into a top-down view as the shockwave ring races outward across the courtyard.
```
用途：L4 的擴散拍。俯拍是唯一能拍出「衝擊波規模」的角度。

### 2.7 跟拍位移（Tracking the Knockback）
```text
The camera trucks right with large amplitude at fast speed, keeping pace with him as he is hurled backward.
```
用途：擊退。跟拍讓觀眾感覺「自己被推著走」。

### 2.8 主觀受擊（POV Impact）
```text
The camera drops to a POV as the fist fills the frame, then rolls counterclockwise and shakes strongly.
```
用途：偶爾用一次，代入感極強。**整段只能用一次**。

---

## 3. 主體動作與鏡頭運動必須分離

這是官方明列的規則，也是 AI 打鬥最容易糊掉的原因。

- ✗ `The camera spins around her as she spins and slashes`（兩個旋轉疊加 → 畫面全糊）
- ✓ `She spins once on her heel and slashes horizontally while the camera holds a static shot.`

原則：**主體動得快，鏡頭就穩；主體不動，鏡頭才動。**

---

## 4. 打鬥分鏡的景別節奏

一段 15 秒的打鬥，景別必須有呼吸：

| 順序 | 景別 | 功能 | 停留 |
|---|---|---|---|
| 1 | 大廣角 / 低角度全景 | 交代空間與人數 | 1.5–2.5s |
| 2 | 中景 | 動作主體 | 0.8–1.2s |
| 3 | 特寫（手、眼、兵器） | 蓄力與意圖 | 0.5–0.8s |
| 4 | 中景 / 跟拍 | 命中 | 0.3–0.5s |
| 5 | 特寫（撞擊點） | 衝擊幀 | 0.1–0.2s |
| 6 | 大廣角 | 衝擊波與環境 | 1.0–2.0s |

**連續兩個同景別 = 剪輯死亡。** 每次切換景別，至少要跳一級（廣角→特寫，或特寫→廣角）。

---

## 5. 速度感的四個開關（按順序開）

1. **前景掠過**：`lanterns whip past the lens`（前景快速劃過 = 速度）
2. **運動模糊**：`the blade smears into a horizontal streak`（只給兵器，不給人）
3. **塵/水/雨被推開**：`rain is pushed into a radial sheet`（環境反應）
4. **鏡頭震動**：`shakes strongly`（最後才加，加了就別再加大幅度）

四個全開會變成災難。**一次最多開三個。**

---

## 6. 常見運鏡錯誤

| 錯誤寫法 | 問題 | 修正 |
|---|---|---|
| `360-degree rotating camera` | H3 會生成一整圈模糊 | 改成 `arcs around with small amplitude at slow speed` |
| `fast zoom` | 容易整個畫面失焦 | `pushes in with small amplitude at fast speed` |
| `camera follows the fight` | 沒有方向與幅度 | 指定 `tracks left / trucks right` + 幅度 |
| 每個鏡頭都 `shakes strongly` | 觀眾暈、且失去層級 | 只有 L3 以上才用 `strongly` |
| 一個鏡頭內切三次景別 | 模型會融成一團 | 一次鏡頭只給一個機位 |
