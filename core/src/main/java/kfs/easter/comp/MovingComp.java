package kfs.easter.comp;

import kfs.easter.ecs.KfsComp;

public class MovingComp implements KfsComp {
    public float posX;
    public float posY;
    public final float targetX;
    public final float targetY;
    public final float speed;

    public MovingComp(float posX, float posY, float targetX, float targetY, float speed) {
        this.posX = posX;
        this.posY = posY;
        this.targetX = targetX;
        this.targetY = targetY;
        this.speed = speed;
    }
}
