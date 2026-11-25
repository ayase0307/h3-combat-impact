# 表情與表演（Facial Performance）

> **打鬥片最容易被忽略、也最致命的一塊。**
> 運鏡再炫、特效再華麗，只要角色的臉是死的，整段就是在「看兩尊雕像打架」。

---

## 0. 診斷：為什麼 H3 的臉會變成死人臉

模型對「表情」的預設值是**中性放空**。你沒寫它就不給，寫得不對它也給不出來。

### 三種失敗寫法（都是我自己踩過的）

| 寫法 | 為什麼無效 |
|---|---|
| `her amber irises narrow` | 這是**眼睛的形狀**，不是臉部肌肉。模型給你一個瞇眼的中性表情 |
| `pale gray eyes lit from below by the molten edge` | 這是**打光**，不是情緒。燈光打在死人臉上還是死人臉 |
| `a determined look` / `fierce expression` | 這是**形容詞**，模型不知道對應哪塊肌肉 |

**三種寫法都只碰到「眼睛」和「光」，沒有碰到「肌肉」。**

實測（本機 H3、8 秒 16:9、Ref2VA）：
用上面三種寫法產出的臉，眼睛是睜開但無神的、眉毛平的、嘴巴閉著中性的
——**是一個正在發呆的人，不是一個在生死邊緣的人**。

---

## 1. 核心原理：表情是肌肉，不是形容詞（且必選對「顏值分檔」）

H3 對**具體的肌肉動作**有反應，對情緒形容詞沒有；**但不同畫風對肌肉幅度的容忍度天差地遠**：
- 在 **3D 國漫／2.5D AI 漫劇／古風仙俠美型角色** 上，若套用歐美硬派寫實的極端肌肉詞（如 `teeth clench`、`lips peel back`、`mouth wrenches open`、`jaw muscles bunch`、`brows slam down into a hard knot`），H3 會把精緻五官過度拉伸成齜牙咧嘴的扭曲醜臉。
- 因此本規範強制將表情分為 **A 檔（美型克制，預設）** 與 **B 檔（粗獷咆哮，限定魔獸／狂戰士／重甲反派）**。

### 1.1 A 檔：國漫／AI 漫劇美型克制檔（預設，顏值保真 — 實測 Anti-Grimace Lock）

> **關鍵實測發現（2026-11-24 PRISM + SelfLift 實證）**：在高速打鬥語境下，H3 本身已經自帶 **60% 戰鬥怒意先驗**；若同時掛載高強度 Dial（特別是 `h3_dramatic_light >= 1.5` / `h3_storm >= 1.0`）又在特寫中寫 `brows knit` / `lower lids tighten` / `tight line`，會與戰鬥先驗疊加過頭（150%），把絕美臉拉扯成皺鼻齜牙的猙獰鬼臉。
>
> **正確解法（冷靜壓制原則）**：在 AI 漫劇／仙俠美型角色的特寫中，用**「冷靜、鬆眉、微闔唇、清冷凝視」**將戰鬥先驗壓回 **30% 恰到好處的清冷殺氣**，只留極細微的眉眼專注、微汗與髮絲拂臉；**禁止齜牙、禁大張嘴、禁皺鼻、禁把眉頭鎖成結**。

| ❌ 過激毀臉詞（美型臉禁寫） | ✅ A 檔冷靜壓制高顏值寫法（實測最穩） |
|---|---|
| `her brows slam down into a hard knot` | `calm cold aristocratic expression, smooth relaxed brows, sharp focused gaze locked on the blade` |
| `her jaw muscles bunch and teeth clench` | `composed serene face, softly closed lips, steady unblinking eyes reflecting blade light` |
| `lips peel back off clenched teeth` | `poised cold expression, lips softly closed, chin held level with quiet resolve` |
| `mouth wrenches open on a gasp, spit flying` | `eyes widen a fraction with lips barely parted on a quiet breath, keeping refined features intact` |
| `a vein stands out at her temple` | `fine sweat sheen at the temple as silky stray hair drifts across her smooth cheek` |

A 檔可用部位清單：

