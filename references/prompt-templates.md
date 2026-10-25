# 提示詞模板（可直接填空）

所有模板遵循官方三欄位結構。英文為交付語言，中文為註解，**不要把中文註解送進模型**。

---

## 模板 A｜T2VA 打鬥片段（單段 ≤15 秒）

```text
integrated_multimodal_description: [Shot 1] 3D CG, cinematic, wuxia. <景別> of <主體A：外觀鎖定> in <場景：材質+光源+大氣>. <主體動作>; <運鏡：類型+幅度+速度>. <能量特效：形狀+運動+顏色>. <環境反應>. The <主體> stays <要保持的特徵>.

[Shot 2] At 00:0X.XXX, the camera cuts to <景別> of <主體B：外觀鎖定>. <蓄力動作>; <運鏡>. <材質/布料細節>.

[Shot 3] At 00:0X.XXX, <命中拍：具名打擊點>. <IMPACT：P0／P1 句型，例 the frame blows out to white at the instant of contact as radial speed lines tear outward, then snaps straight back>; the camera jolts hard for a few frames and settles almost immediately. <衝擊波方向>. <受擊者在同一句被打飛 + 衣髮延遲跟隨>.

[Shot 4] At 00:0X.XXX, the camera cuts to <下一個景別：後果／reveal>. <受擊者已經在結果位置>; <殘留粒子>. <表情肌肉>.

[Shot 5] At 00:0X.XXX, <收勢，動作中段收尾>. The camera steadies.

overall_soundscape: <環境底噪> continues underneath. <物理音：金屬/石/水/布>. <命中音：低頻 + 高頻>. <餘韻：殘響、碎片落地>.

non_diegetic_music: <樂器> at <速度>, <節奏型>, <動態變化（漸強/驟停/收束）>.
```

**填空順序**：景別 → 主體 → 場景 → 動作 → 運鏡 → 特效 → 環境反應 → 聲音。一次只填一項，避免整段重寫。

舊版第 4 鏡（`decelerates to a near-freeze`）已刪：H3 會放大成 0.5–1 s 停頓。要停頓，在組裝時複製命中前 2–10 幀。L4 大招不要用模板 A，用**模板 F**。

---

## 模板 B｜FL2VA 接續（>15 秒必需）

第一行固定為對齊句，時間碼寫**本段時長**（兩位小數）：

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the 7.00-second mark of the target video.

integrated_multimodal_description: [Shot 1] 3D CG, cinematic, wuxia. The shot begins in the exact framing, lighting and pose established by Picture 1: <描述首幀>. <動作啟動>; <運鏡>. <中間變化 1>. <中間變化 2>. Toward the end, <收束動作>, settling into the pose and composition established by Picture 2.

overall_soundscape: ...
non_diegetic_music: ...
```

**FL2VA 三原則**：
1. 偏好**單鏡頭**，讓模型連續插值；多鏡頭只在必要時用。
2. 只寫「首幀 → 中間變化 → 末幀」的**路徑**，不要重複描述兩張圖。
3. 末幀必須由最後一個 `[Shot N]` 在影片結束時抵達。

**接續流程**：生成第 1 段 → 匯出最後一幀 → 當第 2 段 `<Picture 1>` → 第 2 段再匯出末幀 → 依此類推。

---

## 模板 C｜Ref2VA 角色一致性（同一角色跨段不變臉）

```text
subject_definitions:
<Subject 1> is the <角色A：年齡、髮型、服裝逐項> in <Picture 1>.
<Subject 2> is the <角色B> in <Picture 2>.
<Subject 3> is the <場景：材質、光源、標誌物> in <Picture 3>.
<Video 1> is the motion reference for <Subject 1>'s <動作類型>.

summary:
[reference generation] A <時長>-second wuxia duel in which <Subject 1> and <Subject 2> exchange <擊數>, preserving the identities, costumes and set from the reference images while adopting the movement rhythm of <Video 1>.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 3]): fully_preserved - <列出具體特徵>.
<Subject 2> (appears in [Shot 2], [Shot 4]): fully_preserved - <列出具體特徵>.
<Subject 3> (appears in [Shot 1]-[Shot 4]): fully_preserved - <場景特徵>.
<Video 1>: reference - the target copies its <節奏/速度/招式順序> but not its appearance.

detailed_description:
[Shot 1] ...（同模板 A 的寫法）
<IMPACT>（有大招／L3 以上命中必填：P1 句型，或 P2 衝擊幀串段（模板 F 的 Shot 2–3）；走 P3 則不寫、在 block 外附衝擊幀計畫表。見 SKILL.md §3 決策卡）

overall_soundscape: ...
non_diegetic_music: ...
```

**保留等級只有三種**：`fully_preserved`（完整保留）、`partially_copy`（部分複製）、`reference`（僅作參考）。選錯等級會導致模型過度模仿或完全忽略。

**Ref2VA 上限**：圖 ≤9、影片 ≤3（每段 2–15 秒、總計 ≤15 秒）、音訊 ≤3，合計 ≤12 個檔案。

---

## 模板 D｜完整範例（青焰對決，7 秒 5 鏡）

```text
integrated_multimodal_description: [Shot 1] 3D CG, cinematic, wuxia. A low-angle wide shot frames a female swordswoman in a black high-collared sleeveless top, layered white ruffled skirt and thigh-high black boots, crouched at the centre of a rain-soaked temple courtyard. A wall of orange fire erupts behind her, backlighting her silhouette, while teal spirit flame licks along the edge of her black katana. The camera pushes in with small amplitude at fast speed through drifting embers. She drives off her rear leg and springs upward. Her face stays sharp and her long black ponytail trails a beat behind her body.

