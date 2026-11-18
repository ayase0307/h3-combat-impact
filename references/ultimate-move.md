# 大招設計：不是「加特效」，是「改變勝負的那一下」

> 大招（必殺技／覺醒／領域展開）在提示詞裡最常壞成「角色站著發光，然後爆炸」。
> 原因是只寫了特效，沒有寫**賭注**、**代價**、**後果**。這份文件把它拆成五段可寫的結構。

## 1. 三個判準（缺一個就不是大招）

| 判準 | 問題 | 寫法 |
|---|---|---|
| 賭注 | 這一下沒打中會怎樣？ | 前面必須先讓他被打到牆上／刀被壓住／隊友倒下 |
| 代價 | 用了會失去什麼？ | 刀裂、手燒傷、燈全滅、雨被抽乾、體力見底（**看得見**的代價） |
| 後果 | 世界變成什麼樣？ | 牆倒、棍斷、地面留下環形水痕、對手跪地（**不可逆**） |

沒有這三個，特效再亮也只是「技能展示」。

## 2. 五段結構與時間預算

| 段 | 名稱 | 佔比（8 秒） | 畫面 | 相機 |
|---|---|---|---|---|
| 1 | 蓄 Charge | 30%（2.4s） | 靜、收、呼吸、光從傷口／武器長出來；環境先變（雨變慢、燈變暗） | 小幅慢推 |
| 2 | 起 Release | 15%（1.2s） | 一個動作跨越距離；殘影／消失／一步到位 | 甩鏡或跟拍，**不要**這時候切 |
| 3 | 中 Impact | 10%（0.8s） | 命中：白線、火花、卡片、爆白擇一；**這一鏡相機鎖死** | 鎖死 |
| 4 | 果 Aftermath | 30%（2.4s） | 衝擊波、雨環、碎片、對手飛出去；聲音先消失再爆 | 鎖死或極慢拉 |
| 5 | 收 Recover | 15%（1.2s） | 她喘、刀放下、代價出現（手抖、刀裂） | 慢拉遠 |

**鐵律：第 3 段（中）相機一定要鎖死。** 43% 的 3D CG 參考片在最大衝擊時相機不動；
衝擊感來自「特效把背景推開」，不是相機在抖。前後可以動，這一鏡要靜。

## 3. 三種原型（選一個，不要混）

### A · 一閃（斬）
- 一個動作、一條線、一次命中。
- 視覺：細白線 → 延遲火花 → 對手身上的線晚 2 幀才出現。
- 適合：刀劍、居合、速度型角色。
- 提示詞關鍵：`crosses the distance in one step`, `a thin white line`, `the cut lands a beat later`。

### B · 三連（連）
- 同一口氣三段命中（下盤→軀幹→肩），最後一下才爆。
- 視覺：三條線、三段延遲火花、第三下才給衝擊波。
- 適合：拳腳、雙刀、連段型角色。
- 提示詞關鍵：`three cuts land in a single motion`, `each cut leaves a thin white line and a delayed spark`。

### C · 領域（域）
- 先展開一個「場」：雨停、水面浮起、燈火倒流；場內規則改變。
- 視覺：一個球形／環形邊界，邊界內外物理不同（雨在內側靜止、外側照落）。
- 適合：法術、仙俠、Boss。
- 提示詞關鍵：`a ring of suspended raindrops`, `inside the ring the rain hangs still`。

## 4. 視覺調色盤（只准兩個色）

| 角色 | 主色 | 對比色 | 用途 |
|---|---|---|---|
| 劍客／速度 | 青白（teal-white） | 墨黑 | 電弧、刀光、殘影 |
| 火焰／狂暴 | 橙金 | 煙灰 | 火花、熱浪、餘燼 |
| 仙俠／領域 | 月白 | 硃紅 | 陣紋、符光、血 |

**不要三個色以上。** 主色給能量，對比色給材質（墨、煙、血），背景維持原本的冷暖。

## 5. 8 秒模板（官方骨架，可直接改）

