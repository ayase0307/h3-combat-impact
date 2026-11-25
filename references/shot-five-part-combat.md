# 每鏡五小節（打鬥版）：Camera / Motion / Performance / Light / Sound

> 來源：上游 repo `h3-video-prompting` 雲端 `origin/main`（commit `1db923b`，2026-10-21）的 `references/shot-five-part.md`；
> 本檔是它的**打鬥改編版**，加上《提高打鬥的方法》《特效寫法》《衝擊幀教學》三支教學片的蒸餾。
> 可信度：五小節本體在 EP01（12 段、35 鏡、Ref2VA）已有實戰；**打鬥版的鏡數密度與字數預算是本 skill 的推論，尚未 A/B**。

## 為什麼打鬥特別需要五小節

打鬥的每一鏡同時要做四件事：換機位、跑動作、演表情、炸特效。**只寫一句動作時，模型會把這四件事都補成平均值**：

| 漏寫 | 模型補的東西 | 症狀 |
|---|---|---|
| Camera | 一個正對中景，鏡頭自己亂飄 | 運鏡沒有落點，切鏡沒有軸線 |
| Motion | 站著比劃，沒有重心轉移 | 「動作軟」「像木頭人」 |
| Performance | 同一張臉從頭到尾 | 臉是死的，打得再快也不投入 |
| Light | 平光 | 特效再亮也不吃光，像貼圖 |
| Sound | 通用打擊聲 | 打擊點與聲音對不上 |

**五小節＝逐鏡交一張規格卡。** 它同時解決兩件事：生成更有細節，審稿時一眼看出哪一軸漏寫。

## 一行的組成（順序固定，整鏡不換行）

```text
[Shot N] At MM:SS.mmm, the shot cuts to a <景別> (<焦距>, <物距>) of <主體>, as the camera <官方運鏡詞>. Camera: …  Motion: …  Performance: …  Light: …  Sound: …  <台詞 <d>…</d>／外部 TTS 說明／Lips stay closed.>
```

頭句只放官方排版（景別、焦距物距、主體、**唯一的運鏡動詞**）；五小節接在後面；台詞永遠放最後。

## 五小節的內容（打鬥版）

| 小節 | 打鬥時必須寫進去的東西 | 句型 |
|---|---|---|
| **① Camera** | 焦距＋物距＋機位高度／方位；運鏡幅度、速度、時長；**起幅與落幅**（主體在畫左還是畫右、落在哪條線上、鏡頭跟誰）；固定鏡寫 `locked off for 2.0 s` | `85mm from three metres at chest height, pushing in slowly by about fifteen percent over 1.2 s, so she starts small in frame-left and ends filling the right two thirds` |
| **② Motion** | 起始狀態 → **施力點／方向／速度** → **支撐與重心** → 慣性 → 結束狀態。打鬥的關鍵在第三段：哪隻腳承重、重心從哪移到哪、擊中瞬間的支點在哪、被擊中時哪一段先動 | `First her weight sinks into the rear leg, then she drives off that heel and the front foot lands, as her hips rotate ahead of her shoulders, finally her mass arrives behind the halberd head` |
| **③ Performance** | 眉／上眼瞼／下眼瞼／鼻翼／下顎／齒／唇／頸喉／太陽穴／汗淚／呼吸，**寫可見的變化**；打鬥要寫「痛→狠→收」的轉折；無臉鏡改寫手、背、肩線 | `Her jaw muscles bunch and her lips peel back off clenched teeth, one eye narrows against the grit, a nostril flares on the intake, then the face empties flat as the strike lands` |
| **④ Light** | 光源方向＋色溫；**特效本身是光源**（要照亮臉、地面、霧）；材質對光；環境回應（水面、紙、布、灰塵、濕石板）；**跨鏡光源一致** | `The blood-red moon stays behind camera-left, and each white blade flare throws a hard rim up her cheek, while the wet petals under her feet pick up a magenta bounce` |
| **⑤ Sound** | 鏡內音效的秒數（`at about 0.8 s`）、環境音、台詞起口時間；外部 TTS 鏡要寫明說話者嘴不入畫 | `The halberd shaft whistles at about 0.4 s and the impact lands at 0.9 s; rain keeps a steady bed underneath` |

### ② Motion 的「支撐重心」寫法（打鬥最常缺的一段）

