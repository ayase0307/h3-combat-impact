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

## 1. 核心原理：表情是肌肉，不是形容詞

H3 對**具體的肌肉動作**有反應，對情緒形容詞沒有。

| ❌ 形容詞／眼睛形狀 | ✅ 肌肉動作 |
|---|---|
| `a determined expression` | `her jaw muscles bunch and her teeth clench` |
| `fierce eyes` | `her brows slam down into a hard knot above her nose` |
| `she looks shocked` | `her eyes fly wide and her lips part on a sharp intake of breath` |
| `her irises narrow` | `the lower lids tighten and the skin at the corners of her eyes crinkles` |
| `an anguished cry` | `her mouth wrenches open and her throat cords stand out` |

**規則：每一句表情描述都必須有一個「可以動的部位」＋一個「動作」。**

可用的部位清單（照這個挑）：

| 部位 | 可寫的動作 |
|---|---|
| 眉 | `brows slam down` / `brows knit` / `brows shoot up` / `one brow twitches` |
| 上眼瞼 | `upper lids drop` / `lids fly wide` / `a squint cuts her eyes to slits` |
| 下眼瞼／眼周 | `lower lids tighten` / `skin crinkles at the corners` / `a wet shine along the lower lid` |
| 鼻翼 | `nostrils flare` / `her nose wrinkles` |
| 下顎／咀嚼肌 | `jaw muscles bunch` / `jaw drops` / `her jaw locks` |
| 齒 | `teeth clench` / `her lips peel back off her teeth` / `lips press into a hard line` |
| 唇／嘴 | `lips part` / `mouth wrenches open` / `she bites down on her lower lip` |
| 頸／喉 | `throat cords stand out` / `her throat works on a swallow` |
| 太陽穴 | `a vein stands out at her temple` |
| 汗／淚／血 | `sweat tracks down her temple` / `a bead of sweat cuts through the dust on her cheek` |
| 呼吸 | `her chest heaves` / `a sharp breath hisses through her teeth` |

---

## 2. 打鬥要有四種表情狀態（不是一種）

**最常見的錯誤是「全片一個表情」。** 一場打鬥至少要有四個階段的表情轉變：

| 階段 | 情緒 | 寫法 |
|---|---|---|
| **1 交手前（0–0.3s）** | 緊繃、專注 | `her jaw locks and her brows pull together, a hard line across her mouth` |
| **2 吃到重擊** | 痛、失重 | `her eyes fly wide open and her mouth wrenches open on a gasp, spit flying` |
| **3 反擊** | 狠、決斷 | `her brows slam down and her lips peel back off her clenched teeth` |
| **4 收尾** | 喘息、剩勇 | `her chest heaves, a bead of sweat cutting through the dust on her cheek` |

**四種要輪流出現。** 一鏡一種，不要在一個鏡頭裡塞兩種。

---

## 3. 特寫必須配表情，否則就是浪費

**你給一個臉部特寫，卻沒寫表情，模型就給你一張漂亮的死人臉。**

| 特寫類型 | 必配 |
|---|---|
| 極特寫（眼／臉） | **一個肌肉動作**（眉毛／下眼瞼／咬肌） |
| 中近景（胸部以上） | 表情 ＋ **一個呼吸或吞嚥** |
| 越肩 | 被看見的那張臉要有表情 |

寫法模板：

```text
A close-up of Tieya's face. Her brows slam down into a hard knot above her nose,
her lower lids tighten, and the skin at the corners of her eyes crinkles as the
molten-orange edge of her nodachi lights her from below. Sweat tracks down her
temple. The camera pushes in with small amplitude at fast speed; this shot holds
for seven frames.
```

**「眉毛下壓 ＋ 下眼瞼收緊 ＋ 眼周起紋」＝ 一個真的在用力的人。**
光只有「光從下面打上來」＝ 死人臉。

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