```text
integrated_multimodal_description: 3D CG, cinematic. [Shot 1] <場景＋兩人狀態：她已經被打到牆上，刀在抖>. <蓄：她吸一口氣，雨在她周圍變慢並開始上浮；青白電弧從繃帶爬到刀身>. The camera pushes in with small amplitude at slow speed.
[Shot 2] At 00:02.400, <起：她一步跨過庭院，原地只留下一抹雨>. The camera whip-pans with her.
[Shot 3] At 00:03.600, <中：三刀同一口氣命中——前膝、肋骨、肩；每刀一條白線與延遲火花；鐵棍碎成三段>. The camera holds a static shot, low and close.
[Shot 4] At 00:04.400, <果：整幀變成手繪墨爆，黑墨在白底炸開，青白電弧穿過，她的剪影在中央>. 三幀後切回：衝擊波把懸浮的雨推成一圈，積水離地，他被掀飛. The camera is static and wide.
[Shot 5] At 00:06.400, <收：她落地，刀尖點水，手在抖，刀身有一道裂>. The camera pulls back slowly.
overall_soundscape: <蓄：雨聲變薄、耳鳴高頻；中：三聲鋼切＋鐵碎；果：先靜一拍，再一次低頻大鼓與水牆>
non_diegetic_music: <蓄：單一高音弦持續上升；果：大鼓一擊後低頻衰減>
```

## 6. 與其他模式的關係

- **六拍**：大招是「六拍的超級放大版」——蓄更長、停更短、洩更大。
- **ULTRA_SPEED**：不適合放大招（沒有停留空間）；大招一定需要一個「靜」的鏡頭。
- **連續對轟**：大招前一段用連續對轟把壓力堆滿，大招才有落差。

## 7. 常見失敗

| 症狀 | 根因 | 修法 |
|---|---|---|
| 站著發光 2 秒 | 只寫特效，沒寫動作 | 蓄段也要有一個小動作（收刀、吐氣、抬眼） |
| 爆炸很亮但沒感覺 | 相機在抖、沒有前後對比 | 中段鎖死；前面用推、後面用拉 |
| 對手消失 | 「她被光吞沒」這類寫法 | 寫對手的位置與反應（被掀飛、跪地、棍斷） |
| 代價不見 | 只寫威力 | 收段寫手抖、刀裂、喘、燈滅 |
| 三個顏色打架 | 主色＋對比色沒定 | 先定兩色，其餘用環境原色 |
| 卡片看不懂 | 卡片太多、每張 0.2 秒 | 4–6 張、每張 0.3–0.45 秒，出片後再剪快 |
| 招式沒有名字 | 模型不知道這是「同一招」 | 給招式名（中文＋英文），並在每段重述一次 |

## 8. 可重用片段（英文，直接貼）

**蓄**
```text
She plants her rear foot, exhales once, and the rain around her slows and begins to lift in threads; teal-white electric arcs crawl out of her forearm wraps and run along the blade.
```

**起**
```text
She crosses the distance in one step, leaving only a smear of rain where she stood.
```

**中（三連）**
```text
Three cuts land in a single motion — his front knee, his ribs, his shoulder; each cut leaves a thin white line and a delayed spark, and his iron staff shatters into three pieces.
```

**中（一閃）**
```text
One cut passes through him; for two frames nothing happens, then a thin white line opens across his chest and the spark arrives late.
```

**果**
```text
A ring of shockwave pushes the suspended rain outward, the puddles lift off the flagstones, and he is blown back off his feet.
```

**收**
```text
She lands, the blade tip touching the water, her hand shaking, a hairline crack running down the steel.
```

## 9. 驗收（生成後）

1. 不看特效，只看「誰贏了」——看不出來就是賭注沒寫。
2. 遮住畫面只聽聲音——有沒有「先靜一拍再爆」。
3. 逐幀看中段——相機有沒有動（動了就是失敗）。
4. 看收段——有沒有看得見的代價。
5. 量測：`measure_motion.py` 的峰值格應該落在中段，且末 2 秒不為 0（有餘波）。
