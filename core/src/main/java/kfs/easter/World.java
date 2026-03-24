package kfs.easter;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.Pixmap;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import kfs.easter.comp.*;
import kfs.easter.ecs.Entity;
import kfs.easter.ecs.KfsSystem;
import kfs.easter.ecs.KfsWorld;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.*;
import java.util.function.Consumer;

public class World extends KfsWorld {

    private final Consumer<Boolean> gameOverCallback;
    private Tile[][] tiles;
    private int mapWidth;
    private int mapHeight;
    private boolean gameOver;
    private boolean levelComplete;
    private boolean dying;
    private float deathTimer;
    private boolean exitOpen;
    private final Map<Tile, Texture> textures;
    private final Map<String, Texture> spriteTextures;
    private int accumulatedScore;
    private SoundManager soundManager;
    private int preFramePlayerX, preFramePlayerY;

    public World(Consumer<Boolean> gameOverCallback, int accumulatedScore) {
        this.gameOverCallback = gameOverCallback;
        this.accumulatedScore = accumulatedScore;
        this.textures = loadTileTextures();
        this.spriteTextures = loadSpriteTextures();
    }

    public void loadMap(String file) {
        reset();
        gameOver = false;
        levelComplete = false;
        exitOpen = false;

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(
            Gdx.files.internal(file).read()))) {
            String[] lines = reader.lines().toArray(String[]::new);
            int height = lines.length;
            int width = lines[0].length();
            mapWidth = width;
            mapHeight = height;
            tiles = new Tile[width][height];

            int totalEggs = 0;
            List<int[]> tractorPath = new ArrayList<>();

            for (int y = 0; y < height; y++) {
                String line = lines[height - 1 - y];
                for (int x = 0; x < Math.min(line.length(), width); x++) {
                    char c = line.charAt(x);
                    Tile tile = Tile.fromCode(c);
                    tiles[x][y] = tile;

                    switch (tile) {
                        case RABBIT: {
                            Entity p = createEntity();
                            PlayerComp pc = new PlayerComp();
                            pc.startX = x;
                            pc.startY = y;
                            addComponent(p, pc);
                            addComponent(p, new PositionComp(x, y));
                            addComponent(p, new RenderComp(Tile.RABBIT));
                            tiles[x][y] = Tile.GRASS;
                            break;
                        }
                        case DOG: {
                            Entity d = createEntity();
                            addComponent(d, new DogComp(KfsConst.DOG_MOVE_INTERVAL));
                            addComponent(d, new PositionComp(x, y));
                            addComponent(d, new RenderComp(Tile.DOG));
                            tiles[x][y] = Tile.GRASS;
                            break;
                        }
                        case EGG: {
                            Entity e = createEntity();
                            addComponent(e, new EggComp(EggComp.EggType.NORMAL));
                            addComponent(e, new PositionComp(x, y));
                            addComponent(e, new RenderComp(Tile.EGG));
                            totalEggs++;
                            tiles[x][y] = Tile.GRASS;
                            break;
                        }
                        case GOLDEN_EGG: {
                            Entity e = createEntity();
                            addComponent(e, new EggComp(EggComp.EggType.GOLDEN));
                            addComponent(e, new PositionComp(x, y));
                            addComponent(e, new RenderComp(Tile.GOLDEN_EGG));
                            totalEggs++;
                            tiles[x][y] = Tile.GRASS;
                            break;
                        }
                        case SPECIAL_EGG: {
                            Entity e = createEntity();
                            addComponent(e, new EggComp(EggComp.EggType.SPECIAL));
                            addComponent(e, new PositionComp(x, y));
                            addComponent(e, new RenderComp(Tile.SPECIAL_EGG));
                            totalEggs++;
                            tiles[x][y] = Tile.GRASS;
                            break;
                        }
                        case TRACTOR: {
                            tiles[x][y] = Tile.PATH_X;
                            tractorPath.add(new int[]{x, y});
                            break;
                        }
                        case CHICKEN: {
                            Entity ch = createEntity();
                            addComponent(ch, new ChickenComp());
                            addComponent(ch, new PositionComp(x, y));
                            addComponent(ch, new RenderComp(Tile.CHICKEN));
                            tiles[x][y] = Tile.GRASS;
                            break;
                        }
                        case PATH_H:
                        case PATH_V:
                        case PATH_X:
                            tractorPath.add(new int[]{x, y});
                            break;
                    }
                }
            }

            // Set total eggs on player
            for (Entity e : getEntitiesWith(PlayerComp.class)) {
                PlayerComp pc = getComponent(e, PlayerComp.class);
                pc.totalEggs = totalEggs;
                pc.score = accumulatedScore;
            }

            // Create tractor entity if path exists
            if (!tractorPath.isEmpty()) {
                // Sort path to form a continuous route
                List<int[]> sortedPath = buildTractorPath(tractorPath);
                if (!sortedPath.isEmpty()) {
                    Entity t = createEntity();
                    addComponent(t, new TractorComp(sortedPath, KfsConst.TRACTOR_MOVE_INTERVAL));
                    addComponent(t, new PositionComp(sortedPath.get(0)[0], sortedPath.get(0)[1]));
                    addComponent(t, new RenderComp(Tile.TRACTOR));
                }
            }

        } catch (Exception e) {
            Gdx.app.error("World", "Failed to load map: " + e.getMessage());
        }
    }

    private List<int[]> buildTractorPath(List<int[]> pathTiles) {
        if (pathTiles.isEmpty()) return pathTiles;
        List<int[]> sorted = new ArrayList<>();
        Set<String> remaining = new LinkedHashSet<>();
        Map<String, int[]> byKey = new HashMap<>();

        for (int[] p : pathTiles) {
            String key = p[0] + "," + p[1];
            remaining.add(key);
            byKey.put(key, p);
        }

        // Start from first tile
        int[] current = pathTiles.get(0);
        sorted.add(current);
        remaining.remove(current[0] + "," + current[1]);

        while (!remaining.isEmpty()) {
            boolean found = false;
            int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
            for (int[] d : dirs) {
                String key = (current[0] + d[0]) + "," + (current[1] + d[1]);
                if (remaining.contains(key)) {
                    current = byKey.get(key);
                    sorted.add(current);
                    remaining.remove(key);
                    found = true;
                    break;
                }
            }
            if (!found) break;
        }
        return sorted;
    }

    @Override
    public void render(SpriteBatch batch) {
        // Draw tile map
        for (int x = 0; x < mapWidth; x++) {
            for (int y = 0; y < mapHeight; y++) {
                Tile t = tiles[x][y];
                batch.draw(textures.get(t), x * KfsConst.TILE_SIZE, y * KfsConst.TILE_SIZE,
                    KfsConst.TILE_SIZE, KfsConst.TILE_SIZE);
            }
        }
        // Draw entities on top
        super.render(batch);
    }

    public Tile[][] getTiles() { return tiles; }
    public int getMapWidth() { return mapWidth; }
    public int getMapHeight() { return mapHeight; }

    public Tile getTile(int x, int y) {
        if (x < 0 || y < 0 || x >= mapWidth || y >= mapHeight) return Tile.BUSH;
        return tiles[x][y];
    }

    public void setTile(int x, int y, Tile tile) {
        if (x >= 0 && y >= 0 && x < mapWidth && y < mapHeight) {
            tiles[x][y] = tile;
        }
    }

    public boolean canMove(int x, int y) {
        Tile t = getTile(x, y);
        return t != Tile.BUSH && t != Tile.HAY_BALE && t != Tile.EXIT_CLOSED;
    }

    public boolean hasDogAt(int x, int y) {
        for (Entity e : getEntitiesWith(DogComp.class, PositionComp.class)) {
            PositionComp p = getComponent(e, PositionComp.class);
            if (p.x == x && p.y == y) return true;
        }
        return false;
    }

    public boolean hasChickenAt(int x, int y) {
        for (Entity e : getEntitiesWith(ChickenComp.class, PositionComp.class)) {
            PositionComp p = getComponent(e, PositionComp.class);
            if (p.x == x && p.y == y) return true;
        }
        return false;
    }

    public boolean hasTractorAt(int x, int y) {
        for (Entity e : getEntitiesWith(TractorComp.class, PositionComp.class)) {
            PositionComp p = getComponent(e, PositionComp.class);
            if (p.x == x && p.y == y) return true;
        }
        return false;
    }

    public boolean canMoveNPC(int x, int y) {
        Tile t = getTile(x, y);
        return t == Tile.GRASS || t == Tile.PATH_H || t == Tile.PATH_V || t == Tile.PATH_X;
    }

    @Override
    public void update(float delta) {
        // Death sequence: count down, then trigger actual game over
        if (dying) {
            deathTimer -= delta;
            if (deathTimer <= 0) {
                dying = false;
                gameOver(false);
            }
            return;
        }

        // Save player position before systems run — DogAISys uses this
        // so the dog targets where the player WAS, not where they moved to
        for (Entity e : getEntitiesWith(PlayerComp.class, PositionComp.class)) {
            PositionComp pp = getComponent(e, PositionComp.class);
            preFramePlayerX = pp.x;
            preFramePlayerY = pp.y;
        }
        super.update(delta);
    }

    public int getPreFramePlayerX() { return preFramePlayerX; }
    public int getPreFramePlayerY() { return preFramePlayerY; }

    public int getScore() {
        for (Entity e : getEntitiesWith(PlayerComp.class)) {
            return getComponent(e, PlayerComp.class).score;
        }
        return 0;
    }

    public boolean isExitOpen() { return exitOpen; }

    public void setExitOpen(boolean open) {
        this.exitOpen = open;
        if (open) {
            // Replace EXIT_CLOSED with EXIT_OPEN on map
            for (int x = 0; x < mapWidth; x++) {
                for (int y = 0; y < mapHeight; y++) {
                    if (tiles[x][y] == Tile.EXIT_CLOSED) {
                        tiles[x][y] = Tile.EXIT_OPEN;
                    }
                }
            }
        }
    }

    public void setSoundManager(SoundManager sm) { this.soundManager = sm; }
    public void playSound(String name) { if (soundManager != null) soundManager.play(name); }

    public boolean isGameOver() { return gameOver; }
    public boolean isDying() { return dying; }
    public boolean isLevelComplete() { return levelComplete; }

    public void startDying() {
        if (dying || gameOver) return;
        dying = true;
        deathTimer = KfsConst.DEATH_DELAY;
        playSound("hit");
    }

    public void gameOver(boolean win) {
        if (gameOver) return;
        gameOver = true;
        levelComplete = win;
        if (win) {
            for (Entity e : getEntitiesWith(PlayerComp.class)) {
                getComponent(e, PlayerComp.class).score += KfsConst.SCORE_LEVEL_COMPLETE;
            }
        }
        gameOverCallback.accept(win);
    }

    public Texture getTexture(Tile tile) {
        return textures.get(tile);
    }

    /** Get directional sprite for an entity (e.g. "rabbit_front", "dog_left"). */
    public Texture getSprite(String key) {
        return spriteTextures.getOrDefault(key, null);
    }

    public void dispose() {
        textures.values().forEach(Texture::dispose);
        spriteTextures.values().forEach(Texture::dispose);
        runSystems(KfsSystem::done);
    }

    private Texture loadTexture(String path) {
        try {
            if (Gdx.files.internal(path).exists()) {
                return new Texture(Gdx.files.internal(path));
            }
        } catch (Exception e) {
            // fall through to placeholder
        }
        return null;
    }

    private Texture makePlaceholder(Color color) {
        Pixmap pm = new Pixmap(KfsConst.TILE_SIZE, KfsConst.TILE_SIZE, Pixmap.Format.RGBA8888);
        pm.setColor(color);
        pm.fill();
        pm.setColor(new Color(color.r * 0.7f, color.g * 0.7f, color.b * 0.7f, 1));
        pm.drawRectangle(0, 0, KfsConst.TILE_SIZE, KfsConst.TILE_SIZE);
        Texture t = new Texture(pm);
        pm.dispose();
        return t;
    }

    private Map<Tile, Texture> loadTileTextures() {
        Map<Tile, Texture> map = new HashMap<>();
        // Mapping: tile enum -> texture file
        Map<Tile, String> fileMap = new HashMap<>();
        fileMap.put(Tile.GRASS, "textures/tile_grass.png");
        fileMap.put(Tile.BUSH, "textures/tile_bush.png");
        fileMap.put(Tile.HAY_BALE, "textures/tile_hay.png");
        fileMap.put(Tile.FENCE, "textures/tile_fence.png");
        fileMap.put(Tile.MUD, "textures/tile_mud.png");
        fileMap.put(Tile.HOLE, "textures/tile_hole.png");
        fileMap.put(Tile.PATH_H, "textures/tile_path.png");
        fileMap.put(Tile.PATH_V, "textures/tile_path.png");
        fileMap.put(Tile.PATH_X, "textures/tile_path.png");
        fileMap.put(Tile.EXIT_CLOSED, "textures/tile_exit_closed.png");
        fileMap.put(Tile.EXIT_OPEN, "textures/tile_exit_open.png");

        for (Tile t : Tile.values()) {
            String file = fileMap.get(t);
            Texture tex = (file != null) ? loadTexture(file) : null;
            map.put(t, tex != null ? tex : makePlaceholder(t.color));
        }
        return map;
    }

    private Map<String, Texture> loadSpriteTextures() {
        Map<String, Texture> map = new HashMap<>();
        String[] sprites = {
            "rabbit_front", "rabbit_back", "rabbit_left", "rabbit_right",
            "dog_front", "dog_back", "dog_left", "dog_right",
            "tractor_right", "tractor_left", "tractor_front",
            "chicken",
            "egg_normal", "egg_golden", "egg_special"
        };
        for (String name : sprites) {
            Texture tex = loadTexture("textures/" + name + ".png");
            if (tex != null) {
                map.put(name, tex);
            }
        }
        return map;
    }
}
