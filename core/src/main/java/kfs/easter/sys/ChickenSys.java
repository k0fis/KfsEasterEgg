package kfs.easter.sys;

import kfs.easter.KfsConst;
import kfs.easter.World;
import kfs.easter.comp.*;
import kfs.easter.ecs.Entity;
import kfs.easter.ecs.KfsSystem;

public class ChickenSys implements KfsSystem {

    private final World world;

    public ChickenSys(World world) {
        this.world = world;
    }

    @Override
    public void update(float delta) {
        if (world.isGameOver()) return;

        for (Entity e : world.getEntitiesWith(ChickenComp.class, PositionComp.class)) {
            if (world.getComponent(e, MovingComp.class) != null) continue;

            ChickenComp ch = world.getComponent(e, ChickenComp.class);
            ch.moveTimer += delta;
            if (ch.moveTimer < KfsConst.CHICKEN_MOVE_INTERVAL) continue;
            ch.moveTimer = 0;

            PositionComp pos = world.getComponent(e, PositionComp.class);

            // Random direction
            int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
            int[] dir = dirs[(int) (Math.random() * 4)];
            int newX = pos.x + dir[0];
            int newY = pos.y + dir[1];

            if (world.canMoveNPC(newX, newY)) {
                RenderComp rc = world.getComponent(e, RenderComp.class);
                if (rc != null) {
                    if (dir[0] != 0) { rc.facingX = dir[0]; rc.facingY = 0; }
                    else if (dir[1] != 0) { rc.facingY = dir[1]; rc.facingX = 0; }
                }
                world.addComponent(e, new MovingComp(
                    pos.x * KfsConst.TILE_SIZE, pos.y * KfsConst.TILE_SIZE,
                    newX * KfsConst.TILE_SIZE, newY * KfsConst.TILE_SIZE,
                    KfsConst.PLAYER_MOVE_SPEED * 0.5f));
                pos.x = newX;
                pos.y = newY;
            }
        }
    }
}
