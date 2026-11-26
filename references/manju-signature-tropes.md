# 華語武俠／修真仙俠／AI 漫劇王牌招式與大招參考庫（Manju Signature Tropes）

> **定位**：本檔是 `move-library.md`（通用招式）、`ultimate-move.md`（大招五段結構）、`force-field.md`（力場四通道）與 `fight-directing-contract.md`（導演合約）的**題材擴建庫**，專收「高觀賞性、高辨識度」的華語武俠、修真仙俠與 AI 漫劇爆款分鏡資產。
> 使用方式：先在第五篇挑一套 15 秒導演套餐，再回第一至第四篇替換單招；每一組都已拆成「位移與鏡頭／身體發力／力場四通道／戰術交換」四層，並附中文母稿句與可直接貼進 H3 的英文句。

---

## 0. 三條鐵律（本庫每一組都已遵守，改寫時請勿破壞）

1. **招式名絕不直譯進英文提示詞**。英文只寫「身體發力部位＋運動軌跡＋物質力場反應」；本庫英文句內沒有任何招式名、拼音或英譯招名。
2. **零否定詞**。英文句庫嚴禁 `no / not / never / without / instead of / rather than`，一律改寫為正面保持句，例如以 `keeps his boots planted firmly on the cracked stone` 取代「不滑動」。
3. **姿態—位移相容防滑律**。跪姿、蹲姿、盤坐、雙足釘樁開陣時，同句嚴禁描寫水平衝刺或平移；水平位移一律寫離散步態三拍（蹬離支點 → 跨步騰躍 → 前腳踩實沉腰）；全篇避免 `slides / skids / glides` 描寫攻擊位移。大招奇觀嚴禁背景正中央對稱圓輪（會退化成 2D 萬花筒），必須採**偏軸掃出**或**單向空間推進**，並在句中寫明方向（如「由左下往右上」）。

## 1. 每組欄位格式

```text
### 篇-號｜名稱
適用載體｜建議鏡長（相對鏡首秒數）｜推薦 Dials 策略
① 位移與鏡頭關係　② 身體發力機制（肩、胯、腕、足重心）
③ 力場四通道（空氣／物質／光影／粒子）　④ 戰術交換意義
中文導演母稿示範句
English H3 Action Snippet（```h3snippet 區塊，純淨具象英文，供腳本掃描）
```

- **建議鏡長**：沿用合約黃金鏡長 2.2–2.8 秒；開場鉤子可短至 1.2–1.8 秒。`Dials` 內的秒數皆為「該鏡鏡首起算」，貼入整片時請加上該鏡的片內起點。
- **Dials 速查**（細節見 `comfyui-dials-guide.md`）：`P7` 近戰通用、`P8` 定樁大招、`P9` 番劇刀劍雙色刀弧（須搭 `--hires-dials off`，嚴禁 `blur_hook ≤ -1.0`）。**P5／P6 不用於直線大招與近身戰**。`--anchor` 必與任何接地釘樁姿態成對；`--hitstop` 約 `0.25s`（`-1.2 ~ -1.8`）；`--burst` 只開在突進與破空段，並保持 $M_{\text{eff}} \le +0.98$。
- **徒手對兵刃**：合約僅在「導演明確設定」下允許。凡出現雙指夾刀、徒手破兵者，一律在「適用載體」欄標註「導演設定」並在英文寫出力的來源（如指尖氣鞘），不寫裸手硬接刃口。
- **能力型招式**（法相、墨獸、符鏈…）：英文必須點名能量從身體哪個部位或哪件兵器長出來；劍修的毀滅級大招維持劍招本質。

## 2. 資料來源與誠信說明

本庫為**導演原創的分鏡資產**，下列僅為有搜尋結果佐證、可被引用的觀察；其餘一律屬導演原創，不冒充任何作品的逐鏡拆解。

- 《劍來》第 6 集「阿良問劍」：開場以布衣竹刀揮出的墨色劍氣撞上山水正神的金色神甲，神甲如紙屑般散開（澎湃新聞報導）→ 啟發「水墨劍氣對撞金光」的第一、三篇資產。
- 《劍來》水墨基調（以水墨濃淡表現招式強弱，中國日報）、《滄元圖》水墨打戲（新浪）→ 啟發第三篇「水墨化獸」。
- 《鏢人》真人電影：實拍為主、兵器隨戰局切換、雙劍反派、水袖融入武打（新浪、網易）；《鏢人》動畫風格化的寫實拆招（影評觀察）→ 啟發第二篇兵刃與長袖資產。
- 《臥虎藏龍》竹林戲受胡金銓《俠女》竹林戲啟發、長袖捲劍屬「借用現成物」的武俠慣例（SCMP、ACMI）→ 啟發第二篇竹林折線與袖捲。
- AI 漫劇爆款結構：0–3 秒直接放衝突畫面、不交代背景；約每 20 秒一次情緒反轉；耳光聲、心跳、閃白轉場等抓耳音效（網易、新浪分鏡模板）→ 第一篇與第五篇節拍依據。
- 搜尋覆蓋說明：《霧山五行》《不良人》《凡人修仙傳》未搜到可引用的鏡頭級拆解，本庫**不**宣稱複刻其任何具體場面，僅沿用其公認的視覺氣質（水墨寫意、飛劍群、法相壓場）作為方向。

---

# 第一篇：AI 漫劇黃金前 3 秒開場鉤子與境界威壓（9 組）

> 結構依據：開場 0–3 秒直接放「衝突已發生」的畫面、不交代背景；鏡頭以**單一不可逆的境界差**說服觀眾「這人惹不起」。全篇以「小位移吃大動能」為母題，主角位移越小，威壓越大。

### 1-01｜雙指輕夾重劈刀鋒（氣浪向兩側劈開地面灰塵）
**適用載體**：徒手（**導演設定**：指尖覆一層青白氣鞘，夾持刀脊而非刃口）｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--anchor 0.0:1.0:-0.55｜--hitstop 1.0:1.25:-1.2`
- ① 位移與鏡頭：胸高正面雙人同框，敵方重刀由畫面右上斜劈向中線；主角腳下零位移，鏡頭緩推至刀脊與指尖的接觸點。
- ② 身體發力：右足碾實石板重心下沉，胯微坐鎖死骨盆，右肩下沉不聳，腕關節穩定，食中二指並攏夾住刀脊側面；持刀者肩與腕反被刀的反震頂得顫抖。
- ③ 力場：空氣——劈下的氣浪撞上指尖被分成兩股向左右噴開；物質——地面灰塵沿兩側呈扇形推開，主角衣襬與髮絲貼身後飄；光影——指尖氣鞘的一線冷光映亮刀脊，刃面反光被壓暗；粒子——刀脊上迸出細碎金屬屑。
- ④ 戰術交換：以最小位移吃掉一記重劈的全部動能，持刀方兵器被釘死，下一招被迫取消，觀眾一眼讀出境界差。

**中文導演母稿**：「重刀自右上劈落，青衫人立著不動，兩指一夾，刀鋒停在鼻前一寸；刀風被指尖劈成兩股，地上灰塵向左右炸開成扇，持刀壯漢雙臂劇顫。」

```h3snippet
The swordsman keeps his boots planted firmly on the cracked flagstones as the heavy broadsword chops down from the upper right, and he raises two fingers wrapped in a thin pale-blue sheath of qi to pinch the flat of the blade an inch from his nose; the shockwave of the blow splits around his fingertips into two streams that blow a fan of dust away to both sides, his sleeve and hair stream backward, and the attacker's shoulders and wrists tremble with the blade pinned in mid-air.
```

### 1-02｜一步踏碎石階威壓震退群敵
**適用載體**：徒手／刃器皆可（威壓型，不依賴武器）｜**建議鏡長**：2.2 秒｜**Dials**：`P7｜--hitstop 0.9:1.15:-1.2｜--burst 1.15:2.2:0.55`
- ① 位移與鏡頭：低位仰拍石階，主角自上階邁出一步，鏡頭隨右足下落微降；階下八名持械者呈放射狀被同步震退。
- ② 身體發力：後足蹬離支點，胯帶動前腿落步，右足整只踏實於石階邊緣，腰背挺直，肩平不晃，雙腕自然垂落，以「落足」而非「出手」製造重量。
- ③ 力場：空氣——落足瞬間一圈壓縮空氣向前下方推開；物質——石階由落足處放射狀裂開，階下群敵的衣襬與刀穗被向後吹平；光影——裂縫透出一線冷白色亮光，陰影向後甩開；粒子——碎石屑沿階面向下彈跳。
- ④ 戰術交換：不出一招就奪回場面主導權，群敵腳跟失衡後退，主角自然成為畫面唯一的前進方。

**中文導演母稿**：「他只往前踏了一步——整階青石應聲裂開，八名持械者像被無形的牆推著倒退，刀尖一齊垂向地面。」

```h3snippet
The swordsman drives off his rear boot, swings his hip through and stamps his right foot down onto the stone step with his whole weight, and the flagstone splits outward in a starburst of cracks; a pulse of compressed air pushes down the staircase, flattening the robes and sword tassels of the eight guards below who stumble back with their blade tips dropping toward the ground while gravel bounces down the steps.
```

### 1-03｜負手微側身貼臉讓過長槍突刺（髮絲飄起）
**適用載體**：徒手負手（長柄對徒手，靠切線閃避，不接鋒）｜**建議鏡長**：2.0 秒｜**Dials**：`P7｜--burst 0.0:1.0:0.5｜--anchor 1.0:2.0:-0.55`
- ① 位移與鏡頭：近景面部側面，長槍槍尖從畫面左側直線突入，鏡頭鎖在臉旁，槍桿掠過後鏡頭跟著槍桿方向微微拉出。
- ② 身體發力：右手負於腰後，左足向外跨半步並踩實，胯與肩同步向右微旋三十度讓出中線，頸部微偏，腕與雙手保持放鬆，眼神平視前方。
- ③ 力場：空氣——槍尖挾著線狀氣流擦過臉頰；物質——鬢髮與衣領被槍風掀起一束，槍纓貼著肩頭抖動；光影——槍尖寒光掠過眼角形成一道窄亮；粒子——塵屑沿槍桿向後拖成細線。
- ④ 戰術交換：以半寸之差避開直線突刺，把攻擊者推入「突刺用盡、回收未及」的破綻，下一鏡即可反制。

**中文導演母稿**：「槍尖直刺面門，他連手都沒從背後抽出，只是肩一偏，槍風掀起鬢髮，槍纓擦過頰邊，持槍者整個人被自己的衝勢帶了出去。」

```h3snippet
The long spear thrusts from the left straight at his face, and the swordsman keeps his right hand clasped behind his back, steps his left boot out and plants it firmly, then rotates his hip and shoulder a quarter turn so the spearhead passes a hair's breadth from his cheek; the wind of the thrust lifts a lock of his hair and ripples his collar while the red spear tassel flutters against his shoulder and the spearman stumbles forward on his own momentum.
```

### 1-04｜冷眸抬眼氣場炸裂震碎敵方飛劍
**適用載體**：能力型（氣場來源：全身真氣由胸口經雙眼外放，附著型場）｜**建議鏡長**：2.2 秒｜**Dials**：`P8｜--anchor 0.0:1.4:-0.55｜--hitstop 1.4:1.65:-1.2`
- ① 位移與鏡頭：正面眼部特寫拉開至胸上景；七柄飛劍從畫面兩側高速逼向臉部，抬眼瞬間同時炸成碎片，鏡頭鎖死。
- ② 身體發力：雙足分立踏實，胯沉穩，肩胛微收把胸口撐開，頸部上抬，腕自然垂於身側；僅以眼瞼上抬與下頜微收提供動作的「發力點」。
- ③ 力場：空氣——以雙眼為源的氣壓環向外推開，飛劍前方的空氣呈層狀壓縮；物質——飛劍劍身在氣壓前瞬間龜裂成碎片，髮絲與衣袖向後倒飛；光影——眼底一閃冷青色亮光，整個場景光線隨之瞬間偏冷；粒子——劍屑與灰塵被氣壓向外拋成長弧。
- ④ 戰術交換：沒有出手就化解遠程群攻，證明境界碾壓；對手失去兵器後陷入慌亂。

**中文導演母稿**：「七劍齊至，他緩緩抬眼——只此一瞬，眼底冷光一閃，七柄飛劍在離眉心三尺處同時碎成漫天銀屑。」

