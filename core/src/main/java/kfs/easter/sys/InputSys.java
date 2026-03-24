package kfs.easter.sys;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.graphics.Color;
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
    private boolean jumpRequested;
    private boolean touchJumpRequested;

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

        // Jump button - right side of screen
        TextButton jump = new TextButton("J", skin);
        int jumpX = (int) stage.getWidth() - padding - size;
        jump.setBounds(jumpX, baseY + size, size, size);
        jump.addListener(new ClickListener() {
            @Override public boolean touchDown(InputEvent event, float x, float y, int pointer, int button) {
                touchJumpRequested = true; return true;
            }
        });

        Color transparent = new Color(1, 1, 1, 0.25f);
        up.setColor(transparent);
        down.setColor(transparent);
        left.setColor(transparent);
        right.setColor(transparent);
        jump.setColor(transparent);

        stage.addActor(up);
        stage.addActor(down);
        stage.addActor(left);
        stage.addActor(right);
        stage.addActor(jump);
    }

    @Override
    public void update(float delta) {
        if (world.isGameOver()) return;

        // Accumulate jump request before entity loop — isKeyJustPressed is true
        // for only one frame, but the player may be mid-move animation (MovingComp)
        // on that frame, so we buffer it until the player can actually act.
        if (Gdx.input.isKeyJustPressed(Input.Keys.SPACE) || touchJumpRequested) {
            jumpRequested = true;
        }
        touchJumpRequested = false;

        for (Entity e : world.getEntitiesWith(PlayerComp.class, PositionComp.class)) {
            if (world.getComponent(e, MovingComp.class) != null) continue;

            PlayerComp pc = world.getComponent(e, PlayerComp.class);
            pc.jumpCooldown = Math.max(0, pc.jumpCooldown - delta);

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

            if (jumpRequested) {
                jumpRequested = false;
                if (pc.jumpCooldown <= 0) {
                    RenderComp rc = world.getComponent(e, RenderComp.class);
                    int jdx = rc != null ? rc.facingX : 0;
                    int jdy = rc != null ? rc.facingY : -1;
                    if (handleJump(e, pos, pc, jdx, jdy)) {
                        continue;
                    }
                }
            }

            if (dx != 0 || dy != 0) {
                handleMovement(e, pos, dx, dy);
            }
        }
    }

    private boolean handleJump(Entity e, PositionComp pos, PlayerComp pc, int dx, int dy) {
        // Try +3, then +2, then +1
        for (int dist = KfsConst.JUMP_MAX_DISTANCE; dist >= 1; dist--) {
            int targetX = pos.x + dx * dist;
            int targetY = pos.y + dy * dist;
            if (canJumpTo(targetX, targetY)) {
                pc.jumpCooldown = KfsConst.JUMP_COOLDOWN;
                jump(e, pos, targetX, targetY);
                return true;
            }
        }
        return false;
    }

    private boolean canJumpTo(int x, int y) {
        Tile tile = world.getTile(x, y);
        if (tile == null) return false;
        if (tile == Tile.BUSH || tile == Tile.HAY_BALE || tile == Tile.FENCE) return false;
        if (tile == Tile.EXIT_CLOSED) return false;
        if (world.hasDogAt(x, y) || world.hasTractorAt(x, y)) return false;
        return true;
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
            move(e, pos, newX, newY);
        }
    }

    private void move(Entity e, PositionComp pos, int newX, int newY) {
        float speed = KfsConst.PLAYER_MOVE_SPEED;
        if (world.getTile(newX, newY) == Tile.MUD) {
            speed *= KfsConst.MUD_SPEED_MULTIPLIER;
        }
        world.playSound("hop");

        RenderComp rc = world.getComponent(e, RenderComp.class);
        if (rc != null) {
            int dx = newX - pos.x;
            int dy = newY - pos.y;
            if (dx != 0) { rc.facingX = dx > 0 ? 1 : -1; rc.facingY = 0; }
            else if (dy != 0) { rc.facingY = dy > 0 ? 1 : -1; rc.facingX = 0; }
        }

        world.addComponent(e, new MovingComp(
            pos.x * KfsConst.TILE_SIZE, pos.y * KfsConst.TILE_SIZE,
            newX * KfsConst.TILE_SIZE, newY * KfsConst.TILE_SIZE, speed));
        pos.x = newX;
        pos.y = newY;
    }

    private void jump(Entity e, PositionComp pos, int newX, int newY) {
        world.playSound("hop");
        RenderComp rc = world.getComponent(e, RenderComp.class);
        if (rc != null) {
            int dx = newX - pos.x;
            int dy = newY - pos.y;
            if (dx != 0) { rc.facingX = dx > 0 ? 1 : -1; rc.facingY = 0; }
            else if (dy != 0) { rc.facingY = dy > 0 ? 1 : -1; rc.facingX = 0; }
        }

        float speed = KfsConst.PLAYER_MOVE_SPEED * KfsConst.JUMP_SPEED_MULTIPLIER;
        world.addComponent(e, new MovingComp(
            pos.x * KfsConst.TILE_SIZE, pos.y * KfsConst.TILE_SIZE,
            newX * KfsConst.TILE_SIZE, newY * KfsConst.TILE_SIZE, speed));
        pos.x = newX;
        pos.y = newY;
    }
}
