# 獨特機制異能 × 日系 Sakuga 分鏡庫（Unique Skills & Sakuga）

> **定位**：`character-signature-skill.md` 給你「技能母題的四節點」與「視覺語法四件」；本檔給你
> **Part A：16 組有機制的獨特能力**（拒絕無腦光球對轟）與 **Part B：14 組日系作畫（Sakuga）經典鏡頭鏈**。
> 兩者可疊用：**A 決定「這個能力怎麼改變戰場」，B 決定「這一拍怎麼被拍出來」。**
>
> 英文 H3 句庫規則與 `martial-arts-compendium.md` §0.1 完全相同（零否定詞、嚴禁直譯技能名／畫師術語、
> 單鏡空中轉體動詞 ≤ 3、水平位移寫離散步態、無停頓模式禁靜止詞）。

---

## 0. 讀前須知

### 0.1 能力型必過「六問」（缺一問就退化為光球對轟）

| # | 問題 | 寫法 |
|---|---|---|
| 1 | **能力從身體哪個部位／哪件物品出來？** | `from his fingertips` / `from the umbrella rib` |
| 2 | **能力的「形狀」是什麼？**（裂縫、線、荊棘、方塊、環） | 給名詞形狀，不給形容詞 |
| 3 | **它接觸到什麼？** | 柱子、腳踝、箭、刀鋒 |
| 4 | **對手的身體或兵器發生什麼具體變化？** | 雙膝陷入、袖口被勒緊、刀被彈回 |
| 5 | **環境留下什麼殘留？** | 裂縫、冰屑、碎片、塵幕 |
| 6 | **它如何影響下一拍？**（位移、高度、優勢轉換） | 因果鏈才算戰鬥 |

### 0.2 時間／色彩類能力與執行層對接

- **全場抽色灰階** → 執行層用 `h3_colour_drain`（時停或致命一擊前 `0.3s` 瞬切 `+4.0`，`interp: step`），為 `0.1–0.2s` 快切盤，只畫 `0.25–0.35s` 窄脈衝（見 `comfyui-dials-guide.md`）。
- **衝擊閃幀** → 用 `h3_impact_frame` 窄脈衝，或後製 `scripts/impact_frame.py`（路線 C）；**不要把「兩幀」直接寫進一個 shot 時長**（`impact-frame-inline.md` 實測：寫兩幀模型會給整段黑白鏡頭）。
- 這些盤須搭配 `"audio": "protect"`。`P5 / P6` 在 `fight-directing-contract.md` §7.4 明文禁止用於「直線毀滅大招與近身肉搏」；時停鏡若含近身肉搏或單向光束，同樣適用，建議改用 P7／P8。

### 0.3 來源與可信度

- **Part A（異能機制）**：由本技能作者依 `character-signature-skill.md` 的「四節點母題」與 `fight-directing-contract.md` 的「能力型六問」原則，歸納動漫常見的機制型能力類別（空間、影、線、重力、時間、物質變形等），再轉譯成 H3 可演的物理語言，**不採用任何作品專有名詞**。網路檢索只得到泛論（「能力要有清楚規則、外觀要讓人看懂它如何運作」），沒有逐能力的視覺拆解資料，因此各條目的 H3 句與導演提醒屬**導演化設計**，並非某部作品的還原。
- **Part B（作畫語法）**：鏡頭手法本身（魚眼拉遠、速度線追拍、插切、反相閃幀等）屬作畫社群通用語彙，畫師名**只作靈感索引**，不進任何英文 H3 句。

#### 作畫人名核驗表（2026-11-26 網路檢索結果）

