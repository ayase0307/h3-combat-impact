# P2｜衝擊幀串段＋組裝變速（大招／必殺／秒殺的預設路徑）

> 什麼時候讀：衝擊點清單裡有 **L4**（大招、必殺、絕招、一招秒殺、毀天滅地、變身）。
> 來源：老大的衝擊幀教學片（v6，旁白＋片尾 9 頁提示詞＋逐幀量測）、打鬥特效教學（v2）、Hark 漫劇 EP03 S04-a d10–d17 實跑（`combat-recipe.md` §12）。
> H3 狀態：**部分實測**——d17 在 1.40–2.21 s 生出衝擊幀段（橘紅底黑剪影＋白環有出、負片沒出），變速預覽 7.29→6.08 s；張數是否守住、會不會擠成分格，**仍需固定 seed 實測**（見文末待驗證）。

---

## 0. 原則：時間給夠，組裝加速

教學片原話：「**把衝擊幀當成一段單獨的畫面來寫**」「**時間給短了，模型會把幾張擠進一屏**（分格拼貼）；改成約 1.2 秒、每張停 3–4 幀，就會一張一張整屏閃」「時間寫長節奏會慢，剪的時候加速——開炮這段寫了 2 秒，成片開 5 倍速」。

| 步驟 | 生成端（提示詞） | 組裝端（`impact_frame.py ramp`） |
|---|---|---|
| 衝擊幀串 | 獨立一段 **0.8–1.2 s**，N 張（3–5 張 H3 建議；教學片 8–10 張），**每張約 0.2 s** | **5×**（每張剩約 1 幀）；短串可 2–3× |
| 回原鏡頭的主特效 | 衝擊波環、電弧、碎石 2–2.5 s | **1.5×** |
| 開場空等（如果模型拖了） | — | 1.5–2× |

> H3 單段字數有限：**3–5 張**寫進主片的 P2 段；要 8–12 張的長清單，改成**單獨生成一支 4–5 s 的「衝擊幀片」**（只放清單），再用 P3 composite 或 concat 插入。

---

## 1. 寫法五要素（缺一就會失敗）

1. **先寫張數與每張停多久**：`a burst of five impact frames of the same composition, each held about 0.2 seconds`
2. **中間不插回正常畫面、一張比一張狠**：`with no normal frame in between, each harsher than the last`
3. **逐張寫「底色＋畫什麼＋畫法」**：`first …; then …; then …; finally …`
4. **同構圖、每張換一套配色**（洋紅／橙紅加黃／黑白／紅黑／白底紅輪流）
5. **畫攻擊動作本身，不是擺姿勢**：`every impact frame shows the attack itself, not a pose`

### 防分格三句（教學原提示詞翻譯；H3 未實測）

```text
each impact frame fills the whole frame edge to edge as a single full-bleed image, one image per screen, never split into panels;
nothing moves inside an impact frame;
outside the impact frames the picture is never split into panels.
```

（validator 會對 `no`／`never` 報否定詞 WARN：上面第一句可以改成 `one image per screen, full-bleed to all four edges`，避開否定詞。）

### 黑剪影只在衝擊幀裡

`the black silhouettes appear only inside the impact frames; in the normal shots every figure keeps its full colour.`
（否則模型會在正常畫面裡也生出黑色人影。）

---

## 2. 前後兩段怎麼接

### 命中：不拍飛行

```text
At 00:01.000, within a single frame a blinding silver-white column of light thicker than a man is already rammed into the serpent's mid-body, with no visible travel.
```

- 禁 `like a meteor`、`plunges down from the sky`、`flies toward`——H3 會把飛行全程畫出來（d15 光束飛 0.6 s）。
- **命中點寫具名部位**，並寫明與被保護者的距離：`two big steps to his right, with clear open ground between it and him`（打頭時頭在主角肩上，命中＝波及主角）。

### 回原鏡頭：特效已全開

```text
At 00:02.200, the burst cuts straight back to the same camera with the column still blasting: in the very first returning frame a white shockwave ring is already tearing outward, the camera jolts violently three times, each smaller than the last, settling within half a second. A second shockwave ring blasts outward.
```

- **第一格就有白色衝擊波環**在外擴，隔一下再炸第二圈。
- 震屏用「**猛震三下、一下比一下小、0.5 s 內停穩**」，之後鏡頭可以很慢地推近一點。
- 鏡頭二選一：回來猛震三下，**或**最大衝擊那一鏡鎖死讓特效推開背景——不要兩個都上。

### 受擊不延遲

命中 → 衝擊波 → 人被掀起 → 飛出畫，寫在**同一鏡、同一句**：`in the same unbroken moment the wave tears him off his knees and flings him out of frame`。下一鏡第一格直接是結果（已坐在牆腳、牆面淺坑），不要再切一鏡去拍「起飛」（H3 會畫成起跳）。

### 傷害寫成分解事件

不寫終態形容詞（`destroyed`、`badly hurt`），寫命中當下正在發生的分解：`its scales peel back in long strips, the flesh beneath blackened and smoking`。下一段承接殘破狀態。

