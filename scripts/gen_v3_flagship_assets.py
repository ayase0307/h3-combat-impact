#!/usr/bin/env python3
"""批量使用本機 Krea 2（rayArtshoot V5 + krmj_epoch_4）生成 9 套旗艦 AI 漫劇素材（14 角色/神獸 + 9 場景空鏡）。

已存在檔案自動跳過（支援斷點續跑）；傳入套件名稱可只跑指定套件，例：
    python scripts/gen_v3_flagship_assets.py rep01 rep02
"""

import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

from gen_krea2_assets import build_character_graph, build_scene_graph, run_graph

ROOT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "v3-manju"

MANJU_CHAR_HEAD = (
    "krmj, High-end Chinese-Korean 2.5D semi-realistic AI manju guoman character illustration, "
    "studio full-body standing portrait centered on a clean solid seamless neutral mid-grey studio backdrop, "
    "even soft studio key lighting, full head-to-toe visibility with clear margin around boots and head. "
)
MANJU_CHAR_TAIL = (
    " Crisp painterly 2.5D manju rendering, refined attractive facial features, clean fabric and armor highlights, "
    "single solo subject only, completely plain seamless mid-grey backdrop."
)
MANJU_SCENE_HEAD = (
    "krmj, Wide establishing Chinese 2.5D semi-realistic AI manju guoman background plate of "
)
MANJU_SCENE_TAIL = (
    " Completely empty uninhabited location with zero people, zero figures, zero animals, unobstructed open center staging area. "
    "All architectural surfaces and cloth elements are plain unadorned solid materials with geometric patterns only, crisp atmospheric perspective."
)

