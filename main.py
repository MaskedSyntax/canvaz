import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
import os
from tkinter import colorchooser
import subprocess

IMAGE_FOLDER = "/home/maskedsyntax/Pictures/Wallpapers"
THUMBNAIL_SIZE = (200, 120)

class WallpaperViewer(Gtk.Window):
    def __init__(self):
        super().__init__(title="Wallpaper Manager")
        self.set_default_size(1200, 750)

        self.selected_path = None
        self.bg_color = "#000000"
        self.selected_screen = "fullscreen"

        # --- Main Layout ---
        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_vbox.set_margin_top(10)
        main_vbox.set_margin_start(10)
        main_vbox.set_margin_end(10)
        main_vbox.set_margin_bottom(10)
        self.add(main_vbox)

        # --- Top Toolbar --- #
        topbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        topbar.set_halign(Gtk.Align.FILL)
        topbar.set_margin_top(10)
        topbar.set_margin_bottom(10)
        topbar.set_margin_start(10)
        topbar.set_margin_end(10)
        main_vbox.pack_start(topbar, False, False, 0)

        # Screen Dropdown
        screen_menu_btn = Gtk.MenuButton(label="Screen: fullscreen")
        screen_menu = Gtk.Menu()
        self.screen_options = []

        try:
            output = subprocess.check_output(["xrandr"]).decode()
            screens = [line.split()[0] for line in output.splitlines() if " connected" in line]
        except Exception:
            screens = []

        screens.append("fullscreen")
        for screen in screens:
            item = Gtk.MenuItem(label=screen)
            item.connect("activate", self.set_screen_from_menu, screen_menu_btn, screen)
            screen_menu.append(item)
            self.screen_options.append(item)
        screen_menu.show_all()
        screen_menu_btn.set_popup(screen_menu)
        topbar.pack_start(screen_menu_btn, False, False, 0)

        # Fit Dropdown
        fit_menu_btn = Gtk.MenuButton(label="Fit: Fit")
        fit_menu = Gtk.Menu()
        for mode in ["Fit", "Center", "Scaled"]:
            item = Gtk.MenuItem(label=mode)
            item.connect("activate", self.set_fit_mode, fit_menu_btn, mode)
            fit_menu.append(item)
        fit_menu.show_all()
        fit_menu_btn.set_popup(fit_menu)
        topbar.pack_start(fit_menu_btn, False, False, 0)

        # Background color button
        bg_btn = Gtk.Button(label="🎨 Background")
        bg_btn.connect("clicked", self.pick_color)
        topbar.pack_start(bg_btn, False, False, 0)

        # Spacer
        topbar.pack_start(Gtk.Label(), True, True, 0)

        # Right side buttons
        get_online_btn = Gtk.Button(label="⬇ Get Online")
        topbar.pack_start(get_online_btn, False, False, 0)

        prefs_btn = Gtk.Button(label="⚙ Preferences")
        prefs_btn.connect("clicked", self.on_prefs)
        topbar.pack_start(prefs_btn, False, False, 0)

        apply_btn = Gtk.Button(label="✔ Apply Wallpaper")
        apply_btn.set_sensitive(False)
        apply_btn.connect("clicked", self.apply_wallpaper)
        self.apply_btn = apply_btn
        topbar.pack_start(apply_btn, False, False, 0)


        # --- Scrollable Wallpaper Grid ---
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        main_vbox.pack_start(scrolled, True, True, 0)

        self.grid = Gtk.FlowBox()
        self.grid.set_max_children_per_line(5)
        self.grid.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.grid.set_row_spacing(20)
        self.grid.set_column_spacing(20)
        scrolled.add(self.grid)

        self.load_images()

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

                label = Gtk.Label(label=os.path.splitext(file)[0].replace("_", " ").title())
                label.set_ellipsize(3)

                box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
                box.pack_start(image, True, True, 0)
                box.pack_start(label, False, False, 0)

                event_box = Gtk.EventBox()
                event_box.add(box)
                event_box.connect("button-press-event", self.on_image_click, full_path)

                self.grid.add(event_box)
            except Exception as e:
                print(f"Could not load image {file}: {e}")

        self.grid.show_all()

    def on_image_click(self, widget, event, image_path):
        self.selected_path = image_path
        self.apply_btn.set_sensitive(True)
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

        mode = self.mode_combo.get_active_text().lower()
        screen = self.selected_screen
        print(f"Applying wallpaper to {screen} with mode {mode} and bg {self.bg_color}")

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

    def set_screen_from_menu(self, widget, menu_button, screen_name):
        self.selected_screen = screen_name
        menu_button.set_label(f"Screen: {screen_name}")
        print(f"Selected screen: {screen_name}")

    def set_fit_mode(self, widget, menu_button, mode):
        self.fit_mode = mode.lower()
        menu_button.set_label(f"Fit: {mode}")
        print(f"Fit mode set to: {mode}")


def main():
    win = WallpaperViewer()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