```h3snippet
The swordsman plants both boots wide on the stone, draws his shoulder blades together and lifts his gaze slowly; a pale-blue pulse of qi leaves his eyes and rolls outward as layered sheets of compressed air, and the seven flying swords racing at his face crack across their blades and burst into silver fragments a few feet before his brow, while his hair and sleeves whip backward and the surrounding light turns cold blue in the same beat.
```

### 1-05｜單手按住對手頭頂砸入青磚
**適用載體**：徒手（擒拿＋重砸）｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--burst 0.0:0.9:0.6｜--hitstop 0.9:1.15:-1.8`
- ① 位移與鏡頭：腰上雙人近景，敵人撲來；主角左手探出扣住其頭頂，鏡頭追著手臂方向由平視壓成俯視，對手面部被向下砸入地磚後定機。
- ② 身體發力：右足蹬離支點、左足跨步踩實，胯下沉帶動腰背把整條左臂當作重錘，肩壓住對手頭頂，腕根扣緊髮髻，砸落時全身重量隨著下沉。
- ③ 力場：空氣——砸落瞬間一圈壓縮氣浪沿地面向四周掃出；物質——青磚由接觸點裂成蛛網並下陷，周邊磚塊翹起；光影——塵爆形成短暫亮灰色遮罩，陰影猛然收縮；粒子——碎磚屑隨氣浪向外彈射。
- ④ 戰術交換：以單手結束近戰，同時製造不可逆的環境損壞（磚坑），讓之後所有人踩在坑邊都有心理壓力。

**中文導演母稿**：「對手撲來，他左手如鐵鉗按住頭頂，腰一沉，整個人被連著按進青磚——磚面蛛網般裂開，四周碎屑被氣浪掃成一圈塵環。」

```h3snippet
The swordsman drives off his right boot, steps his left foot down firmly beside the lunging attacker, sinks his hip and clamps his left hand over the man's crown; his shoulder and wrist drive straight down and slam the attacker's head into the blue brick floor, the bricks splitting into a spiderweb of cracks around the dent while a pulse of air sweeps dust and brick chips outward across the ground.
```

### 1-06｜拂袖拍開圍攻者並向外推開人牆
**適用載體**：長袖（布帛武器，附著型氣場）｜**建議鏡長**：2.2 秒｜**Dials**：`P7｜--burst 0.0:0.8:0.6｜--hitstop 0.8:1.05:-1.2`
- ① 位移與鏡頭：腰上正面，六人由三面圍攏；主角左臂橫掃一道大弧，鏡頭沿袖口軌跡平移半圈，人牆被向外推成一個缺口。
- ② 身體發力：右足蹬實，胯帶動腰旋，肩帶動左臂外展，腕一抖把長袖抖成一道硬弧；袖緣擦過第一人胸口時，足底重心前移半步壓上去。
- ③ 力場：空氣——袖緣掃出一道可見的白色氣弧，空氣在其前方被壓縮成層；物質——被掃中的六人衣襟向外翻飛，倒退時鞋底在石板上帶起灰痕；光影——袖面反射冷光劃過鏡頭；粒子——袖緣掀起的細塵沿弧線拖尾。
- ④ 戰術交換：以柔制群，單一動作清出一條前進通道，把「被圍」翻成「掌控圈」。

**中文導演母稿**：「六人三面圍上，他左袖一拂，白色袖浪像一堵牆橫掃而過，六人被齊刷刷推出五步，中間空出一條筆直的路。」

```h3snippet
Surrounded by six attackers, the swordsman plants his right boot, spins his hip and swings his left arm in a wide outward arc, snapping his wrist so the long white sleeve cracks into a taut curve; the sleeve edge pushes a visible arc of compressed air ahead of it, the six attackers' robes flare outward as they stumble back with their soles scraping grey streaks on the flagstones, and a lane of open ground appears in front of him.
```

### 1-07｜單足踩住飛劍劍脊壓入石中
**適用載體**：徒手（足技，對遠程兵器的以足制劍）｜**建議鏡長**：2.2 秒｜**Dials**：`P7｜--hitstop 0.9:1.15:-1.2｜--anchor 1.15:2.2:-0.55`
- ① 位移與鏡頭：低位地面視角，一柄飛劍貼地刺來；主角右足抬起踩落在劍脊上，鏡頭上搖至其立定的全身。
- ② 身體發力：左足支撐，胯微旋讓出角度，右足以足弓內側踏住劍脊（而非劍刃），膝下壓、足掌下蹬，肩與腕自然垂於身側保持平衡。
- ③ 力場：空氣——劍尖急停帶出一圈向前的氣浪；物質——劍脊被踩出一個凹陷，劍身彎出弧度並抖動，石板被壓出裂縫；光影——劍刃寒光被足背遮住，亮度驟降；粒子——火星與碎石屑從足底四散。
- ④ 戰術交換：以最小動作令對手的飛劍失效，並用一個「腳踩兵器」的畫面讓對手失面子。

**中文導演母稿**：「飛劍貼地射來，他右足輕輕一抬、一落，劍脊被他整個踩進石縫，劍身彎成弓形，嗡嗡作響卻再也飛不起來。」

```h3snippet
A flying sword skims toward him along the ground, and the swordsman balances on his left leg, turns his hip and brings the arch of his right foot down onto the spine of the blade, pressing it into the flagstone; the sword bows into a curve and hums, the stone cracks in a web around his heel, and sparks and gravel scatter from beneath his sole while a ring of air pushes forward from the stalled sword tip.
```

### 1-08｜兩指彈劍尖反震持劍者
**適用載體**：徒手（**導演設定**：指尖覆氣鞘，彈擊劍身側面）｜**建議鏡長**：2.0 秒｜**Dials**：`P7｜--hitstop 0.8:1.05:-1.2｜--burst 1.05:2.0:0.5`
- ① 位移與鏡頭：胸高雙人近景，敵人長劍直刺主角胸口；鏡頭推至劍尖與指尖相觸一瞬，劍柄端的持劍者受反震後仰。
- ② 身體發力：右足踩實，胯微旋讓劍尖偏離中線，肩放鬆，腕一彈、指節以氣鞘為甲彈在劍身側面，把力沿劍身傳回持劍者的肩與腕。
- ③ 力場：空氣——彈擊點爆出一圈短促氣環，沿劍身往持劍者方向傳遞；物質——劍身出現一圈細微共振紋，持劍者袖口與衣襟被衝撞波掀開；光影——彈擊點閃過一點白光；粒子——劍身上的灰塵被震成一圈微塵環後飛散。
- ④ 戰術交換：用「彈」代替「擋」，把攻擊者的力量原路送回，使其連人帶劍被震退。

**中文導演母稿**：「劍尖刺來，他指尖一彈，一聲清脆的鳴響沿劍身傳回去——持劍者虎口迸裂，長劍脫手，人倒飛三步。」

```h3snippet
The long sword thrusts at his chest, and the swordsman rotates his hip a few degrees, plants his right boot and flicks his fingertips, sheathed in a thin film of qi, against the flat of the blade; a short ring of shockwave runs back along the steel into the swordsman's shoulder and wrist, tiny ripples shiver across the blade, the attacker's sleeve whips open, and the sword leaps out of his grip as he reels backward.
```

### 1-09｜收刀入鞘一聲眾人倒伏（延遲爆發）
**適用載體**：刃器（居合型，延遲斬擊）｜**建議鏡長**：2.6 秒｜**Dials**：`P8｜--anchor 0.0:1.2:-0.55｜--hitstop 1.2:1.45:-1.2`
- ① 位移與鏡頭：低位廣角，刀客背對群敵，右手緩緩推刀入鞘；鏡頭鎖死，鞘口合上的清脆一聲後，身後群敵才同時倒下。
- ② 身體發力：雙足分立踏實，胯沉穩，左肩略前、右肩後收，右腕穩推刀身入鞘，左手拇指頂住鍔口，足底重心不動，所有動態交給延遲反應。
- ③ 力場：空氣——鞘口合上時一圈薄薄的氣環向身後擴開；物質——群敵胸前衣襟在一拍後同時裂開一道橫線，兵器脫手落地；光影——鞘口金屬閃過一線亮光，身後陰影隨之搖晃；粒子——地面塵土在群敵倒下時被衝起一層低霧。
- ④ 戰術交換：以「已經結束」的方式開場，把懸念換成結果，是 0–3 秒鉤子最強的「先給結果」寫法。

**中文導演母稿**：「他背對眾人，刀緩緩入鞘——『嗒』的一聲，鞘口合攏。身後二十人胸前同時裂開一道細線，兵器落地，無一人還站得住。」

```h3snippet
The swordsman stands with both boots set wide and planted on the stone, his back to the crowd, and his right wrist pushes the long blade smoothly home into its scabbard while his left thumb presses the guard; as the scabbard mouth snaps shut a thin ring of air spreads out behind him, a beat later a single horizontal line opens across the chest of every attacker, their weapons drop to the floor, and a low layer of dust lifts off the ground as they collapse.
```

---

# 第二篇：華語武俠經典兵刃與身法奇招（11 組）

> 本篇資產追求「一眼看得出是哪種兵器、哪條身法」。凡位移一律寫離散步態三拍；凡兵刃對兵刃，注意 180 度軸線與雙色刀弧（P9 路線）讓刀路在 24fps 下仍可讀。

### 2-01｜貼地拖刀火花撩斬
**適用載體**：刃器（長刀）｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--burst 0.0:1.0:0.65｜--hitstop 1.0:1.25:-1.2`
- ① 位移與鏡頭：腰上雙人近景略低機位，刀客刀尖拖在石板上帶出火花線，三步逼近後由下往上撩斬；鏡頭隨刀尖軌跡由地面緩緩上搖至敵人胸口高度。
- ② 身體發力：右足蹬離支點、左足跨步、右足再踩實沉腰（三拍）；胯帶動腰旋，肩與腕在最後一步才解鎖，右腕反翻把刀從下往上撩出，前期以低重心壓住上身。
- ③ 力場：空氣——撩起時刀身前方壓出一道上揚的氣弧；物質——被刀尖犁過的石板留下一條淺溝與細屑，敵人護胸的衣襟被刀風掀開；光影——火花線與刃面反光把刀路畫成一道由低到高的亮弧；粒子——火星沿刀路向後拉成長線。
- ④ 戰術交換：以「拖」建立壓迫距離與蓄力，再以由下往上的路線打穿對手的中下段防守。

**中文導演母稿**：「刀尖在青石上拖出一串火花，三步之後驟然上撩，火線從地面劃到敵人胸前，對手雙臂被撩得向上彈開。」

```h3snippet
The swordsman drags the tip of his long blade along the flagstones in a line of orange sparks, drives off his right boot, strides across with his left and plants his right boot firmly with his hips sinking, then flips his wrist and rips the blade upward from below; the sparks streak into a rising arc behind the edge, a shallow groove and gravel trail mark the stone where the tip ran, and the guard's raised forearms are thrown open as the blade passes his chest.
```

### 2-02｜借刃踏劍騰空翻越
**適用載體**：刃器對刃器（借敵兵器為跳板）｜**建議鏡長**：2.4 秒｜**Dials**：`P9（+ --hires-dials off）｜--hitstop 1.1:1.35:-1.2`
- ① 位移與鏡頭：正側面兩人對峙，敵人長劍橫掃腰際；主角足尖點上劍面騰空，從敵人頭頂翻越，鏡頭上搖追著雙足，落地後換到敵背視角。
- ② 身體發力：後足蹬離支點、前足足尖輕點在劍身側面作為轉換，胯帶動身體倒轉，肩與腕收緊把劍護於胸前，落地時雙足先後踩實並沉腰。
- ③ 力場：空氣——劍橫掃的氣流被足底踩斷、向上翻起；物質——敵人的衣襬與鬢髮被翻越時的風撩起，足尖點過之處劍身下彎；光影——紅色與冰藍刀光在翻越瞬間交疊成十字；粒子——塵屑被足尖帶起一小串。
- ④ 戰術交換：把「被橫掃」翻成「借力過頂」，同時完成換位，直接送入對手後背。

**中文導演母稿**：「長劍橫掃腰間，他足尖在劍面上輕輕一點，人如燕子從對手頭頂翻過，落地時劍尖已指向對手的後頸。」

