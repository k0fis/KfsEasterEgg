package kfs.easter.sys;

import kfs.easter.Tile;
import kfs.easter.World;
import kfs.easter.comp.*;
import kfs.easter.ecs.Entity;
import kfs.easter.ecs.KfsSystem;

public class LevelSys implements KfsSystem {

    private final World world;

    public LevelSys(World world) {
        this.world = world;
    }

    @Override
    public void update(float delta) {
        if (world.isGameOver()) return;

        for (Entity e : world.getEntitiesWith(PlayerComp.class, PositionComp.class)) {
            PlayerComp player = world.getComponent(e, PlayerComp.class);
            PositionComp pos = world.getComponent(e, PositionComp.class);

            // Check if all eggs collected → open exit
            if (!world.isExitOpen() && player.eggsCollected >= player.totalEggs) {
                world.setExitOpen(true);
            }

            // Check if player reached open exit
            if (world.isExitOpen()) {
                Tile t = world.getTile(pos.x, pos.y);
                if (t == Tile.EXIT_OPEN) {
                    world.playSound("win");
                    world.gameOver(true);
                }
            }
        }
    }
}
