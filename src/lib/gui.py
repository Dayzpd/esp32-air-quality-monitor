import lvgl as lv

import utils

@utils.stacktrace
def thermometer(
    temp: int,
    unit: str = "F",
    major_ticks: list = [0, 25, 50, 75, 100],
):

    unit_label = {
        "c": "°C",
        "f": "°F"
    }[unit.lower()]

    scale = lv.scale(lv.screen_active())
    scale.set_size(30, 100)
    scale.set_label_show(True)
    scale.set_mode(lv.scale.MODE.VERTICAL_RIGHT)
    scale.center()


    custom_labels = [
        f"{tick} {unit_label}"
        for tick in major_ticks
    ]

    scale.set_total_tick_count(21)
    scale.set_major_tick_every(5)

    scale.set_style_length(10, lv.PART.INDICATOR)
    scale.set_style_length(len(custom_labels), lv.PART.ITEMS)
    scale.set_range(0, 100)


    scale.set_text_src(custom_labels)

    indicator_style = lv.style_t()
    indicator_style.init()
    indicator_style.set_text_font(lv.font_default())
    indicator_style.set_text_color(lv.palette_darken(lv.PALETTE.BLUE, 3))
    indicator_style.set_line_color(lv.palette_darken(lv.PALETTE.BLUE, 3))
    indicator_style.set_width(10)  # Tick length
    indicator_style.set_line_width(2)  # Tick width
    scale.add_style(indicator_style, lv.PART.INDICATOR)

    minor_ticks_style = lv.style_t()
    minor_ticks_style.init()
    minor_ticks_style.set_line_color(lv.palette_lighten(lv.PALETTE.BLUE, 2))
    minor_ticks_style.set_width(5)  # Tick length
    minor_ticks_style.set_line_width(2)  # Tick width
    scale.add_style(minor_ticks_style, lv.PART.ITEMS)

    main_line_style = lv.style_t()
    main_line_style.init()
    main_line_style.set_line_color(lv.palette_darken(lv.PALETTE.BLUE, 3))
    main_line_style.set_line_width(2)  # Tick width
    scale.add_style(main_line_style, lv.PART.MAIN)

    section_minor_tick_style = lv.style_t()
    section_label_style = lv.style_t()
    section_main_line_style = lv.style_t()

    section_label_style.init()
    section_minor_tick_style.init()
    section_main_line_style.init()

    section_label_style.set_text_font(lv.font_default())
    section_label_style.set_text_color(lv.palette_darken(lv.PALETTE.RED, 3))
    section_label_style.set_line_color(lv.palette_darken(lv.PALETTE.RED, 3))
    section_label_style.set_line_width(5)  # Tick width

    section_minor_tick_style.set_line_color(lv.palette_lighten(lv.PALETTE.RED, 2))
    section_minor_tick_style.set_line_width(4)  # Tick width

    section_main_line_style.set_line_color(lv.palette_darken(lv.PALETTE.RED, 3))
    section_main_line_style.set_line_width(4)  # Tick width

    section = scale.add_section()
    section.set_range(0, temp)
    section.set_style(lv.PART.INDICATOR, section_label_style)
    section.set_style(lv.PART.ITEMS, section_minor_tick_style)
    section.set_style(lv.PART.MAIN, section_main_line_style)

    scale.set_style_bg_color(lv.palette_main(lv.PALETTE.BLUE_GREY), 0)
    scale.set_style_bg_opa(lv.OPA._50, 0)
    scale.set_style_pad_left(8, 0)
    scale.set_style_radius(8, 0)
    scale.set_style_pad_ver(20, 0)


def settings():
    win = lv.win(lv.screen_active())
    ta = lv.textarea(win)
    ta.set_one_line(True)
    utils.debug(lv.screen_active().get_display(), "get")
    print(lv.screen_active().get_self_height())
    kb = lv.keyboard(win)
    kb.set_textarea(ta)

    utils.debug(ta)

    def handler(ev):
        code = ev.get_code()

        if code == lv.EVENT.READY:
            print("Ready event triggered")
        elif code == lv.EVENT.VALUE_CHANGED:
            print("Value Changed event triggered")

    ta.add_event_cb(handler, lv.EVENT.ALL, None )
    lv.screen_load(lv.screen_active())


class TextArea:
    def __init__(self, screen):
        self._screen = screen
        self.ta = lv.textarea(screen)
        self.ta.add_event_cb(self._ta_event_cb, lv.EVENT.ALL, None)
        self._kb = None

    def _ta_event_cb(self, event):
        code = event.get_code()
        if code == lv.EVENT.CLICKED or code == lv.EVENT.FOCUSED:
            if self._kb is None:
                # Create keyboard
                self._kb = lv.keyboard(self._screen)
                self._kb.set_size(self._screen.get_width(), int(self._screen.get_height() / 2))
                self._kb.align_to(self.ta, lv.ALIGN.OUT_BOTTOM_MID, 0, 0)
                self._kb.set_x(0)
                self._kb.set_textarea(self.ta)
                self._kb.add_event_cb(self._kb_event_cb, lv.EVENT.ALL, None)
        elif code == lv.EVENT.DEFOCUSED:
            if self._kb is not None:
                self._kb.delete()
                self._kb = None

    def _kb_event_cb(self, event):
        code = event.get_code()
        if code == lv.EVENT.READY or code == lv.EVENT.CANCEL:
            self.ta.send_event(lv.EVENT.DEFOCUSED, self.ta)

class WifiScreen:
    def __init__(self):
        self._screen = lv.obj()
        self._construct()

    def load(self):
        lv.screen_load(self._screen)

    def _construct(self):
        screen = self._screen
        # Title
        title = lv.label(screen)
        title.set_text("Wifi Configuration")
        title.align(lv.ALIGN.TOP_MID, 0, 0)

        # SSID textarea
        ss_ta = TextArea(screen)
        self.ss_ta = ss_ta
        ss_ta.ta.set_text("")
        ss_ta.ta.set_one_line(True)
        ss_ta.ta.set_width(lv.pct(50))
        ss_ta.ta.set_pos(100, 20)


class AirQualityScreen:
    def __init__(self):
        self._screen = lv.screen_active()

        self._h_res = lv.screen_active().get_display().get_horizontal_resolution()
        self._v_res = lv.screen_active().get_display().get_vertical_resolution()

        self._construct()

    def load(self):
        lv.screen_load(self._screen)

    def _construct(self):
        screen = self._screen

        # Title
        title = lv.label(screen)
        title.set_text("Air Quality Monitor")
        title.align(lv.ALIGN.TOP_MID, 0, 10)

        # Create a tileview
        tileview = lv.tileview(screen)

        tileview.set_style_bg_color(lv.color_hex(0xEFEFEF), lv.PART.MAIN)

        # Add data labels
        labels = [
            "Temperature: 25°C",
            "Humidity: 50%",
            "PM1: 10 µg/m³",
            "PM2.5: 15 µg/m³",
            "PM10: 20 µg/m³",
            "CO2: 400 ppm",
            "TVOC: 50 ppb",
            "NH3: 5 ppb",
            "CO: 2 ppm"
        ]

        # Set tile positions
        tile_height = 40
        tiles_per_row = 3
        for i, label_text in enumerate(labels):
            row = i // tiles_per_row
            col = i % tiles_per_row
            tile = lv.obj(tileview)

            tile.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
            tile.set_pos(col * (self._h_res // tiles_per_row), row * tile_height)
            tile.set_size(self._h_res // tiles_per_row, tile_height)
            label = lv.label(tile)
            label.set_text(label_text)
            label.set_align(lv.ALIGN.CENTER)
