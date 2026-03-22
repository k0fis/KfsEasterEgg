package kfs.easter.comp;

import kfs.easter.Tile;
import kfs.easter.ecs.KfsComp;

public class RenderComp implements KfsComp {
    public Tile tile;
    public int dx;

    public RenderComp(Tile tile) {
        this.tile = tile;
        this.dx = 0;
    }
}
