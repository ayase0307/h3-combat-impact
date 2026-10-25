# 超高速戰鬥（ULTRA_SPEED 模式）

> 第三種節奏模式。**不要停頓、不要蓄力、不要把重點放在拍點結構上。**
> 目標是「看得喘不過氣」的高速對打，畫面重心放在**運鏡、戰鬥、特效、周圍連動**。

---

## 0. 三種模式怎麼選

| 模式 | 節奏單位 | 用途 | 規則 |
|---|---|---|---|
| **六拍** | 一次交手 | 單次重擊、有蓄力與收勢 | `impact-design.md` |
| **連續對轟** | 一次交換（0.8–1.5s） | 近身纏鬥、壓著打 | `continuous-brawl.md` |
| **ULTRA_SPEED** | **一個鏡頭（雙峰鏡長）** | **無人機高速跟拍、不間斷** | 本文件 |

**判斷訊號**：需求裡出現「超高速」「不要停」「一直打」「喘不過氣」「運鏡一直在動」→ ULTRA_SPEED。

> **ULTRA_SPEED 與連續對轟的差異**：連續對轟仍有「攻→擋→反」的交換結構；
> ULTRA_SPEED **不追求交換結構**，追求的是**鏡頭位置一直在換、動作一直在跑、周圍一直在壞**。

---

## 1. 參數

| 項目 | 值 | 理由 |
|---|---|---|
| 8 秒的鏡數 | **10–14 鏡** | — |
| 鏡長分布 | **雙峰**：1–2 個 1.2–2.0 s 錨定鏡 ＋ 8–10 個 0.25–0.6 s ＋ 2–3 個 ≤0.2 s 插入 | 參考片鏡長 CV 0.90–1.17；舊版「每鏡 0.4–0.8 秒」寫出等距 0.7 s（37 號 CV 0.51），節奏像節拍器 |
| 短鏡（≤0.25s） | 2–3 個 | 插入格與衝擊幀；≤0.2 s 的插入多半靠後製（composite）或衝擊幀鏡 |
| 時間碼間隔 | **不可等距**（validator：間隔 CV <0.4 → WARN） | — |
| 每鏡動作數 | **1 個** | 動作預算有限（見 `continuous-brawl.md`） |
| 每鏡運鏡 | **1 個** | 但機位要換（見 `drone-camera.md`） |
| 片頭／片尾 | **各保留 0.5 秒** | H3 會自動定格（見 `SKILL.md` 收尾定格） |

### 這覆寫了哪些既有規則

| 既有規則 | 在 ULTRA_SPEED 下 |
|---|---|
| `continuous-brawl.md`「7.5 秒的動作總量固定，刀數與每刀動作數互斥」 | **仍然成立**——所以每鏡只能 1 個動作 |
| `continuous-brawl.md`「每刀一次交換（攻→擋→反）」 | **降級為選用**；超高速下優先給「1 動作 + 1 運鏡 + 1 特效 + 1 環境連動」 |
| `qa-checklist.md` 鏡數 | **以 §6 統一表為準**（8 秒 10–14 鏡） |
| `impact-design.md`「每 3–4 擊插一次靜止」 | **停用**；靜止改由片頭片尾各 0.5 秒提供 |
| `SKILL.md`「六拍結構」 | **不適用**；超高速不靠拍點結構 |

**換句話說：超高速靠的是「鏡頭一直在換位置」，不是「每一拍都設計得很漂亮」。**

---

## 2. 每鏡的四件套

ULTRA_SPEED 的每個鏡頭都給四樣東西，缺一樣就會變慢：

```text
[鏡位] + [主體動作] + [運鏡] + [特效] + [周圍連動]
```

實例：

```text
[Shot 3] At 00:02.100, a hard cut to a distant wide shot from across the courtyard,
the two fighters tiny against the burning braziers as the taller swordswoman
swings through a full circle and drives the other through a stone pillar that
explodes into rubble and a cloud of grey dust. The camera pushes in with large
amplitude at fast speed.
```

拆解：

| 要素 | 內容 |
|---|---|
| 鏡位 | `a distant wide shot from across the courtyard` |
| 主體動作 | `swings through a full circle and drives the other through a stone pillar` |
| 運鏡 | `pushes in with large amplitude at fast speed` |
| 特效 | `the pillar explodes into rubble` |
| 周圍連動 | `a cloud of grey dust` |

**周圍連動是「高速感」的來源**——不只角色在動，環境也在被摧毀。
爆炸、煙霧、碎石、飛揚的布條、濺起的水、崩塌的柱子、揚起的灰。

---

## 3. 周圍連動的清單（每鏡至少挑一個）

