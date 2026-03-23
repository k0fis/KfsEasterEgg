# KFS Easter Egg - Stav projektu

**Slot:** gm008 | **gameId:** kfs-easter-egg | **Package:** kfs.easter
**Repo:** https://github.com/k0fis/KfsEasterEgg.git
**Deploy:** https://kofis.eu/kuba/gm008/

## Hotovo

### Kód (37 Java souborů)
- [x] ECS framework (Entity, KfsComp, KfsSystem, KfsWorld)
- [x] 8 komponent (Position, Moving, Render, Player, Dog, Tractor, Chicken, Egg)
- [x] 8 systémů (Input, Moving, DogAI, Tractor, Chicken, Collision, Level, Render)
- [x] World.java - tile grid, loadMap(), PNG textury s fallbackem na Pixmap placeholder
- [x] KfsMain.java - entry point, getMaps(), accumulatedScore
- [x] KfsConst.java - TILE_SIZE=48, 1024x768, rychlosti, scoring, jump params
- [x] Tile.java - 18 tile typů s char kódy a barvami
- [x] ScoreClient.java - HTTP klient pro leaderboard
- [x] MusicManager.java + SoundManager.java (kostry, bez souborů)

### Screeny (6)
- [x] BaseScreen - fonty 10/16/32, bg_menu.png pozadí (fallback zelený Pixmap)
- [x] MainScreen - EASTER EGG title, Play/Leaderboard/Music/Quit, async hi-score
- [x] LevelSelectScreen - ScrollPane s 10 levely
- [x] GameScreen - kamera follow, bg_game.png za mapou, HUD (score + eggs + jump + menu), touch controls
- [x] GameOverScreen - win: name entry + submit + next level; lose: try again + menu
- [x] LeaderboardScreen - TOP 10 s gold/silver/bronze

### Launchery
- [x] Lwjgl3Launcher (1024x768, ANGLE_GLES20)
- [x] StartupHelper (macOS -XstartOnFirstThread)
- [x] TeaVMLauncher (responsive canvas)
- [x] TeaVMBuilder (JAVASCRIPT, ADVANCED optimization)

### Mapy (10 levelů, 30x20 tiles)
- [x] 01-10 kompletní (Tutorial → Easter Chaos)

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
- [x] **Jump (Space / touch J)** - skok +3/+2/+1 ve směru facingu, 2s cooldown, přeskočí cokoliv
- [x] Kamera sleduje hráče s clampem na mapu

### Textury & grafika
- [x] generate_sprites.py - Pillow skript generující 28 PNG sprites (entity + terrain + bg)
- [x] Directional sprites (rabbit/dog/tractor front/back/left/right)
- [x] RenderSys - resolveSprite() s facingX/facingY
- [x] bg_menu.png, bg_game.png, splash.png, startup-logo.png
- [x] leonardo-prompts.md - Bing/DALL-E 3 prompty pro finální grafiku

### Web (TeaVM)
- [x] Splash screen (Easter Egg + "pro Kubu" + progress bar + fade-out)
- [x] Touch controls (D-pad + Jump) s 25% průhledností
- [x] copyResources v build.gradle (custom index.html se správně nasazuje)

### Build & CI/CD
- [x] Gradle multi-module (core, lwjgl3, teavm)
- [x] `.github/workflows/build.yml` - build + release + deploy
- [x] GitHub secrets (DEPLOY_SSH_KEY=id_kfs_deploy, PORT=8080, HOST=kofis.eu, USER=kofis)
- [x] CI zelené - deploy na gm008 funguje
- [x] SSL certifikáty opraveny (IPv6 VirtualHost)

### Leaderboard
- [x] GameId `KFS_EASTER_EGG("kfs-easter-egg", "Easter Egg")` registrován v kfsLeaderboard
- [x] kfsLeaderboard commit + push (auto-deploy)

## TODO

### Priorita 1 - Testování
- [ ] Otestovat desktop (`./gradlew lwjgl3:run`) - end-to-end gameplay
- [ ] Otestovat web (kofis.eu/kuba/gm008/) - TeaVM kompatibilita
- [ ] Ověřit leaderboard submit (score.kofis.eu přijímá kfs-easter-egg)
- [ ] Vyladit balancing (obtížnost, rychlost nepřátel, rozmístění vajíček)

### Priorita 2 - Zvuky & hudba
- [ ] CC0 SFX z Kenney.nl (hop, egg_collect, dog_bark, tractor, hit, level_complete, game_over)
- [ ] CC0 spring/Easter chiptune (2-3 tracky)
- [ ] Doplnit volání v SoundManager a MusicManager

### Priorita 3 - Vylepšení grafiky
- [ ] Nahradit programatické sprites za AI-generované (Bing/DALL-E 3)
- [ ] Thumbnail `gm008.jpg` pro kuba_games_index

### Priorita 4 - Index & finalizace
- [ ] Přidat gm008 card do `kuba_games_index`
- [ ] Finální test na kofis.eu/kuba/gm008/