| 人名 | 檢索到的公開資料 | 對應本檔 | 可信度 |
|---|---|---|---|
| 中村豐（Yutaka Nakamura） | Wikipedia：碎片動畫常呈立方體，故稱 **yutapon cubes**；描述其打戲為重擊感強、善用衝擊幀；Animetudes 文章指其常用一拍一／一拍二的高幀率，碎片受大塚康生影響並被稱 Nakamura debris | SK-01、SK-06 | 已核實（二手來源） |
| 吉成曜（Yoh Yoshinari） | Wikipedia／日文詞條：《天元突破》的「吉成爆發」爆炸特效、《FLCL》高難度動作；中文個人部落格另提關節運動強調與跟拍運鏡（非官方資料） | SK-01（爆炸形狀參考）、SK-05（跟拍） | 部分核實；「擠壓拉伸殘像」一說**未找到來源，已刪除對其的歸屬** |
| 沓名健一（Kenichi Kutsuna） | 文春採訪：以《鬼滅之刃 無限列車篇》為例，解說夜戰色彩少時，發光呼吸特效如何以作畫、攝影、3DCG 組合擴展色彩並製造視覺刺激的緩急 | A4 物質變形系（單一主色發光）、§0.1 | 部分核實（僅採訪，無作畫風格系統資料） |
| 竹內哲也 | 公開資料只有履歷（原畫參與多部作品、作畫監督），**沒有作畫風格描述** | 無 | 未核實，不作任何風格主張 |
| 伍柏諭 | 檢索**未找到任何相關資料** | 無 | 未核實，不引用 |

> 以上五人中，只有中村豐的「立方碎石」有明確公開依據；其餘人名請勿拿來當「某某式」的保證。

---

# Part A｜機制型獨特技能（16 組）

> 每組格式：機制 → H3 → 物理結果／殘留 → 戰術 → 導演提醒。
> 色彩建議：**一個能力一個主色**，與環境對立（`character-signature-skill.md` 視覺語法）。

## A1 空間系（3 組）

### US-01 空間折疊裂隙瞬身背刺

- **機制**：在身旁撕開一道豎直細縫 → 踏入 → 從對手背後的另一道細縫鑽出 → 刀已在前進 → 兩縫在身後閉合
- **H3**：`tears a thin vertical seam in the air beside her, steps into it and emerges through a matching seam behind her shoulder with the dagger already travelling forward, and both seams zip shut in a spray of pale glitter`
- **物理結果／殘留**：裂縫邊緣碎光、空氣被吸入時衣料朝裂縫飄動
- **戰術**：繞過正面防線，打盲區
- **導演**：入口與出口必須同一鏡可見（形成因果）；不得寫「消失」後鏡頭切走

### US-02 鏡面碎裂換位

- **機制**：對手的倒影在鏡中碎裂 → 鏡中人從鏡面走出到對手背後 → 本體散成碎片
- **H3**：`her reflection in the tall mirror cracks outward and a mirrored copy steps out of the glass behind the attacker, the original dissolving into glittering shards while the copy's palm drives into his spine`
- **物理結果／殘留**：玻璃碎片懸浮後落地、鏡框空洞
- **戰術**：換位誘敵、破對手鎖定
- **導演**：換位鏡之後的第一鏡要寫清「誰是本體」（防止雙胞胎錯亂）

### US-03 傳送門截斷投射物反還

- **機制**：胸前開一環光門吞掉箭 → 弓手頭側另開一環 → 同一支箭射出
- **H3**：`opens a ring of blue light in front of her chest so the incoming arrow vanishes into it, and a second ring flares open beside the archer's head, the same arrow bursting out of it at point-blank range`
- **物理結果／殘留**：光環邊緣火花、箭羽被氣流扯動
- **戰術**：把對手遠程攻擊還給他
- **導演**：兩個環必須同鏡可見或使用「正反打」兩鏡，並寫同一支箭的羽色

## A2 操控與束縛系（4 組）

### US-04 影縫潛行・黑影荊棘鎖踝

- **機制**：沒入柱影 → 沿地面像污漬般流動 → 對手身後影中長出帶刺黑藤鎖雙踝
- **H3**：`sinks into the pool of shadow beneath a pillar and flows across the floor as a dark stain, then lifts out behind him as black thorned vines erupt through the stone, wrapping both ankles and dragging him down`
- **物理結果／殘留**：石縫被撐裂、荊棘上有細小反光、地面一道墨痕
- **戰術**：束縛下盤、製造空檔
- **導演**：先寫影的位置才合理；對手腳踝被鎖必須在同鏡可見

