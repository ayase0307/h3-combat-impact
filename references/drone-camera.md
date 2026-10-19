# 無人機式運鏡（Drone Camera）

> 打鬥鏡頭要像**無人機在場邊飛**：從各種角度俯拍、鑽進戰鬥、穿過前景、拉遠看整個場面。
> **不是繞著人物轉圈圈。**

---

## 0. 為什麼「繞著人物轉圈圈」是錯的

`camera-grammar.md` 早期唯一主推的套路是 **Arc Shot（繞主體弧線移動）**。
結果是每一鏡都在繞同一個人轉，觀眾感受到的是「攝影機繞著模特兒轉」，
不是「無人機在拍一場戰鬥」。

**兩者的差別：**

| | 繞圈圈（arc / orbit） | 無人機式 |
|---|---|---|
| 機位變化 | 繞同一個中心，距離不變 | 每鏡換一個**完全不同**的位置與高度 |
| 焦段 | 主角一直同樣大小 | 主角時大時小，時而佔滿畫面、時而是小點 |
| 觀感 | 展示角色 | **觀看一場戰鬥** |
| 空間 | 平面，看不出深度 | 有高、有低、有遠、有近 |

> **規則：全片 `arcs around` / `orbits` 最多 1 個，且只能當「轉接鏡」**（用來從一個位置接到下一個位置），
> 不能當主要運動。

---

## 1. 無人機的 8 個機位

H3 官方運鏡詞只有 15 種，這 8 個機位是它們的**運用方式**，不是新詞彙。

| # | 機位 | 官方運鏡詞 | 說什麼 |
|---|---|---|---|
| 1 | **高空俯拍**（drone top-down） | `Pedestal Up` | `A high overhead aerial shot looking almost straight down` |
| 2 | **頂視鳥瞰**（bird's-eye） | `Pedestal Up` | `A bird's-eye view straight down onto the wet stone` |
| 3 | **高角度俯視**（high angle 45°） | `Tilt Down` | `A high-angle shot looking down at the fighters` |
| 4 | **貼地仰拍**（low angle） | `Tilt Up` | `A ground-level camera almost touching the stone, looking up between them` |
| 5 | **穿前景**（through foreground） | `Truck` + `Pan` | `The camera passes behind a torn banner, the fighters glimpsed through it` |
| 6 | **越肩**（over-the-shoulder） | `Arc`（小幅） | `A tight over-the-shoulder close-up from behind <Subject 1>'s shoulder` |
| 7 | **遠方大遠景**（far establishing） | `Push In` | `A distant wide shot from across the courtyard, the two fighters tiny` |
| 8 | **特寫插入**（insert CU） | `Push In` / `Static` | `A tight close-up of the face` |

### 關鍵：**機位要真的換掉**

寫機位詞不夠，**要寫出「這個鏡頭跟前一個鏡頭不一樣」**。
最有用的寫法是把**高度**與**距離**寫出來：

```text
[Shot 1] A high overhead aerial shot looking almost straight down into the courtyard...
[Shot 2] A ground-level camera almost touching the wet stone, looking up between the two fighters...
[Shot 3] A distant wide shot from across the courtyard, the two fighters tiny against the burning braziers...
[Shot 4] A tight over-the-shoulder close-up from behind the taller fighter's shoulder...
[Shot 5] A bird's-eye view straight down, spinning with the ring of sparks...
[Shot 6] A low-angle hero close-up of the taller fighter's face...
[Shot 7] A very wide crane shot rising above the broken colonnade...
```

**高 → 貼地 → 遠 → 貼近 → 頂 → 貼臉 → 高空。** 這才像無人機在飛。

---

## 2. 必備組合：五種尺度都要有到

一個 8 秒的高速打鬥片段，**這五種尺度至少各出現一次**：

| 尺度 | 觀感 | 建議占比 |
|---|---|---|
| **貼臉特寫** | 情緒、角色細節、能量錨點 | 1–2 鏡 |
| **貼地／近身** | 衝擊、接觸、體感 | 2–3 鏡 |
| **中景** | 動作主體 | 2–3 鏡 |
| **穿前景** | 深度、臨場感 | 1 鏡 |
| **遠方大遠景** | 規模、戰場感 | 1–2 鏡 |

