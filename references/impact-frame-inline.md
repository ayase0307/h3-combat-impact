# 衝擊幀寫進提示詞：生成端的三條路線

> 同一支裡的一拍圖形衝擊走 `SKILL.md` 的減去式＋退出（約 0.2 秒、厚黑剪影、色彩與細節回來並留住）。本檔仍是多卡、變身、後製。內嵌衝擊幀做得到。

> 蒸餾來源：《衝擊幀教學》85 秒（9:16，含完整提示詞畫面）、
> 《打鬥特效》「要點 1 衝擊幀」（變身 0.3 秒閃 5 下、逐幀拆解 UI）。
> 兩片都把提示詞直接打在畫面上，本檔的數字與句子是逐字轉錄。
> **本檔修正** `impact-frame-and-shake.md` §1.1.1 的結論「想要 2 幀精度只能在後期剪」——
> 那不是唯一解，還有一條「時間膨脹法」（見 §5）。

## 0. 三條路線，先選一條

| 路線 | 做法 | 精度 | 成本 | 什麼時候用 |
|---|---|---|---|---|
| **A 多卡閃切** | 在提示詞裡給衝擊幀一個**獨立時間段**，寫明幾張、每張停幾幀、每張的底色與畫法 | 中（幀數不精確，但「一張一張」讀得出來） | 低（純提示詞） | 動畫／漫畫風、水墨、手繪 |
| **B 變身六層** | 白閃→發光線稿→閃切 2D 漫畫→同一姿勢落定，總長 0.3 秒 | 中 | 低 | 變身、開大、切換形態 |
| **C 後製合成** | 主片與衝擊幀分開生成，再抽幀疊回主片 | 高（逐幀可控） | 中（要 ffmpeg） | 需要精確 2 幀、真人／3D 寫實 |

原片作者的立場很清楚：**「網上大多教你截圖、生圖，再一張張貼回去，其實直接寫進提示詞就行。」**
本 skill 的立場：**A／B 拿「讀得出來」，C 拿「逐幀精確」。三者可以混用。**

## 1. 路線 A：多卡閃切（原片核心做法）

### 1.1 提示詞結構（逐字轉錄）

```text
[5.5-6.7s] 冲击帧：八张静止的图，每张停三四帧
4. 洋红平涂底，中间一团黑墨爆炸开
7. 米白纸上用黑墨画的她正面全身的剪影
5. 粉白底上，大片洋红和深红的…
```

三個要件，缺一不可：

| 要件 | 寫法 | 為什麼 |
|---|---|---|
| **總張數** | `八张静止的图` | 不寫張數，模型會當成「一個畫面劇烈閃爍」 |
| **每張停幾幀** | `每张停三四帧` | 這是「一張一張」與「一團糊」的分界 |
| **每張的底色＋內容** | `洋红平涂底，中间一团黑墨爆炸开` | 換底色＝換卡；不換底色模型會連成一張 |

### 1.2 畫法約束（原片原文）

```text
每张都是粗暴的手绘，不是干净的 3D 渲染图
墨点飞溅、粗笔刷、飞白、刮痕
每张换一套配色，洋红、橙红如黄、黑白轮着来
```

- **「不是乾淨的 3D 渲染圖」是負面約束**——H3 沒有 negative 欄位，所以它跟在正面句後面（`crude hand-drawn,
  never a clean 3D render`）。這一條是「手繪漫畫感」與「塑膠 CG」的分界。
- **每張換配色**：洋紅／橙紅／黑白輪著來。同色系連排會被讀成一張長圖。

### 1.3 時間要給夠（實測數字，原片）

| 寫給模型的時間 | 結果 |
|---|---|
| **0.3 秒** | ❌ 模型把 8 張**擠進同一屏**（變成一張拼貼） |
| **1.2 秒** | ✅ 一張一張整屏閃（每張 3–4 幀） |
| **2.0 秒** | ✅ 可以，但成片節奏慢 → **剪輯時開 5 倍速** |

> **所以「給 1.2 秒」是安全的預設值。** 換算：8 張 × 3–4 幀 = 24–32 幀 ≈ 1.0–1.33 秒 @24fps。

### 1.3.1 重新實測：張數少一點、每張久一點（2026-11-04，Pika H3 Flex）

> 範圍：REMIX 的 Pika H3 Flex（480／768），每種寫法 2–3 個 seed，只跑過這個後端。當成目前的最佳猜測，不是定論。

