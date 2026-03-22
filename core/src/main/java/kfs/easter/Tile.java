package kfs.easter;

import com.badlogic.gdx.graphics.Color;

import java.util.Arrays;
import java.util.Map;
import java.util.stream.Collectors;

public enum Tile {
    GRASS('.', new Color(0.3f, 0.7f, 0.2f, 1)),
    BUSH('#', new Color(0.1f, 0.4f, 0.1f, 1)),
    RABBIT('R', new Color(0.9f, 0.9f, 0.9f, 1)),
    DOG('D', new Color(0.6f, 0.3f, 0.1f, 1)),
    EGG('E', new Color(1f, 0.95f, 0.8f, 1)),
    GOLDEN_EGG('G', new Color(1f, 0.84f, 0f, 1)),
    SPECIAL_EGG('S', new Color(0.6f, 0.2f, 0.9f, 1)),
    HAY_BALE('B', new Color(0.8f, 0.7f, 0.3f, 1)),
    FENCE('F', new Color(0.6f, 0.4f, 0.2f, 1)),
    MUD('M', new Color(0.4f, 0.3f, 0.15f, 1)),
    HOLE('H', new Color(0.15f, 0.15f, 0.15f, 1)),
    TRACTOR('T', new Color(0.8f, 0.1f, 0.1f, 1)),
    PATH_H('=', new Color(0.5f, 0.5f, 0.4f, 1)),
    PATH_V('|', new Color(0.5f, 0.5f, 0.4f, 1)),
    PATH_X('+', new Color(0.55f, 0.55f, 0.45f, 1)),
    EXIT_CLOSED('X', new Color(0.5f, 0.0f, 0.0f, 1)),
    EXIT_OPEN('O', new Color(0.0f, 0.8f, 0.0f, 1)),
    CHICKEN('C', new Color(1f, 1f, 0.6f, 1));

    public final char sym;
    public final Color color;

    Tile(char sym, Color color) {
        this.sym = sym;
        this.color = color;
    }

    public char getCode() {
        return sym;
    }

    private static final Map<Character, Tile> BY_CODE =
        Arrays.stream(values())
            .collect(Collectors.toMap(Tile::getCode, e -> e));

    public static Tile fromCode(char c) {
        return BY_CODE.getOrDefault(c, GRASS);
    }
}