**沒有大遠景 = 觀眾不知道場面多大。沒有特寫 = 觀眾不知道角色是誰。**

---

## 3. 高速打鬥的無人機運鏡寫法

超高速戰鬥裡，**運鏡要跟著動作走，不是自己動**。

```text
[Shot 2] At 00:01.100, a hard cut to a ground-level camera almost touching the
wet stone, looking up between the two fighters as they close. The oversized
nodachi crashes down and the slender katana meets it; a burst of orange sparks
and shattered flagstone fragments spray toward the lens, water bursting up
between their boots. The camera whips sideways with large amplitude at fast
speed, following the impact.
```

拆解：
- **機位**：`a ground-level camera almost touching the wet stone, looking up between the two fighters`
- **主體動作**：`the oversized nodachi crashes down and the slender katana meets it`
- **連動**：`a burst of orange sparks and shattered flagstone fragments spray toward the lens, water bursting up between their boots`
- **運鏡**：`whips sideways with large amplitude at fast speed, following the impact`

**`following the impact` 這個尾巴很重要**——它把運鏡綁在動作上，而不是各自動。

---

## 4. 穿前景：最便宜的臨場感

在打鬥鏡頭前面放一個前景物，鏡頭從它旁邊掠過。觀眾立刻感覺「攝影機在現場」。

```text
The camera passes behind a torn red banner, the fighters glimpsed through the
gaps in the cloth, the banner whipping across the lens.
```

| 前景物 | 適合 |
|---|---|
| 破損的布條／旗幟 | 戰場、混亂 |
| 樹幹／斷柱 | 廢墟、追擊 |
| 飛散的碎石／火星 | 衝擊瞬間 |
| 斷裂的武器殘骸 | 戰後、死鬥 |

**「飛向鏡頭」的碎屑**是另一種臨場感：

```text
a burst of orange sparks and shattered flagstone fragments spray toward the lens
```

---

## 5. 遠方大遠景：規模感

```text
A distant wide shot from across the courtyard, the two fighters tiny against the
burning braziers and torn banners, a wall of dust rising between them.
```

**關鍵字**：`distant` / `tiny` / `far across`。沒有這些詞，模型會給一個中景。

---

## 6. 高速運鏡的四個開關

打鬥片的速度感不只來自切點，也來自鏡頭本身。全部打開會變成災難，**一次最多開三個**。

| 開關 | 寫法 | 效果 |
|---|---|---|
| **前景掠過** | `the torn banner whips across the lens` | 最強 |
| **主體拖影** | `the blade smears into a horizontal streak` | 強 |
| **碎屑飛向鏡頭** | `fragments spray toward the lens` | 強 |
| **甩鏡** | `whips sideways with large amplitude at fast speed` | 中 |

---

## 7. 常見錯誤

| 錯誤寫法 | 問題 | 修正 |
|---|---|---|
| 每鏡都 `the camera arcs around them` | **繞圈圈**，觀眾只覺得轉圈 | 改用 8 機位換位置 |
| `the camera follows the fight` | 沒有位置與高度資訊 | 寫明是俯拍／仰拍／多遠 |
| `the camera tracks the action` | 跟誰？往哪？ | `whips sideways ... following the impact` |
| 連續三鏡都是中景 | 平 | 每鏡換尺度（特寫／貼地／遠方） |
| 全部 `push in` | 一直在靠近，沒有空間感 | 推／拉／搖／移／環繞／垂直輪流 |
| 大遠景之後接大遠景 | 兩個都小，看不出變化 | 大遠景之後接特寫 |
| 寫 `arcs around` 但沒有其他機位 | 全片等於沒運鏡 | `arcs around` 全片 ≤1 個，只當轉接 |

---

## 8. 驗收清單

- [ ] 全片 `arcs around` / `orbits` **≤1 個**
- [ ] 五種尺度（特寫／貼地／中景／穿前景／大遠景）**都出現過**
- [ ] **連續兩鏡的機位高度不同**（例如上一鏡俯拍、下一鏡不能還是俯拍）
- [ ] 至少 1 鏡有前景物掠過
- [ ] 至少 1 鏡是大遠景且主體很小（`tiny` / `distant`）
- [ ] 每個高速鏡的運鏡都綁在動作上（`following the impact` 這類尾巴）
- [ ] 沒有連續三個同景別
