# Sporion

Fintech platforma pro soukromé skupinové "money poty" (sbírky na narozeniny, svatby,
dovolené apod.) pro český a slovenský trh. Inspirováno francouzským Leetchi.
Aktuálně ve fázi UI prototypu — single-page aplikace v čistém HTML/CSS/JS, bez frameworků.

## Struktura souborů

ZDROJOVÉ soubory (zde se edituje) — každý je samostatné, plně funkční téma:
- `sporion_minimal_spa2.html` — téma "Minimal Elegance" (font Outfit, čistá B&W, banner se souhvězdím, SVG progress kroužky)
- `sporion_pixel_spa.html`    — téma "8Bit Shroomies" (font Silkscreen, pixel art, houby jako progress, banner s raketkou + hvězdami). Obsahuje base64 PNG hub (~870 KB).
- `sporion_noir3.html`        — téma "Neon Noir" (font Comfortaa, tmavé pozadí, modrá #00cfff + žlutá #ffe600, banner s kapkami na skle + bleskem, hvězda jako progress)

VÝSLEDNÝ soubor (build artefakt):
- `sporion_7r22b03ja1ol8zsy.html` — wrapper se třemi tématy v `<iframe srcdoc>`.
  **POZOR: appka ho už NEPOUŽÍVÁ.** `sporion_landing.html` načítá téma PŘÍMO do `#app-frame`
  (`appFrame.src = THEME_FILES[t]`, jen 1 úroveň vnoření — kvůli scrollu kolečkem na desktopu,
  viz níže). Landing je sync-hub: drží stav potů/zobrazení/jazyk a po přepnutí tématu (reload
  iframu → téma pošle `hello`) je vrátí. Wrapper zůstává jen jako artefakt (build_app.py ho umí
  vyrobit), pro appku není v cestě.

**Scroll (DŮLEŽITÉ):** Appka MUSÍ být v `#app-frame` jen 1 úroveň hluboko (tj. téma přímo, ne přes
wrapper). Ve 2 úrovních vnoření pod fixním iframem se na desktopu kolečko nedoručí do tématu a
detail potu nejde odrolovat. Vzor je dárcovská stránka (`#contrib-frame` → stránka přímo), která
roluje bez potíží. Nezanořovat appku hlouběji.

## Build krok (DŮLEŽITÉ)

Po JAKÉKOLIV změně ve zdrojovém souboru je nutné přegenerovat `sporion_7r22b03ja1ol8zsy.html`.
Postup: každý zdroj se přečte jako text, HTML-escapuje se (`&`→`&amp;`, `"`→`&quot;`) a vloží
do wrapperu jako `<iframe srcdoc="...">`. Wrapper poslouchá `message` event a přepíná
`.active` třídu na iframech. Tři ID: frame-minimal, frame-pixel, frame-noir.

**PROČ srcdoc a NE data-URL:** srcdoc dědí origin rodiče → téma je SAME-ORIGIN (in-process).
data-URL dělal z tématu cross-origin OOPIF a prohlížeč pak ve vnoření pod fixním landing
`#app-frame` NEDORUČIL scroll (kolečko/dotyk) do detailu potu. srcdoc to opravuje. Sync
přes postMessage funguje dál (nikde se nekontroluje `e.origin`). Viz memory `scroll-vnorene-iframy`.

Hotový build skript: **`python3 build_app.py`** (přečte tři zdroje, escapuje, vloží do šablony
wrapperu a zapíše `sporion_7r22b03ja1ol8zsy.html`). Po každé změně zdroje spustit.

## Společná architektura všech tří témat

- Jednostránková aplikace (SPA): stránky #page-dashboard, #page-detail, #page-settings
  se přepínají třídou .active. Žádný router.
- Data potů: pole `POTS` v <script> (id, name, occasion, collected, goal, mush,
  contributors, occasion_date, contributions[]). Stejná struktura ve všech třech.
- Horní lišta (sticky): ikonky Dashboard (domeček), Zobrazení (Karty/Seznam),
  Téma (žárovka), Nastavení (ozubené kolečko); tlačítko "Nový pot" vpravo.
- Detail potu: velký progress vizuál, 4 statistiky, graf průběhu (canvas),
  odhad dokončení, seznam příspěvků.
- Progress vizuál se liší dle tématu: kroužek (minimal) / houba zdola nahoru (pixel) / hvězda (noir).

## Konvence

- Kapitálky (uppercase) všude KROMĚ názvů potů. Názvy potů ponechat jak jsou.
- Pixel téma: BEZ diakritiky (font Silkscreen ji nepodporuje). Minimal a Noir diakritiku mají.
- Hotový pot (collected >= goal): minimal = černá karta; pixel = zelené pozadí + "HOTOVO";
  noir = žlutý border + žluté prvky.
- Měna: "Kč", formát částek přes toLocaleString('cs').
- Houby (10 druhů): pravak, muchomurka, vaclavky, lisky, holubinka, bedla, kremenac,
  hliva, shiitake, kuratko. V pixel verzi se renderují na <canvas> s PRŮHLEDNÝM pozadím
  (žádný obdélník): sebraná část se plní plnou barvou zdola nahoru, zbytek je jemný
  odbarvený "duch" (předpočítaný v `ghosts{}`). Při zobrazení se houba plynule naplní
  (`animateMush`, rAF + setTimeout fallback na správný koncový stav). 100% = plně barevná.
- Pixel téma má TEPLÉ retro pozadí (béžová #ebd9b2, karty/lišta krém #fdf6e7) — odlišení
  od minimal (chladná B&W) a noir (tmavá). Černé rámy a akcenty zůstávají.

## Otevřené úkoly / TODO

- Funkce záložek zatím nehotové: formulář "Nový pot", "Přidat příspěvek", "Sdílet",
  "Upravit" (zatím alert() nebo neaktivní).
- Anglická lokalizace (přepínač jazyka CZ/EN je v Nastavení, EN zatím "coming soon").
- Pixel houby mají jemný bílý anti-aliasing okraj (řešeno flood-fillem removeWhiteHalo,
  zatím ne 100%). Nízká priorita.
- Odemykání hub: 6 základních + 4 prémiové za 50 splněných potů (koncept, neimplementováno).

## Čeho se vyvarovat

- Needitovat `sporion_7r22b03ja1ol8zsy.html` ručně — vždy přegenerovat ze zdrojů.
- Neměnit fonty (Outfit / Silkscreen / Comfortaa jsou záměrná identita každého tématu).
- Nepřidávat reklamy (monetizace = transakční poplatky 3–5 % + prémiové funkce).
- Nezavádět build nástroje/frameworky — záměrně čisté HTML/CSS/JS v jednom souboru na téma.
