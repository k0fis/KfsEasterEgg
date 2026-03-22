package kfs.easter.sys;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.input.GestureDetector;
import com.badlogic.gdx.scenes.scene2d.InputEvent;
import com.badlogic.gdx.scenes.scene2d.Stage;
import com.badlogic.gdx.scenes.scene2d.ui.Skin;
import com.badlogic.gdx.scenes.scene2d.ui.TextButton;
import com.badlogic.gdx.scenes.scene2d.utils.ClickListener;
import kfs.easter.*;
import kfs.easter.comp.*;
import kfs.easter.ecs.Entity;
import kfs.easter.ecs.KfsSystem;

public class InputSys implements KfsSystem {

    private final World world;
    private int touchDx, touchDy;
    private int swipeDx, swipeDy;

    public InputSys(World world) {
        this.world = world;

        GestureDetector gd = new GestureDetector(new GestureDetector.GestureAdapter() {
            @Override
            public boolean fling(float velocityX, float velocityY, int button) {
                if (Math.abs(velocityX) > Math.abs(velocityY)) {
                    swipeDx = velocityX > 0 ? 1 : -1;
                    swipeDy = 0;
                } else {
                    swipeDx = 0;
                    swipeDy = velocityY > 0 ? 1 : -1;
                }
                return true;
            }

            @Override
            public boolean touchDown(float x, float y, int pointer, int button) {
                swipeDx = 0;
                swipeDy = 0;
                return false;
            }
        });
        Gdx.input.setInputProcessor(gd);
    }

    public void setupTouchControls(Stage stage, Skin skin) {
        int size = 80;
        int padding = 10;
        int baseX = padding;
        int baseY = padding;

        TextButton up = new TextButton("U", skin);
        up.setBounds(baseX + size, baseY + size * 2, size, size);
        up.addListener(new ClickListener() {
            @Override public boolean touchDown(InputEvent event, float x, float y, int pointer, int button) {
                touchDy = 1; return true;
            }
            @Override public void touchUp(InputEvent event, float x, float y, int pointer, int button) {
                touchDy = 0;
            }
        });

        TextButton down = new TextButton("D", skin);
        down.setBounds(baseX + size, baseY, size, size);
        down.addListener(new ClickListener() {
            @Override public boolean touchDown(InputEvent event, float x, float y, int pointer, int button) {
                touchDy = -1; return true;
            }
            @Override public void touchUp(InputEvent event, float x, float y, int pointer, int button) {
                touchDy = 0;
            }
        });

        TextButton left = new TextButton("L", skin);
        left.setBounds(baseX, baseY + size, size, size);
        left.addListener(new ClickListener() {
            @Override public boolean touchDown(InputEvent event, float x, float y, int pointer, int button) {
                touchDx = -1; return true;
            }
            @Override public void touchUp(InputEvent event, float x, float y, int pointer, int button) {
                touchDx = 0;
            }
        });

        TextButton right = new TextButton("R", skin);
        right.setBounds(baseX + size * 2, baseY + size, size, size);
        right.addListener(new ClickListener() {
            @Override public boolean touchDown(InputEvent event, float x, float y, int pointer, int button) {
                touchDx = 1; return true;
            }
            @Override public void touchUp(InputEvent event, float x, float y, int pointer, int button) {
                touchDx = 0;
            }
        });

        stage.addActor(up);
        stage.addActor(down);
        stage.addActor(left);
        stage.addActor(right);
    }

    @Override
    public void update(float delta) {
        if (world.isGameOver()) return;

        for (Entity e : world.getEntitiesWith(PlayerComp.class, PositionComp.class)) {
            if (world.getComponent(e, MovingComp.class) != null) continue;

            PositionComp pos = world.getComponent(e, PositionComp.class);
            int dx = 0, dy = 0;

            if (Gdx.input.isKeyPressed(Input.Keys.LEFT) || Gdx.input.isKeyPressed(Input.Keys.A)) dx = -1;
            if (Gdx.input.isKeyPressed(Input.Keys.RIGHT) || Gdx.input.isKeyPressed(Input.Keys.D)) dx = 1;
            if (Gdx.input.isKeyPressed(Input.Keys.UP) || Gdx.input.isKeyPressed(Input.Keys.W)) dy = 1;
            if (Gdx.input.isKeyPressed(Input.Keys.DOWN) || Gdx.input.isKeyPressed(Input.Keys.S)) dy = -1;

            if (touchDx != 0) dx = touchDx;
            if (touchDy != 0) dy = touchDy;
            if (swipeDx != 0) dx = swipeDx;
            if (swipeDy != 0) dy = swipeDy;
            swipeDx = 0;
            swipeDy = 0;

            if (dx != 0 || dy != 0) {
                handleMovement(e, pos, dx, dy);
            }
        }
    }

    private void handleMovement(Entity e, PositionComp pos, int dx, int dy) {
        int newX = pos.x + dx;
        int newY = pos.y + dy;

        Tile target = world.getTile(newX, newY);

        // Fence: jump over to the other side
        if (target == Tile.FENCE) {
            int jumpX = newX + dx;
            int jumpY = newY + dy;
            if (world.canMove(jumpX, jumpY)) {
                move(e, pos, jumpX, jumpY);
                return;
            }
            return;
        }

        // Hole: teleport back to start
        if (target == Tile.HOLE) {
            PlayerComp pc = world.getComponent(e, PlayerComp.class);
            move(e, pos, pc.startX, pc.startY);
            return;
        }

        // Exit: only if open
        if (target == Tile.EXIT_OPEN) {
            move(e, pos, newX, newY);
            return;
        }
        if (target == Tile.EXIT_CLOSED) {
            return;
        }

        if (world.canMove(newX, newY)) {
            // Dog or chicken at target: jump over (like fence)
            if (world.hasDogAt(newX, newY) || world.hasChickenAt(newX, newY)) {
                int jumpX = newX + dx;
                int jumpY = newY + dy;
                if (world.canMove(jumpX, jumpY) && !world.hasDogAt(jumpX, jumpY)
                    && !world.hasTractorAt(jumpX, jumpY)) {
                    move(e, pos, jumpX, jumpY);
                    return;
                }
                // Can't jump over — don't move (would die)
                return;
            }
            move(e, pos, newX, newY);
        }
    }

    private void move(Entity e, PositionComp pos, int newX, int newY) {
        PlayerComp pc = world.getComponent(e, PlayerComp.class);
        float speed = KfsConst.PLAYER_MOVE_SPEED;
        // Mud slows down
        if (world.getTile(newX, newY) == Tile.MUD) {
            speed *= KfsConst.MUD_SPEED_MULTIPLIER;
        }

        world.addComponent(e, new MovingComp(
            pos.x * KfsConst.TILE_SIZE, pos.y * KfsConst.TILE_SIZE,
            newX * KfsConst.TILE_SIZE, newY * KfsConst.TILE_SIZE, speed));
        pos.x = newX;
        pos.y = newY;

        if (world.getComponent(e, RenderComp.class) != null) {
            // Update facing direction for rendering
        }
    }
}
