package kfs.easter.comp;

import kfs.easter.ecs.KfsComp;

import java.util.List;

public class TractorComp implements KfsComp {
    public List<int[]> path;
    public int pathIndex;
    public int pathDir;
    public float moveTimer;
    public float moveInterval;

    public TractorComp(List<int[]> path, float moveInterval) {
        this.path = path;
        this.pathIndex = 0;
        this.pathDir = 1;
        this.moveTimer = 0;
        this.moveInterval = moveInterval;
    }
}