```h3snippet
The opponent's long sword sweeps across waist height, and the swordsman drives off his rear boot and taps the toe of his front boot on the flat of the passing blade, tucks his chest and vaults over the man's head in a tight somersault with his sword held close to his chest; the blade dips under his toe and crimson and ice-blue blade-light arcs cross in an X beneath him, then he lands on one boot and the other in turn behind the opponent, sinking into his hips with the point of his sword aimed at the man's nape.
```

### 2-03｜竹林蹬踏折線變向斬
**適用載體**：刃器（長劍）｜**建議鏡長**：2.6 秒｜**Dials**：`P9（+ --hires-dials off）｜--hitstop 1.8:2.05:-1.2`
- ① 位移與鏡頭：低機位仰拍竹林，劍客以三次折線蹬踏上升再下切；鏡頭鎖定一側不跟隨，讓折線軌跡自己畫在畫面裡。
- ② 身體發力：右足蹬住竹幹借反作用力、胯帶動身體轉向，左足蹬另一根竹幹折向，肩與腕在最後一次折向時才亮劍，從上往下斬；每一次蹬踏都以足跟與膝完成吃力與轉向。
- ③ 力場：空氣——每次蹬踏後留下一條向後的氣痕；物質——被蹬的竹幹彎曲彈回，竹葉大片震落；光影——綠色竹影被劍光劃出一道冷白斜線；粒子——竹屑與葉片沿折線拖成一串。
- ④ 戰術交換：在垂直障礙之間製造不可預測的軌跡，使對手的視線與格擋預判全部落空。

**中文導演母稿**：「他一蹬竹幹，人斜飛向左；再一蹬，折向右上；第三蹬已經在對手頭頂，一劍自上而下斬落，竹葉落了一地。」

```h3snippet
The swordsman kicks off a bamboo trunk with his right heel so the stalk bends and snaps back, his hip turns him left, he kicks the next trunk with his left foot to cut sharply up and to the right, and on the third kick he arrives above the opponent and brings the long sword down from overhead; green leaves rain from the shaking stalks, each kick leaves a streak of torn bark and fibres in the air, and a pale blade-light slash cuts diagonally across the dark bamboo shadows.
```

### 2-04｜殘壁石柱折線借力下劈
**適用載體**：刃器（單手劍）｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--burst 0.0:1.2:0.6｜--hitstop 1.2:1.45:-1.2`
- ① 位移與鏡頭：胸高平視的廢墟，兩根石柱前後錯開；劍客蹬柱 A 反彈到柱 B、再從柱 B 下劈；鏡頭保持在敵人肩後，避免追拍造成滑行錯覺。
- ② 身體發力：右足蹬離柱 A、胯扭轉身體、左足踩住柱 B 蹲伏一瞬後蹬出，肩與腕在落劈時才解鎖，重心集中在落點前腳的足底。
- ③ 力場：空氣——蹬出時石柱前方的空氣被壓成兩次短促的波；物質——柱面被蹬出放射裂紋並掉下石屑，敵人被劈中時肩頭凹陷；光影——劍光劃過時把柱影斜斜撕開；粒子——石粉沿折線懸浮成兩段雲。
- ④ 戰術交換：用環境結構製造「來自兩個不同方向」的攻擊，使單一防守姿勢無法覆蓋。

**中文導演母稿**：「他蹬左柱、折向右柱、再自右柱頂端騰起——劍光從敵人意想不到的上方劈落，兩根石柱留下兩個裂開的腳印。」

```h3snippet
The swordsman drives off the first stone pillar with his right boot so the stone cracks, swings his hip to turn in mid-air and plants his left foot against the second pillar, then kicks off it and cuts straight down at the enemy's shoulder with his single-handed sword; stone chips fall from both pillars, the air bursts in two short pulses where he pushed off, and the blade-light tears a slanting line through the pillar shadows as the enemy's shoulder caves in.
```

### 2-05｜摺扇點腕鎖喉卸兵
**適用載體**：鈍短兵（鐵骨摺扇）＋徒手近身擒拿｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--hitstop 0.9:1.15:-1.2｜--anchor 1.5:2.4:-0.55`
- ① 位移與鏡頭：腰上雙人貼身，敵人短刀刺向腹部；主角摺扇點在其手腕，刀落地，扇尖接著頂住喉結，鏡頭由手腕搖到喉部。
- ② 身體發力：左足踩實、右足斜跨半步，胯旋讓過刀尖，肩下沉，腕一翻用扇骨敲在敵腕內側麻筋位，再把扇骨平推抵住喉部。
- ③ 力場：空氣——敲擊時一小圈氣環；物質——敵人手指鬆開，短刀自指間滑落到磚面反彈，衣襟被撞擊波掀起；光影——扇面金屬骨在敲擊時閃一道白線；粒子——細屑自手腕彈起。
- ④ 戰術交換：以扇子完成「卸兵＋鎖喉」兩個目標，場面由「被刺」翻成「被制」，爽點是反差。

**中文導演母稿**：「短刀刺向腹部，他的摺扇輕輕一敲手腕，刀噹啷落地，扇尖已抵在對手喉結上。」

```h3snippet
The attacker's short knife stabs toward his stomach, and the swordsman steps his right foot out at an angle, turns his hip so the point passes his ribs and snaps his wrist to rap the iron ribs of a closed folding fan against the inside of the attacker's wrist; the fingers spring open, the knife drops and bounces on the bricks, and the fan tip presses flat against the man's throat while a small ring of air puffs outward from the contact.
```

### 2-06｜長袖捲刃借力反甩
**適用載體**：長袖（布帛武器，戲曲水袖化用）｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--burst 0.0:0.9:0.6｜--hitstop 0.9:1.15:-1.2`
- ① 位移與鏡頭：腰上雙人，敵刀由上劈下；主角右袖迎上去繞住刀身，鏡頭沿袖浪軌跡半圈，下一幀袖子把刀甩向對手身側。
- ② 身體發力：左足蹬離支點、右足跨步踩實，胯旋帶動腰與肩，腕一抖把長袖抖成一道弧，在刀身上繞一圈後以肩帶臂向外一拉，力量從足底經胯傳到袖端。
- ③ 力場：空氣——袖浪在刀身周圍形成一圈卷動氣流；物質——白色袖面纏緊刀身一圈、刀被拽離原線，敵人身體前傾；光影——袖緣與刃面反光交錯；粒子——袖上細絲與灰塵被捲成螺旋。
- ④ 戰術交換：以柔化剛，用對手的力量反甩其兵器，並讓敵人被自己的重刀帶得失去平衡。

**中文導演母稿**：「重刀劈落，長袖像白蛇繞上刀身，他手腕一抖，袖子一拉，刀勢被帶偏三尺，持刀人整個身子被刀拖得向前撲去。」

```h3snippet
The enemy's heavy blade chops down from overhead, and the swordsman drives off his left boot, steps his right foot down hard, spins his hip and snaps his wrist so the long white sleeve whips around the blade in a full coil; he pulls his shoulder back and the sleeve drags the blade off line while the sleeve fibres and dust spin into a spiral around the steel, and the enemy is hauled forward by the weight of his own weapon.
```

### 2-07｜雙刀交叉剪殺破甲
**適用載體**：刃器（雙刀）｜**建議鏡長**：2.4 秒｜**Dials**：`P9（+ --hires-dials off）｜--hitstop 1.1:1.35:-1.2`
- ① 位移與鏡頭：胸以上正面對撞，敵人披重甲持盾；雙刀由左右兩側交叉切入甲縫，鏡頭鎖在甲片接縫處，剪合瞬間定機。
- ② 身體發力：左足蹬離、右足踏實沉腰，胯向前傾，雙肩同時下沉，兩腕反向一絞，讓兩刀像剪刀般在敵人頸側與腋下的甲縫交會。
- ③ 力場：空氣——兩刀交會時擠出一道尖銳氣流；物質——甲片接縫崩斷，鉚釘飛散，護肩翹起；光影——紅藍雙色刀光在交會點爆成一個白點；粒子——金屬屑與火星呈 X 形噴出。
- ④ 戰術交換：避開正面硬碰，以雙刀製造兩個同步剪力撕開防禦，是「破甲」的標準答案。

**中文導演母稿**：「重甲兵橫盾而立，雙刀自兩側交叉絞入甲縫——『喀』的一聲，護肩甲片崩開，鉚釘飛濺。」

```h3snippet
Facing the armoured guard, the swordsman drives off his left boot, sets his right foot down firmly, sinks his hips and sweeps both blades in from the left and right to cross like a pair of shears at the seam between the guard's shoulder plate and breastplate; crimson and ice-blue blade-light collide into a white point, rivets burst off the armour, and sparks and steel shavings spray outward in an X shape as the plate peels open.
```

### 2-08｜劍鞘格擋連帶拔劍寸斬
**適用載體**：刃器（居合＋鞘術）｜**建議鏡長**：2.4 秒｜**Dials**：`P9（+ --hires-dials off）｜--hitstop 0.8:1.05:-1.2`
- ① 位移與鏡頭：腰上平視，敵劍橫斬；主角左手連鞘上舉格開，劍鞘擋住劍身後右手拔劍從鞘口寸斬，鏡頭鎖死拍清「擋→拔→斬」。
- ② 身體發力：左足踩實、右足斜跨半步，胯旋帶動左肩上提，左腕把鞘推向來劍，右腕同時反握劍柄，劍出鞘半寸即以腰勁劃出一道寸距短斬。
- ③ 力場：空氣——鞘與劍相擊的一圈震波；物質——敵人的劍被鞘磕偏，衣襟被短斬劃開一道線；光影——拔劍瞬間一線寒光從鞘口閃出；粒子——鞘面漆屑與火星迸開。
- ④ 戰術交換：把「防守」與「進攻」折成同一個動作，節省一拍，使反擊快於對手的下一招。

**中文導演母稿**：「敵劍橫斬，他不拔劍，只用連鞘一擋；一聲脆響，劍已出鞘半寸，寒光一閃，對手衣襟裂開一道細口。」

```h3snippet
The enemy's sword cuts across at waist height, and the swordsman steps his right foot out at an angle, raises his left shoulder and uses his left wrist to push the scabbard up into the oncoming steel; the clash sends a ring of shock outward and knocks the enemy's sword off line, and in the same beat his right wrist draws the blade half an inch out of the scabbard for a short cut that opens a thin line across the enemy's robe, with lacquer chips and sparks flying from the scabbard.
```

### 2-09｜腳尖挑起地上兵器接住反刺
**適用載體**：長槍（足技取械＋槍術）｜**建議鏡長**：2.2 秒｜**Dials**：`P7｜--burst 0.0:0.9:0.6｜--hitstop 1.4:1.65:-1.2`
- ① 位移與鏡頭：低位平視，主角兵器被打落在地；他一腳踩住槍尾，另一腳尖挑起槍桿，右手在空中接住並反手突刺，鏡頭由地面順著槍桿上搖到突刺。
- ② 身體發力：左足踩實支撐，右足尖勾住槍桿下沿，胯與膝帶動一挑，肩帶臂前探，腕握住槍桿的瞬間五指發力，突刺時重心前移到左足。
- ③ 力場：空氣——槍桿被挑起時掃出一道上揚氣流；物質——槍纓揚起，石板上留下槍尾的刮痕；光影——槍尖寒光自下往上掃過鏡頭；粒子——地面灰塵被槍桿帶起一條線。
- ④ 戰術交換：從「被繳械」到「兵器回手」只用一拍，使敵人誤以為勝利後被直接反殺。

**中文導演母稿**：「長槍被打落在地，他腳尖一挑，槍桿翻起，穩穩落進掌心，下一瞬槍尖已經刺到對手胸前。」

```h3snippet
His spear lies on the ground, and the swordsman plants his left boot, hooks the toe of his right foot under the shaft, snaps his knee and hip upward to flip the spear into the air and catches it in his right hand, then shifts his weight onto his left foot and thrusts the point straight at the enemy's chest; the red tassel flares upward, the spear tail scrapes a pale line in the stone, and a thin trail of dust follows the shaft as it rises.
```

### 2-10｜傘面旋擋反彈暗器（靈巧傘修）
**適用載體**：傘（防禦兼反擊的複合兵器）｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--burst 0.0:1.0:0.6｜--hitstop 1.0:1.25:-1.2`
- ① 位移與鏡頭：腰上平視，十餘枚暗器自畫面左側成扇形襲來；撐傘者旋傘擋住，傘面把暗器彈回敵方，鏡頭鎖在傘沿看暗器回彈。
- ② 身體發力：右足踩實，胯旋帶傘柄轉動，肩與腕同步畫圓，傘面傾斜成斜面，把暗器的動量沿傘面反送回去；落步時左足跟進踩實以穩定身體。
- ③ 力場：空氣——傘面旋轉掀起一圈氣旋；物質——暗器撞上傘面後以相同速度彈回，傘骨顫動，傘面的雨水甩成一道水扇；光影——雨水與金屬暗器反光交織；粒子——水珠沿傘沿呈切線飛出。
- ④ 戰術交換：持兵器靈巧、不硬接，把遠程壓制翻成反向壓制，對應「重刃狂戰 vs 靈巧傘修」第五篇套餐。