動作軌跡不是位移動畫，是**質量轉移**。同一招寫不寫重心，模型給的是兩個東西：

```text
❌ She swings the halberd.
✅ Her weight sinks into the rear leg, she drives off that heel, the front foot plants
   and takes the whole body, her hips rotate ahead of her shoulders, and her mass arrives
   behind the blade head at the moment of contact.
```

四個可寫的重心參數（每鏡挑 1–2 個，不要全寫）：

| 參數 | 英文句 | 什麼時候用 |
|---|---|---|
| **承重腳** | `her weight is on the rear foot` ／ `he takes his base on the lead leg` | 每一次出手前必須交代，否則看起來在飄 |
| **重心位移** | `her hips travel forward a hand's width before the strike leaves` | 想讓擊打有推進去的力量 |
| **支點** | `the polearm pivots on her rear hand while the front hand drives` | 長兵器、大劍、槍 |
| **失衡／慣性** | `his weight tips past his toes and he has to step to catch it` | 受擊、被騙、被破站勢 |

> 只有「打中」而沒有「重心到位」，就是觀眾說的「軟」。這一段是打擊感的成本最低來源，比加特效便宜。

## 打鬥版的六條硬規則（五小節內也要守）

1. **運鏡詞只出現在頭句。** 五小節內不寫第二個運鏡動詞（push／pan／tilt／zoom／truck／dolly／pedestal／track），不寫 `the camera`，不寫 orbit／arc／360。
2. **每鏡只有一個主動作。** Motion 可以寫四個階段，但只能有一個「位移型」的動作；第二個大動作請切鏡。
3. **不重述參考圖外觀。** 髮型、五官、服裝只寫在 `subject_definitions`（Ref2VA）或頭句一次。
4. **Performance 必須是「部位＋動作」。** `a determined expression`、`fierce eyes` 一律不算。
5. **Sound 不寫配樂。** 配樂只寫在 `non_diegetic_music`；五小節的 Sound 只寫鏡內物理音與環境音。
6. **收尾停在動作中。** 不寫 `comes to rest` / `settles`；寫 `holds there`、`stays suspended`、`is still travelling`，否則會被定格吃掉。

## 與三種節奏模式的對應

五小節是**每鏡的規格卡**，六拍是**一次交手的節拍**。兩者不衝突，嵌套使用：

| 模式 | 每鏡承載的拍 | 五小節的重心 |
|---|---|---|
| **六拍** | 一鏡可含 2–3 拍（蓄＋觸，或洩＋退） | Camera 寫固定或緩推；Motion 寫蓄力的反向預備 |
| **連續對轟** | 一鏡一拍或半拍 | Camera 每鏡換軸線；Motion 寫「交換」而非「完成」 |
| **ULTRA_SPEED** | 一鏡＝一個瞬間 | Camera 主導（每鏡換機位）；Motion 只寫一個離散動作 |

## 字數預算（五小節會膨脹，先算好）

五小節寫滿，每個鏡頭約 **120–190 英文字**。所以：

| 時長 | 鏡數 | 五小節版預估 | 舊版一句式 |
|---|---:|---:|---:|
| 4–6 秒 | 2–3 | 350–570 字 | 120–200 字 |
| 8 秒 | 4–5 | 500–900 字 | 200–350 字 |
| 15 秒 | 8–12 | 1000–2000 字 | 400–700 字 |

> **7500 字元是送件端硬上限（`validate_prompt.py` 會算）。** 超過就拆段，不要砍鏡內小節——
> 照 `h3-video-prompting` 的壓縮順序：先壓 `retention_analysis`、次要角色服裝尾巴、場景圖描述，最後才動小節。
> 實測風險：字數越長，**寫在最後的約束越容易失效**——重要約束（相機鎖死、人物佔比）一律往前放。

## 完整範例（8 秒、5 鏡、血月戰場）

