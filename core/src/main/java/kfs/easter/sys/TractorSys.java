package kfs.easter.sys;

import kfs.easter.KfsConst;
import kfs.easter.World;
import kfs.easter.comp.*;
import kfs.easter.ecs.Entity;
import kfs.easter.ecs.KfsSystem;

public class TractorSys implements KfsSystem {

    private final World world;

    public TractorSys(World world) {
        this.world = world;
    }

    @Override
    public void update(float delta) {
        if (world.isGameOver()) return;

        for (Entity e : world.getEntitiesWith(TractorComp.class, PositionComp.class)) {
            if (world.getComponent(e, MovingComp.class) != null) continue;

            TractorComp tc = world.getComponent(e, TractorComp.class);
            tc.moveTimer += delta;
            if (tc.moveTimer < tc.moveInterval) continue;
            tc.moveTimer = 0;

            if (tc.path == null || tc.path.size() < 2) continue;

            // Move along path
            tc.pathIndex += tc.pathDir;
            if (tc.pathIndex >= tc.path.size()) {
                tc.pathDir = -1;
                tc.pathIndex = tc.path.size() - 2;
            }
            if (tc.pathIndex < 0) {
                tc.pathDir = 1;
                tc.pathIndex = 1;
            }

            PositionComp pos = world.getComponent(e, PositionComp.class);
            int[] target = tc.path.get(tc.pathIndex);

            world.addComponent(e, new MovingComp(
                pos.x * KfsConst.TILE_SIZE, pos.y * KfsConst.TILE_SIZE,
                target[0] * KfsConst.TILE_SIZE, target[1] * KfsConst.TILE_SIZE,
                KfsConst.PLAYER_MOVE_SPEED));
            pos.x = target[0];
            pos.y = target[1];
        }
    }
}