### US-05 指尖隱形鋼絲：切裂石柱與牽引變向

- **機制**：指尖輕彈 → 一道極細反光線繃緊庭院 → 石柱被切成石板 → 身體沿線被拉向新角度
- **H3**：`flicks her fingers and an invisible filament snaps taut across the courtyard with a thin glint, shearing a stone pillar into slabs that crash down in a cloud of dust, then hauls her body sideways along the wire into a new angle of attack`
- **物理結果／殘留**：石粉切口平整、細線高光、落石
- **戰術**：用環境結構做路線改變
- **導演**：線只能「閃一下」，不要寫成滿畫面紅線

### US-06 重力倍增球壓塌地面

- **機制**：握拳收攏掌心上方的暗球 → 球下方重力場把地面壓成碗狀 → 對手雙膝陷落
- **H3**：`closes his fist around a dark sphere that swells above his opponent, the pressure crushing the flagstones into a bowl and forcing both of the opponent's knees into the rubble as dust is dragged downward`
- **物理結果／殘留**：地磚向內凹陷、塵土向下吸、衣料下垂
- **戰術**：壓制行動、為終結鋪路
- **導演**：塵土方向全部朝下，是重力能力的辨識特徵

### US-07 磁力牽引金屬

- **機制**：掌心向前攤開 → 對手劍與甲片被吸向掌心 → 飛來的金屬環繞成盾
- **H3**：`spreads his palm forward and the opponent's sword jerks out of her grip, the steel plates of her armour peeling off and flying toward his hand with a ringing clatter to circle him as a spinning shield, sparks jumping where the plates collide`
- **物理結果／殘留**：金屬鳴響、甲片碰撞火花、她的空手
- **戰術**：解除對手兵器、化為己用
- **導演**：先寫「她握著劍」再被奪，因果才完整

## A3 時間與感知系（3 組）

### US-08 時停領域・全場抽色＋懸浮雨滴被刀鋒切開

- **機制**：全畫面瞬間褪成灰階 → 雨滴懸停空中 → 他在雨滴間走過 → 刀鋒把一滴雨切成兩半 → 色彩倒灌、對手防線塌陷
- **H3**：`the whole courtyard drains to grey in one instant and every raindrop stays suspended in the air as he strides between them, his blade parting a single drop into two halves before the colour floods back and her guard collapses`
- **執行層**：首選 `h3_colour_drain +4.0`（`0.3s` 瞬切、`interp: step`）窄脈衝，作用在同一鏡內的抽色段，並加 `"audio": "protect"`；**不要把整鏡寫成灰階**。僅當走「提示詞內嵌衝擊幀」路線（`impact-frame-inline.md`）時，才把抽色寫成 ≥1.2 秒的獨立短鏡
- **物理結果／殘留**：雨滴切口、倒灌的色彩、防線崩塌
- **戰術**：以視覺奇觀終結
- **導演**：全場灰階只給一個「彩色」元素（刀光），否則畫面無焦點

### US-09 超加速領域

- **機制**：自身高速移動、周遭近乎靜止 → 在懸浮的碎屑與火星間穿行 → 一刀連斬三處
- **H3**：`the world around her drifts in slow motion as she runs through it at full speed, weaving between hanging sparks and falling leaves and cutting three times along a single line, the afterimage of each cut still glowing behind her`
- **物理結果／殘留**：三道刀痕同時綻開、火星懸浮、殘影
- **戰術**：以速度差壓制
- **導演**：與 US-08 的差別：此技仍有「自己在動」，所以不寫灰階，用殘影與慢速背景製造差距

### US-10 殘影分身左右夾擊／真身上空重劈

- **機制**：留下兩個半透明殘影左右衝擊 → 對手分神 → 真身從上方重劈
- **H3**：`splits into two translucent afterimages that rush in from the left and right while the real body vaults above, bringing the sword down onto his shoulders as his blade is still turning toward the decoys, the ground cracking under the impact and the afterimages bursting into points of light`
- **物理結果／殘留**：殘影在碰到對手時散成光點、重劈使地面龜裂
- **戰術**：虛實換位（`character-signature-skill.md` 母題 4 連閃殘影）
- **導演**：空中轉體動詞 0；真身落點要與殘影有明顯高度差

