package kfs.easter.sys;

import kfs.easter.KfsConst;
import kfs.easter.World;
import kfs.easter.comp.*;
import kfs.easter.ecs.Entity;
import kfs.easter.ecs.KfsSystem;

public class CollisionSys implements KfsSystem {

    private final World world;

    public CollisionSys(World world) {
        this.world = world;
    }

    @Override
    public void update(float delta) {
        if (world.isGameOver()) return;

        for (Entity pe : world.getEntitiesWith(PlayerComp.class, PositionComp.class)) {
            PlayerComp player = world.getComponent(pe, PlayerComp.class);
            PositionComp playerPos = world.getComponent(pe, PositionComp.class);

            // Update power-up timer
            if (player.activePower != PlayerComp.PowerUp.NONE) {
                player.powerTimer -= delta;
                if (player.powerTimer <= 0) {
                    player.activePower = PlayerComp.PowerUp.NONE;
                }
            }

            // Check egg collection
            for (Entity ee : world.getEntitiesWith(EggComp.class, PositionComp.class)) {
                PositionComp eggPos = world.getComponent(ee, PositionComp.class);
                if (eggPos.x == playerPos.x && eggPos.y == playerPos.y) {
                    EggComp egg = world.getComponent(ee, EggComp.class);
                    switch (egg.type) {
                        case NORMAL:
                            player.score += KfsConst.SCORE_EGG_NORMAL;
                            break;
                        case GOLDEN:
                            player.score += KfsConst.SCORE_EGG_GOLDEN;
                            break;
                        case SPECIAL:
                            player.score += KfsConst.SCORE_EGG_SPECIAL;
                            player.activePower = PlayerComp.PowerUp.SPEED;
                            player.powerTimer = 5f;
                            break;
                    }
                    player.eggsCollected++;
                    world.deleteEntity(ee);
                    break;
                }
            }

            // Check dog collision
            if (player.activePower != PlayerComp.PowerUp.INVISIBLE) {
                for (Entity de : world.getEntitiesWith(DogComp.class, PositionComp.class)) {
                    PositionComp dogPos = world.getComponent(de, PositionComp.class);
                    if (dogPos.x == playerPos.x && dogPos.y == playerPos.y) {
                        world.gameOver(false);
                        return;
                    }
                }
            }

            // Check tractor collision
            for (Entity te : world.getEntitiesWith(TractorComp.class, PositionComp.class)) {
                PositionComp tractorPos = world.getComponent(te, PositionComp.class);
                if (tractorPos.x == playerPos.x && tractorPos.y == playerPos.y) {
                    world.gameOver(false);
                    return;
                }
            }
        }
    }
}
