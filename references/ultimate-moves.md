# 大招、必殺、一招秒殺與變身：招式設計到命中後果

> 什麼時候讀：有大招／必殺技／絕招／一招秒殺／變身，或使用者說「大招沒感覺」「要毀天滅地」「招式太弱」。
> 這份管「招怎麼設計、怎麼起勢、怎麼命中、怎麼收」；衝擊幀串的寫法在 `impact-frame/burst-strip.md`，形態在 `impact-frame/forms.md`。
>
> 來源標記：〔H3 實測〕＝Hark 漫劇 EP03 S04-a 等實跑；〔教學〕＝老大的教學片（v2 打鬥特效、v5 特效寫法、v6 衝擊幀教學）與 1026 圖文提示詞；〔參考〕＝參考片（v7 雙女劍鬥、32 號 3D CG 片）；〔改寫實驗〕＝`秒殺風格改寫實驗.md`。**凡沒有〔H3 實測〕的，都是 H3 未實測。**

---

## 1. 先設計招，再寫特效

### 1.1 自創招名要翻成畫面〔教學 v5〕

「木遁切割」「九天雷引」這種名字 AI 不知道長什麼樣。每個大招寫清楚四件事：

| 要寫 | 例子 |
|---|---|
| **外觀與形態** | 七道倒流的白色瀑布，外包黑金墨刺，直衝天際 |
| **空間範圍**（最關鍵） | 從她指尖到整條河面、高過兩側山崖 |
| **打哪裡** | 蛇身中段（不是頭）；巨龍下顎、兩角之間、前腿、龍腹——上下左右換著打〔教學 v2〕 |
| **怎麼沒的** | 鱗片一條條撕開、焦黑冒煙；或化成妖霧流光、只剩鱗甲碎片落地 |

### 1.2 一技能鎖一顏色〔教學 v2；參考 v7〕

每招（或每個角色）只用一種能量色：刀光紫／旋風青／海嘯深藍／龍焰橙紅；A 只用冰藍、B 只用暖金。顏色是觀眾分辨「這是哪一招／誰的招」的唯一線索，混色就讀不出來。能量色錨在眼瞳或寶石上（`vfx-vocabulary.md` §7.2）。

### 1.3 招牌符號

給大招一個可以特寫的標誌物（硬幣之眼、紋章、符陣）。它可以出現在蓄力、衝擊幀串中段當「拍子」〔教學 v6〕，也可以當收尾的最後一格。

---

## 2. 大招三拍（取代舊 L4 五段版）〔H3 實測：EP03 S04-a d10–d17〕

| 拍 | 內容 | 時長（生成端） | 組裝 |
|---|---|---|---|
| ① 命中 | 具名部位；寫明與被保護者的距離；命中不拍飛行 | 約 1.0 s | 開場若空等，1.5–2× |
| ② 衝擊幀串＋衝擊波 | 獨立一段 P2（3–5 張×0.2 s），回原鏡頭時特效已全開 | 0.8–1.2 s ＋ 2–2.5 s | 5× ＋ 1.5× |
| ③ 後果 | 受擊者同一句被掀飛；傷害寫成分解事件；下一段承接殘破 | 其餘 | 1× |

舊五段版的「凍結 0.3 秒全畫面近白」與「L4 前 0.5–1 秒完全靜止」在 H3 都會被放大成長時間發光或空等（d10 命中等到 3.71 s），已刪。

---

## 3. 一招秒殺：三鏡結構與三種擊殺邏輯〔改寫實驗；H3 未實測〕

同一組角色、三種擊殺邏輯，分鏡可以直接複用：

| 鏡 | 景別 | 運鏡 | 內容 |
|---|---|---|---|
| **1 起勢** | 極微特寫 → 中近景 | 從掌心符紋／刀柄極微特寫**拉焦上搖**到臉，再快速橫移帶出敵人 | 能量點亮、敵人撲來（或逃、或蓄勢） |
| **2 命中** | 中景 → 局部衝擊特寫 | 先保持兩人同框中景，**迅速推近到接觸點形成衝擊幀** | 命中、妖身開始崩解 |
| **3 消散** | 中遠景 | 從爆散中心**快速後拉**拉開空間，最後輕推收勢 | 敵人化成碎片／霧、主角收招 |