| 部位 | 美型安全動作（壓制怒意先驗、100% 鎖顏值） |
|---|---|
| 眉 | `smooth relaxed brows` / `brows resting calm and level` / `brows lift a fraction` |
| 眼與眼瞼 | `sharp steady unblinking gaze` / `cool composed eyes reflecting blade light` / `eyes widen a fraction` |
| 唇與下顎 | `softly closed lips` / `lips barely parted on a quiet breath` / `poised level chin` |
| 呼吸與胸肩 | `chest rises slightly on a quiet breath` / `shoulders settle calmly as she exhales` |
| 汗與髮絲 | `fine sweat sheen at the temple` / `silky loose hair strands drift across her cheek` |

### 1.2 B 檔：粗獷寫實咆哮檔（僅限魔獸、狂戰士、粗獷寫實反派）

| ❌ 形容詞／眼睛形狀 | ✅ B 檔強肌肉動作 |
|---|---|
| `a determined expression` | `his jaw muscles bunch and his teeth clench` |
| `fierce eyes` | `his brows slam down into a hard knot above his nose` |
| `he looks shocked` | `his eyes fly wide and his lips part on a sharp intake of breath` |
| `an anguished cry` | `his mouth wrenches open and his throat cords stand out` |

**規則：每一句表情描述都必須有一個「可以動的部位」＋一個「動作」，並嚴格對應該角色的顏值分檔（美型角色一律走 A 檔）。**

---

## 2. 打鬥要有四種表情狀態（不是一種）

**最常見的錯誤是「全片一個表情」。** 一場打鬥至少要有四個階段的表情轉變（以下提供 A 檔美型預設寫法，粗獷角色才升格至 B 檔）：

| 階段 | 情緒 | A 檔美型克制寫法（預設） | B 檔粗獷寫法（野獸／狂戰士） |
|---|---|---|---|
| **1 交手前（0–0.3s）** | 專注、沉靜 | `her brows knit slightly, lips pressed in a composed line, steady cold gaze locked on the blade` | `his jaw locks and brows pull together` |
| **2 吃到重擊** | 驚愕、受迫 | `her brows lift a fraction and her lips part slightly on a sharp breath as her head tilts with the jolt` | `eyes fly wide open and mouth wrenches open on a gasp` |
| **3 反擊** | 凌厲、決斷 | `her brow furrows lightly, lower lids tightening with cool resolve as stray hair whips past her cheek` | `brows slam down and lips peel back off clenched teeth` |
| **4 收尾** | 喘息、餘韻 | `her chest rises on a quick breath, fine sweat sheen at her temple, composed gaze holding steady` | `chest heaves, sweat cutting through dust on his cheek` |

**四種要輪流出現。** 一鏡一種，不要在一個鏡頭裡塞兩種。

---

## 3. 特寫必須配表情，否則就是浪費

**你給一個臉部特寫，卻沒寫表情，模型就給你一張漂亮的死人臉；但寫得太過火又會毀掉顏值。**

| 特寫類型 | 必配 |
|---|---|
| 極特寫（眼／臉） | **1–2 個 A 檔小幅度肌肉動作**（輕微蹙眉＋下眼瞼微收／唇線緊抿） |
| 中近景（胸部以上） | 表情 ＋ **一個呼吸起伏或髮絲拂面** |
| 越肩 | 被看見的那張臉要有明確微表情 |

A 檔高顏值特寫模板：

```text
A close-up of Feixue's face. Her brows knit slightly, her lower lids tighten in a
sharp steady gaze locked on the oncoming steel, and her lips press into a composed
line as fine sweat glistens at her temple and stray black hair whips past her cheek.
The camera pushes in smoothly at medium speed; this shot holds for seven frames.
```

**「輕微蹙眉 ＋ 下眼瞼微收 ＋ 唇線微抿 ＋ 額角細汗」＝ 有生命力又維持 100% 俊美五官。**

---

## 4. 表情要跟動作同步，不是獨立一句

表情寫成獨立一句，模型會把它當靜態屬性。
**綁在動作上，它才會動。**

```text
❌ Her face shows fierce determination. She swings the blade.

✅ She swings the blade and her mouth wrenches open with the effort, her brows
   slamming down as the strike lands.
```

