package kfs.easter.sys;

import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import kfs.easter.KfsConst;
import kfs.easter.World;
import kfs.easter.comp.*;
import kfs.easter.ecs.Entity;
import kfs.easter.ecs.KfsSystem;

public class RenderSys implements KfsSystem {

    private final World world;

    public RenderSys(World world) {
        this.world = world;
    }

    @Override
    public void render(SpriteBatch batch) {
        // Render all entities with RenderComp + PositionComp
        for (Entity e : world.getEntitiesWith(RenderComp.class, PositionComp.class)) {
            RenderComp rc = world.getComponent(e, RenderComp.class);
            PositionComp pos = world.getComponent(e, PositionComp.class);
            MovingComp mc = world.getComponent(e, MovingComp.class);

            float drawX, drawY;
            if (mc != null) {
                drawX = mc.posX;
                drawY = mc.posY;
            } else {
                drawX = pos.x * KfsConst.TILE_SIZE;
                drawY = pos.y * KfsConst.TILE_SIZE;
            }

            // Use placeholder texture
            batch.draw(world.getTexture(rc.tile), drawX, drawY,
                KfsConst.TILE_SIZE, KfsConst.TILE_SIZE);
        }
    }
}