| 擊殺邏輯 | 起勢 | 命中 | 運鏡重點 |
|---|---|---|---|
| **法術轟殺** | 掌心符陣點亮、敵人正面撲擊 | 灵力光刃正面轟中 | 推近到兩者之間的接觸點 |
| **遠程氣刃追斬** | 拔刀、敵人轉身逃 | 刀氣破空追上、命中後背 | 推近到後背命中點 |
| **瞬身近身刺殺** | 主角靜立戒備、敵人蓄勢 | 瞬身突進（跟搖＋輕微動態模糊）→ 刀劃過咽喉 | 多一鏡突進，共四鏡 |

H3 寫法提醒：第 2 鏡的「推近形成衝擊幀」在 H3 上照 P1／P2 寫，不要寫 `freezes`；第 3 鏡的「緩緩飄落」「緩緩收刀」是收尾，可以慢，但大招段（第 2 鏡）不寫 `slowly`。

---

## 4. 起勢：用動作與光蓄，不用靜止

| 手法 | 寫法 | 來源 |
|---|---|---|
| **環境預反應** | 招還沒到，城先有反應：燈從靠海那邊一片片滅掉、光流前面的海水被往前吸 | 〔教學 v6〕 |
| **大爆前先暗一下** | 電很快散掉、畫面暗約 0.3 s，她接著走，再接最粗的一道 | 〔教學 v6〕 |
| **遞增曲線＝時間戳＋數量** | 2.0 s 一兩道 → 2.8 s 四五道 → 3.6 s 六七道 → 4.4 s 起八到十道；每 0.3 s 炸一陣，一陣比一陣多 | 〔教學 v6〕 |
| **空間蓄力** | 蓄力可以是兩個角色之間的東西：臉與臉之間的電弧（參考片 1.2 s） | 〔參考 32 號〕 |
| **瞳孔倒映來襲物** | 0.1 s 推鏡切眼部極近特寫，瞳孔倒映砸落的巨手與面具；全局死寂約 0.5 s | 〔教學 1026 圖文〕 |
| **心跳式低頻震動** | 空間裂縫、魔神巨手出現時，畫面與聲音隨心跳節奏低頻震 | 〔教學 1026 圖文〕 |
| **聲音驟窄** | 重擊前聲音驟窄、甚至靜音，碰撞時低頻與裂響同時壓入 | 〔教學 v5〕 |

```text
The lights of the city go out block by block from the seaward side before the beam even arrives, and the sea ahead of it is sucked forward.
```

```text
At 00:07.000, a hard cut to an extreme close-up of the swordswoman's eye; the falling demon hand and the bone-white mask are reflected in her pupil, her lower lids tighten and her breath catches, and the sound drops away as the camera creeps in.
```

> 「死寂 0.5 s」在 H3 可能被放大；若要用，放在**大招之前的獨立特寫鏡**，大招段本身不寫秒數。

---

## 5. 命中

### 5.1 命中不拍飛行〔H3 實測〕

```text
within a single frame a blinding silver-white column of light thicker than a man is already rammed into the serpent's mid-body, with no visible travel
```

禁 `like a meteor`、`plunges down from the sky`、`flies toward`。「機甲飛向巨龍」會軟；寫 `kicks off the ground and becomes a violet afterimage, instantly blinking around the dragon seven times`〔教學 v2〕。

### 5.2 打擊點離被保護者遠〔H3 實測：EP03 §11.4〕

打頭時頭在主角肩上，命中＝波及主角。選離主角遠的部位，寫明距離與中間空地：`two big steps to his right, with clear open ground between it and him`。

### 5.3 頂住半拍（畫面化的 hit stop）〔教學 v6〕

不寫凍結，寫「被頂住」的物理：

