# Bing Image Creator (DALL-E 3) - KFS Easter Egg sprites

Generátor: **Bing Image Creator** (https://www.bing.com/images/create)
Model: DALL-E 3, aspect ratio 1:1, 4 obrázky najednou.

Všechny sprite cíl **48x48 px** - generovat na 1024x1024 a pak downscale.
Styl: **cute pixel art, front-facing** (ne top-down) - viz 01.jpg referenční zajíc.

**Společný suffix** ke každému promptu:
> pixel art style, cute cartoon, Easter spring theme, bright colors, clean black outlines, checkered transparent background, single sprite centered, no text, no watermark

---

## 1. Zajíc (Player)

### 1a. Zajíc - čelem (default) -- HOTOVO viz 01.jpg
```
cute white pixel art bunny rabbit facing forward, big floppy ears with pink inside, large black eyes, pink nose, small paws visible, sitting on a small patch of green grass with tiny flowers, Easter spring theme, pixel art style, bright colors, clean black outlines, checkered transparent background, single character centered
```

### 1b. Zajíc - zezadu
```
cute white pixel art bunny rabbit seen from behind, big floppy ears visible from back, fluffy round cotton tail, small paws, sitting on a small patch of green grass, Easter spring theme, pixel art style, bright colors, clean black outlines, checkered transparent background, single character centered
```

### 1c. Zajíc - doleva
```
cute white pixel art bunny rabbit facing left, side profile view, big floppy ear visible, pink nose, one eye visible, small paws, sitting on a small patch of green grass, Easter spring theme, pixel art style, bright colors, clean black outlines, checkered transparent background, single character centered
```

**Tip:** Doprava = horizontální flip doleva.

---

## 2. Pes (Enemy)

### 2a. Pes - čelem
```
cute brown pixel art farm dog facing forward, floppy ears, friendly but alert expression, red collar with tag, medium size, sitting on green grass, Easter spring farm theme, pixel art style, bright colors, clean black outlines, checkered transparent background, single character centered
```

### 2b. Pes - zezadu
```
cute brown pixel art farm dog seen from behind, floppy ears, red collar visible, wagging tail, sitting on green grass, Easter spring farm theme, pixel art style, bright colors, clean black outlines, checkered transparent background, single character centered
```

### 2c. Pes - doleva
```
cute brown pixel art farm dog facing left, side profile, floppy ear, red collar, alert posture, standing on green grass, Easter spring farm theme, pixel art style, bright colors, clean black outlines, checkered transparent background, single character centered
```

**Tip:** Doprava = flip doleva.

---

## 3. Traktor (Enemy)

### 3a. Traktor - boční pohled (doprava)
```
small red pixel art farm tractor facing right, side view, big green wheels, simple cute design, exhaust pipe, no driver, Easter spring farm theme, pixel art style, bright colors, clean black outlines, checkered transparent background, single vehicle centered
```

### 3b. Traktor - čelní pohled
```
small red pixel art farm tractor facing forward, front view, big green wheels on sides, simple cute design, Easter spring farm theme, pixel art style, bright colors, clean black outlines, checkered transparent background, single vehicle centered
```

**Tip:** Doleva = flip doprava. Nahoru/dolů = čelní/zadní.

---

## 4. Slepice

```
cute white pixel art farm chicken facing forward, red comb on head, small orange beak, round plump body, tiny yellow feet, standing on green grass, Easter spring farm theme, pixel art style, bright colors, clean black outlines, checkered transparent background, single character centered
```

---

## 5. Vajíčka

### 5a. Normální vejce
```
single decorated pixel art Easter egg, pastel pink and light blue stripes, zigzag pattern, sitting on small green grass patch, pixel art style, cute cartoon, bright colors, clean black outlines, checkered transparent background, centered
```

### 5b. Zlaté vejce
```
single shiny golden pixel art Easter egg, glowing gold surface, small sparkle stars around it, precious treasure look, sitting on small green grass patch, pixel art style, cute cartoon, bright colors, clean black outlines, checkered transparent background, centered
```

### 5c. Speciální vejce (power-up)
```
single magical purple pixel art Easter egg, glowing purple aura, star and moon pattern, mystical shimmer effect, sitting on small green grass patch, pixel art style, cute cartoon, bright colors, clean black outlines, checkered transparent background, centered
```

---

## 6. Terén - Tiles

### 6a. Tráva (GRASS)
```
simple green grass tile, top-down view from above, lush spring meadow with a few tiny flowers and clovers, uniform flat coverage, seamless tileable square texture, pixel art style, bright green, no objects, no characters
```

### 6b. Keř / zeď (BUSH)
```
dense dark green bush tile, top-down view from above, thick hedge leaves, impenetrable wall of vegetation, seamless tileable square texture, pixel art style, darker green, clean outlines
```

### 6c. Balík sena (HAY_BALE)
```
round golden hay bale seen from above, top-down view, circular spiral straw pattern, farm obstacle, green grass around edges, pixel art style, cute cartoon, warm yellow colors, clean outlines, square tile
```

### 6d. Plot (FENCE)
```
wooden farm fence section from above, top-down view, brown wooden planks and posts, rustic countryside style, green grass visible on sides, pixel art style, warm brown colors, clean outlines, square tile
```

### 6e. Bláto (MUD)
```
muddy ground patch from above, top-down view, wet brown dirt with small puddles, splashy texture, seamless tileable square, pixel art style, dark brown tones, no objects
```

### 6f. Díra (HOLE)
```
dark circular hole in green ground from above, top-down view, black pit center, dirt crumbling around edges, grass rim, pixel art style, dark center fading to green edges, clean outlines, square tile
```

### 6g. Cesta (PATH - pro traktor)
```
dirt farm path tile from above, top-down view, light brown compacted soil, subtle tire tracks, flat road surface, seamless tileable square, pixel art style, beige brown colors, no objects
```

### 6h. Východ - zavřený (EXIT_CLOSED)
```
closed wooden barn door from above, top-down view, red painted wood, iron padlock, blocked entrance, pixel art style, red and brown colors, clean outlines, green grass around, square tile
```

### 6i. Východ - otevřený (EXIT_OPEN)
```
open barn door from above, top-down view, green glowing entrance, welcoming golden light shining out, pixel art style, green glow effect, clean outlines, green grass around, square tile
```

---

## 7. Pozadí za mapou (game background)

Viditelné kolem mapy. Rozměr: **1024x768** (aspect ratio 4:3 v Bingu vybrat "Widescreen" nebo generovat čtverec a oříznout).

```
spring countryside landscape pixel art, rolling green hills, patches of colorful wildflowers, small farm fields, distant red barn and windmill, blue sky with fluffy white clouds, soft pastel spring colors, peaceful atmosphere, no characters, no text, bright and cheerful, Easter spring theme
```

---

## 8. Pozadí menu (MainScreen background)

Rozměr: **1024x768**. Text "pro Kubu" přidat v kódu.

```
pixel art Easter farm scene, cute cartoon style, spring meadow with colorful Easter eggs scattered in green grass, white picket fence, blooming pink cherry trees, blue sky with fluffy clouds, small cute farmhouse with red roof in distance, butterflies, warm golden sunlight, cheerful and inviting, bright vivid colors, game menu background, no text, no characters
```

Varianta s "pro Kubu" přímo v obrázku:
```
pixel art Easter farm scene, spring meadow with Easter eggs in grass, cherry blossom trees, blue sky, a decorative wooden sign in the center reading "pro Kubu" in golden letters, warm sunlight, cheerful bright colors, game title screen
```

---

## 9. Splash screen (loading screen pro web)

Tmavší pozadí, aby fungoval s progress barem. Rozměr: čtverec, pak oříznout.

### 9a. S textem
```
pixel art Easter game loading screen, dark green night background with stars, cute white bunny rabbit sitting in center holding a glowing colorful Easter egg, surrounded by spring flowers and small decorated eggs, soft magical glow around bunny, text "pro Kubu" in warm golden pixel letters below bunny, cozy night atmosphere, centered composition
```

### 9b. Bez textu (text přidat v HTML)
```
pixel art cute white bunny rabbit holding a glowing golden Easter egg, sitting on dark green grass at night, spring flowers around, soft magical glow, dark background with tiny stars, centered composition, simple and clean, Easter theme
```

Text "pro Kubu" pak přidat v HTML přes CSS:
```html
<div id="splash" style="background: #0a1a0a; text-align: center;">
  <img src="splash.png" style="margin-top: 20%;">
  <p style="font-family: 'Press Start 2P'; color: #ffcc00; font-size: 18px;">pro Kubu</p>
  <div id="progress">...</div>
</div>
```

---

## 10. Startup logo (TeaVM boot logo)

Nahrazuje defaultní LibGDX logo. Rozměr: **500x83** (wide banner).
DALL-E neumí dobře úzké bannery - lepší vygenerovat přes ImageMagick:

```bash
magick -size 500x83 xc:'#0a1a0a' \
  -font assets/fonts/PressStart2P.ttf \
  -pointsize 28 -fill '#ff6699' -gravity center -annotate +0-14 'EASTER EGG' \
  -pointsize 12 -fill '#ffcc00' -annotate +0+18 'pro Kubu' \
  assets/startup-logo.png
```

Případně v Bingu vygenerovat čtverec a oříznout střed:
```
pixel art game logo banner, text "EASTER EGG" in large playful pixel font with cute bunny ears on the E letters, small text "pro Kubu" below in golden color, pastel Easter eggs and spring flowers decorating the sides, dark green background, retro game title style, bright cheerful colors
```

---

## Postup zpracování

1. Vygenerovat v **Bing Image Creator** (https://www.bing.com/images/create)
2. Vybrat nejlepší ze 4 variant
3. Stáhnout (pravý klik → Save image)
4. Odstranit pozadí (šachovnice = už transparentní, jinak použít remove.bg nebo GIMP)
5. **Sprite:** Downscale na **48x48** pomocí nearest neighbor (ne bilinear!)
   - GIMP: Image → Scale Image → Interpolation: None
   - ImageMagick: `magick input.png -resize 48x48 -filter point output.png`
6. **Pozadí:** Downscale na 1024x768 (bilinear OK)
7. Uložit jako PNG s transparencí (sprite) nebo JPG (pozadí)

### Pojmenování souborů
```
assets/textures/
├── rabbit_front.png      (čelem)
├── rabbit_back.png       (zezadu)
├── rabbit_left.png       (doleva)
├── rabbit_right.png      (doprava = flip left)
├── dog_front.png
├── dog_back.png
├── dog_left.png
├── dog_right.png         (flip left)
├── tractor_right.png
├── tractor_left.png      (flip right)
├── tractor_front.png
├── chicken.png
├── egg_normal.png
├── egg_golden.png
├── egg_special.png
├── tile_grass.png        (top-down)
├── tile_bush.png         (top-down)
├── tile_hay.png          (top-down)
├── tile_fence.png        (top-down)
├── tile_mud.png          (top-down)
├── tile_hole.png         (top-down)
├── tile_path.png         (top-down)
├── tile_exit_closed.png  (top-down)
├── tile_exit_open.png    (top-down)
├── bg_game.png           → pozadí za mapou (1024x768)
├── bg_menu.png           → pozadí hlavního menu (1024x768)
├── splash.png            → loading screen pro web
└── startup-logo.png      → TeaVM boot logo (500x83)
```

### Pořadí generování (doporučené)

1. **Zajíc čelem** - HOTOVO (01.jpg)
2. **Zajíc zezadu + doleva** - doladí se konzistentní styl
3. **Pes** (3 směry) - důležitý nepřítel
4. **Vajíčka** (3 typy) - klíčový herní prvek
5. **Slepice** - jednoduchá
6. **Traktor** (2 směry)
7. **Terénní tiles** (9 kusů) - top-down, jiný styl než entity
8. **Pozadí menu + splash** - větší obrázky
9. **Pozadí za mapou**
10. **Startup logo** (ImageMagick)
