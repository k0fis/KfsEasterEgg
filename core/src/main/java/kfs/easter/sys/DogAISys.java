package kfs.easter.sys;

import kfs.easter.KfsConst;
import kfs.easter.World;
import kfs.easter.comp.*;
import kfs.easter.ecs.Entity;
import kfs.easter.ecs.KfsSystem;

import java.util.List;

public class DogAISys implements KfsSystem {

    private final World world;

    public DogAISys(World world) {
        this.world = world;
    }

    @Override
    public void update(float delta) {
        if (world.isGameOver() || world.isDying()) return;

        // Use pre-frame player position so the dog targets where the player
        // WAS at the start of this frame, not where InputSys moved them.
        // This prevents diagonal "instant catch" when both move in the same frame.
        int playerX = world.getPreFramePlayerX();
        int playerY = world.getPreFramePlayerY();

        // Check if player is invisible (power-up)
        for (Entity pe : world.getEntitiesWith(PlayerComp.class)) {
            PlayerComp pc = world.getComponent(pe, PlayerComp.class);
            if (pc.activePower == PlayerComp.PowerUp.INVISIBLE) return;
        }
        if (playerX <= 0 && playerY <= 0) return;

        for (Entity e : world.getEntitiesWith(DogComp.class, PositionComp.class)) {
            if (world.getComponent(e, MovingComp.class) != null) continue;

            DogComp dog = world.getComponent(e, DogComp.class);
            dog.moveTimer += delta;
            if (dog.moveTimer < dog.moveInterval) continue;
            dog.moveTimer = 0;

            PositionComp pos = world.getComponent(e, PositionComp.class);

            // Simple AI: move toward player (manhattan distance)
            int dx = Integer.compare(playerX, pos.x);
            int dy = Integer.compare(playerY, pos.y);

            // Try horizontal first, then vertical
            int newX = pos.x + dx;
            int newY = pos.y + dy;

            if (dx != 0 && world.canMoveNPC(newX, pos.y)) {
                moveDog(e, pos, newX, pos.y);
            } else if (dy != 0 && world.canMoveNPC(pos.x, newY)) {
                moveDog(e, pos, pos.x, newY);
            }
        }
    }

    private void moveDog(Entity e, PositionComp pos, int newX, int newY) {
        RenderComp rc = world.getComponent(e, RenderComp.class);
        if (rc != null) {
            int dx = newX - pos.x;
            int dy = newY - pos.y;
            if (dx != 0) { rc.facingX = dx; rc.facingY = 0; }
            else if (dy != 0) { rc.facingY = dy; rc.facingX = 0; }
        }
        world.addComponent(e, new MovingComp(
            pos.x * KfsConst.TILE_SIZE, pos.y * KfsConst.TILE_SIZE,
            newX * KfsConst.TILE_SIZE, newY * KfsConst.TILE_SIZE,
            KfsConst.PLAYER_MOVE_SPEED * 0.8f));
        pos.x = newX;
        pos.y = newY;
    }
}
