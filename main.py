import os
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from tkinter import Canvas, Scrollbar, filedialog, colorchooser
from PIL import Image, ImageTk

# Settings
IMAGE_FOLDER = "/home/maskedsyntax/Pictures/Wallpapers"
THUMBNAIL_SIZE = (150, 100)
COLUMNS = 5

# Setup
style = Style(theme="darkly")
root = style.master
root.geometry("1000x700")
root.title("Wallpaper Gallery")

# ---------------- Top Thumbnail Gallery ---------------- #
frame_top = tb.Frame(root, bootstyle="dark")
frame_top.pack(fill="both", expand=True)

canvas = Canvas(frame_top, bg=style.colors.bg)
scroll_y = Scrollbar(frame_top, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set)

scroll_y.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

image_container = tb.Frame(canvas, bootstyle="dark")
canvas.create_window((0, 0), window=image_container, anchor="nw")

image_paths = [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER)
               if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]

thumbnail_refs = []

row = col = 0
for path in image_paths:
    try:
        img = Image.open(path)
        img.thumbnail(THUMBNAIL_SIZE)
        photo = ImageTk.PhotoImage(img)
        thumbnail_refs.append(photo)
        label = tb.Label(image_container, image=photo, bootstyle="dark")
        label.grid(row=row, column=col, padx=10, pady=10)
        col += 1
        if col >= COLUMNS:
            col = 0
            row += 1
    except Exception as e:
        print(f"Error loading image {path}: {e}")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

image_container.bind("<Configure>", on_configure)

# ---------------- Bottom Toolbar ---------------- #
frame_bottom = tb.Frame(root, bootstyle="secondary")
frame_bottom.pack(fill="x", padx=5, pady=5)

frame_left = tb.Frame(frame_bottom, bootstyle="secondary")
frame_spacer = tb.Frame(frame_bottom, bootstyle="secondary")
frame_right = tb.Frame(frame_bottom, bootstyle="secondary")

frame_left.pack(side="left", padx=10)
frame_spacer.pack(side="left", expand=True, fill="both")
frame_right.pack(side="right", padx=10)

# -- MenuButtons (like dropdowns) --
menu_btn1 = tb.Menubutton(frame_left, text="Scaled", bootstyle="secondary")
menu1 = tb.Menu(menu_btn1, tearoff=0)
menu1.add_command(label="Fit to Window")
menu1.add_command(label="Original Size")
menu_btn1["menu"] = menu1
menu_btn1.pack(side="left", padx=5)

menu_btn2 = tb.Menubutton(frame_left, text="Full Screen", bootstyle="secondary")
menu2 = tb.Menu(menu_btn2, tearoff=0)
menu2.add_command(label="Enable")
menu2.add_command(label="Disable")
menu_btn2["menu"] = menu2
menu_btn2.pack(side="left", padx=5)

# -- Color Picker Button --
def pick_color():
    color = colorchooser.askcolor(title="Pick Background Color")[1]
    if color:
        frame_top.config(style="", background=color)
        image_container.config(style="", background=color)

color_btn = tb.Button(frame_left, text="Background Color", bootstyle="dark",  command=pick_color)
color_btn.pack(side="left", padx=5)

# -- Right Side Buttons --
btn_prefs = tb.Button(frame_right, text="⚙ Preferences", bootstyle="secondary")
btn_prefs.pack(side="left", padx=5, ipadx=5)

btn_apply = tb.Button(frame_right, text="✔ Apply", bootstyle="success")
btn_apply.pack(side="left", padx=5, ipadx=5)

root.mainloop()