## A4 物質變形系（6 組）

### US-11 黑金流體覆臂凝重盾→硬接重斬→碎裂成飛刃反射

- **機制**：黑金液體包住右臂 → 凝固成厚重盾面 → 吃下重斬 → 盾碎成鋒利碎片向外飛射
- **H3**：`pours black-gold liquid over his right arm until it hardens into a thick shield and takes the heavy cut full on its face, then the shield shatters outward into blade-edged shards that fly back at his attacker`
- **物理結果／殘留**：液態金屬波紋、盾面裂紋、碎片嵌入牆
- **戰術**：以防禦轉攻擊（換手點）
- **導演**：必寫「盾面承受重斬」的接觸點與裂紋，不能只寫「變成盾」

### US-12 冰晶覆臂重盾→碎裂冰刃反射

- **機制**：霜紋沿手臂向外凝成白色冰盾 → 硬接劈斬 → 冰盾崩裂成尖銳冰錐反射
- **H3**：`spreads frost along his right forearm until it locks into a heavy ice shield, which cracks open under the downward chop and bursts into sharp icicles that spray back across her chest`
- **物理結果／殘留**：白霧、冰屑懸浮、碎冰反光
- **戰術**：與 US-11 並列，冷色版本
- **導演**：冰盾要寫厚度（`thick`），否則 H3 會畫成薄冰片

### US-13 砂鐵聚散化刃

- **機制**：灑出的砂鐵在空中聚成長刃 → 揮斬後散開 → 再聚為新形
- **H3**：`scatters a handful of iron sand that gathers mid-air into a long blade and cuts through the guard. The blade then breaks apart into a drifting cloud and reforms as a second blade at her back`
- **物理結果／殘留**：砂粒在空氣中的軌跡、切痕
- **戰術**：多方向切割，防守困難
- **導演**：形變不可超過三段，以保持清晰

### US-14 紙片聚散化刃

- **機制**：袖中放出紙片 → 紙片聚成刀刃 → 切開後散成紙雪
- **H3**：`shakes a stack of white paper strips from his sleeve and they whirl together into a blade that slashes across her sword, then scatter into drifting paper snow`
- **物理結果／殘留**：飄落紙雪、割痕邊緣的紙屑
- **戰術**：輕盈切割、遮擋視線
- **導演**：空中轉體動詞只用 `whirl` 一個，其餘用「聚、散、飄」

### US-15 音律空氣波紋可視化環狀切割

- **機制**：撥弦 → 空氣波紋化為可見環 → 環向外擴散切過石柱與對手
- **H3**：`plucks a string and a visible ring of rippling air spreads outward, slicing a clean circular groove through the pillar and shaking the dust off her shoulders as the ring passes through her`
- **物理結果／殘留**：石柱環狀斷面、塵埃被震落、衣料震顫
- **戰術**：範圍切割、無法閃避的廣域攻擊
- **導演**：環必須有「厚度與邊緣」，避免被畫成圓形光效

### US-16 符紙結界截斷→彈返

- **機制**：拋出符紙成陣 → 結界擋下火球 → 符紙反彈燃燒 → 火球折返
- **H3**：`flings a talisman strip that unfolds into a flat wall of glowing script in front of him, catching the fireball on its face and sending it rebounding into the caster with a flare of sparks`
- **物理結果／殘留**：符文逐字熄滅、火星彈回
- **戰術**：防禦反制
- **導演**：結界只出現在一鏡，後續鏡頭由符紙碎片和焦痕銜接

---

# Part B｜日系 Sakuga 經典動作分鏡鏈（14 組）

> 這一部直接升級導演分鏡感。每組格式：**鏡頭語法 → H3 → 時長建議 → 為什麼有效 → 不要這樣用**。
> 時長原則：**黃金攻防鏡長 2.2–2.8 秒**（`fight-directing-contract.md` §7.2）；特效插入鏡 1.0–1.5 秒。