**中文導演母稿**：「暗器如雨從左側射來，他旋傘一擋——叮叮叮連響，十餘枚暗器被傘面反彈，原路飛回，釘進對手腳邊的石板。」

```h3snippet
A fan of throwing darts flies in from the left, and the umbrella fighter plants his right boot, turns his hip and rotates the paper umbrella at a slant so the darts strike its canopy and ricochet back along their original paths; the ribs of the umbrella tremble, rain water flings off the rim in a bright sheet, and the returned darts thud into the flagstones around the attacker's feet.
```

### 2-11｜劍身貼槍桿逼近破長兵
**適用載體**：刃器對長柄（短破長）｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--burst 0.0:1.0:0.6｜--hitstop 1.4:1.65:-1.2`
- ① 位移與鏡頭：側面雙人，長槍直刺；劍客劍身貼著槍桿壓住，三步逼進槍手內圈，劍尖最後抵住槍手腕部，鏡頭沿槍桿方向推進。
- ② 身體發力：左足蹬離、右足跨步踩實、左足再跟進踩實（三拍進圈），胯與肩壓低，腕用劍身壓桿向下，使槍尖下沉並偏離中線。
- ③ 力場：空氣——劍壓槍桿時擠出一道貼地氣流；物質——槍桿被壓得彎曲，槍纓貼地抖動，槍手握桿的指節發白；光影——劍刃與槍桿接觸線上一道細亮；粒子——桿上木屑與灰塵飛散。
- ④ 戰術交換：以身法與接觸線化解距離優勢，把「長兵的距離」變成「短兵的近身」。

**中文導演母稿**：「長槍直刺，他用劍身貼住槍桿壓下去，三步逼近，槍手還沒來得及收槍，劍尖已經抵在他的手腕上。」

```h3snippet
The long spear thrusts straight at him, and the swordsman lays the flat of his blade against the shaft, drives off his left boot, strides across with his right and plants it firmly before bringing his left foot up behind, pressing the spear down and off line with his wrist while his shoulders stay low; the shaft bows under the pressure, the red tassel whips against the ground, wood chips and dust fly off the contact line, and his sword tip comes to rest against the spearman's wrist.
```

---

# 第三篇：修真仙俠高燃御物與陣法大招（11 組，嚴守防萬花筒不對稱規則）

> **本篇共同硬規格**：
> 1. 每組大招的英文句都寫明**能量來源**（劍尖、掌心、筆鋒、符紙、後背法相…）與**單一空間方向**（例如「由畫面左下往右上」），**不**把主體釘在畫面正中央向四周同心擴張。
> 2. 劍修的毀滅級大招維持劍招本質（劍氣、劍陣、劈斬），不把「召喚物從天而降」寫成劍修的主技（見 `ultimate-move.md` §1）。
> 3. 全篇不開 `P5`／`P6`；所有直線毀滅與御物大招走 `P8`（定樁段 `--anchor`、破空段 `--burst`）。
> 4. 大招的「中」鏡鎖機位（`ultimate-move.md` §2 鐵律）；追拍鏡只拍彈頭在完好地形上方逼近，不提前炸目標（導演合約 §7-6）。

### 3-01｜萬劍歸宗三段式（定樁凝劍 → 貼地劍流追尾 → 左下往右上單向山谷傾瀉）
**適用載體**：刃器／御劍（劍修）｜**建議鏡長**：3 鏡 × 2.4 秒（共 7.2 秒）｜**Dials**：`P8｜--anchor 0.0:2.4:-0.65｜--anchor 2.4:4.8:-0.30｜--burst 4.8:7.2:0.65｜--hit 4.8:5.1`（相對該三鏡鏡首）
- ① 位移與鏡頭：**鏡 A** 低位廣角鎖機位，劍修單膝釘樁於崖頂左下前景，百劍在其身後上方升起；**鏡 B** 貼地追隨一串劍流沿崖面低飛；**鏡 C** 高空固定機位，劍流由左下掌心往右上遠峰單向傾瀉，機位全程不退、不拉。
- ② 身體發力：右膝與左足底踩死同一塊石板，胯沉如樁，左肩壓低，右肩前探，右腕提劍訣指向右上；樁定後上身只以腕與指節的微小頓挫驅動劍陣，足底重心全程零位移。
- ③ 力場：空氣——劍陣升起時身後空氣被壓成層；物質——腳邊碎石懸浮、白袍與銀髮向兩側獵獵翻飛，山谷松林被劍風壓伏；光影——劍身金光使雲層下緣整片偏暖；粒子——金色劍屑沿單一方向拖成長尾，聚在劍流後方。
- ④ 戰術交換：「釘樁」顯示重量與蓄壓，「貼地追尾」製造空間深度，「單向傾瀉」把畫面最終落點定在遠峰，讓觀眾的視線被一條對角線帶走，避免對稱圖騰。

**中文導演母稿**：「他單膝釘在崖頂左下角，一抬指，身後百柄金劍升起；劍流貼著崖面低掠而出，最後整條劍河自畫面左下傾向右上遠峰，遠山被劍河從中貫穿。」

```h3snippet
The swordsman kneels on one knee at the lower left of the frame with his right knee and left boot sole planted firmly on a single flagstone, his left hand resting on his thigh and his silver hair and white sleeves whipping outward in the gale, and a hundred golden swords rise behind his back above the cliff edge while loose pebbles lift around his knee. The swords then stream low over the green pine canopy along the cliff face, trailing golden streaks behind each blade as the treetops bend away. From a locked high aerial view, the whole river of swords pours from his raised right hand at the lower left toward the distant peak at the upper right in one unbroken diagonal line, golden shards trailing behind the swords and the peak cracking open as they strike it.
```

### 3-02｜背後巨型半透明武神法相與本體同步揮斬
**適用載體**：能力型（法相自背脊真氣凝成，附著型場）＋刃器｜**建議鏡長**：2.6 秒｜**Dials**：`P8｜--anchor 0.0:1.2:-0.55｜--burst 1.2:2.6:0.65｜--hit 1.5:1.8`
- ① 位移與鏡頭：低位仰拍，劍客立於畫面右下前景，一尊三丈高半透明金色武神法相於其左後方由背脊升起；本體與法相同一方向斜劈（由左上往右下），鏡頭鎖機位。
- ② 身體發力：後足蹬離支點、前足踩實，胯旋、肩帶臂，腕一抖把劍由左上劈向右下；法相的肩與臂與本體同拍運動，足下重心壓向前足。
- ③ 力場：空氣——法相揮臂的位置把空氣向右下推出一道壓縮斜面；物質——敵陣地面沿斜線裂開，敵人的衣襟與旌旗向右下倒伏；光影——整個戰場光線隨著斜劈由暖金轉冷白；粒子——法相邊緣的金色微塵被拉成順斜線的長尾。
- ④ 戰術交換：把一劍的威力放大成「一個武神的一劍」，並以「本體小、法相大」的比例反差把體量壓場；斜線構圖避免法相居中對稱。

**中文導演母稿**：「他劍起左上，身後半透明的武神法相同時舉臂；一劍落下，本體與法相同向斜斬，整條右下斜線上的敵陣被一斬劈開。」

```h3snippet
The swordsman stands at the lower right of the frame, plants his front boot and drives off his rear boot as a translucent golden war-god figure the height of a watchtower rises out of his spine behind his left shoulder; he swings his sword diagonally from upper left to lower right with his hip, shoulder and wrist, and the giant figure swings its arm in the same beat along the same line, pressing the air into a slanted sheet of compression while a long crack splits the ground toward the lower right, banners and robes of the enemy ranks fall flat along the diagonal, and golden dust streams behind the giant arm.
```

### 3-03｜符籙金鏈破土纏縛鎖死
**適用載體**：能力型（符紙為源，鎖鏈沿地脈破土）｜**建議鏡長**：2.4 秒｜**Dials**：`P8｜--anchor 0.0:1.2:-0.55｜--burst 1.2:2.4:0.6`
- ① 位移與鏡頭：低位側面，符師立於左前景，擲出一疊符紙貼在地面一線；金色鎖鏈由左往右依序破土而出，纏住畫面右側巨獸的四肢，鏡頭鎖機位。
- ② 身體發力：右足蹬住地面、左足踩實沉腰，胯微旋，肩帶臂橫擲，腕一抖把符紙甩成一條直線貼地，另一手結劍指向鎖鏈延伸的方向。
- ③ 力場：空氣——鎖鏈出土時地面空氣被擠出一道向右的氣浪；物質——泥土與石塊被鏈條頂開、鏈條繃緊時巨獸皮甲被勒出凹痕；光影——金鏈放光，符文沿鏈身逐節亮起，巨獸身側陰影被推向右側；粒子——符紙灰燼與金屑沿鏈條方向飄揚。
- ④ 戰術交換：從遠距離封鎖對手移動，把強攻方的優勢轉成被動，下一鏡主角即可以安全距離補擊。

**中文導演母稿**：「符紙貼地成線，金鏈由左往右一節節破土，轉瞬纏住巨獸四肢，越勒越緊，巨獸怒吼卻動彈不得。」

```h3snippet
The talisman master plants his left boot, sinks his hips and flicks his right wrist to fling a strip of yellow talisman papers in a straight line across the ground toward the right, and golden chains burst out of the earth one after another from left to right, throwing up soil and stones; the chains wrap the four legs of the great beast at the right of the frame and tighten until its hide dents under the links, glowing runes light up segment by segment along each chain, and ash and golden sparks drift along the chains' direction.
```

### 3-04｜水墨化獸（墨虎貼地撲咬爆散墨刺）
**適用載體**：能力型（毛筆為源，墨色化獸）｜**建議鏡長**：2.4 秒｜**Dials**：`P8｜--anchor 0.0:1.0:-0.55｜--burst 1.0:2.4:0.6｜--hit 1.8:2.1`
- ① 位移與鏡頭：側機位低位，畫師立於左側，毛筆橫掃出一道墨痕，墨痕在地面隆起成虎，由左往右貼地撲向右側敵人，撲咬瞬間爆成墨刺。
- ② 身體發力：右足蹬離、左足踩實沉腰，胯旋帶肩，腕帶筆鋒由左下往右上提甩，筆尖落點即墨虎出現的位置。
- ③ 力場：空氣——墨虎前掠時帶出貼地氣流；物質——地面浮塵與落葉被向右掀起，敵人衣襬向後倒伏；光影——濃墨吞掉局部光線形成一條暗帶，爆散時墨刺邊緣有冷白高光；粒子——墨珠與墨絲沿撲擊方向噴出。
- ④ 戰術交換：以寫意方式展現「濃淡即強弱」的水墨語彙（《劍來》水墨基調的借鑑方向），並以貼地低軌避免墨虎與角色並排對稱。

**中文導演母稿**：「他提筆一揮，濃墨在地上隆起成虎，自左往右貼地撲去，一口咬中敵人，墨虎瞬間炸成漫天墨刺。」

```h3snippet
The ink painter plants his left boot, drives off his right, swings his hip and flicks his wrist so the brush tip sweeps from lower left to upper right and leaves a thick black stroke that swells off the ground into a tiger of liquid ink; the ink tiger pounces low along the ground from left to right, dust and fallen leaves lift off the earth behind it, and as its jaws close on the enemy at the right of the frame it bursts into a spray of ink spikes and droplets that shoot outward along the line of the pounce.
```

### 3-05｜墨龍單向俯衝（高空）
**適用載體**：能力型（毛筆為源）｜**建議鏡長**：2.6 秒｜**Dials**：`P8｜--anchor 0.0:1.0:-0.55｜--burst 1.0:2.6:0.65`
- ① 位移與鏡頭：高空固定俯瞰，畫師立於左下前景，筆鋒向天劃出一條墨線，墨線伸展成長龍，沿一條由左下往右上的長弧攀升後，由右上俯衝向右側的敵方山寨城門。
- ② 身體發力：後足蹬實、前足踩實，胯扭帶動肩，腕以長弧揮筆，右臂劃出由低到高的長線；落筆收尾時足底重心前移。
- ③ 力場：空氣——龍身行進處的雲氣被排開成一條長溝；物質——山寨旌旗與木牆被龍首壓過來的風吹倒；光影——墨色在雲間形成深淺濃淡，龍首的高光與遠方火光相映；粒子——墨霧沿龍尾向後拖成長帶。
- ④ 戰術交換：展示「一筆成龍」的氣勢，單向長軌使鏡頭讀出方向與目標，不產生圓形盤繞的萬花筒。

**中文導演母稿**：「他向天一筆，墨龍沿著長弧由左下往右上升起，到頂後調頭一沉，帶著長長的墨尾砸向右側城門。」

```h3snippet
Seen from a locked high aerial view, the ink painter stands at the lower left and sweeps his brush upward in one long rising stroke, and the black line unrolls into a long dragon of ink that climbs along a single arc toward the upper right, then lowers its head and dives onto the fortress gate at the right of the frame; clouds part in a long groove along its body, banners and wooden walls bow flat under the wind of its descent, and trails of black mist stream behind its tail.
```

### 3-06｜血月裂空斜斬（劍氣月牙）
**適用載體**：刃器（斬擊延伸的劍氣，屬劍招）｜**建議鏡長**：2.4 秒｜**Dials**：`P8｜--anchor 0.0:1.2:-0.55｜--burst 1.2:2.4:0.65｜--hit 1.4:1.7`
- ① 位移與鏡頭：低位廣角仰拍，劍客立於左下前景，一輪暗紅真月懸在畫面右上遠方；他一劍斜斬，劍氣月牙由刃口撕出，沿左下到右上的斜線裂開天幕。
- ② 身體發力：後足蹬離、前足踩實，胯旋、肩帶臂，腕由下往上撩劍，把全身動力鏈集中到刃口的一記斜撩。
- ③ 力場：空氣——月牙劍氣前方壓縮出層狀空氣；物質——雲層被劈成兩半向兩側捲開，劍客衣袂與長髮向後飄；光影——月牙的暗紅光使整個場景偏暖，雲縫中透出一線慘白；粒子——紅色劍屑沿裂縫的方向拖成細線。
- ④ 戰術交換：劍修以「斬」製造天象奇觀，能量從刃口與動力鏈長出，不是召喚物，符合「劍士大招必須是劍招」的修正。

**中文導演母稿**：「他由下往上一劍撩起，一道血紅月牙從刀鋒撕出，沿左下到右上斜斜劃過夜空，雲層被劈成兩半。」

```h3snippet
At the lower left of the frame the swordsman drives off his rear boot, plants his front boot firmly, spins his hip and rips his blade upward from below, and a crescent of crimson sword qi tears off the edge and cuts across the night sky along a slanted line from the lower left to the upper right; the clouds split open and curl away to both sides, the air in front of the crescent compresses into layered sheets, his long hair and sleeves stream backward, and the whole scene turns warm red as a thin line of pale light shows through the crack.
```

### 3-07｜九霄落雷麒麟俯衝
**適用載體**：能力型（劍尖引雷，麒麟由雷光塑形）｜**建議鏡長**：2.6 秒｜**Dials**：`P8｜--anchor 0.0:1.2:-0.55｜--burst 1.2:2.6:0.65｜--hit 2.0:2.3`
- ① 位移與鏡頭：低位仰拍，劍客在右下前景舉劍指天；雷雲自畫面上方右側裂開，一頭由雷光組成的麒麟由右上俯衝向左下的敵人，機位鎖死。
- ② 身體發力：雙足踩實分立，胯沉，雙肩上抬，右腕舉劍直指天空，劍尖是引雷點；落雷時全身重心下壓到前足。
- ③ 力場：空氣——雷光經過處空氣被電離，周圍壓縮成層；物質——敵陣地面被衝擊波掀起石屑，旌旗與衣襟向左下倒伏；光影——整片戰場瞬間被雷光照成冷白，陰影向左下被推開；粒子——電弧與焦屑沿俯衝路線噴濺。
- ④ 戰術交換：以天雷為殺招，劍尖為源頭，單向俯衝保持對角線，避免麒麟變成畫面中心的對稱圖騰。

**中文導演母稿**：「他舉劍指天，九霄雷雲裂開，一頭由雷光化成的麒麟從右上俯衝向左下，所經之處空氣炸成層層電浪。」

```h3snippet
At the lower right of the frame the swordsman plants both boots wide, sinks his hips and raises his right arm to point his sword tip at the storm cloud; a crack of violet-white lightning splits the cloud at the upper right and forms a qilin of living lightning that dives along one diagonal toward the enemy at the lower left, the air around its path compressing into layered sheets, gravel and banners blowing toward the lower left, and the whole battlefield flashing cold white for an instant as arcs and charred dust spray along the line of descent.
```

### 3-08｜青蓮劍域貼地綻放切碎石柱
**適用載體**：刃器（劍插入地面，劍氣成形）｜**建議鏡長**：2.6 秒｜**Dials**：`P8｜--anchor 0.0:1.0:-0.55｜--burst 1.0:2.6:0.6｜--hit 1.6:1.9`
- ① 位移與鏡頭：低機位平視，劍客立於畫面左前景，把劍插入地面；青色劍氣由劍身下方沿地面向畫面右側依序綻開成一串花瓣形劍刃，一路切碎右側三根石柱。
- ② 身體發力：雙手握劍，右足蹬離支點、左足跨步踩實沉腰，胯下壓帶動肩，腕一送把劍貫入石板；足底重心全部壓向劍柄。
- ③ 力場：空氣——花瓣劍刃每綻開一枚都推出一道貼地氣流；物質——石板沿劍刃行進路線裂開，石柱斷成兩截向右倒下；光影——青色冷光沿地面一路亮向右側遠處，石柱斷面反出細亮；粒子——石屑與青色微塵沿綻開路徑跳躍。
- ④ 戰術交換：展示「領域」的單向推進版：劍域沿一條通道展開而非以角色為圓心，避免曼陀羅式圓陣，卻保留「蓮花綻放」的辨識度。

**中文導演母稿**：「他一劍插地，青色劍氣沿著地面向右一朵朵綻開，花瓣般的劍刃接連切過，三根石柱應聲斷成兩截。」

```h3snippet
At the left of the frame the swordsman grips his sword with both hands, drives off his right boot, steps his left foot down hard and sinks his hips so that the blade punches into the flagstones; blue blades of qi in the shape of lotus petals unfold one after another along the ground toward the right of the frame, each petal sending a low pulse of air ahead of it, the flagstones splitting along their path, and the three stone pillars at the right are cut through in sequence and topple to the right as stone dust and blue sparks skip along the line of bloom.
```

### 3-09｜開山闢地劈山（劈地裂線）
**適用載體**：刃器（重劍，開山闢地型）｜**建議鏡長**：2.6 秒｜**Dials**：`P8｜--anchor 0.0:1.2:-0.55｜--burst 1.2:2.6:0.65｜--hit 1.4:1.7`
- ① 位移與鏡頭：低位廣角，劍客立於左前景；重劍高舉過頭後垂直下劈，劈出一條裂線沿地面飛馳向畫面深處，將遠山從山腳劈到山頂；機位鎖死。
- ② 身體發力：雙足踩實分立，胯沉、肩把重劍舉過頭頂再下壓，雙腕在最低點一抖把力送入劍尖，足底重心壓向前足。
- ③ 力場：空氣——裂線前方的空氣被推成一道白色壓縮牆向前；物質——地面沿裂線翻起岩片，遠處山體由山腳到山頂緩緩裂開；光影——裂縫內透出暖橘色光，沿線的雲影被切成兩半；粒子——岩屑與塵霧沿裂線向上升起。
- ④ 戰術交換：使用單一直線把畫面深度與勝負一次說完，裂縫的方向是唯一的軸線。

**中文導演母稿**：「他雙手舉劍過頂，一劍劈下，一道裂線貼地直奔遠山，從山腳劈到山頂，大山無聲裂開。」

```h3snippet
At the left foreground the swordsman plants both boots wide, sinks his hips, raises the heavy sword overhead with both hands and brings it straight down with a snap of both wrists; a straight crack races away from the blade across the plain toward the distant mountain, pushing a white wall of compressed air ahead of it, slabs of rock flip up along its length, warm orange light spills from the crack, and the far mountain splits slowly from its base to its summit as dust and rock fragments rise along the line.
```

### 3-10｜劍河繞柱追弧貫穿
**適用載體**：御劍（劍修，劍鏈追蹤型）｜**建議鏡長**：2.4 秒｜**Dials**：`P8｜--anchor 0.0:1.0:-0.55｜--burst 1.0:2.4:0.65`
- ① 位移與鏡頭：側機位中景，劍客立於左側；一條由三十柄飛劍首尾相連的劍河由他手中起，從左往右先繞過畫面中的石柱，再繞回敵人側面貫穿；鏡頭只在敵人側面推近一點，不繞劍河旋轉。
- ② 身體發力：右足踩實、左足蹬離支點，胯旋帶動肩，腕帶劍訣在身前畫出一條由左到右的弧線，劍河沿同一條弧線推進；足底重心壓在前足。
- ③ 力場：空氣——劍河前端壓出一道細長氣流；物質——被擦過的石柱表面掀起細屑，敵人的衣襟被劍風扯向右側；光影——劍河銀光沿弧線一路照亮石柱與敵人側臉；粒子——劍屑沿弧線尾端拖出一條明亮長帶。
- ④ 戰術交換：以彎弧避開敵人的正面防守，從側翼貫穿，展示「御劍可以拐彎」的獨特優勢。

**中文導演母稿**：「三十柄飛劍首尾相連，自他指尖流出，繞過石柱、拐一個大弧，從敵人側面貫穿而過。」

```h3snippet
At the left of the frame the swordsman plants his right boot, drives off his left and turns his hip so his wrist sweeps a sword-fingers gesture in one smooth arc from left to right, and thirty flying swords linked head to tail stream out of his fingertips along that arc, curl around the stone pillar and pierce the enemy's flank from the side; the lead blade pushes a thin line of air ahead, the pillar surface throws off fine chips as the swords pass, the enemy's robe is dragged toward the right, and a bright trail of silver sparks follows the arc to its tail.
```

### 3-11｜玄冰封江單向推進
**適用載體**：能力型（掌心為源，冰鋒沿水面前進）｜**建議鏡長**：2.6 秒｜**Dials**：`P8｜--anchor 0.0:1.2:-0.55｜--burst 1.2:2.6:0.6`
- ① 位移與鏡頭：高空固定俯瞰江面，修士立於左下岸邊，右掌拍向水面，冰線由掌下沿江面向右上方單向推進，凍住浪頭並爬上遠處敵船；機位全程不倒退。
- ② 身體發力：左足踩實、右足蹬離，胯微旋，肩壓向前，右腕以掌根重拍水面，掌心真氣沿水面外放；落掌後上身保持前傾。
- ③ 力場：空氣——冰鋒前方空氣驟冷，白霧沿冰線攀升；物質——浪頭在躍起的瞬間被凍成尖峰、敵船船舷結霜龜裂；光影——冰面反射月光形成沿江面延伸的冷白光帶；粒子——冰晶與霜屑沿冰線向前噴出。
- ④ 戰術交換：以單向前進的冰鋒建立壓迫，並以「浪頭凍住」這一不可逆結果讓觀眾確認殺招有效。

**中文導演母稿**：「他一掌拍向江面，一道白色冰線由左下沿江向右上疾進，浪頭被凍成冰峰，遠處敵船船舷結出白霜。」

```h3snippet
From a locked high aerial view the cultivator at the lower left bank plants his left boot, drives off his right and slaps his right palm down on the river surface; an ice front runs out from beneath his palm across the water toward the upper right in one straight line, turning each wave crest into a sharp ice peak, white mist climbing along the ice line, ice crystals spraying forward from the front edge, and the hull of the enemy boat far at the upper right frosting over and cracking as the cold light of the moon reflects along the ice.
```

---

# 第四篇：鬥氣／罡氣環繞與雙人對波逆轉機制（7 組）

> **共同設計**：本篇處理「A 周身環繞鬥氣、氣浪壓迫 → 雙方對撞僵持 → B 以**技術**而非更大的光團破局」。
> - 固定 **A 在左、B 在右** 的 180 度軸線，單鏡內不互換左右。
> - 鬥氣為**附著型場**（薄邊、貼身、隨身體運動），只在邊緣做一層折射；能量洪流為**持續型場**，必須有明確的出手部位與飛行方向。
> - 對轟逆轉的勝負由「切角／偏軸／卸向／點破」決定，嚴禁退化成兩個無源光球越撞越大。
> - 鬥氣與罡氣的外觀預設用「金白＋暗灰」兩色（`ultimate-move.md` §4 只許兩色）。

### 4-01｜鬥氣點燃地面碎石懸浮
**適用載體**：能力型（附著型場：鬥氣自皮膚外放，貼附手臂與軀幹）｜**建議鏡長**：2.4 秒｜**Dials**：`P8｜--anchor 0.0:2.4:-0.55`
- ① 位移與鏡頭：低位平視，A 立於畫面左前景，鏡頭緩慢推進（小幅），讓鬥氣邊緣的細微變化與碎石懸浮成為主要動態；A 的雙足全程不離位。
- ② 身體發力：雙足分立踩實，胯沉成馬步，雙肩下沉，雙腕外翻、掌心朝下，把氣從足底經胯送到肩與腕；呼氣時胸腔擴張帶動氣勢。
- ③ 力場：空氣——鬥氣邊緣貼著手臂有一層薄薄的折射波紋；物質——腳邊的碎石一粒粒浮起，被牽引著繞行手臂；光影——金白色鬥氣把近處地面映成暖色、遠處維持冷灰；粒子——細小火星沿手臂向上漂。
- ④ 戰術交換：在動手之前先用「氣場可見」建立壓迫，讓 B 看見自己的衣襬被鬥氣的風推動，心理上已先退一步。

**中文導演母稿**：「金白色的鬥氣貼著他的雙臂燃起，腳邊碎石一粒粒浮上半空；他一動不動，氣勢卻把對面人的衣襬一寸寸吹向後方。」

```h3snippet
The fighter plants both boots wide on the cracked ground, sinks into a horse stance with his hips low and shoulders dropped, and turns his wrists outward with the palms facing down; a thin rim of gold-white aura hugs both forearms and flickers along his torso, the air immediately around it ripples with a faint refraction, small stones lift off the ground one by one and orbit his arms, sparks drift upward along his sleeves, and the robe of the opponent in the distance is pushed backward by the wind of his presence.
```

### 4-02｜護體罡氣硬扛重擊碎裂反震
**適用載體**：能力型（罡氣自丹田經背脊外放為一層貼身護罩）＋鈍器對撞｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--hitstop 0.9:1.15:-1.8｜--burst 1.15:2.4:0.55`
- ① 位移與鏡頭：腰上雙人近景略仰，A 肩膀迎著 B 的重錘；罡氣護罩在錘頭接觸處由內向外龜裂，B 被反震向後彈開，鏡頭鎖死。
- ② 身體發力：A 右足踩實、左足蹬住，胯沉，肩與背肌收緊，腕與肘貼肋，以身體整體硬吃一擊；B 出錘時肩與腕全力下砸，被反震反彈。
- ③ 力場：空氣——錘頭撞上罡氣瞬間一圈壓縮氣浪向四周擴散；物質——罡氣表面出現蛛網裂紋後碎裂成透明碎片，B 的衣襟與鬍鬚被反震波向後吹；光影——裂紋處閃出金色亮光，A 身後的影子短暫被推向地面；粒子——碎裂的罡氣碎片如玻璃屑向外飛散。
- ④ 戰術交換：展示「以硬碰硬後勝者仍站著」的壓倒性，但罡氣碎裂也表示有代價，為下一次對波留出逆轉空間。

