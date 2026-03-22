package kfs.easter;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.audio.Sound;

import java.util.HashMap;
import java.util.Map;

public class SoundManager {

    private final Map<String, Sound> sounds = new HashMap<>();
    private boolean enabled = true;

    public SoundManager() {
        loadSound("hop", "sounds/hop.wav");
        loadSound("egg", "sounds/egg.wav");
        loadSound("golden", "sounds/golden.wav");
        loadSound("hit", "sounds/hit.wav");
        loadSound("win", "sounds/win.wav");
        loadSound("lose", "sounds/lose.wav");
    }

    private void loadSound(String name, String path) {
        try {
            if (Gdx.files.internal(path).exists()) {
                sounds.put(name, Gdx.audio.newSound(Gdx.files.internal(path)));
            }
        } catch (Exception e) {
            Gdx.app.log("SoundManager", "Could not load " + path);
        }
    }

    public void play(String name) {
        if (!enabled) return;
        Sound s = sounds.get(name);
        if (s != null) s.play(0.6f);
    }

    public void toggle() {
        enabled = !enabled;
    }

    public boolean isEnabled() { return enabled; }

    public void dispose() {
        sounds.values().forEach(Sound::dispose);
        sounds.clear();
    }
}
