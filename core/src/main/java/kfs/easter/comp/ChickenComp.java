package kfs.easter.comp;

import kfs.easter.ecs.KfsComp;

public class ChickenComp implements KfsComp {
    public float moveTimer;

    public ChickenComp() {
        this.moveTimer = 0;
    }
}