**中文導演母稿**：「重錘轟在他肩頭——罡氣像玻璃一樣瞬間布滿裂紋，隨即碎成漫天透明碎片，反震之力把持錘者整個人震得倒退三步。」

```h3snippet
The heavy hammer smashes down toward his shoulder, and the fighter plants his right boot, braces his left, sinks his hips and tightens his shoulder and back to take the blow on his whole body; a spiderweb of golden cracks spreads across the shimmering shell of qi around him and it bursts into glassy shards that scatter outward, a ring of compressed air bursts from the point of impact, and the hammer wielder's shoulders and wrists are thrown back by the rebound so that he staggers three steps backward with his robe flaring.
```

### 4-03｜偏軸能量洪流被斜劈一分為二穿過突襲本體
**適用載體**：刃器對能力（持刀者劈開有明確來源的能量洪流）｜**建議鏡長**：2.6 秒｜**Dials**：`P8｜--burst 0.0:1.4:0.65｜--hitstop 1.4:1.65:-1.2`
- ① 位移與鏡頭：高位微俯固定機位，A 立於畫面右側釋放洪流，洪流由右往左偏軸射向畫面左側的 B；B 持刀斜劈，洪流被一分為二向兩側噴開，B 從縫隙中穿過，逼近 A。
- ② 身體發力：B 左足蹬離支點、右足跨步踩實沉腰，胯旋帶肩，腕以反手斜上劈由左下往右上切入洪流；穿過縫隙時肩與胯收窄，把身體貼進兩股洪流之間的空隙。A 以雙掌推出洪流，腕下壓、肩向前送。
- ③ 力場：空氣——被劈開處空氣撕成兩道向外的氣刃；物質——兩股洪流旁的地面被削出兩條平行深溝，碎石向兩側噴起；光影——刀口劃過洪流瞬間閃一道白線，兩股洪流把兩側牆面染成金色；粒子——能量碎屑沿兩股分流的軌跡噴出。
- ④ 戰術交換：把「能量越大越強」翻轉成「角度比力量重要」，B 以技術切入而非對抗，直接撲到 A 本體。

