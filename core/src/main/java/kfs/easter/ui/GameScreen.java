package kfs.easter.ui;

import com.badlogic.gdx.Application;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.Color;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.*;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.utils.viewport.FitViewport;
import com.badlogic.gdx.utils.viewport.Viewport;
import kfs.easter.*;
import kfs.easter.comp.PlayerComp;
import kfs.easter.comp.PositionComp;
import kfs.easter.ecs.Entity;
import kfs.easter.sys.*;

public class GameScreen extends BaseScreen {

    private final OrthographicCamera camera;
    private final Viewport viewport;
    private final SpriteBatch batch;
    private World world;
    private Stage uiStage;
    private Label scoreLabel;
    private Label eggsLabel;
    private Label jumpLabel;
    private final String mapName;
    private Texture bgGame;

    public GameScreen(KfsMain game, String mapName) {
        super(game, false);
        this.mapName = mapName;

        camera = new OrthographicCamera();
        camera.setToOrtho(false, 1024, 768);
        viewport = new FitViewport(1024, 768, camera);
        viewport.apply();

        batch = new SpriteBatch();

        try {
            if (Gdx.files.internal("textures/bg_game.png").exists()) {
                bgGame = new Texture(Gdx.files.internal("textures/bg_game.png"));
            }
        } catch (Exception ignored) {}

        world = new World(win -> {
            if (win) {
                game.accumulatedScore = GameScreen.this.world.getScore();
                game.setScreen(new GameOverScreen(game, GameScreen.this.world.getScore(), mapName, true));
            } else {
                game.setScreen(new GameOverScreen(game, GameScreen.this.world.getScore(), mapName, false));
            }
        }, game.accumulatedScore);

        world.addSys(new InputSys(world));
        world.addSys(new MovingSys(world));
        world.addSys(new DogAISys(world));
        world.addSys(new TractorSys(world));
        world.addSys(new ChickenSys(world));
        world.addSys(new CollisionSys(world));
        world.addSys(new LevelSys(world));
        world.addSys(new RenderSys(world));

        setupUI();

        if (Gdx.app.getType() == Application.ApplicationType.WebGL) {
            world.getSystem(InputSys.class).setupTouchControls(uiStage, skin);
        }

        world.loadMap(mapName);
    }

    private void setupUI() {
        uiStage = new Stage(new FitViewport(1024, 768));
        Gdx.input.setInputProcessor(uiStage);

        Table table = new Table();
        table.setFillParent(true);
        table.top().pad(10);
        uiStage.addActor(table);

        Label.LabelStyle scoreStyle = new Label.LabelStyle(fontSmall, Color.YELLOW);
        scoreLabel = new Label("Score: 0", scoreStyle);
        table.add(scoreLabel).expandX().left();

        Label.LabelStyle eggsStyle = new Label.LabelStyle(fontSmall, Color.WHITE);
        eggsLabel = new Label("Eggs: 0/0", eggsStyle);
        table.add(eggsLabel).expandX().center();

        Label.LabelStyle jumpStyle = new Label.LabelStyle(fontSmall, Color.GREEN);
        jumpLabel = new Label("JUMP", jumpStyle);
        table.add(jumpLabel).expandX().center();

        TextButton.TextButtonStyle buttonStyle = getTextButtonStyle(fontSmall, Color.WHITE);
        TextButton exitButton = new TextButton("Menu", buttonStyle);
        exitButton.addListener(e -> {
            if (exitButton.isPressed()) game.setScreen(new LevelSelectScreen(game));
            return false;
        });
        table.add(exitButton).right();
    }

    @Override
    public void render(float delta) {
        world.update(delta);

        // Camera follow player
        for (Entity e : world.getEntitiesWith(PlayerComp.class, PositionComp.class)) {
            PositionComp pos = world.getComponent(e, PositionComp.class);
            float targetX = pos.x * KfsConst.TILE_SIZE + KfsConst.TILE_SIZE / 2f;
            float targetY = pos.y * KfsConst.TILE_SIZE + KfsConst.TILE_SIZE / 2f;
            camera.position.x += (targetX - camera.position.x) * KfsConst.CAMERA_SMOOTH;
            camera.position.y += (targetY - camera.position.y) * KfsConst.CAMERA_SMOOTH;
        }

        // Clamp camera to map bounds
        float halfW = viewport.getWorldWidth() / 2f;
        float halfH = viewport.getWorldHeight() / 2f;
        float mapPxW = world.getMapWidth() * KfsConst.TILE_SIZE;
        float mapPxH = world.getMapHeight() * KfsConst.TILE_SIZE;

        camera.position.x = Math.max(halfW, Math.min(mapPxW - halfW, camera.position.x));
        camera.position.y = Math.max(halfH, Math.min(mapPxH - halfH, camera.position.y));
        camera.update();

        ScreenUtils.clear(0.1f, 0.25f, 0.05f, 1);
        batch.setProjectionMatrix(camera.combined);
        batch.begin();
        // Draw background behind map
        if (bgGame != null) {
            float mapPxW2 = world.getMapWidth() * KfsConst.TILE_SIZE;
            float mapPxH2 = world.getMapHeight() * KfsConst.TILE_SIZE;
            batch.draw(bgGame, 0, 0, mapPxW2, mapPxH2);
        }
        world.render(batch);
        batch.end();

        // Update HUD
        scoreLabel.setText("Score: " + world.getScore());
        for (Entity e : world.getEntitiesWith(PlayerComp.class)) {
            PlayerComp pc = world.getComponent(e, PlayerComp.class);
            eggsLabel.setText("Eggs: " + pc.eggsCollected + "/" + pc.totalEggs);
            if (world.isExitOpen()) {
                eggsLabel.setColor(Color.GREEN);
            }
            if (pc.jumpCooldown <= 0) {
                jumpLabel.setText("JUMP [SPACE]");
                jumpLabel.setColor(Color.GREEN);
            } else {
                jumpLabel.setText("JUMP " + String.format("%.1f", pc.jumpCooldown));
                jumpLabel.setColor(Color.GRAY);
            }
        }

        uiStage.act(delta);
        uiStage.draw();
    }

    @Override
    public void resize(int width, int height) {
        viewport.update(width, height, true);
        uiStage.getViewport().update(width, height, true);
    }

    @Override
    public void dispose() {
        super.dispose();
        batch.dispose();
        uiStage.dispose();
        world.dispose();
        if (bgGame != null) bgGame.dispose();
    }
}
