package kfs.easter.comp;

import kfs.easter.ecs.KfsComp;

public class DogComp implements KfsComp {
    public float moveTimer;
    public float moveInterval;

    public DogComp(float moveInterval) {
        this.moveTimer = 0;
        this.moveInterval = moveInterval;
    }
}