四種「綁定」方式：

| 綁定對象 | 例句 |
|---|---|
| 攻擊 | `she drives the cut through and her jaw muscles bunch with it` |
| 受擊 | `the block jolts her head back and her eyes fly wide` |
| 蓄力 | `she sucks a sharp breath through her teeth as her weight sinks` |
| 環境 | `embers wash past and her eyes narrow against the heat` |

---

## 5. 兩人的表情要不同（對比才有戲）

兩個角色都用同一套表情＝沒有戲。

| | 寫法 |
|---|---|
| **佔上風的一方** | 表情**收**：`her jaw locks, her mouth a flat line, her eyes flat and cold` |
| **處於下風的一方** | 表情**放**：`her brows climb, her lips part, a bead of sweat at her temple` |
| **逆轉的一方** | 從「放」轉「收」：`her mouth closes into a hard line and her brows come down` |

**「收 vs 放」是最省字、最有效的對比。** 不用寫「誰強誰弱」，觀眾看臉就知道。

---

## 6. 不可省的三個生理反應

再快的打鬥，人也會喘。**沒有生理反應 = 沒有力氣消耗 = 看起來很輕。**

| 反應 | 寫法 | 頻率 |
|---|---|---|
| **呼吸** | `her chest heaves` / `a sharp breath hisses through her teeth` | 每 4–6 秒至少一次 |
| **汗** | `sweat tracks down her temple` / `a bead of sweat cuts through the dust on her cheek` | 中後段開始出現 |
| **吞嚥／喉結** | `her throat works on a swallow` | 對峙或喘息時 |

---

## 7. 常見失敗

| 症狀 | 根因 | 修法 |
|---|---|---|
| **臉像死人** | 只寫眼睛形狀與打光，沒有肌肉 | 每句表情都要有「部位＋動作」 |
| 表情從頭到尾一樣 | 只有一種情緒 | 四階段輪替（緊繃／痛／狠／喘） |
| 喊叫只張嘴不出聲 | 只寫嘴，沒寫頸與齒 | 加 `throat cords stand out`、`teeth clench` |
| 表情跟動作對不上 | 表情寫成獨立句 | 綁在動作上 |
| 兩人表情一樣 | 沒有對比 | 一方「收」一方「放」 |
| 打得再猛也感覺很輕 | 沒有呼吸／汗 | 每 4–6 秒一次呼吸 |
| 特寫很漂亮但很無聊 | 特寫沒配表情 | 見 §3 |
| 臉部渲染變形 | 動作太快、鏡頭太晃 | 特寫鏡頭給 `holds for seven frames` 穩定下來 |

---

## 8. 檢查清單

- [ ] 每一句表情描述都有「**部位 ＋ 動作**」（眉毛／下眼瞼／咬肌／嘴／頸／喉）
- [ ] 沒有用 `determined` / `fierce` 這類形容詞代替肌肉
- [ ] 四種表情狀態（緊繃／痛／狠／喘）都出現過
- [ ] 每個臉部特寫都配了至少一個肌肉動作
- [ ] 表情綁在動作上（不是獨立一句）
- [ ] 兩人表情有「收／放」對比
- [ ] 每 4–6 秒有一次呼吸或喘息
- [ ] 中後段出現汗
- [ ] 重要特寫有 `holds for seven frames` 讓臉穩定下來

---

## 9. 與既有規則的關係

| 既有規則 | 本文件補充 |
|---|---|
| `impact-design.md`「受力方鏡頭（爽感來源）」 | 受力方鏡頭**必須**配受擊表情（眼睜大、嘴張開、頭被打歪），否則就只是「一個人站著被刀碰了一下」 |
| `move-library.md`「招式要具名」 | 招式具名解決「動作單調」，表情解決「人物沒有生命」，**兩者都要** |
| `ref-identity-lock.md`「身份保真」 | 身份保真解決「是不是那個人」，表情解決「那個人有沒有在戰鬥」 |
| `drone-camera.md`「特寫插入」 | 特寫的價值來自表情；沒有表情的特寫不如不拍 |