| 類別 | 例句 |
|---|---|
| **破碎** | `the stone pillar explodes into rubble` |
| **塵土** | `a cloud of grey dust rolls outward along the ground` |
| **煙霧** | `thick smoke boils up from the broken masonry` |
| **液體** | `water bursts up between their boots` |
| **布料** | `the torn red banners whip violently` |
| **火星** | `a burst of orange sparks tears off the impact` |
| **碎屑飛向鏡頭** | `shattered flagstone fragments spray toward the lens` |
| **反應證據** | `the wet stone floor reflects the moonlight and firelight` |

> **優先序：破碎 > 塵土 > 布料 > 火星 > 液體 > 煙霧。**
> 破碎與塵土最有效，煙霧最容易被模型做成一片糊。

---

## 4. 不要寫的東西

超高速下，這些寫法會讓畫面慢下來：

| 別寫 | 為什麼 | 改寫 |
|---|---|---|
| `a held impact frame` | 停住 | 衝擊幀另外生成後製（見 `impact-frame/post.md`）——**而且後製是必經步驟**，交付時要附 composite 指令，否則成品沒有衝擊幀（37／38 號：0 去飽和、0 黑幀） |
| `the action decelerates to a near-freeze` | 慢動作 | 刪掉 |
| `draws back, weight sinks, gathering power` | 蓄力是慢的 | 刪掉，直接進攻 |
| `both fighters reset and lunge again` | 重置＝停頓 | 刪掉 |
| `a static shot on the two silhouettes` | 靜止 | 換成新的機位 |
| `establishing the space` | 交代空間＝慢 | 讓大遠景同時有打鬥在進行 |

---

## 5. 片頭片尾各留 0.5 秒

H3 在片段最後 1–2 秒會自動減速（`SKILL.md` 收尾定格）。
超高速如果一路衝到底，結尾會僵在那裡。

**做法**：把最後 0.5 秒的鏡頭寫成「動作結束、鏡頭仍在收」的狀態，
不要寫成「兩人站定對峙」。

```text
[Shot 12] At 00:07.500, a hard cut to a low-angle close-up of the taller
swordswoman's face as she drives through the crossing blades, her shoulder
already carrying the follow-through while the light blooms between them.
```

**剪輯時把最後 0.5 秒切掉**，用 7.5 秒的版本。

---

## 6. 鏡頭密度統一表

**舊的 skill 有 8 條互相矛盾的鏡頭密度規則**（見 `35_技能缺口稽核` §5）。
以下為統一版，優先級高於其他所有檔案：

| 模式 | 8 秒的鏡數 | 中位鏡長 | 短鏡占比 |
|---|---|---|---|
| **六拍**（單次重擊） | 4–5 鏡 | 1.2–2.0s | ≤20% |
| **連續對轟** | 9–10 鏡 | 0.6–0.9s | ≥30% |
| **ULTRA_SPEED** | **10–14 鏡** | **雙峰**（見 §1） | 2–3 個 ≤0.2 s |

**若其他文件寫了不同的數字，以本表為準**（`SKILL.md` §4 是同一張表）。

---

## 7. ULTRA_SPEED 檢查清單

- [ ] 8 秒有 10–14 個鏡頭，鏡長雙峰（1–2 個長錨定鏡＋大量短鏡），時間碼不等距
- [ ] 每鏡都有：鏡位 + 動作 + 運鏡 + 特效或周圍連動
- [ ] 沒有 `a held impact frame`、沒有 `near-freeze`、沒有 `reset`
- [ ] 沒有蓄力段（`draws back` / `gathering power`）
- [ ] 機位高度每鏡都不同（見 `drone-camera.md`）
- [ ] 五種尺度都有出現
- [ ] 片頭片尾各留 0.5 秒，結尾不是站定
- [ ] 衝擊幀改走後製路徑（見 `impact-frame/post.md`），交付附 composite 指令
- [ ] 同一 15 秒內俯拍 ≤2 次且內容不同（37 號俯拍塵環出現 4 次，像同一模板）
- [ ] 用 `measure_motion.py` 量測：末 2s ÷ 中段 ≥ 60%、最長低潮 ≤ 0.8s

## 8. 每組四欄＋節奏與聲音（教學 v5；H3 未實測）

四件套之外，教學片的每組還多一欄**【節奏與聲音】**：這一組是加速、驟停還是靜音，聲音是驟窄、低頻壓入還是裂響。寫在鏡頭末句：

```text
… The sound narrows to a thin whine just before contact, then the low boom and the crack of stone hit together.
```

全片頭先寫一次【全招式統一特效】（`impact-design.md` §2.1 三級碰撞），後面每組只寫「觸發輕／重碰撞」，省字數。
