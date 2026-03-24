package kfs.easter.sys;

import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import kfs.easter.KfsConst;
import kfs.easter.Tile;
import kfs.easter.World;
import kfs.easter.comp.*;
import kfs.easter.ecs.Entity;
import kfs.easter.ecs.KfsSystem;

public class RenderSys implements KfsSystem {

    private final World world;
    private float deathBlinkTimer;

    public RenderSys(World world) {
        this.world = world;
    }

    @Override
    public void render(SpriteBatch batch) {
        if (world.isDying()) {
            deathBlinkTimer += 0.05f; // ~3 blinks/sec at 60fps
        }

        for (Entity e : world.getEntitiesWith(RenderComp.class, PositionComp.class)) {
            RenderComp rc = world.getComponent(e, RenderComp.class);
            PositionComp pos = world.getComponent(e, PositionComp.class);
            MovingComp mc = world.getComponent(e, MovingComp.class);

            // During death: blink the player sprite
            boolean isPlayer = rc.tile == Tile.RABBIT;
            if (world.isDying() && isPlayer && ((int)(deathBlinkTimer * 8) % 2 == 0)) {
                continue; // skip drawing = blink off
            }

            float drawX, drawY;
            if (mc != null) {
                drawX = mc.posX;
                drawY = mc.posY;
            } else {
                drawX = pos.x * KfsConst.TILE_SIZE;
                drawY = pos.y * KfsConst.TILE_SIZE;
            }

            Texture tex = resolveSprite(rc);
            if (tex == null) {
                tex = world.getTexture(rc.tile);
            }

            // During death: tint player red on visible frames
            if (world.isDying() && isPlayer) {
                batch.setColor(1f, 0.3f, 0.3f, 1f);
            }
            batch.draw(tex, drawX, drawY, KfsConst.TILE_SIZE, KfsConst.TILE_SIZE);
            if (world.isDying() && isPlayer) {
                batch.setColor(1f, 1f, 1f, 1f);
            }
        }
    }

    private Texture resolveSprite(RenderComp rc) {
        String prefix = getSpritePrefix(rc.tile);
        if (prefix == null) return null;

        // For eggs - no direction, just type
        if (rc.tile == Tile.EGG) return world.getSprite("egg_normal");
        if (rc.tile == Tile.GOLDEN_EGG) return world.getSprite("egg_golden");
        if (rc.tile == Tile.SPECIAL_EGG) return world.getSprite("egg_special");
        if (rc.tile == Tile.CHICKEN) return world.getSprite("chicken");

        // Directional sprites
        String suffix = getFacingSuffix(rc.facingX, rc.facingY);
        Texture tex = world.getSprite(prefix + "_" + suffix);
        if (tex != null) return tex;

        // Fallback to front
        tex = world.getSprite(prefix + "_front");
        return tex;
    }

    private String getSpritePrefix(Tile tile) {
        switch (tile) {
            case RABBIT: return "rabbit";
            case DOG: return "dog";
            case TRACTOR: return "tractor";
            case CHICKEN: return "chicken";
            case EGG: return "egg";
            case GOLDEN_EGG: return "egg";
            case SPECIAL_EGG: return "egg";
            default: return null;
        }
    }

    private String getFacingSuffix(int fx, int fy) {
        if (fx < 0) return "left";
        if (fx > 0) return "right";
        if (fy > 0) return "back";
        return "front"; // fy <= 0 or default
    }
}