**中文導演母稿**：「金色洪流從右側轟來，他反手一刀斜劈，洪流被從中劈成兩股，向兩邊轟開，他貼著縫隙穿過，刀尖已經遞到對手面前。」

```h3snippet
A thick golden torrent of qi pours from the palms of the fighter on the right across the frame toward the left, and the swordsman at the left drives off his left boot, steps his right foot down firmly, spins his hip and cuts upward on a slant with a reverse grip, splitting the torrent in two; the air tears into two outward blades of wind, two parallel trenches are carved in the ground on either side, a white line flashes along the cut, and he passes through the narrow gap between the two streams with his shoulders turned to stay inside it until the point of his sword reaches his opponent's chest.
```

### 4-04｜雙掌對撞僵持 → 低身切入技術破局
**適用載體**：能力型對能力（近中距攻防，雙方皆有氣源）｜**建議鏡長**：2.6 秒｜**Dials**：`P7｜--anchor 0.0:1.2:-0.55｜--hitstop 1.2:1.45:-1.2｜--burst 1.45:2.6:0.6`
- ① 位移與鏡頭：腰上雙人近景，A 與 B 掌心相抵成對抗，鏡頭鎖機位；B 突然降低重心並偏轉身體，A 的力量落空向前撲出，B 反手擊其肋。
- ② 身體發力：僵持階段雙方足底踩實、胯沉、肩與肘撐住；B 在關鍵一拍把右足橫向撤半步、左肩下沉、胯旋帶開對手的掌根（腕部接觸點由推改為引），A 失去支撐點。
- ③ 力場：空氣——兩掌相抵處壓出一圈短暫的圓形壓縮波，破局時被拉成偏向一側的氣流；物質——兩人足下地面被各自的力壓出兩個淺坑，A 前撲時碎石被拖出一道線；光影——僵持階段兩色光（金與藍）在接觸點交鋒，破局後藍光溢向 A 的側面；粒子——能量碎屑沿力的新方向噴出。
- ④ 戰術交換：僵持不靠「更大一團光」解決，而是靠重心與角度的細微調整，是修真戰鬥最有說服力的技術性逆轉。

**中文導演母稿**：「雙掌相抵，兩人腳下石板都被壓出淺坑；他忽然撤半步、肩一沉，把對方的力引向一側，對手整個人撲空，肋下被他反手一擊。」

```h3snippet
The fighter on the left and the fighter on the right press their palms together in a standoff, boots planted deep in two shallow craters; the right-hand fighter shifts his right foot back half a step, drops his left shoulder and turns his hip so that his wrist redirects the other man's palm to the side, the left-hand fighter's force finds open air and pitches him forward with gravel dragged in a line behind his boots, and gold and blue light that had met at the point of contact spills toward his flank as the right-hand fighter's backhand lands under his ribs.
```

