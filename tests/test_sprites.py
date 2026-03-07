from frinterflow.sprites import SPRITES, SPRITE_COLOR_MAP, draw_sprite_on_canvas


def test_all_sprites_defined():
    for name in ("tree", "heart", "brain", "bot", "wave"):
        assert name in SPRITES, f"Missing sprite: {name}"


def test_all_sprites_have_color_map():
    for name in SPRITES:
        assert name in SPRITE_COLOR_MAP, f"Missing color map for: {name}"


def test_wave_dimensions():
    assert len(SPRITES["wave"]) == 8, "wave must have 8 rows"
    assert all(len(row) == 12 for row in SPRITES["wave"]), "wave rows must be 12 wide"


def test_bot_dimensions():
    assert len(SPRITES["bot"]) == 12, "bot must have 12 rows"
    assert all(len(row) == 12 for row in SPRITES["bot"]), "bot rows must be 12 wide"


def test_bot_has_all_cell_types():
    flat = [c for row in SPRITES["bot"] for c in row]
    assert 1 in flat, "bot must have body cells (1)"
    assert 2 in flat, "bot must have eye cells (2)"
    assert 3 in flat, "bot must have antenna cells (3)"


def test_no_invalid_cell_values():
    valid = {0, 1, 2, 3}
    for name, matrix in SPRITES.items():
        for row in matrix:
            for cell in row:
                assert cell in valid, f"Invalid cell value {cell} in sprite '{name}'"


def test_bot_color_map_has_three_keys():
    assert set(SPRITE_COLOR_MAP["bot"].keys()) == {1, 2, 3}


def test_draw_sprite_on_canvas_runs():
    """Verify renderer doesn't crash with a mock canvas."""
    class MockCanvas:
        def delete(self, _): pass
        def create_rectangle(self, *args, **kwargs): pass

    for name in SPRITES:
        draw_sprite_on_canvas(MockCanvas(), name, pixel_size=5, bob_offset=0)
        draw_sprite_on_canvas(MockCanvas(), name, pixel_size=5, bob_offset=2)
