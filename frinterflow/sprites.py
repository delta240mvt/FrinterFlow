# frinterflow/sprites.py
"""
Pixel-art sprite matrices and tkinter Canvas renderer.

Cell values:
  0 = transparent (skip)
  1 = primary color
  2 = highlight / eyes
  3 = accent / gold (bot only)
"""

SPRITES = {
    "tree": [
        [0,0,0,0,1,1,1,1,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,2,2,1,1,1,1,1,0],
        [1,1,1,1,2,2,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,2,2,1,1,1],
        [0,1,1,1,1,1,1,2,2,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,0,0,0,0,0],
        [0,0,0,1,1,1,1,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,0,0,0,0],
    ],
    "heart": [
        [0,0,1,1,1,0,0,0,1,1,1,0,0],
        [0,1,1,1,1,1,0,1,1,1,1,1,0],
        [1,1,1,2,2,1,1,1,1,1,1,1,1],
        [1,1,1,2,2,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,0,0,0],
        [0,0,0,0,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,1,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0,0,0,0],
    ],
    "brain": [
        [0,0,0,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,2,2,1,1,1,2,2,1,0],
        [1,1,1,2,2,1,1,1,2,2,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,2,2,2,2,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,0,0,1,1,1,0,0],
        [0,0,0,1,1,0,0,1,1,0,0,0],
    ],
    # bot: 1=COLOR_BLOOM (body), 2=COLOR_RELATION (eyes), 3=COLOR_FOCUS (antenna/glow)
    "bot": [
        [0,0,0,3,3,3,3,3,3,0,0,0],
        [0,0,0,0,0,3,3,0,0,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,1,2,2,1,1,2,2,1,1,0],
        [0,1,1,2,2,1,1,2,2,1,1,0],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,1,1,3,3,3,3,3,3,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,0,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,1,1,0,0,0,0,1,1,0,0],
    ],
    # wave: 1=COLOR_BLOOM (ocean), 2=foam white "#e8f8f5" (crest)
    "wave": [
        [0,0,1,1,0,0,0,0,0,1,1,0],
        [0,1,1,1,1,0,0,0,1,1,1,1],
        [1,1,2,2,1,1,0,1,1,2,2,1],
        [1,2,2,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,0,1,1,1,1,0,0,0,0],
    ],
}

# Color maps for tkinter Canvas rendering
SPRITE_COLOR_MAP = {
    "bot":   {1: "#4a8d83", 2: "#8a4e64", 3: "#d6b779"},
    "tree":  {1: "#4a8d83", 2: "#aaffee"},
    "heart": {1: "#8a4e64", 2: "#ffaad4"},
    "brain": {1: "#d6b779", 2: "#fff3c0"},
    "wave":  {1: "#4a8d83", 2: "#e8f8f5"},
}


def draw_sprite_on_canvas(canvas, sprite_name: str, pixel_size: int, bob_offset: int = 0):
    """
    Draw a sprite onto a tkinter Canvas using filled rectangles.

    Args:
        canvas: tkinter.Canvas instance
        sprite_name: key from SPRITES dict
        pixel_size: px width/height of each cell
        bob_offset: vertical pixel shift for animation (0, 1, or 2)

    Call canvas.delete("all") before calling this to redraw cleanly.
    """
    matrix = SPRITES[sprite_name]
    color_map = SPRITE_COLOR_MAP[sprite_name]

    for r_idx, row in enumerate(matrix):
        y0 = r_idx * pixel_size + bob_offset
        y1 = y0 + pixel_size
        for c_idx, cell in enumerate(row):
            if cell == 0:
                continue
            x0 = c_idx * pixel_size
            x1 = x0 + pixel_size
            color = color_map.get(cell, "#4a8d83")
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