### 4-05｜針尖點破罡氣罩
**適用載體**：長兵（槍尖）對能力（護罩）｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--anchor 0.0:1.0:-0.55｜--hitstop 1.0:1.25:-1.8｜--burst 1.25:2.4:0.55`
- ① 位移與鏡頭：側面中景，A 在左，周身罡氣護罩浮動；B 持槍在右，槍尖一點一點試探同一個位置；鏡頭在槍尖與護罩接觸點上緩推，裂紋出現後槍桿向前突進。
- ② 身體發力：B 左足踩實、右足蹬離支點，胯旋，肩帶臂把力量集中在槍尖一個點，腕穩住桿身並在最後一拍以短促腕力推出，槍尖點破護罩。
- ③ 力場：空氣——槍尖貼近護罩時一圈高頻抖動的波；物質——護罩接觸點出現蛛網裂紋後整體粉碎，A 的衣襟被碎罩的氣浪掀起；光影——裂紋處閃白，護罩碎片反射冷光；粒子——護罩碎片沿槍桿兩側向後噴開。
- ④ 戰術交換：以「點」破「面」，用細節戰術擊潰氣場優勢，並讓持槍者以短促的一拍取回主動權。

**中文導演母稿**：「他三次輕點同一個位置，罡氣罩泛起細細漣漪；第四次，槍尖一抖，裂紋像蛛網般炸開，整個罩子瞬間碎成透明碎片。」

```h3snippet
The spearman on the right plants his left boot, drives off his right and tracks the spearhead to the same point on the shimmering shell of qi that surrounds his opponent on the left, a high-frequency ripple trembling across the shell; his shoulder pushes and his wrist stabilises the shaft, and on the fourth touch a short flick of the wrist drives the tip through, spiderweb cracks burst outward, the shell shatters into cold glassy shards that spray backward along both sides of the shaft, and the opponent's robe flares in the blast.
```

### 4-06｜借力卸勁，把光束沿前臂引向地面
**適用載體**：能力型對能力（卸力型技術）｜**建議鏡長**：2.4 秒｜**Dials**：`P7｜--burst 0.0:0.9:0.6｜--hitstop 0.9:1.15:-1.2｜--anchor 1.15:2.4:-0.55`
- ① 位移與鏡頭：腰上雙人近景，A 在左發射光束，B 在右伸出覆有氣鞘的前臂迎光；光束沿前臂被導向地面，鏡頭鎖機位後緩推。
- ② 身體發力：B 左足踩實、右足斜跨半步，胯旋帶肩，腕外翻讓前臂形成斜面，肘貼肋、肩壓低，把光束的力從腕沿前臂送到肩再導入地面；足底重心緩緩壓向後足，吃力卸力。
- ③ 力場：空氣——光束接觸前臂時被拉長成一道貼臂的氣流；物質——被導入地面處石板炸出一條淺溝，B 的袖口被光束邊緣燒出焦痕；光影——光束被引向地面後，B 身後的牆面亮起一道向下的斜光；粒子——能量碎屑沿前臂與地面溝槽向外噴濺。
- ④ 戰術交換：「接住而不頂回去」，改用導向把攻擊方的優勢轉化為對地面的損耗，為 B 的反擊爭取下一拍。

**中文導演母稿**：「光束轟向他的前臂，他不硬頂，手腕一翻，把力沿著手臂送進地面——石板炸出一條長溝，光束被卸得七零八落。」

```h3snippet
A beam of white light fires from the palm of the fighter on the left, and the fighter on the right plants his left boot, steps his right foot out at an angle and rolls his wrist outward so that his forearm, wrapped in a pale sheath of qi, meets the beam on a slant; the light is dragged into a long streak along his arm and driven down into the ground through his shoulder and hip, tearing a shallow trench in the flagstones, scorching the edge of his sleeve and scattering sparks along the trench while a slanted shaft of light falls on the wall behind him.
```

### 4-07｜劍氣橫切對轟，月牙切斷洪流反擊本體
**適用載體**：刃器（劍氣）對能力（洪流）｜**建議鏡長**：2.6 秒｜**Dials**：`P8｜--anchor 0.0:1.0:-0.55｜--burst 1.0:2.6:0.65｜--hit 1.8:2.1`
- ① 位移與鏡頭：高空固定俯瞰，A 在左下以掌發洪流向右上；B 在右上以劍橫揮，劍氣月牙由上往下垂直於洪流軸線切入，洪流被攔腰截斷，月牙餘勢繼續飛向 A。
- ② 身體發力：B 右足踩實、左足蹬離，胯旋、肩帶臂，腕反手橫揮一劍，把月牙劍氣垂直壓向洪流軸線；A 以腕與肩把洪流推出，足底重心前傾。
- ③ 力場：空氣——月牙切入洪流處空氣撕成兩半，截斷口噴出兩道反向氣浪；物質——洪流斷口的地面被壓出一道直線凹痕，A 身後的樹木被餘波向後吹彎；光影——洪流被截斷處熄成暗色，月牙銀光持續向左下延伸；粒子——被切開的光屑沿兩個方向分別向前與向後拖尾。
- ④ 戰術交換：用垂直切入取代同向對轟，使勝負取決於角度與劍氣的連續性，最終由 B 的劍氣餘勢命中 A，完成逆轉。

**中文導演母稿**：「洪流自左下轟來，他橫揮一劍，銀色月牙垂直切入洪流，把它攔腰截斷；月牙餘勢不減，直奔洪流源頭而去。」

```h3snippet
From a locked high aerial view, the fighter at the lower left drives a golden torrent from his palms toward the upper right, and the swordsman at the upper right plants his right boot, drives off his left, spins his hip and sweeps his blade across in a backhand cut so that a silver crescent of sword qi drops across the line of the torrent at a right angle; the torrent is cut in two, the air tears into two opposing gusts at the break, a straight dent is pressed into the ground at the cut, and the crescent keeps flying toward the lower left until it strikes the fighter at the source while the trees behind him bend backward.
```

---

# 第五篇：漫劇 15 秒五段式高燃導演套餐模板（4 套完整招式鏈）

> **使用規則**
> - 時間軸固定為 `0–3s / 3–6s / 6–10s / 10–13s / 13–15s`（導演合約 §4 五段狀態接力），切為 **6 鏡**：第 3 段（6–10s）拆成 `6.0–8.2s` 與 `8.2–10.0s` 兩鏡，其餘各一鏡（單鏡 ≤3.0s，核心攻防動詞 ≤4）。
> - 首接觸 ≤0.5s；第 4 段由被壓制方以環境借力折返；第 5 段「敗者最後反擊 → 勝者三拍」，結尾仍在運動（衣料、塵霧、碎石或火花持續到最後一幀）。
> - 每套固定 **左 A 右 B** 的 180 度軸線；每一鏡繼承上一鏡 ≥4 項狀態（位置、朝向、速度方向、高度、資產狀態、受擊狀態、環境餘波）。
> - 套餐內的單招可由第一至第四篇對應條目替換（每套結尾列出建議替換表）。
> - 輸出時依 `fight-directing-contract.md` §5 同步編寫中文七段母稿與英文六欄位；此處英文 snippet 為 `detailed_description` 內 6 個 `[Shot]` 的**動作內核**，貼入時再補身分／場景／鏡頭語言。
> - `--hires-dials` 一律依各套備註；所有 `--burst` 強度 ≤ 0.65 以守住 $M_{\text{eff}} \le +0.98$。

### 5-01｜劍修逆襲破陣（被陣法壓制 → 定樁凝劍 → 一閃破陣眼）
**適用載體**：刃器（劍修 A）對 能力型（符籙鎖陣修士 B，鎖鏈由符紙為源）｜**建議鏡長**：15 秒／6 鏡（3.0 / 3.0 / 2.2 / 1.8 / 3.0 / 2.0）｜**Dials**：`P8｜--anchor 6.0:8.2:-0.65｜--burst 0.0:3.0:0.60｜--burst 8.2:10.0:0.65｜--burst 10.0:12.7:0.60｜--hitstop 4.6:4.85:-1.2｜--hitstop 9.0:9.25:-1.8｜--hitstop 14.2:14.45:-1.2`，`--hires-dials phase-motion`
- ① 位移與鏡頭：S1 腰上雙人同框，金鏈由左右地面破土纏來；S2 中景借石柱折線；S3a 低位廣角，A 單膝釘樁、鏡頭鎖死；S3b 同機位切到劍氣斬破陣眼；S4 追蹤 A 從側面穿過鎖鏈縫；S5 高位略俯，三拍收尾。
- ② 身體發力：S1 右足蹬離、左足踩實沉腰，胯旋、肩帶腕斬鏈；S2 左足蹬柱折向、右足落步；S3a 右膝與左足底釘死石板、胯沉、左肩壓低、右腕引劍；S3b 全身動力鏈由足經胯到肩到腕在最低點一抖；S4 側身收窄肩胯穿隙；S5 三拍以足步＋腕換軸。
- ③ 力場：空氣——鎖鏈破土與劍氣月牙各推一道壓縮波；物質——石柱碎屑、陣眼石板龜裂、袖袍與銀髮向單側獵獵；光影——陣紋金光被劍氣冷白光逐步蓋過；粒子——符紙灰與劍屑沿一條方向拖尾。
- ④ 戰術交換：被動 → 蓄壓 → 以一記「劍招」破壞陣眼，使 B 的優勢（群鎖）在一拍內崩塌；B 的陣法為能力、A 的破局為劍招，載體不混用。
- 因果鏈：鎖鏈纏來 → 斬斷一條 → 石柱借力 → 被鏈鞭擊飛 → 單膝釘樁凝劍 → 劍氣月牙斬破陣眼 → 陣眼石柱崩塌 → B 封鎖退路 → A 借碎石折返 → 三拍終結。
- 建議替換：S1 → 1-09；S3b → 3-06；S4 → 2-04；整套延伸 → 3-01。

**中文導演母稿**：
- `0–3s`：金色符鎖自左右地面破土，劍修右足一蹬、長劍橫斬斬斷第一條鏈，火花四濺，另一條鏈已纏上左臂。
- `3–6s`：他借殘柱一蹬折向右上，被第三條鏈如鞭抽中肩頭，倒飛翻滾撞在陣眼石柱腳下，單膝穩住。
- `6–8.2s`：他單膝釘在石板上，左足底與右膝踩死同一塊石，長劍反插入地，劍身泛起冷白光，周身碎石懸浮。
- `8.2–10s`：他拔劍由下往上撩斬，劍氣月牙沿左下到右上撕開空氣，一劍斬碎陣眼，整座符陣的金光瞬間暗了一半。
- `10–13s`：B 抬手以殘符封住去路，A 踩碎落石借力折向右側盲區，貼著符鎖縫隙穿過。
- `13–15s`：B 拍出最後一道符火；A 三拍——逼 B 舉符盾、換軸繞側、一劍從左後方命中；陣眼崩塌，B 倒退撞上石柱，符紙灰燼飄到最後一幀。

```h3snippet
[0-3s] Golden talisman chains burst out of the ground from the left and right, and the swordsman drives off his right boot, plants his left firmly on the flagstone and cuts his long sword across to sever the first chain in a spray of sparks while a second chain coils around his left forearm.
[3-6s] He kicks off a broken pillar with his right foot to turn toward the upper right, a third chain whips across his shoulder and throws him into a tumble that ends on one knee at the foot of the array's stone pillar, loose gravel bouncing around him.
[6-8.2s] He kneels with his right knee and left boot sole planted on a single stone slab, drives the sword point into the ground in front of him, and pale light climbs the blade as pebbles lift off the ground around his knee and his white sleeves flutter to one side.
[8.2-10s] He rips the sword up from below along a line from the lower left to the upper right, his shoulder and wrist snapping through, and a crescent of sword qi tears off the edge and cuts the glowing stone at the heart of the array in two, the golden light of the array dimming as stone slabs crack outward.
[10-13s] The talisman master flings a wall of paper charms across the path, and the swordsman stamps on a falling rock, turns off the line and slips between two chains on the right with his shoulders turned, torn paper and ash whirling in his wake.
[13-15s] The talisman master hurls one last blast of talisman fire; the swordsman cuts it off with his blade, steps around to the talisman master's left side on three firm steps and lands a final cut across his ribs, and the man stumbles back against the pillar as ash and sparks keep drifting through the last frame.
```

### 5-02｜重刃狂戰 vs 靈巧傘修（以柔克剛的連鎖逆轉）
**適用載體**：鈍器／重刃（A，大劍）對 傘（B，傘面與傘骨）｜**建議鏡長**：15 秒／6 鏡（3.0 / 3.0 / 2.2 / 1.8 / 3.0 / 2.0）｜**Dials**：`P7｜--burst 0.0:2.6:0.65｜--burst 3.0:5.0:0.60｜--burst 5.3:7.5:0.60｜--burst 9.0:12.7:0.60｜--anchor 7.5:8.5:-0.55｜--hitstop 2.6:2.85:-1.2｜--hitstop 5.0:5.25:-1.8｜--hitstop 8.5:8.75:-1.8｜--hitstop 13.8:14.05:-1.8`，`--hires-dials phase-motion`
- ① 位移與鏡頭：S1 腰上雙人近景，大劍橫掃撞上傘面；S2 側面，傘尖連點；S3a 近景鎖定「傘骨卡刃」的鎖刃點；S3b 同機位切到扭轉奪刃；S4 追拍 B 從柱後繞到 A 的側面；S5 中景三拍收尾，鏡頭固定在 B 身後。
- ② 身體發力：A 右足蹬、左足踩實沉腰，胯與肩轉出整條重劍，雙腕壓劍；B 以足尖輕點借力，胯旋帶肩，腕轉傘柄把傘面當斜盾、把傘尖當點擊。
- ③ 力場：空氣——重劍橫掃壓縮一道低頻氣浪，傘面旋轉捲出一圈小氣旋；物質——石板被劍風刮出灰痕，傘骨彎曲後彈回，雨滴與水珠被甩成扇形；光影——劍面暗鐵反光與傘面油紙透光對比；粒子——雨與灰塵被兩人的動作各自帶成不同方向的流線。
- ④ 戰術交換：A 依賴重量與慣性，B 依賴角度與接觸點；B 每一次不直接擋而改成「導向與點擊」，最後以傘骨卡刃把 A 的重量變成 A 的負擔。
- 因果鏈：重劍橫掃 → 傘面斜擋被震退 → 傘尖點中 A 腕 → 大劍砸地 → 傘骨卡住劍刃 → 扭轉奪刃 → A 失重心 → B 封路 → A 借碎石折返 → 傘修三拍反制。
- 建議替換：S1／S2 → 2-10；S3b → 2-06；S5 → 2-05。

**中文導演母稿**：
- `0–3s`：大劍自右橫掃，傘修撐傘斜擋，傘面被劍風壓彎，雙足在石板上帶出兩道灰痕後穩住。
- `3–6s`：傘修收傘為點，傘尖連點大劍者手腕三下，最後一下點中虎口，大劍失控砸向地面，碎石四濺。
- `6–8.2s`：大劍者單膝壓劍穩住重心，雙手重新握緊，傘修展開傘面橫在劍路上，傘骨卡進劍刃凹槽。
- `8.2–10s`：傘修轉腕一擰，傘骨把大劍整個絞偏，劍脫手半尺，大劍者被拖得失去重心向前撲。
- `10–13s`：大劍者怒吼著撿起劍、踩碎落石向右側折返，從傘修左側盲區斜劈；傘修貼著石柱一轉，傘面撐開擋住劍勢。
- `13–15s`：大劍者最後一記全力下劈；傘修三拍——以傘面逼其舉劍、換軸繞側、收傘一點命中其肩窩，大劍者重劍脫手插進石板，雨水沿傘沿甩出最後一圈水痕。

```h3snippet
[0-3s] The great-sword fighter drives off his right boot, plants his left firmly and swings the huge blade across from the right in a flat arc, and the umbrella fighter tilts her open umbrella to meet it at a slant, the canopy bowing under the blow while her boots scrape two grey lines on the flagstones.
[3-6s] She snaps the umbrella shut and jabs its tip at his wrist three times, the third jab landing on the web of his hand, and the great sword jerks out of line and crashes into the floor, throwing up a spray of gravel.
[6-8.2s] He kneels on one knee with his weight on the planted blade, gripping the hilt with both hands, while she spreads the umbrella wide across the path of the steel and its ribs bite into a notch on the blade.
[8.2-10s] She twists her wrist and hips together and the umbrella ribs wrench the heavy blade sideways out of his hands, and he lurches forward off balance with his shoulders dragged after the sword.
[10-13s] He scoops the sword up, stamps a falling rock to turn off the line and swings diagonally at her left side, and she pivots around the stone pillar and snaps the umbrella open so the canopy catches the blow, rain beads fanning from the rim.
[13-15s] He raises the sword overhead for a final chop; she lifts the umbrella to draw his guard up, steps around him on three firm steps and drives the closed tip into the hollow of his shoulder, and the great sword falls and stands in the stone as water droplets keep flying off the canopy to the final frame.
```

### 5-03｜徒手宗師硬破兵刃（導演設定：雙手覆氣鞘，只觸刀脊與持刀者手腕）
**適用載體**：徒手（**導演設定**：宗師 A 雙手與前臂覆青白氣鞘，僅接觸刀脊側面與持刀者的非鋒利部位）對 刃器（長刀 B，腰間另有一柄短刀作為斷刀後的導演補全武器）｜**建議鏡長**：15 秒／6 鏡（3.0 / 3.0 / 2.2 / 1.8 / 3.0 / 2.0）｜**Dials**：`P7｜--burst 0.0:2.7:0.65｜--burst 4.7:6.0:0.60｜--burst 10.0:12.8:0.60｜--anchor 8.15:9.2:-0.55｜--hitstop 4.4:4.65:-1.2｜--hitstop 7.9:8.15:-1.8｜--hitstop 14.0:14.25:-1.2`，`--hires-dials phase-motion`
- ① 位移與鏡頭：S1 腰上近景，長刀三連斬逼近，宗師三次貼身閃避；S2 宗師切入後以掌背拍偏刀脊並肩撞；S3a 近景，B 雙手重劈，宗師雙掌夾刀脊；S3b 獨立鏡頭拍「斷刀的結束狀態」；S4 追拍宗師穿過崩塌石柱的煙塵；S5 高位中景三拍。
- ② 身體發力：S1 左足蹬、右足踩實，胯旋、肩讓出刀線，腕不外伸；S2 右足蹬離、左足跨步，胯旋帶肩撞；S3a 雙足踩實、胯沉，雙肩下沉，雙腕外翻夾住刀脊；S3b 肘部下壓配足底重心；S5 以足步與腕控制換軸。
- ③ 力場：空氣——刀風擦過宗師衣料形成三條細長氣痕；物質——刀脊被夾住時刃身彎曲，斷刀處迸出金屬屑，石柱崩落砸起塵霧；光影——氣鞘青光與刀身冷光形成對比，斷刃切口一條白線；粒子——金屬屑與塵土被兩人的動作各自帶成細長軌跡。
- ④ 戰術交換：徒手方不裸手接刃口，而以氣鞘夾刀脊、掌背拍刀脊、以肩撞與肘壓使兵器自己崩斷，符合「持械對徒手」非對稱規則。
- 因果鏈：三連斬被閃 → 掌背拍脊 → 肩撞擊飛 → 撞柱反撲重劈 → 夾刀脊 → 肘壓斷刀 → B 撿起短刀封鎖 → 宗師借煙塵折返 → 三拍終結。
- 建議替換：S2 → 1-08；S3a → 1-01；S5 → 1-05。

**中文導演母稿**：
- `0–3s`：長刀自右上起連斬三下，宗師三次側閃、後仰、墊步，刀風擦過衣角，裂開一道細口。
- `3–6s`：宗師切入貼身，右掌背拍在刀脊側面，刀被拍偏，隨即肩撞命中胸口，長刀者撞向後方石柱。
- `6–8.2s`：長刀者借石柱反撲，雙手過頂重劈；宗師雙足踩實沉胯，兩掌覆著青白氣鞘夾住刀脊，刀鋒停在眉前。
- `8.2–10s`：宗師肘一壓、腕一擰，長刀從中段「啪」一聲折斷；半截刀點朝下插進石板立著，長刀者手中只剩短柄與一道切口白光。
- `10–13s`：長刀者拔出腰間短刀，踢翻石柱封住退路；宗師借崩塌煙塵折向左側盲區，從碎石之間穿過。
- `13–15s`：長刀者最後一刺；宗師三拍——側身讓開、扣腕換軸、右掌擊中胸口；長刀者倒飛撞牆，塵霧與碎屑落到最後一幀。

```h3snippet
[0-3s] A long blade cuts three times from the upper right, and the bare-handed grandmaster leans aside, arches back and steps in with his boots planted firmly, the wind of the blade opening a thin tear in his sleeve.
[3-6s] He steps inside the blade line, slaps the back of his palm, wrapped in a pale-blue sheath of qi, against the flat of the blade to push it aside, and drives his shoulder into the swordsman's chest, throwing him backward against a stone pillar.
[6-8.2s] The swordsman rebounds off the pillar and chops down with both hands, and the grandmaster plants both boots, sinks his hips and clamps the flat of the steel between his two sheathed palms an inch above his brows, the blade bowing under the pressure.
[8.2-10s] In a dedicated shot of the cracked stone floor, the grandmaster's elbow presses down and his wrist twists, and the long blade is already broken, its upper half standing tip-down in the flagstone with a white line along the cut, the swordsman gripping only a short stub of the hilt.
[10-13s] The swordsman draws a short knife from his belt and kicks a pillar down across the exit, and the grandmaster turns off the line into the dust of the collapse, weaving between falling rubble with his shoulders narrowed.
[13-15s] The swordsman thrusts the knife for a final strike; the grandmaster leans aside, clamps the man's wrist from below and turns around his arm with three firm steps, then lands a palm strike on the sternum that throws him against the wall as dust and chips keep falling through the last frame.
```

### 5-04｜高空御劍追逐斬首（雲海追擊，單向推進）
**適用載體**：刃器／御劍（A、B 皆踏飛劍飛行，空戰）｜**建議鏡長**：15 秒／6 鏡（3.0 / 3.0 / 2.2 / 1.8 / 3.0 / 2.0）｜**Dials**：`P9（--hires-dials off）｜--hitstop 4.9:5.15:-1.2｜--hitstop 8.4:8.65:-1.2｜--hitstop 14.0:14.25:-1.2`（P9 常駐已含 $M_{\text{eff}}=+0.69$，本套不疊 `--burst`；全程無跪蹲姿態，不需 `--anchor`）
- ① 位移與鏡頭：全程以**同一方向（由左上往右下）**的追逐為主軸；S1 高空側面追拍，A 在後追 B；S2 追進雲海；S3a 峰壁間隙，機位鎖在峰壁側；S3b 同機位看到 A 反向切入；S4 俯拍雲海，A 側面穿過劍雨；S5 低位仰拍三拍終結。
- ② 身體發力：踏劍時雙足踩實劍身，胯微沉，膝彎曲吸收氣流；轉彎靠胯與肩側傾帶動飛劍傾斜；出劍時右肩帶腕斬、左臂向外平衡；落點瞬間重心前移到前足。
- ③ 力場：空氣——飛劍前端壓出一道錐形白色氣雲；物質——雲海被劍身劃開、袖袍與長髮向後飄成直線；光影——雲縫透出晨光，劍身反光掃過 B 的側臉；粒子——雲霧碎片與冰晶沿追逐方向拖成長尾。
- ④ 戰術交換：高度與速度即優勢，A 利用峰壁與劍雨殘片轉向，由下方與側面切入，最後以三拍收尾一記斬落護身飛劍與髮冠，B 失去飛劍墜入雲海。
- 因果鏈：追擊俯衝 → 劍刃相交 → 鑽入雲海被擊偏 → 峰壁借力反向 → 切斷 B 的護身飛劍 → B 放劍雨封鎖 → A 借殘劍折返 → 三拍斬落髮冠。
- 建議替換：S1 → 3-10；S3b → 2-03；S5 → 3-06。

**中文導演母稿**：
- `0–3s`：A 踏劍俯衝，自左上追向右下的 B，長劍橫斬，兩劍相交迸出火花，雲氣被撞開一道裂口。
- `3–6s`：B 翻身鑽入雲海，A 追進；B 回劍一擊擦中 A 的飛劍劍尖，A 的飛劍被帶得旋轉半圈，但雙足仍牢牢踩在劍身上。
- `6–8.2s`：兩人穿過兩座山峰的狹縫，A 以足尖蹬峰壁折向，翻身貼著峰壁反向追上。
- `8.2–10s`：A 從 B 下方切入，一劍斬斷 B 的護身飛劍，劍刃斷口一條白光，B 身形驟降。
- `10–13s`：B 召出一陣劍雨封住前路，A 借被打碎的劍片轉向，從劍雨縫隙側身穿過，劍雨在他身後炸成碎光。
- `13–15s`：B 最後一擊回身斬；A 三拍——逼其舉劍、換軸翻到上方、一劍掠過其頸側斬落髮冠，B 失去飛劍墜入雲海，髮冠碎片與雲霧飄到最後一幀。

```h3snippet
[0-3s] The sword rider dives after his rival along a diagonal from the upper left to the lower right, planting both boots on the flat of his flying sword and swinging his blade across in a flat cut, and the two blades meet in a burst of sparks that tears a gap through the cloud.
[3-6s] The rival rolls his flying sword into the cloud sea and the pursuer follows, and the rival's backward stroke clips the tip of the pursuer's sword so that it spins half a turn while the pursuer's boots stay firmly planted on the blade.
[6-8.2s] Both riders pass through a narrow gap between two cliffs, and the pursuer pushes off the rock face with the toe of his right boot to turn his sword over and chase the rival back along the cliff wall.
[8.2-10s] He cuts in from below and slices the rival's protective flying sword in two with a white line along the cut, and the rival drops sharply as the broken blade falls through the cloud.
[10-13s] The rival summons a rain of swords across the path, and the pursuer bumps off a shattered blade fragment to turn aside and weaves through a gap in the rain with his shoulders turned, the swords bursting into sparks behind him.
[13-15s] The rival spins for a last cut; the pursuer draws his guard up, rolls his sword over to the upper side on three firm moves and passes his blade by the rival's neck to cut off the hair crown, and the rival tumbles off his broken flying sword into the cloud sea as shards of the crown and wisps of mist keep drifting through the last frame.
```

---

## 附錄：各鏡「單招替換」速查

| 要換的段落 | 想要的觀感 | 建議替換條目 |
|---|---|---|
| 0–3s 開場鉤子 | 先給結果的威壓 | 1-01、1-02、1-09 |
| 3–6s 變軸首中 | 借環境折線與首次命中 | 2-03、2-04、2-09 |
| 6–10s 技術逆轉 | 以柔克剛、以點破面 | 2-06、2-08、4-04、4-05、4-06 |
| 10–13s 封鎖折返 | 借碎石與劍雨殘片折返 | 2-04、3-10、4-03 |
| 13–15s 三拍終結 | 單向傾瀉或斬擊終結 | 3-01、3-06、3-09、4-07 |

## 附錄：自我檢核（改寫本庫任何條目時先過一遍）

1. 英文句內有沒有出現招式名、拼音或英譯招名？（應為零）
2. 英文句內有沒有 `no / not / never / without / instead of / rather than`？（應為零；也避免 `nothing / none / n't`）
3. 接地姿態（跪、蹲、馬步、盤坐、雙足釘樁）同句有沒有水平衝刺或平移？（應為零；並已配 `--anchor`）
4. 有沒有 `slides / skids / glides` 描寫攻擊位移？（應為零）
5. 大招有沒有指明單一方向（如左下往右上）與能量來源？有沒有退化為畫面正中央的對稱圓輪？
6. 徒手對兵刃是否標註「導演設定」並寫出氣鞘等力的來源？
7. `--burst` 是否 ≤ 0.65、`--hitstop` 是否約 0.25 秒？P9 是否搭配 `--hires-dials off`？
