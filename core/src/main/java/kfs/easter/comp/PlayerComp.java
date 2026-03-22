package kfs.easter.comp;

import kfs.easter.ecs.KfsComp;

public class PlayerComp implements KfsComp {
    public int eggsCollected;
    public int totalEggs;
    public int score;
    public PowerUp activePower;
    public float powerTimer;
    public int startX;
    public int startY;

    public enum PowerUp {
        NONE, SPEED, INVISIBLE
    }

    public PlayerComp() {
        this.eggsCollected = 0;
        this.totalEggs = 0;
        this.score = 0;
        this.activePower = PowerUp.NONE;
        this.powerTimer = 0;
    }
}