---

## 3. 次要特效（主特效旁邊的小東西）

教學片第 3 步：開炮除了主炮，還寫四周亂竄的電、往外擴的衝擊波環、空氣被熱浪扭得發虛、碎石滿地飛。對應力場四通道（`../force-field.md`）：

```text
the asphalt is ploughed open into a long glowing trench, slabs of concrete as big as wash basins fly out to both sides, the whole row of windows bursts into glittering shards, the plaster is ripped off the wall, the air wavers in heat haze, and forks of silver-white electricity crackle out in every direction
```

---

## 4. 聲音

```text
overall_soundscape: A charging shriek rises; during the impact frames a rapid string of electric shrieks climbs higher and higher; on the return a single deafening boom with a sustained low rumble, debris crashing down and plaster peeling off the walls.
```

教學片另一招：**重擊前聲音驟窄**，碰撞時低頻與裂響同時壓入；大爆後接「靜」（幾乎無聲的極近特寫）。

---

## 5. H3 禁用慢詞（大招段）

| 慢詞 | H3 實際結果 |
|---|---|
| `near-freeze`、`decelerates to a near-freeze` | 放大成 0.5–1 s 停頓 |
| `hangs poised`、`poised and still`、`still for half a second` | 命中前空等 1–3.7 s（d10 等到 3.71 s） |
| `like a meteor`、`plunges down from` | 畫出光束飛行全程 |
| `for half a second`（閃光）、`swallows the whole frame` | 長時間發光淡出 |
| `slowly`、`gradually` | 整段變慢 |

蓄力可以拍，但**用動作與光蓄**（能量在掌心聚集、地面碎石浮起、燈一片片滅），不寫靜止詞。要停頓，就在組裝時複製 1–3 幀，放在命中**前**。

---

## 6. 段落標題寫剪輯計畫（教學片做法）

每段提示詞外（交付說明裡）寫：「出 N 秒，成片用 a–b 秒（X 倍速）」。例：

> 段 6｜出 5 秒，成片用 1.03–2.65 秒（衝擊幀 5 倍速）、2.65–4.09 秒（開炮 1.5 倍速）。

這就是 `output-format.md` 的「衝擊幀計畫表」，對應的指令：

```bash
python scripts/impact_frame.py ramp --in S06.mp4 --seg 1.03-2.65:5 --seg 2.65-4.09:1.5 --keep 1.03-4.09 --out S06.ramped.mp4
```

生成後先用 `impact_frame.py find-peak --in S06.mp4` 找出衝擊幀段實際落在哪幾秒（模型常常提早或延後 0.3–0.6 s），再填 `--seg`。

---

## 7. 完整範例（模板 F 已填）

```text
integrated_multimodal_description: [Shot 1] 3D CG, cinematic, semi-realistic. A ruined school corridor at dusk, a giant serpent reared two big steps to the boy's right, with clear open ground between it and him. Silver light gathers in the girl's raised palm, loose gravel lifts off the floor around her feet and the corridor lights die one by one toward the serpent. The camera pushes in with small amplitude at fast speed. [Shot 2] At 00:01.000, within a single frame a blinding silver-white column of light thicker than a man is already rammed into the serpent's mid-body, with no visible travel. At that most violent instant the picture flashes through a burst of four impact frames of the same composition, each held about 0.2 seconds with no normal frame in between, each harsher than the last: first pure white; then stark black and white, the serpent as a black silhouette on white with thick black radial streaks bursting out from the point of impact; then a red-orange frame with a huge white shockwave ring tearing outward; finally black with every edge drawn as glowing silver-white lines. Every impact frame shows the attack itself. [Shot 3] At 00:02.000, the burst cuts straight back to the same camera with the column still blasting: in the very first returning frame a white shockwave ring is already tearing outward, the camera jolts violently three times, each smaller than the last, settling within half a second. The serpent's scales peel back in long strips, blackened and smoking, the floor is ploughed open into a glowing trench and the whole row of windows bursts into glittering shards. In the same unbroken moment the wave tears the boy off his knees and flings him out of frame. A second shockwave ring blasts outward.
overall_soundscape: A charging shriek rises; during the impact frames a rapid string of electric shrieks climbs higher and higher; on the return a single deafening boom with a sustained low rumble, glass and concrete crashing down.
non_diegetic_music: N/A
```

組裝：`--seg 1.00-2.00:5 --seg 2.00-4.00:1.5`（實際區間以 `find-peak` 為準）。

---

## 8. 待驗證（固定 seed，未做）

- [ ] 3／5／8 張清單在 H3 的實際張數與每張停留幀數。
- [ ] 防分格三句有沒有效（H3 會不會擠成兩三聯）。
- [ ] 負片（colour negative）要怎麼寫才穩定出現（d17 沒出）。
- [ ] 主片內 P2 段 vs 單獨衝擊幀片＋composite，哪個觀感好。
- [ ] 單獨生成 0.5 s 黑白放射板裁 9 幀 vs 2 幀，哪個讀起來更像衝擊（B 報告待實驗 a）。