### SK-01 幾何方塊碎石爆發（Cubic Debris Impact）

- **語法**：地面受擊 → 石板炸成「厚重幾何方塊」碎岩向四方飛出，每塊緩慢自轉
- **H3**：`the stone slab detonates into heavy geometric blocks of rock that tumble outward in a wide arc, each block turning slowly in the air with a thin trail of dust`
- **時長**：1.2–2.0 秒
- **為什麼有效**：方塊有明確體積與稜角，比「碎片」更有重量感；慢速自轉提供「爆炸前後」的時間層次
- **來源**：立方碎片爆破（社群稱 yutapon cubes，得名於中村豐；見 §0.3 核驗表）
- **禁忌**：方塊數量寫「約十餘塊」即可，過多會變成霧團；不要與全場煙塵同時給滿

### SK-02 極端廣角魚眼透視拳逼近鏡頭瞬間拉遠

- **語法**：廣角魚眼鏡頭，拳頭逼近鏡頭佔滿畫面 → 鏡頭快速拉遠，顯示全身與受擊者
- **H3**：`through a very wide fisheye lens her fist swells toward the camera until it fills the frame, then the lens snaps back to a medium wide shot as the punch lands on his jaw, his head whips sideways and a shock ring of dust bursts off the wall behind him`
- **時長**：1.2–1.6 秒
- **為什麼有效**：透視誇張強化衝擊，拉遠給出接觸結果
- **禁忌**：「拉遠」必須在拳接觸之後；寫成「拉遠後再出拳」會導致節奏顛倒

### SK-03 劍尖逼近鏡頭瞬間拉遠

- **語法**：劍尖指向鏡頭、鏡頭保持微距 → 劍尖穿過 → 鏡頭向後拉出，顯示對手側身閃過
- **H3**：`the sword point races toward the lens in extreme foreshortening, then the camera pulls back to show him twisting his torso sideways so the blade passes a thumb's width from his ribs, tearing his sleeve and throwing sparks off the pillar behind him`
- **時長**：1.4–2.0 秒
- **為什麼有效**：把「險些命中」轉成視覺高潮
- **禁忌**：`twisting` 算 1 個轉體動詞，勿與其他空中動作疊加

### SK-04 高速橫移流線背景追拍（Speed-Line Tracking Pan）

- **語法**：鏡頭與角色同速橫移，背景拉成水平速度線
- **H3**：`the camera tracks sideways at the same speed as the runner so the background streaks into long horizontal lines while the figure stays sharp, his coat snapping behind him with each stride and dust jumping from every footfall`
- **時長**：1.6–2.4 秒
- **為什麼有效**：角色清晰、背景模糊，提供速度而不依賴大位移
- **執行層**：奔跑追拍屬動態交鋒，用 `--burst`（正向運動軌）；**不要掛 `--anchor`**（anchor 只用於定樁、接地姿態與穩態特寫，見 `fight-directing-contract.md` §7.1、§7.4）
- **禁忌**：不要寫 `slides` / `skates`；步態仍須寫 `drives off / lunges / plants`

### SK-05 背動長鏡頭（貼背跟拍）

- **語法**：鏡頭貼背跟在角色後方，角色高速閃過落石、切入近戰
- **H3**：`the camera follows closely behind his shoulder as he weaves between falling boulders and cuts into the knot of enemies, each rock whipping past the lens before his sword flashes out ahead of him`
- **時長**：2.4–2.8 秒
- **為什麼有效**：把觀眾放到角色視角，近戰接觸成為「被帶入」的瞬間
- **禁忌**：單鏡接觸點 ≤ 2；超過會糊

### SK-06 2 幀黑白反相衝擊閃幀＋0.25 秒卡肉頓幀→遠景煙塵柱

