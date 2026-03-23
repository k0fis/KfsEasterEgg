package kfs.easter.comp;

import kfs.easter.Tile;
import kfs.easter.ecs.KfsComp;

public class RenderComp implements KfsComp {
    public Tile tile;
    public int facingX;  // -1=left, 0=neutral, 1=right
    public int facingY;  // -1=down, 0=neutral, 1=up

    public RenderComp(Tile tile) {
        this.tile = tile;
        this.facingX = 0;
        this.facingY = -1; // default facing down/front
    }
}