- **時間**：每張寫約 0.3–0.45 秒、共 4–6 張，這樣寫的劇本式 4/4 整屏不分格，出片後在剪輯加速到每張約 0.1 秒。
- **一定要寫的句子**：每張鋪滿整個畫面、不分格、不拼成兩三聯、畫到四邊不留白、圖裡什麼都不動、粗暴手繪不是 3D。
- **格式會影響樣式**：同一題（踩地、出拳、衝擊幀）官方六段式 1/3 變三聯；劇本式 3/3 整屏，但多半是拳頭與爆炸圖形，人物常是貼上去的 3D。官方格式比較會用墨線重畫人物。
- **張數與時間都不聽**：`examples/impact-frame-inline.txt` 寫 3 張共 0.6 秒（4.6–5.2 秒），最好的一支出了約 5 種畫面，從 4.875 秒到約 6.2 秒，卡裡的圖還會動。另外兩個 seed 一支三聯、一支是短短三張。
- **預期會晚**：切點常晚 0.2–0.8 秒，有時會穿插真畫面。剪輯時挑著用，不要照提示詞的時間碼剪。
- **剪輯**：倉庫展示片（`assets/showcase/impact-inline.mp4`）把卡加速到每張約 0.1 秒。變身段的提示詞在 `examples/impact-frame-screenplay.txt`（劇本式，2/2 整屏）。

### 1.4 H3 的英文寫法（本 skill 改寫）

```text
[Shot 5] At 00:05.500, the shot cuts to an eight-card impact sequence held for one point two
seconds, each card a still frame on screen for three to four frames, every card drawn by hand:
The first card is flat magenta with a ball of black ink exploding open at its centre. The second
is off-white paper with her full-body silhouette cut in black ink. The third is pale pink with a
broad magenta and deep crimson wash behind her. The fourth flips to black ground with white ink
spitting outward. The fifth returns to magenta with the silhouette inverted. The sixth is
bone-white with a single hard black slash across the frame. The seventh is black with a white
radial burst. The eighth is off-white again with ink still dripping down from the top edge.
Every card is crude hand-drawn ink work with spatter, coarse brush strokes, dry-brush breaks and
scratches, never a clean 3D render.
```

英文版把「八張、每張三四幀、每張的底色與內容、畫法」四件事都寫齊；`one point two seconds` 是給模型的時間。

## 2. 路線 B：變身六層序列（打鬥特效，0.3 秒閃 5 下）

原片逐幀拆解的 UI 與數字（照抄；原片為 60fps 素材，見下方換算警告）：

| # | 層 | 幀數 | 時長 |
|---|---|---:|---:|
| ① | 白閃 | 3 幀 | 0.05 s |
| ② | 發光線稿（反色） | 5 幀 | 0.08 s |
| ③ | 漫畫＋色散（RGB 分離） | 5 幀 | 0.08 s |
| ④ | 色調分離 | 4 幀 | 0.07 s |
| ⑤ | 白閃 | 2 幀 | 0.03 s |
| ⑥ | 3D 本體落定，**同一個姿勢** | — | — |
| | **合計** | **19 幀** | **0.3 s** |

### 提示詞公式（原片原文）

```text
闪白 → 发光线稿 → 闪切 2D 漫画 → 同一姿势落定
✔ 写「闪切」 ✖ 别写「变形」（会融化粘连）
剪辑：每种画面只留 2-5 帧
```

> ⚠️ **幀率換算**：原片是 60fps 素材（所以 3 幀＝0.05 秒、19 幀＝0.3 秒才對得上）。
> 換到 H3 的 24fps，同樣的**感知時長**只要約 7 幀：白閃 3 幀 ≈ 1–2 幀、漫畫＋色散 5 幀 ≈ 2 幀、色調分離 4 幀 ≈ 2 幀。
> **寫給模型的是秒數（`a third of a second`），不是幀數**——幀數留給剪輯。

**「同一姿勢落定」是這條路線的靈魂**：所有過渡層都是**同一個姿勢**的不同畫風，
模型才不會在風格跳轉時把人體融掉。這也是「✖ 別寫變形」的原因——`transform` / `morph` 會讓模型去做形體漸變，
得到一團黏在一起的東西；`flash cut` 是**切**，不是**變**。

### H3 的英文寫法

```text
[Shot 3] At 00:03.000, the shot flash-cuts through five layers inside a third of a second while
she holds exactly the same pose throughout: three frames of pure white, five frames of glowing
inverted line art, five frames of flat 2D comic art with RGB channel separation, four frames of
posterised duotone, two frames of pure white, then the fully rendered 3D figure settles back in
the identical pose without any morphing in between.
```

`flash-cuts`、`holds exactly the same pose`、`without any morphing in between` 三個詞一組，缺一個就可能融。

## 3. 路線 C（片段）：爆發前的 3 幀純白

原片在巨浪最高點用了一句：**「冲击帧再用一次：爆发前插 3 帧纯白」**。

```text
[Shot 7] At 00:06.200, three frames of pure white are cut in right before the wave breaks,
then the whole wall of water collapses forward.
```