- **語法**：接觸瞬間畫面黑白反相閃一下 → 動作短暫停頓（卡肉）→ 立刻切遠景，煙塵沖天
- **H3**：`on contact the frame flashes in inverted black and white for an instant and the impact lingers for a quarter of a second, then the shot cuts to a distant view as a tall column of smoke and dust rises from the point of impact`
- **時長**：1.2 秒（閃幀）＋ 1.5–2.0 秒（遠景）
- **執行層**：重擊瞬間打 `--hitstop`（`0.25s` 負向頓幀＋`+4.8` 衝擊閃幀，見 `fight-directing-contract.md` §7.4），閃幀用 `h3_impact_frame` 窄脈衝（`+4.6~+5.0`、`0.25–0.35s`），或後製 `scripts/impact_frame.py`；**「兩幀」不能寫進 shot 時長**，需當作窄脈衝或後製
- **為什麼有效**：反相閃幀＋停頓製造「命中重量」，遠景煙柱交代規模
- **禁忌**：無停頓模式下頓幀只能是「畫面持續晃動的卡肉」，不是人物靜止

### SK-07 兵器碰撞火花照亮冷峻雙眸微特寫插切（Cut-in）

- **語法**：刀劍相撞火花爆開 → 插切雙眼微特寫，火花光照亮眼眸
- **H3**：`as the blades crash together a burst of sparks lights up his narrowed eyes in a tight close-up, the orange glow flickering across his brow before the shot cuts back to the clashing steel`
- **時長**：0.8–1.2 秒（插切）
- **為什麼有效**：把「動作」與「表情」連接，在不拖慢節奏的情況下加入角色感
- **必配**：眼部寫肌肉動作（`facial-performance.md`）：眼瞼收緊、眉間壓低
- **禁忌**：不要連續使用兩次插切

### SK-08 受擊貼地犁出十米碎石溝渠雙足釘死煞停

- **語法**：受擊者被擊飛後雙腳落地，向後犁出長長的碎石溝渠，最後穩住
- **H3**：`struck by the blow, he lands on both boots and ploughs backward through the gravel, carving a long furrow ten metres long, his heels digging deeper until he stops with a plume of dust rolling off his shoulders`
- **時長**：1.8–2.4 秒
- **為什麼有效**：後退的距離就是力量的度量
- **禁忌**：此處屬「受擊被動位移」，可用 `ploughs`；**主動進攻位移仍不可用 slide / skid**

### SK-09 擠壓拉伸殘像拳（Smear Frame Fist）

- **語法**：拳頭在揮出途中被拉長成一道弧形殘像，接觸瞬間回復正常形狀
- **H3**：`her arm stretches into a blurred arc of motion as the punch whips forward, and snaps back to its normal shape at the instant the knuckles land on his cheek, whipping his head round in a burst of sweat spray`
- **時長**：0.8–1.2 秒
- **為什麼有效**：賦予日式作畫的誇張感
- **來源**：作畫社群通用的 smear（殘像拉伸）手法，未歸屬任何特定畫師（早先的畫師歸屬無來源，已移除）
- **禁忌**：只能用在「近戰拳腳」，不能用在長兵器

### SK-10 低角仰視巨大揮擊＋前景碎片遮擋視差

- **語法**：鏡頭貼地仰拍巨兵劈下，前景碎石高速劃過鏡頭
- **H3**：`from a low angle near the ground the camera looks up as the massive blade comes down, shards of broken stone whipping across the foreground and the figure's silhouette towering against the darkening sky`
- **時長**：1.6–2.4 秒
- **為什麼有效**：前景遮擋製造縱深；仰角製造重量
- **禁忌**：前景碎片只需要 3–5 個，避免遮掉角色

### SK-11 俯瞰 90° 環形衝擊波地面龜裂

- **語法**：兩股力量對撞 → 切 90° 俯瞰 → 衝擊波環形擴散、地面龜裂
- **H3**：`the shot cuts to a straight-down overhead view as the clash detonates, a ring of pressure racing outward across the flagstones and splitting them into a wide web of cracks`
- **時長**：1.2–1.6 秒
- **為什麼有效**：俯視讓圓環完整可讀（`character-signature-skill.md` 結構 3）
- **禁忌**：環只出現一次，後續用碎石持續運動接續

