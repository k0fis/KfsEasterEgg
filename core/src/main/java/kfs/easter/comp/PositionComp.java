package kfs.easter.comp;

import kfs.easter.ecs.KfsComp;

public class PositionComp implements KfsComp {
    public int x;
    public int y;

    public PositionComp(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public final boolean equals(Object o) {
        if (!(o instanceof PositionComp)) return false;
        PositionComp that = (PositionComp) o;
        return x == that.x && y == that.y;
    }

    @Override
    public int hashCode() {
        return 31 * x + y;
    }
}