```text
the beam slams into the waist of the tower and fails to punch through; the tower holds it for half a beat, the head of the beam squashing flat as white light spreads across the tower's surface
```

### 5.4 吸收型命中（反制模型預設的火花）〔教學 v6〕

能量灌進角色而不是炸開時：`the lightning pours into her like water into her body; the point of contact neither bursts nor sprays sparks, and the light spreads across her skin and clothes through her whole body`（validator 會對 `neither` 以外的否定詞報 WARN，可改寫成 `the point of contact stays calm`）。

---

## 6. 後果

| 規則 | 寫法 | 來源 |
|---|---|---|
| **受擊不延遲** | 命中 → 衝擊波 → 人被掀起 → 飛出畫，同一鏡同一句 `in the same unbroken moment`；下一鏡第一格直接是結果（已坐在牆腳、牆面淺坑） | 〔H3 實測〕 |
| **傷害寫成分解事件** | `its scales peel back in long strips, the flesh beneath blackened and smoking`；不寫 `destroyed` 這類終態形容詞 | 〔H3 實測：EP03 R3-20〕 |
| **下一段承接殘破** | 大招後的下一段，敵人是殘骸，不是完好在掙扎 | 〔H3 實測〕 |
| **重擊必擊飛＋瞬間追擊** | 重擊命中後被擊飛，攻擊者立刻追上（不站樁、不隔空對波） | 〔教學 1026 圖文〕 |
| **命中硬切特寫＋短升格** | 命中瞬間硬切特寫看甲冑凹陷、氣場碎裂（原文 0.5 s 升格）→ 0.3 s 倒飛；升格在組裝做 | 〔教學 1026 圖文〕 |

---

## 7. 延遲命中（高級感）〔參考 v7；H3 未實測〕

攻方收劍、不回頭；守方維持被斬姿勢停一拍，**之後**胸前才出現極亮的星形能量核心，先是小亮點再展開成星芒，能量絲線沿衣裙擴散。

```text
She draws the blade back to her side and walks on, calm, her silver hair still stirred by the wind. Behind her, the other swordswoman keeps her guard raised for a beat; then a tiny point of blue-white light appears at her chest and blooms into a sharp star burst, thin ice-blue threads of energy racing out along the seams of her dress.
```

> H3 可能把「停一拍」拉長；守方的停滯用「keeps her guard raised」這種**姿勢描述**，不要寫 `frozen`／`still`。

---

## 8. 定格海報〔教學 v6；H3 未實測〕

全身同時定住、只剩一個小物件還在動（硬幣在轉）；定住那一下鏡頭猛震一下，畫面四邊掃進幾十條白色集中線往她身上收。適合大招完成、變身完成的那一格。H3 上的定格容易變成整段靜止，建議**生成時寫集中線與小物件運動，定格長度在組裝時複製幀**。

---

## 9. 變身

- **閃白 → 發光線稿 → 閃切 2D 漫畫 → 同一姿勢 3D 落定**；寫「閃切」（`cuts to`），不寫「變形」（`morphs into`，會融化粘連）〔教學 v2〕。
- **衝擊幀遮切**：衝擊幀之前只准出現變身前造型、之後才出現變身後造型；回來「白光退開，同一機位、同一步子，她已經變身」〔教學 v6〕。
- Ref2VA 時，變身前／後各給一張參考圖，`retention_analysis` 寫清楚各自出現在哪幾鏡。

細節與英文見 `impact-frame/forms.md` §4。

---

## 10. 收尾

- **大爆後接「靜」**：嘴唇或眼部極近特寫、只有道具光、幾乎無聲〔教學 v6〕。
- **吞沒鏡頭**：貼地超廣角、機位極速後拉，煙塵或光牆撲面吞沒鏡頭 → 黑屏或全白 → 靜〔教學 1026 圖文、v6 段 8〕。寫法見 `cinematic-camera.md` §9。
- **尺度反差**：超遠景、人物極小、巨型劍氣撕開雲海，機位從背後後拉升高〔參考 v7〕。
