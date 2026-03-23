# KFS Easter Egg - Stav projektu

**Slot:** gm008 | **gameId:** kfs-easter-egg | **Package:** kfs.easter
**Repo:** https://github.com/k0fis/KfsEasterEgg.git
**Deploy:** https://kofis.eu/kuba/gm008/

## Hotovo

### Kód (37 Java souborů)
- [x] ECS framework (Entity, KfsComp, KfsSystem, KfsWorld)
- [x] 8 komponent (Position, Moving, Render, Player, Dog, Tractor, Chicken, Egg)
- [x] 8 systémů (Input, Moving, DogAI, Tractor, Chicken, Collision, Level, Render)
- [x] World.java - tile grid, loadMap(), placeholder textury (barevné Pixmap)
- [x] KfsMain.java - entry point, getMaps(), accumulatedScore
- [x] KfsConst.java - TILE_SIZE=48, 1024x768, rychlosti, scoring
- [x] Tile.java - 18 tile typů s char kódy a barvami
- [x] ScoreClient.java - HTTP klient pro leaderboard
- [x] MusicManager.java + SoundManager.java (kostry, bez souborů)

### Screeny (6)
- [x] BaseScreen - fonty 10/16/32, zelený styl
- [x] MainScreen - EASTER EGG title, Play/Leaderboard/Music/Quit, async hi-score
- [x] LevelSelectScreen - ScrollPane s 10 levely
- [x] GameScreen - kamera follow, HUD (score + eggs + menu), touch controls (WebGL)
- [x] GameOverScreen - win: name entry + submit + next level; lose: try again + menu
- [x] LeaderboardScreen - TOP 10 s gold/silver/bronze

### Launchery
- [x] Lwjgl3Launcher (1024x768, ANGLE_GLES20)
- [x] StartupHelper (macOS -XstartOnFirstThread)
- [x] TeaVMLauncher (responsive canvas)
- [x] TeaVMBuilder (JAVASCRIPT, ADVANCED optimization)

### Mapy (10 levelů, 30x20 tiles)
- [x] 01 Tutorial Farm - jen vejce, žádný nepřítel
- [x] 02 First Dog - 1 pes
- [x] 03 Muddy Path - bláto, seno
- [x] 04 Tractor Trouble - traktor na cestě
- [x] 05 Fences and Holes - ploty, díry
- [x] 06 Chicken Run - slepice + pes
- [x] 07 Double Dog - 2 psi
- [x] 08 Fast Tractor - rychlejší traktor
- [x] 09 Golden Farm - zlatá vejce, komplex mapa
- [x] 10 Easter Chaos - vše dohromady

### Herní mechaniky
- [x] Grid-based pohyb (šipky + WASD + touch + swipe)
- [x] Plynulá animace pohybu (lerp MovingComp)
- [x] Pes honí zajíce (manhattan AI)
- [x] Traktor jezdí po předdefinované cestě
- [x] Slepice chodí náhodně
- [x] Sbírání vajíček (normal=10, golden=50, special=25)
- [x] Win: všechna vejce → exit otevřen → doběhnout k X
- [x] Lose: srážka se psem nebo traktorem
- [x] Plot = přeskok na druhou stranu (2 tiles)
- [x] Díra = teleport zpět na start
- [x] Bláto = zpomalení
- [x] **Přeskakování nepřátel** - zajíc přeskočí psa/slepici (jako plot), ne traktor
- [x] Kamera sleduje hráče s clampem na mapu

### Build & CI/CD
- [x] Gradle multi-module (core, lwjgl3, teavm)
- [x] `./gradlew core:build` kompiluje
- [x] `.github/workflows/build.yml` - build + release + deploy
- [x] GitHub secrets (DEPLOY_SSH_KEY=id_kfs_deploy, PORT=8080, HOST=kofis.eu, USER=kofis)
- [x] CI zelené - deploy na gm008 funguje

### Leaderboard
- [x] GameId `KFS_EASTER_EGG("kfs-easter-egg", "Easter Egg")` registrován v kfsLeaderboard
- [x] kfsLeaderboard commit + push (auto-deploy)

## TODO

### Priorita 1 - Hratelnost
- [ ] **Otestovat desktop** (`./gradlew lwjgl3:run`) - ověřit že vše funguje end-to-end
- [ ] **Otestovat web** (`./gradlew teavm:build` + `teavm:run`) - ověřit TeaVM kompatibilitu
- [ ] Vyladit balancing map (obtížnost, rozmístění vajíček, rychlost nepřátel)
- [ ] Ověřit leaderboard submit funguje (score.kofis.eu přijímá kfs-easter-egg)

### Priorita 2 - Zvuky & hudba
- [ ] Stáhnout CC0 SFX z Kenney.nl (hop, egg_collect, dog_bark, tractor, hit, level_complete, game_over)
- [ ] Stáhnout CC0 spring/Easter chiptune (2-3 tracky z opengameart.org nebo Kenney Music Jingles)
- [ ] Konvertovat na WAV (SFX) a MP3 (music)
- [ ] Umístit do `assets/sounds/` a `assets/music/`
- [ ] Doplnit volání v SoundManager a MusicManager

### Priorita 3 - Grafika
- [ ] Vytvořit `startup-logo.png` (500x83, Easter themed)
- [ ] Vytvořit ikony `libgdx{16,32,64,128}.png`
- [ ] LeonardoAI prompty pro 48x48 pixel art sprites:
  - Rabbit (4 directions + idle)
  - Dog (4 directions)
  - Tractor (4 directions)
  - Chicken (2 frames)
  - Eggs (normal, golden, special)
  - Tiles: grass, bush, hay bale, fence, mud, hole, exit
- [ ] Nahradit placeholder Pixmap za sprite textury
- [ ] Thumbnail `gm008.jpg` pro kuba_games_index

### Priorita 4 - Index & finalizace
- [ ] Přidat gm008 card do `kuba_games_index`
- [ ] Push index → auto-deploy → kofis.eu/kuba/ ukazuje Easter Egg
- [ ] Finální test na kofis.eu/kuba/gm008/