```text
integrated_multimodal_description: [Shot 1] 3D CG, cinematic anime game trailer, high-contrast blood-red and bone-white. A wide low-angle shot (35mm, 9 m) of the white-coated girl standing alone in a red petal field under a huge blood moon, as the camera holds a locked-off static shot. Camera: 35mm from nine metres at knee height, locked off for 2.0 s, her figure small in the lower right third with the moon filling the upper left. Motion: First her weight settles onto the rear foot and her shoulders drop, then her chin lifts a finger's width, and her coat hem keeps travelling a beat after she stops. Performance: Her eyes stay closed, the blood streak on her right cheek catching the moonlight, her jaw loose, one slow breath lifting her collarbone. Light: The blood moon sits behind camera-left and rims her hair in cold crimson while the field throws magenta bounce up the inside of her coat. Sound: Petals hiss across the ground at about 1.0 s, rain-fine and constant.

[Shot 2] At 00:02.000, the shot cuts to an extreme close-up (100mm, 1 m) of her face as she opens her eyes, as the camera pushes in slowly. Camera: 100mm from one metre at eye height, closing about ten percent over 1.2 s, her left eye ending on the upper third line. Motion: First her lids part, then her pupils contract, and the blood streak on her cheek tightens as the skin below it moves. Performance: Her lower lids tense, her lips part a slit and press closed again, the tendon in her neck stands out for one beat. Light: A hard crimson rim runs along her cheekbone and the wet streak catches it as a wet silver line. Sound: A single low string swell under a paper-thin whisper of petals.

[Shot 3] At 00:03.600, the shot cuts to a medium wide shot (50mm, 6 m) of her snapping her fingers, as the camera holds a locked-off static shot. Camera: 50mm from six metres at waist height, locked off for 1.4 s, her hand entering frame-right and stopping dead centre. Motion: First her weight shifts onto the front foot, then she stomps that heel down flat as her arm whips up, and the recoil runs back through her shoulder. Performance: Her jaw locks, her brows slam down, and her mouth flattens into a hard line as the snap lands. Light: A white core ignites at her fingertips and throws a flat hard key across her face for one beat, then decays into the crimson ambient. Sound: Fabric snaps at about 0.3 s, the finger snap cracks at 0.6 s, and grit shifts under her heel at 0.4 s.

[Shot 4] At 00:05.000, the shot cuts to a full shot (28mm, 12 m) of the field as the air around her splinters into black polyhedral shards, as the camera pushes forward fast. Camera: 28mm from twelve metres at chest height, closing fast with large amplitude over 1.6 s, so her silhouette ends filling the centre third. Motion: First the shards tear open outward from her, then her coat and hair are pulled toward the fracture, and her feet stay planted against the drag. Performance: Her shoulders square up and her chin drops, the smile arriving before the eyes do. Light: Every shard edge carries a hard white specular and the moon's crimson light refracts through them into fanned magenta streaks across the petals. Sound: Glassy fracturing at about 0.4 s, then a rising airy pull under a low hum.

[Shot 5] At 00:07.000, the shot cuts to a low-angle wide shot (24mm, 14 m) of three red light pillars erupting through the field, as the camera tilts up fast. Camera: 24mm from fourteen metres at ground level, rising at fast speed over 1.0 s, the pillars climbing out of the top of frame. Motion: First the ground splits, then the pillars punch upward and the shockwave flattens the petals outward, and her coat is thrown flat against her body. Performance: She holds her face still, only her eyes narrow and her head turns a few degrees into the light. Light: The pillars are the only key, washing the whole field in saturated red and turning her white coat pink at the edges. Sound: A sub-bass thump at 0.2 s, stone grinding apart under it, then a long pressure roar.

overall_soundscape: A thin wind over wet petals with a distant low drone that hangs unresolved, then three heavy stone-tearing impacts, each followed by a rain of grit pattering down.

non_diegetic_music: A single sustained low cello note under sparse high string harmonics, the percussion held back until the last beat, and that last taiko hit cut dead at the last beat.
```

數一下：5 鏡、約 780 英文字、4.4k 字元——這是「五小節寫滿」之後的正常體積。

## 自檢

```bash
python scripts/validate_prompt.py prompt.txt --duration 8 --five-part
```

`--five-part` 會逐鏡檢查：五個標籤都在、順序正確、**五小節內沒有第二個運鏡動詞**。
FAIL 全修掉才交付。

## 什麼時候不要用五小節

- **1–2 秒的單鏡插入鏡**（ULTRA_SPEED 的 0.4–0.8 秒鏡）：五小節的體積會擠掉動作本身，用「四件套」即可（見 `ultra-speed.md`）。
- **純特效鏡**（只有爆炸、沒有人）：Performance 沒有東西可寫，改成寫材質與環境回應。
- 送件端硬上限吃緊時：先壓其他欄位，再考慮把 Performance 併進 Motion。