[Shot 2] At 00:01.800, the camera cuts to a wide shot from below. She hangs at the apex of the jump, and eight spinning vortex orbs of teal smoke-tailed energy orbit her in a slow ring. The camera arcs around her with small amplitude at slow speed. The orbs accelerate, their tails streaking into a continuous ring.

[Shot 3] At 00:03.600, the camera cuts to a close-up of a silver-haired male swordsman in a dark navy layered robe, a thin streak of blood at the corner of his mouth. He drags a massive bronze blade inlaid with a row of ancient coins along the flagstones, throwing sparks. The camera tilts up with small amplitude at slow speed from the blade to his eyes.

[Shot 4] At 00:05.000, he swings the blade upward into her guard. The frame blows out to white at the instant of contact as radial speed lines tear outward, then snaps straight back; the camera punches in with small amplitude at fast speed and jolts hard for a few frames, settling almost immediately. A ring of grey dust bursts outward along the ground, roof tiles rattle loose overhead, and the teal orbs are scattered outward in a widening circle. In the same unbroken moment she is driven back, boots gouging two lines in the wet stone, her ponytail whipping a beat late.

[Shot 5] At 00:06.200, the camera cuts to a low medium shot as she skids to a stop and rises straight into a low guard, her jaw locking and her chest heaving, sparks and embers drifting between them. The camera steadies.

overall_soundscape: Fine rain ticks on the flagstones while low wind moves through the canopy. Steel grinds along stone, then a deep bass impact is followed by a sharp metallic crack and a long reverberant tail as tiles clatter down. Wet boots skid and stop.

non_diegetic_music: Low sustained strings and a single bowed erhu line at a slow tempo, cut abruptly to silence on the impact, then a low drum pulse returns at half volume.
```

---

## 模板 E｜爆炸三段式（衝擊幀 + 力場 + 震屏）

```text
[Shot N] At 00:0X.XXX, <場源> bursts outward at extreme speed and the entire frame blows out to pure white, then snaps straight back; <震屏二選一：the camera holds a static shot while the blast pushes the background away／the camera jolts hard for a few frames and settles almost immediately>. <衝擊波形狀> races outward. <物質通道：塵土/玻璃/碎石>. <光通道：全域光影聯動、陰影偏移>. <空氣通道：折射/熱浪/層狀撕裂>. <粒子通道>. <反向證據：主角衣襬或頭髮被推，延遲半拍>.
```

四通道至少填三個。**空氣通道的句子最有效，粒子通道最廉價。**

填空順序：場源 → 閃白 → 震屏 → 波形 → 物質 → 光 → 空氣 → 粒子 → 反向證據。

---

## 模板 F｜大招 P2（衝擊幀串＋組裝變速；T2VA／I2VA／Ref2VA 通用）

L4 大招、必殺、一招秒殺、毀天滅地的**預設模板**。寫法細節與禁用慢詞見 `impact-frame/burst-strip.md`；完整已填範例在該檔 §7。

```text
[Shot 1] <風格錨定>. <攻擊者與目標的距離與中間空地>. <蓄力：用動作與光，例 light gathers in her palm, gravel lifts, the lights die one by one toward the target；不寫 still／poised>. <表情肌肉>. <運鏡>.
[Shot 2] At 00:01.000, within a single frame <能量> is already rammed into <具名打擊點>, with no visible travel. At that most violent instant the picture flashes through a burst of <N=3–5> impact frames of the same composition, each held about 0.2 seconds with no normal frame in between, each harsher than the last: first <底色＋畫什麼>; then <…>; then <…>; finally <…>. Every impact frame shows the attack itself.
[Shot 3] At 00:0X.XXX, the burst cuts straight back to the same camera with the attack still at full force: in the very first returning frame a white shockwave ring is already tearing outward, the camera jolts violently three times, each smaller than the last, settling within half a second. <物質／空氣／光 三通道>. <傷害寫成分解事件>. In the same unbroken moment <受擊者被掀飛>. A second shockwave ring blasts outward.
[Shot 4] At 00:0X.XXX, the camera cuts to <後果：受擊者已在結果位置>, <表情肌肉＋呼吸>.
overall_soundscape: <蓄能尖嘯> rising; during the impact frames a rapid string of electric shrieks climbs higher and higher; on the return a single deafening boom with a sustained low rumble, debris crashing down.
```

- 衝擊幀串每張的配方：2D／動畫用手繪（墨點、粗筆刷、飛白、刮痕），每張換一套配色；寫實／半寫實用「純白 → 全幀負片 → 黑白剪影＋粗放射線 → 橘紅底白環 → 黑底銀白描邊」（`impact-frame/forms.md` §2）。
- 交付時附衝擊幀計畫表與 `ramp` 指令（`output-format.md` §1.1–1.2）：Shot 2 區間 5×、Shot 3 主特效 1.5×。
- 要 8–12 張的長清單 → 改成單獨生成一支 4–5 s 衝擊幀片（P3）。

---

## 參數建議（依模式）

| 情境 | 建議 |
|---|---|
| 首次打樣 | T2VA、6–8 秒、16:9、768p，先確認節奏與特效 |
| 角色固定 | 先生成角色定裝圖，再用 Ref2VA 或 I2VA |
| 長片 | 每段 ≤8 秒，FL2VA 接續；不要用 15 秒硬塞 8 個鏡頭 |
| 大招 | 模板 F，生成時衝擊幀段給 0.8–1.2 s，組裝 5× |
| 出片 | 定稿後走 2K Regenerate，不要一開始就 2K |
| 音訊 | 原生立體聲已含衝擊音，`overall_soundscape` 寫得越具體，低頻越紮實 |
