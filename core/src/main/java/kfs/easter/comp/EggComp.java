package kfs.easter.comp;

import kfs.easter.ecs.KfsComp;

public class EggComp implements KfsComp {

    public enum EggType {
        NORMAL, GOLDEN, SPECIAL
    }

    public final EggType type;

    public EggComp(EggType type) {
        this.type = type;
    }
}