### SK-12 慢進快出時間重映射（Slow-in Fast-out）

- **語法**：蓄勢時碎片懸浮緩慢，斬擊瞬間加速到全速，餘波再慢下來
- **H3**：`splinters drift almost motionless in the air as he rises into the cut, then the blade whips through at full speed and the debris snaps outward before falling into a slow rain`
- **時長**：2.0–2.6 秒
- **為什麼有效**：用速度對比製造衝擊
- **禁忌**：無停頓模式下，慢速仍須有微動；`settling` 僅指碎片，不指人物

### SK-13 360° 環繞鏡（Orbit Cross）

- **語法**：鏡頭繞兩人刀鋒相交點旋轉，背景隨之滾動
- **H3**：`the camera arcs a full circle around the point where the two blades cross, the background wheeling past as sparks fly out in a widening spiral`
- **時長**：2.0–2.6 秒
- **為什麼有效**：把一次碰撞拍成多角度奇觀
- **禁忌**：環繞鏡只用於「雙方位置不變」的對撞，不用在位移大的追逐

### SK-14 景深切焦（Rack Focus）前景刀刃→背景敵人

- **語法**：前景刀鋒清晰、背景敵人模糊 → 焦點切到背景，敵人露出表情
- **H3**：`the focus shifts from the sharp edge of the blade in the foreground to the blurred enemy behind it, who sharpens into view with his jaw set and his eyes fixed on the steel, a spark drifting across the lens`
- **時長**：1.0–1.4 秒
- **為什麼有效**：快速建立「威脅—反應」的因果
- **禁忌**：不要用在連續動作中間（會破壞節奏）

---

## 組合配方

### B.1 一拍完整衝擊鏈（約 6 秒，3 鏡）

```text
[Shot 1] SK-02 魚眼拳逼近 → 拉遠（1.4 秒）
[Shot 2] SK-06 反相閃幀＋卡肉（1.2 秒，獨立鏡或後製）
[Shot 3] SK-08 受擊犁地 → SK-01 方塊碎石（2.4 秒）
```

### B.2 能力 × 鏡頭配對表

| 能力 | 最搭的 Sakuga 鏡 | 原因 |
|---|---|---|
| US-01 空間折疊 | SK-05 背動長鏡頭 | 鏡頭跟著背影鑽出裂縫 |
| US-06 重力球 | SK-11 俯瞰環波 | 地面凹陷最清楚 |
| US-08 時停領域 | SK-12 慢進快出 | 速度對比即時間概念 |
| US-11 流體重盾 | SK-07 插切 | 碎片火花照亮眼眸 |
| US-15 音波環切 | SK-13 環繞鏡 | 環形擴散適合圓周運鏡 |

### B.3 自檢清單

- [ ] 每句 H3 零否定詞、零招式名／畫師名
- [ ] 每個能力寫了「來源部位、形狀、接觸物、結果、殘留、下一拍」
- [ ] 單鏡空中轉體動詞 ≤ 3
- [ ] 閃幀／頓幀的「兩幀」未直接寫進 shot 時長
- [ ] 全篇主動進攻位移沒有 `slides / skids / glides`
- [ ] 含近身肉搏或單向光束的時停鏡沒有長開 `P5 / P6`
- [ ] 一個畫面只有一個主色

---

## 常見失敗

| 症狀 | 根因 | 修法 |
|---|---|---|
| 能力畫成通用光球 | 沒寫形狀與接觸物 | 回 §0.1 六問 |
| 時停鏡整段變黑白 | 把「抽色」當整鏡寫 | 同鏡內窄脈衝（`h3_colour_drain` 0.25–0.35s）；內嵌路線才用獨立短鏡 |
| 方塊碎石糊成煙霧 | 數量過多或同時給塵幕 | 方塊 10 餘塊＋薄塵尾 |
| 魚眼拳沒有拉遠 | 順序寫反 | 拳接觸後才拉遠 |
| 分身與本體難分 | 沒有高度差或色彩差 | 殘影半透明＋真身在上空 |
