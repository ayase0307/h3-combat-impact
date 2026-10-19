# 參考圖保真（Ref2VA Identity Lock）

> 讓生成結果**看起來就是參考圖裡那個人／那個場景**，而不是「差不多的角色」。
> 這是 Ref2VA 唯一值得用的理由——不用參考圖，用純文字描述就夠了。

---

## 0. 為什麼要寫這份

既有 skill 的 Ref2VA 模板只有佔位符（`<角色A：年齡、髮型、服裝逐項>`），
沒有告訴你**該列哪些特徵、用什麼句型寫、寫到什麼密度**。

結果就是：模型拿到一個模糊的「黑髮女劍客」，會自己發明臉、服裝細節、武器細節。
角色看起來像，但不是**那一個**。

**保真的做法是把參考圖裡能辨識的特徵逐項寫成文字，讓模型沒有自由發揮的空間。**

---

## 1. 身份列舉：9 類必列

從參考圖反推時，**照這 9 類逐項看圖**。缺哪一類就補哪一類，不要憑印象寫。

| # | 類別 | 要寫的東西 | 例 |
|---|---|---|---|
| 1 | **臉型** | 臉的輪廓特徵 | `her broad cheekbones and strong square jaw` |
| 2 | **眼睛** | 顏色 + 形狀 | `pale gray eyes`、`amber almond eyes` |
| 3 | **疤／胎記／刺青** | 位置 | `the scar under her right eye` |
| 4 | **髮型** | 長度 + 剪法 + 顏色 | `short black wolf-cut hair`、`long black high ponytail` |
| 5 | **配件** | **含數量** | `three iron hoop earrings`、`a dark-gold hairpin` |
| 6 | **服裝結構** | 具體構造，不是色系 | `asymmetrical black iron armor with an exposed right arm` |
| 7 | **顏色綁在衣物上** | 顏色跟著衣物走，不要單獨列 | `a rust-red rope sash`、`a navy hakama` |
| 8 | **剪影與比例** | 高矮、寬窄、體型 | `broad-shouldered silhouette`、`the smaller swordswoman` |
| 9 | **武器** | 型號 + **相對長度** | `an oversized molten-orange nodachi`、`a standard cold-blue katana` |

### 武器長度一定要用相對量

模型不懂「1.4 公尺的太刀」，但懂「oversized」與「standard」。

```text
❌ a 1.4-meter odachi
✅ an oversized nodachi, longer than she is tall
✅ a standard-length katana, reaching her hip
```

### 相對身高一定要寫

兩人同框時，模型不知道誰高誰矮。**寫在 `detailed_description` 的開場**：

```text
Tieya remains taller and more powerfully built than Bailu.
```

---

## 2. 畫風保真：3–4 個材質錨

只寫 `3D CG` 不夠。要鎖的是**渲染質感**，不是標籤。

從參考圖反推 3–4 個材質錨：

| 錨 | 例句 |
|---|---|
| 皮膚 | `soft subsurface scattering in the skin` |
| 織物 | `fine woven fabric texture with visible thread` |
| 金屬 | `matte forged iron with polished edges` |
| 光 | `cinematic bloom on every bright edge` |
| 材質對比 | `painted CG materials with coherent anatomy` |

**位置有規定：同一句話要在兩個地方出現。**

1. `detailed_description` 的**第一句**（描述整體質感）
2. `[Shot 1]` 的**第一句**（描述該鏡的質感）

兩處一致，模型才會把它當成全片的基底，而不是只有第一鏡有。

```text
detailed_description:
Premium cinematic 3D donghua realism with sophisticated painted CG materials,
coherent anatomy, realistic cloth dynamics, precise sword geometry, grounded
physical impacts.

[Shot 1] Premium cinematic 3D donghua realism with sophisticated painted CG
materials, coherent anatomy. A high overhead aerial shot ...
```

### ⚠️ 畫風錨定不可膨脹

**畫風修飾詞最多 3 個。** 實測：參考圖給太強會讓模型把參考圖當成「要重現的內容」，
整段變成靜止圖（運動量 0.49，見 `impact-design.md`）。

| 畫風描述 | 結果 |
|---|---|
| 只有 `3D CG` | 畫風會漂 |
| 3–4 個材質錨 | ✅ 畫風穩定且畫面會動 |
| 5 個以上錨／一大段材質描述 | ❌ 變靜止圖 |

---

## 3. 環境參考：鎖「建築與標誌物」，不鎖「構圖」

場景參考圖（`<Subject 3>`）要保留的是**可辨識的場景特徵**，不是原本的取景。

```text
<Subject 3> is the moonlit ruined-stone battlefield from <Picture 3>. Preserve the
recognizable ruined fortress architecture, broken pillars, torn red banners, wet
reflective stone flooring, burning braziers, cold moonlight, warm firelight, and
atmospheric mist. <Picture 3> provides the environmental reference rather than an
exact camera frame.
```

**用正面句寫，不要用 `rather than` 這種否定式**（`output-format.md` 的禁用清單）。

| 該寫 | 不該寫 |
|---|---|
| `provides the environmental reference rather than an exact camera frame` | `provides the environmental reference, not an exact camera frame` |
| `its pose and background are adapted to the new battle scene` | `its pose and background are replaced` |

> **實務上 `rather than` 會被 validator 抓到**（`validate_prompt.py` 的否定詞表有它），
> 但 `output-format.md` 的禁用清單漏列了它——兩邊不一致。**直接避開 `rather than` 最安全。**

### 環境特徵要列 5–7 項

```text
✅ 架構（ruined fortress architecture）／建材（wet reflective stone flooring）
   ／標誌物（torn red banners, burning braziers）／光源（cold moonlight, warm firelight）
   ／大氣（atmospheric mist）
```