這是**最便宜的一次衝擊幀**：只要 3 幀，插在「事件臨界點之前」，不需要新素材、不需要後製。
本 skill 的 3D CG 實測也支持——參考片全片零爆白，但會在接觸點前給極短的亮部跳變。

## 4. 次級特效四件套（原片原文）

衝擊幀只是「主特效」，原片要求同時寫主特效旁邊的**小東西**：

```text
① 光炮四周炸出一阵阵电，劈出大小不一的电弧
② 魔法阵前炸开一圈白色冲击波环往外扩
③ 光炮四周的空气被热浪扭曲
④ 碎水泥块、碎石和土尘往两边飞
```

對照本 skill 的力場四通道（`force-field.md`）：① 粒子 ② 空氣（波形）③ 空氣（折射）④ 物質。
**原片沒有寫「光」通道**——那是本 skill 補的（全域亮度與陰影聯動）。四件套＋光＝五通道，但一次最多開三個。

「**劈出大小不一的電弧**」這個細節值得抄：`arcs of different sizes and lengths`。同尺寸的電弧看起來像貼圖。

## 5. 時間膨脹法：要逐幀的 2 幀時，改要一串卡

### 問題

在同一段高速動作裡把整幀寫成黑白漫畫格並寫 `for two frames`，H3 給 **23 幀（958 ms）**，而且角色會整個消失（`impact-frame-and-shake.md` §1.1.1）。那一則是風格跳轉。同段圖形拍的減去式＋退出做得到（見 `SKILL.md`）。要鎖死 2 幀時，改要一串卡再剪。

### 解法：不要叫它給 2 幀，叫它給**多張卡**

| 你想要的成片 | 生成時怎麼寫 | 剪輯動作 |
|---|---|---|
| 2 幀（83 ms）單張閃 | 8 卡 / 1.2 s | 只留 1 張卡的 2 幀，其餘丟掉 |
| 6 幀（250 ms）三連閃 | 8 卡 / 1.2 s | 挑 3 張卡各留 2 幀 |
| 0.25 s 一整段快閃 | 8 卡 / 1.2 s | 整段 5 倍速 |
| 0.3 s 變身五層 | 五層序列寫成 1.5 s | 3–5 倍速壓回 0.3 s |

**核心：把「精度」換成「素材量」。** 生成端只負責「一張一張讀得出來」，剪輯端負責「幾幀」。

### 為什麼這比後製合成好

| 項目 | 後製合成（路線 C） | 時間膨脹（A/B） |
|---|---|---|
| 需要先有主片 | 是 | 否 |
| 風格一致性 | 要自己對齊（曾出現 PSNR 20 dB 的「重新渲染」） | 同一顆模型、同一段提示詞，天然一致 |
| 工時 | 三素材 + 合成腳本 | 剪一刀 |
| 精度 | 逐幀 | 卡級（3–4 幀） |

**結論：能用 A/B 就用 A/B；要「精確 2 幀」才動 C。**

## 6. 四個數量關係（直接查表）

| 名稱 | 數值 | 說明 |
|---|---|---|
| 1 幀 @24fps | 41.7 ms | H3 的時基 |
| 2 幀（標準衝擊幀） | 83 ms | 參考片 30fps 的 2 幀＝67 ms |
| 3 幀（爆白上限） | 125 ms | 再長就變燈光故障 |
| 8 卡 × 3–4 幀 | 1.0–1.33 s | 生成端要給的時間 |
| 5 倍速壓縮 | 1.2 s → 0.24 s | 剪輯端 |

## 7. 三條「剪輯規則」（原片交代的後半段）

1. **每種畫面只留 2–5 幀。** 超過就是「看著它變」，不是「打斷」。
2. **慢放放在動作之後。** 原片用 3–4 倍慢放做子彈時間（微距貼刀刃）；順序顛倒力量會被提前洩掉。
3. **一次爆發只用一次衝擊幀。** 原片在變身用一次、巨浪前用一次，中間隔了 30 秒。

## 8. 反模式

| ❌ | 為什麼失敗 | ✅ |
|---|---|---|
| `for two frames the panel goes black and white` | 模型給整段黑白鏡頭（實測 23 幀） | 寫成獨立 `[Shot N]`，1.2 秒多卡 |
| `transform into her powered form` | 形體漸變 → 融化黏連 | `flash-cuts through five layers in the same pose` |
| 只寫「八張閃爍」 | 模型給一團糊 | 每張寫底色＋內容 |
| 給 0.3 秒 | 八張擠成一屏 | 給 1.2 秒 |
| 八張同色系 | 被讀成一張長圖 | 洋紅／橙紅／黑白輪替 |
| 只寫主特效 | 沒有環境證據＝貼圖 | 加四件套（電弧／衝擊環／熱浪／碎石） |
