import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf, Gdk
import os
from tkinter import colorchooser
import subprocess

IMAGE_FOLDER = "/home/maskedsyntax/Pictures/Wallpapers"
THUMBNAIL_SIZE = (200, 120)

class WallpaperViewer(Gtk.Window):
    def __init__(self):
        super().__init__(title="Wallpaper Viewer")
        self.set_default_size(1000, 700)

        # Main layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vbox)

        # --- Scrollable Image Grid --- #
        scrolled = Gtk.ScrolledWindow()
        vbox.pack_start(scrolled, True, True, 0)

        self.grid = Gtk.FlowBox()
        # self.grid.set_max_children_per_line(5)
        self.grid.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.grid.set_row_spacing(0) #
        self.grid.set_column_spacing(0) #
        scrolled.add(self.grid)

        self.selected_path = None
        self.bg_color = "#000000"
        self.selected_screen = "fullscreen"

        self.load_images()

        # --- Bottom Toolbar --- #
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        toolbar.set_margin_top(5)
        toolbar.set_margin_bottom(5)
        toolbar.set_margin_start(10)
        toolbar.set_margin_end(10)
        vbox.pack_start(toolbar, False, False, 0)

        # Mode ComboBox
        self.mode_combo = Gtk.ComboBoxText()
        for mode in ["fit", "center", "scaled"]:
            self.mode_combo.append_text(mode)
        self.mode_combo.set_active(0)
        toolbar.pack_start(self.mode_combo, False, False, 0)

        # Screen ComboBox
        self.screen_combo = Gtk.ComboBoxText()
        self.populate_screens()
        toolbar.pack_start(self.screen_combo, False, False, 0)

        # Color Picker
        color_btn = Gtk.Button(label="🖌 Background")
        color_btn.connect("clicked", self.pick_color)
        toolbar.pack_start(color_btn, False, False, 0)

        # Spacer
        toolbar.pack_start(Gtk.Label(), True, True, 0)

        # Preferences
        prefs_btn = Gtk.Button(label="⚙ Preferences")
        prefs_btn.connect("clicked", self.on_prefs)
        toolbar.pack_start(prefs_btn, False, False, 0)

        # Apply
        apply_btn = Gtk.Button(label="✔ Apply")
        apply_btn.connect("clicked", self.apply_wallpaper)
        toolbar.pack_start(apply_btn, False, False, 0)

    def load_images(self):
        for file in sorted(os.listdir(IMAGE_FOLDER)):
            if not file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                continue
            full_path = os.path.join(IMAGE_FOLDER, file)

            try:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    full_path, width=THUMBNAIL_SIZE[0], height=THUMBNAIL_SIZE[1], preserve_aspect_ratio=True
                )
                image = Gtk.Image.new_from_pixbuf(pixbuf)

                event_box = Gtk.EventBox()
                event_box.add(image)
                event_box.connect("button-press-event", self.on_image_click, full_path)

                frame = Gtk.Frame()
                frame.set_shadow_type(Gtk.ShadowType.IN)
                frame.add(event_box)

                self.grid.add(frame)
            except Exception as e:
                print(f"Could not load image {file}: {e}")

        self.grid.show_all()

    def on_image_click(self, widget, event, image_path):
        self.selected_path = image_path
        print(f"Selected: {image_path}")

    def pick_color(self, button):
        color = colorchooser.askcolor(title="Pick Background")[1]
        if color:
            self.bg_color = color
            print(f"Picked color: {color}")

    def apply_wallpaper(self, button):
        if not self.selected_path:
            print("No wallpaper selected.")
            return

        mode = self.mode_combo.get_active_text()
        screen = self.selected_screen
        print(f"Applying wallpaper to {screen} with mode {mode} and bg {self.bg_color}")

        # Example command using feh (you can change this to swaybg, xwallpaper, etc.)
        cmd = ["feh", f"--bg-{mode}", "--image-bg", self.bg_color, self.selected_path]
        subprocess.run(cmd)

    def on_prefs(self, button):
        print("Preferences clicked — not implemented.")

    def populate_screens(self):
        self.screen_combo.remove_all()

        try:
            output = subprocess.check_output(["xrandr"]).decode()
            screens = [line.split()[0] for line in output.splitlines() if " connected" in line]
        except Exception:
            screens = []

        screens.append("fullscreen")

        for screen in screens:
            self.screen_combo.append_text(screen)

        self.screen_combo.set_active(0)
        self.selected_screen = screens[0]
        self.screen_combo.connect("changed", self.set_screen_from_combo)

    def set_screen_from_combo(self, combo):
        self.selected_screen = combo.get_active_text()
        print(f"Selected screen: {self.selected_screen}")

    def set_screen(self, menuitem, screen_name):
        self.selected_screen = screen_name
        self.screen_menu_btn.set_label(screen_name)
        print(f"Selected screen: {screen_name}")

def main():
    win = WallpaperViewer()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