SUITES = {
    "rep01": [
        ("leijin.png", "character", 2026112411, 0.72,
         MANJU_CHAR_HEAD
         + "A tall strikingly handsome young East Asian lightning warrior in his mid-twenties, clean masculine jaw, "
         + "calm cold aristocratic expression with softly closed lips, sharp dark eyes, long flowing silver-white hair tied high with a dark steel clasp. "
         + "Wearing sleek obsidian-black and dark-gold sleeveless xianxia battle armor with leather shoulder straps, engraved gauntlets, dark draped waist sash, and armored combat boots. "
         + "Holding a long ornate curved dark-steel katana-jian blade with faint violet-white lightning glint and a small iron chain ring at the pommel angled cleanly downward in his right hand."
         + MANJU_CHAR_TAIL),
        ("bg_volcano.png", "scene", 2026112412, 0.70,
         MANJU_SCENE_HEAD
         + "a vast scorched volcanic obsidian battlefield under towering dark violet-grey storm clouds crackling with distant purple lightning. "
         + "Wide expanse of cracked charred dark basalt ground laced with thin glowing orange magma fissures stretching across the entire center foreground, flanked by jagged dark volcanic boulders and drifting glowing embers."
         + MANJU_SCENE_TAIL),
    ],
    "rep02": [
        ("chichuan.png", "character", 2026112421, 0.72,
         MANJU_CHAR_HEAD
         + "A handsome agile young East Asian swordsman in his early twenties, calm composed expression with softly closed lips, "
         + "warm sharp dark eyes, wind-swept dark brown hair tied in a loose high ponytail. "
         + "Wearing a flowing cream-white and warm bronze-trimmed traditional xianxia martial robe with wide cuffed sleeves, dark brown cloth belt carrying twin small bronze wine gourds at the hip, and dark martial boots. "
         + "Holding a sleek forged Chinese jian sword angled cleanly downward in his right hand."
         + MANJU_CHAR_TAIL),
        ("xuanlan.png", "character", 2026112422, 0.72,
         MANJU_CHAR_HEAD
         + "A tall sharp-featured handsome East Asian dark warrior in his late twenties, cold composed aristocratic face with closed lips, "
         + "sharp teal-grey eyes, tousled jet-black wind-swept hair. "
         + "Wearing layered ink-black and deep dark-teal feathered battle armor with sculpted shoulder plates, tattered dark-teal cloak hem, and tall armored boots. "
         + "Holding a long heavy curved dark-steel war saber with subtle cyan metallic edge angled cleanly downward in his right hand."
         + MANJU_CHAR_TAIL),
        ("bg_ink_sea.png", "scene", 2026112423, 0.70,
         MANJU_SCENE_HEAD
         + "a dramatic stormy dark ocean bay framed by towering misty dark slate cliffs and a massive white roaring waterfall pouring into surging teal-grey waves under overcast silver clouds. "
         + "A wide unobstructed expanse of dark rippling sea water with a small weathered plain empty wooden rowboat floating gently near center distance, ink-wash cloud mist drifting over open water."
         + MANJU_SCENE_TAIL),
    ],
    "rep03": [
        ("qinglan.png", "character", 2026112431, 0.75,
         MANJU_CHAR_HEAD
         + "A strikingly handsome bright-eyed East Asian teen fantasy hero around eighteen, clean refined face with calm focused expression and softly closed lips, "
         + "energetic spiky short black hair with a thin red headband ribbon. "
         + "Wearing a fitted navy-blue sleeveless xianxia martial tunic with braided red waist sash, rugged leather forearm wraps, dark trousers, and laced adventure boots. "
         + "Holding a hefty ornate glowing translucent jade-green crystal warhammer with bronze handle resting cleanly at his side."
         + MANJU_CHAR_TAIL),
        ("dragon_azure.png", "character", 2026112432, 0.72,
         "krmj, High-end Chinese 2.5D semi-realistic AI manju fantasy creature concept illustration, "
         + "full-body coiling pose centered on a clean solid seamless neutral mid-grey studio backdrop, even studio lighting, complete head-to-tail visibility with clear margin. "
         + "A majestic colossal serpentine Eastern water dragon with shimmering emerald-turquoise iridescent scales, flowing translucent coral-pink feathered mane and wide ear fins, "
         + "curved ivory antlers, four clawed legs, and luminous golden eyes. Crisp painterly 2.5D manju rendering, single solo dragon creature only, completely plain seamless mid-grey backdrop."),
        ("bg_fairy_gorge.png", "scene", 2026112433, 0.70,
         MANJU_SCENE_HEAD
         + "a radiant sunlit emerald fairy gorge river lake surrounded by soaring lush mossy green karst limestone peaks and cascading white waterfalls under a vivid blue sky with bright white clouds. "
         + "Wide unobstructed crystal-clear turquoise water surface across the entire foreground and center, framed by smooth sunlit shoreline boulders and hanging green vines."
         + MANJU_SCENE_TAIL),
    ],
    "rep04": [
        ("taixuan.png", "character", 2026112441, 0.72,
         MANJU_CHAR_HEAD
         + "An ethereally handsome young East Asian celestial immortal swordsman in his mid-twenties, impeccably refined pale aristocratic face, "
         + "subtle delicate vertical gold sword seal between his brows, calm serene cold expression with softly closed lips, piercing dark eyes, "
         + "long cascading silky silver-white hair flowing past his waist. "
         + "Wearing layered flowing ivory-white and champagne-gold embroidered xianxia immortal silk robes with wide graceful sleeves, golden cloud belt clasp, and pale silk martial boots, standing poised and empty-handed."
         + MANJU_CHAR_TAIL),
        ("bg_pine_cliff.png", "scene", 2026112442, 0.70,
         MANJU_SCENE_HEAD
         + "a monumental high-altitude stormy mountain summit cliff overlooking an endless jagged pine-covered alpine valley shrouded in swirling silver clouds and dramatic dark grey thunderclouds with shafts of pale sunlight. "
         + "A broad open weathered dark granite cliff ledge strewn with moss and scattered dry pine needles extending cleanly across the center foreground, flanked by wind-bent gnarled mountain pines."
         + MANJU_SCENE_TAIL),
    ],
    "rep05": [
        ("yeshi.png", "character", 2026112451, 0.75,
         MANJU_CHAR_HEAD
         + "A breathtakingly beautiful young East Asian dark fantasy empress in her early twenties, refined cold aristocratic oval face, "
         + "calm composed expression with softly closed lips, piercing dark eyes, long flowing silver-white hair topped with an intricate sculpted obsidian-black gothic thorn crown. "
         + "Wearing a fitted obsidian-black and dark-silver sculpted spiky armor bodice transitioning into a dramatic layered translucent dark-violet sheer silk gown and sleek armored heels, standing poised."
         + MANJU_CHAR_TAIL),
        ("lihuang.png", "character", 2026112452, 0.75,
         MANJU_CHAR_HEAD
         + "An ethereally beautiful young East Asian celestial peacock goddess in her early twenties, impeccably refined serene face, "
         + "calm gentle composed expression with softly closed lips, luminous emerald-gold eyes, long silky dark hair adorned with an ornate gold-and-emerald peacock feather filigree crown and hanging jade ear drops. "
         + "Wearing a regal emerald-teal, ivory, and gold-embroidered celestial silk gown with long floating iridescent gauze ribbons, standing gracefully centered."
         + MANJU_CHAR_TAIL),
        ("bg_sunset_meadow.png", "scene", 2026112453, 0.70,
         MANJU_SCENE_HEAD
         + "a vast boundless wind-swept emerald green highland grassland stretching uninterrupted to a distant twilight horizon where warm golden sunset light blends into deep steel-blue evening sky. "
         + "A low weathered pale limestone flat ledge occupies the near left edge while wide lush rolling green grass opens cleanly across the entire center and distance."
         + MANJU_SCENE_TAIL),
    ],
    "orig01": [
        ("jinyuan.png", "character", 2026112461, 0.75,
         MANJU_CHAR_HEAD
         + "A strikingly beautiful agile young East Asian female assassin in her early twenties, clean refined oval face, "
         + "calm cold focused expression with softly closed lips, sharp dark eyes, sleek glossy jet-black chin-length bob haircut with twin long thin braided strands. "
         + "Wearing tailored ink-teal and dark-gold fitted short xianxia stealth combat attire with cropped armored vest, leather cross-straps, fitted fingerless gauntlets, dark leg wraps, and sleek combat boots. "
         + "Holding twin ornate crimson-and-gold nine-section linked chain-blades draped cleanly in both hands."
         + MANJU_CHAR_TAIL),
        ("heming.png", "character", 2026112462, 0.72,
         MANJU_CHAR_HEAD
         + "A tall strikingly handsome young East Asian master artificer swordsman in his mid-twenties, clean aristocratic jawline, "
         + "calm poised expression with softly closed lips, sharp dark eyes, silky black hair half-tied with a sleek engraved bronze hairpin. "
         + "Wearing a tailored ivory-white, charcoal, and antique-gold layered steampunk-xianxia martial long coat with fitted bronze cuffs, geometric brass waist clasp, and dark leather boots. "
         + "Holding twin ornate dark-steel and gold folding mechanical war-fans, one held open and one folded cleanly at his sides."
         + MANJU_CHAR_TAIL),
        ("bg_clocktower.png", "scene", 2026112463, 0.70,
         MANJU_SCENE_HEAD
         + "the monumental cavernous interior of a colossal ancient bronze mechanical clocktower during a midnight lightning storm. "
         + "Enormous interlocking ornate bronze and brass clockwork gears and a giant suspended pendulum fill the towering arched hall, backlit by tall rain-streaked blue-lit stained-glass gothic arch windows. "
         + "A wide unobstructed bronze-plated flat gear platform and iron walkway stretches cleanly across the center foreground for staging."
         + MANJU_SCENE_TAIL),
    ],
    "orig02": [
        ("feiyu.png", "character", 2026112471, 0.75,
         MANJU_CHAR_HEAD
         + "A breathtakingly beautiful young East Asian wuxia heroine in her early twenties, refined delicate oval face, "
         + "calm cool expression with softly closed lips, dark upswept eyes, long silky jet-black hair half-pinned with a crimson silk tassel. "
         + "Wearing a tailored ink-black and deep crimson silk embroidered wuxia combat robe with fitted wrist guards, slender waist sash, flowing layered skirt, and black leather boots. "
         + "Holding a sleek crimson steel-ribbed traditional oil-paper umbrella tilted cleanly over one shoulder in her right hand, with delicate crimson silk threads looped lightly around her left fingers."
         + MANJU_CHAR_TAIL),
        ("hanji.png", "character", 2026112472, 0.72,
         MANJU_CHAR_HEAD
         + "A tall handsome cold-faced East Asian spear warrior in his mid-twenties, clean sharp masculine jawline, "
         + "calm aloof expression with softly closed lips, cool silver-grey eyes, sleek jet-black hair tied in a crisp high warrior topknot. "
         + "Wearing layered obsidian-black and brushed-silver armored wuxia robe with engraved steel shoulder guards, dark sash, and armored combat boots. "
         + "Holding a tall slender translucent frost-steel Chinese spear angled vertically in his right hand."
         + MANJU_CHAR_TAIL),
        ("bg_bamboo_lanterns.png", "scene", 2026112473, 0.70,
         MANJU_SCENE_HEAD
         + "a cinematic rain-soaked deep emerald bamboo forest at midnight illuminated by dozens of plain unadorned round glowing crimson silk lanterns suspended among tall wet green bamboo stalks. "
         + "A broad unobstructed rain-slick dark flagstone path covered in shallow reflective puddles mirroring warm red lantern light runs cleanly through the center foreground under falling silver rain streaks."
         + MANJU_SCENE_TAIL),
    ],
    "ult01": [
        ("moli.png", "character", 2026112481, 0.75,
         MANJU_CHAR_HEAD
         + "An ethereally beautiful young East Asian calligraphy immortal heroine in her early twenties, refined serene oval face, "
         + "calm aristocratic expression with softly closed lips, clear dark eyes, long flowing silky jet-black hair secured with a pale celadon jade hairpin. "
         + "Wearing layered flowing ivory-white and ink-black gradient silk hanfu robes edged with delicate gold brushstroke embroidery and long wide graceful sleeves. "
         + "Holding a tall ornate pale-jade giant calligraphy brush staff with ink-dipped dark bristle tip upright in her right hand."
         + MANJU_CHAR_TAIL),
        ("bg_fortress_pass.png", "scene", 2026112482, 0.70,
         MANJU_SCENE_HEAD
         + "an epic ancient dark-stone mountain fortress pass and weathered stepped bastion wall overlooking a wide winding misty valley flagstone approach road under dramatic stormy twilight clouds with golden horizon light. "
         + "Wide unobstructed stone rampart walkway in the near foreground overlooking the broad open valley road below, plain unadorned weathered granite masonry."
         + MANJU_SCENE_TAIL),
    ],
    "ult02": [
        ("wangshu.png", "character", 2026112491, 0.75,
         MANJU_CHAR_HEAD
         + "An ethereally gorgeous young East Asian lunar ice empress in her early twenties, impeccably delicate porcelain-refined face, "
         + "calm transcendent expression with softly closed lips, luminous pale ice-blue eyes, long flowing silky silver-white hair crowned with a delicate translucent silver-and-crystal diadem. "
         + "Wearing a layered flowing pearl-white and pale ice-blue translucent celestial silk gown with intricate silver frost embroidery and drifting sheer ribbons, standing poised barefoot."
         + MANJU_CHAR_TAIL),
        ("bg_lunar_lake.png", "scene", 2026112492, 0.70,
         MANJU_SCENE_HEAD
         + "a boundless glassy jet-black mirror lake at night under a colossal luminous silver-white full moon suspended low in a deep indigo starry nebula sky with faint cyan aurora mist along the distant horizon. "
         + "Completely smooth unbroken dark mirror-like water surface reflecting the huge glowing moon and stars across the entire open foreground and center."
         + MANJU_SCENE_TAIL),
    ],
}


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(SUITES.keys())
    total = sum(len(SUITES[t]) for t in targets)
    done = 0
    for suite in targets:
        sdir = ROOT / suite
        for fname, kind, seed, lstr, prompt in SUITES[suite]:
            done += 1
            out = sdir / fname
            if out.exists() and out.stat().st_size > 10000:
                print(f"[{done}/{total}] SKIP existing {suite}/{fname}", flush=True)
                continue
            prefix = f"{suite}_{pathlib.Path(fname).stem}"
            print(f"[{done}/{total}] GEN {suite}/{fname} ({kind})...", flush=True)
            g = build_character_graph(prompt, seed, lstr, prefix) if kind == "character" else build_scene_graph(prompt, seed, lstr, prefix)
            run_graph(g, out)


if __name__ == "__main__":
    main()
