# Easter Egg - Velikonocni hra pro Kubu

Arcade hra inspirovana BoulderDash. Hrac ovlada zajice na farme, sbira velikonocni vajicka, vyhyba se psum a traktorum. Sbere vsechna vejce, utece k vychodu a vyhrava!

**Web:** https://kofis.eu/kuba/gm008/

## Ovladani

| Akce | Klavesnice | Mobil |
|------|-----------|-------|
| Pohyb | Sipky / WASD | D-pad (L/R/U/D) nebo swipe |
| Skok | Space | Tlacitko J |

**Skok** - zajic skoci az o 3 pole ve smeru kam se diva. Preskoci psa, slepici, blato i diru. Pokud +3 neni volne, doskoci na +2 nebo +1. Cooldown 2 sekundy.

## Herni prvky

| Znak | Tile | Popis |
|------|------|-------|
| `R` | Zajic (start) | Hrac |
| `E` | Vejce | Normalni vajicko (+10 bodu) |
| `G` | Zlate vejce | Vzacne vajicko (+50 bodu) |
| `S` | Specialni vejce | Power-up vajicko (+25 bodu) |
| `D` | Pes | Nepritel - honi zajice, kontakt = smrt |
| `T` | Traktor | Nepritel - jezdi po ceste, kontakt = smrt |
| `C` | Slepice | Chodi nahodne, neubliži |
| `X` | Vychod | Zavreny dokud nejsou sebrana vsechna vejce |
| `#` | Ker/zed | Neprostupny |
| `B` | Balik sena | Prekazka |
| `F` | Plot | Preskok na druhou stranu (2 tile) |
| `M` | Blato | Zpomaluje pohyb |
| `H` | Dira | Teleport zpet na start |
| `.` | Trava | Volne pole |
| `=` `|` `+` | Cesta | Trasa traktoru |

## Levely

| # | Nazev | Popis |
|---|-------|-------|
| 01 | Tutorial Farm | Jen vejce, zadny nepritel |
| 02 | First Dog | 1 pes, jednoducha mapa |
| 03 | Muddy Path | Blato a seno |
| 04 | Tractor Trouble | Traktor na ceste |
| 05 | Fences and Holes | Ploty a diry |
| 06 | Chicken Run | Slepice + pes |
| 07 | Double Dog | 2 psi |
| 08 | Fast Tractor | Rychlejsi traktor |
| 09 | Golden Farm | Zlata vejce, komplexni mapa |
| 10 | Easter Chaos | Vse dohromady |

## Scoring

| Akce | Body |
|------|------|
| Normalni vejce | 10 |
| Specialni vejce | 25 |
| Zlate vejce | 50 |
| Dokonceni levelu | 100 |

Skore se akumuluje pres levely. Po skonceni hry (win/lose) lze odeslat na leaderboard.

## Technologie

- **Java 17** + **LibGDX 1.14**
- **TeaVM** - transpilace do JS pro webovou verzi
- **Custom ECS** - Entity-Component-System architektura
- **Leaderboard** - score.kofis.eu (Spring Boot)

## Build

```bash
# Desktop
./gradlew lwjgl3:run

# Web (lokalni server na localhost:8080)
./gradlew teavm:run

# Web build
./gradlew teavm:build
```

## Struktura

```
kfsEasterEgg/
├── core/src/main/java/kfs/easter/
│   ├── KfsMain.java          # Entry point
│   ├── KfsConst.java         # Konstanty (tile size, rychlosti, scoring)
│   ├── Tile.java             # Enum tile typu
│   ├── World.java            # Herni svet, mapa, entity management
│   ├── comp/                 # ECS komponenty (8)
│   ├── sys/                  # ECS systemy (8)
│   ├── ecs/                  # ECS framework
│   └── ui/                   # Screeny (6)
├── assets/
│   ├── maps/                 # 10 ASCII levelu
│   ├── textures/             # Sprite PNG (programaticky generovane)
│   ├── fonts/                # Press Start 2P (10/16/32)
│   └── ui/                   # LibGDX skin
├── lwjgl3/                   # Desktop launcher
└── teavm/                    # Web launcher + index.html
```

## Autor

Vytvořeno pro Kubu, Velikonoce 2026.

## Licence a zdroje

### Zvukove efekty
Vsechny zvukove efekty (hop, egg, golden, hit, win, lose) byly **programaticky vygenerovany** skriptem `generate_sounds.py` pomoci Python modulu `wave`. Zadne externi zvuky nebyly pouzity. Bez licencnich omezeni.

### Hudba
Vsechny 3 chiptune tracky (Happy Spring Walk, Easter Bunny Bounce, Sunny Farm) byly **programaticky vygenerovany** skriptem `generate_music.py` pomoci Python modulu `wave`. Jsou to originalni kompozice vytvorene syntetizovanymi vlnovymi formami (pulse, triangle, square wave). Zadna externi hudba nebyla pouzita. Bez licencnich omezeni.

### Textury
Vsechny sprite textury a pozadi byly **programaticky vygenerovany** skriptem `generate_sprites.py` pomoci Python knihovny Pillow. Zadne externi obrazky nebyly pouzity. Bez licencnich omezeni.

### Font
**Press Start 2P** - font od Cody "CodeMan38" Boisclair, licencovany pod [SIL Open Font License 1.1](https://scripts.sil.org/OFL). Volne pouzitelny vcetne komercniho pouziti.

### Framework
**LibGDX** - Apache License 2.0. **TeaVM** - Apache License 2.0.