---

## 4. 完整可用範例（已通過 validator）

```text
subject_definitions:
<Subject 1> is Tieya, the tall northern female warrior from <Picture 1>. Preserve her exact facial identity, pale gray eyes, the scar under her right eye, her short black wolf-cut hair, her three iron hoop earrings, her broad-shouldered silhouette, her asymmetrical black iron armor, her exposed right arm, her rust-red rope sash, her damaged short hakama, her armored boots, and her oversized molten-orange nodachi. <Picture 1> provides her character and weapon identity, while her pose and background are adapted to the new battle scene.

<Subject 2> is Bailu, the smaller female swordswoman from <Picture 2>. Preserve her exact facial identity, her amber almond eyes, her long black high ponytail, her dark-gold hairpin, her ivory-white kimono, her navy hakama, her dark-gold crest details, her obi, her white tabi, her black geta, and her standard cold-blue katana. <Picture 2> provides her character and weapon identity, while her pose and background are adapted to the new battle scene.

<Subject 3> is the moonlit ruined-stone battlefield from <Picture 3>. Preserve the recognizable ruined fortress architecture, the broken pillars, the torn red banners, the wet reflective stone flooring, the burning braziers, the cold moonlight, the warm firelight, and the atmospheric mist. <Picture 3> provides the environmental reference as the environmental basis for the new battle scene.

summary:
[reference generation] An 8-second 16:9 cinematic sword duel between <Subject 1> and <Subject 2> inside <Subject 3>, fought at ultra-high speed with relentless camera repositioning and continuous environmental destruction, ending on one decisive weapon collision. The scene preserves both characters' distinct appearances, weapon identities, and the established environment.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5], [Shot 6], [Shot 7], [Shot 8]): fully_preserved - Maintain the reference face, hairstyle, scar, earrings, armor construction, body silhouette, costume colors, and the enormous molten-orange nodachi throughout all visible shots.

<Subject 2> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5], [Shot 6], [Shot 7], [Shot 8]): fully_preserved - Maintain the reference face, high ponytail, hairpin, white-and-navy outfit, body silhouette, and the slender cold-blue katana throughout all visible shots.

<Subject 3> (appears in [Shot 1], [Shot 2], [Shot 3], [Shot 4], [Shot 5], [Shot 6], [Shot 7], [Shot 8]): fully_preserved - Maintain the same recognizable ruined courtyard, moonlit and firelit atmosphere, red banners, stone surfaces, braziers, and wet ground across every camera angle.

detailed_description:
Premium cinematic 3D donghua realism with sophisticated painted CG materials, coherent anatomy, realistic cloth dynamics, precise sword geometry, restrained energy effects, and grounded physical impacts. Tieya remains taller and more powerfully built than Bailu. Their costumes, hair, faces, and weapons retain their separate visual identities at every cut.

[Shot 1] Premium cinematic 3D donghua realism with sophisticated painted CG materials, coherent anatomy. A high overhead aerial shot looking almost straight down into <Subject 3>...
```

---

## 5. retention_analysis 的三個等級

| 等級 | 意義 | 什麼時候用 |
|---|---|---|
| `fully_preserved` | 完整保留 | 角色臉、服裝、武器；場景建築 |
| `partially_copy` | 部分複製 | 只想保留姿勢、想換裝 |
| `reference` | 僅作參考 | 動作節奏、運鏡參考片 |

**選錯等級的後果**：給 `fully_preserved` 但描述太長太細 → 模型過度模仿、畫面變靜止；
該給 `fully_preserved` 卻給 `reference` → 模型完全忽略參考圖。

---

## 6. 保真檢查清單（生成前逐項打勾）

- [ ] 每個角色都列滿 9 類特徵（缺的類別在 `retention_analysis` 裡重述）
- [ ] 配件寫了**數量**（`three iron hoop earrings`）
- [ ] 武器長度用**相對量**（`oversized` / `standard` / `longer than she is tall`）
- [ ] 兩人身高差寫在 `detailed_description` 開場
- [ ] 畫風錨 3–4 個，**不超過 3 個形容詞**
- [ ] 畫風句在 `detailed_description` 與 `[Shot 1]` **兩處一致**
- [ ] 場景參考寫「環境基礎」而非「原始取景」
- [ ] `retention_analysis` 裡把關鍵特徵**重述一次**（不能只在 `subject_definitions` 宣告）
- [ ] 每個出現的鏡頭都列進 `appears in [...]`

---

## 7. 常見失敗

| 症狀 | 根因 | 修法 |
|---|---|---|
| 角色長得像但不是**那一個** | 特徵列舉不夠，模型有空間自由發揮 | 補滿 9 類，尤其是疤／配件數量／剪影比例 |
| 臉變了但服裝對 | `retention_analysis` 沒重述臉部特徵 | 在 retention 裡逐項重述 |
| 畫風變了（變成通用 3D CG） | 只寫 `3D CG`，沒有材質錨 | 加 3–4 個材質錨，兩處一致 |
| **整段變成靜止圖** | 參考圖給太強（畫風描述太長／特徵太細） | 畫風錨砍到 3 個；特徵列舉控制在 15 個以內 |
| 場景變了（不像原參考圖） | 沒寫可辨識的場景特徵 | 場景列 5–7 項：架構／建材／標誌物／光源／大氣 |
| 武器比例錯（太刀變短刀） | 沒寫相對長度 | 寫 `oversized`、`longer than she is tall` |
| 兩人身高一樣 | 沒寫相對身高 | `detailed_description` 開場寫清楚 |
| 場景構圖被鎖死 | 把環境參考當成首幀 | 明寫「provides the environmental reference as the environmental basis」 |
