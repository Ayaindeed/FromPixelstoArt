# Libraries
import cv2
import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageFilter, ImageTk


original_image = Image.new("RGB", (1, 1))  # empty image
filtered_image = None


# Function to open image
def open_image():
    global original_image
    filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")])
    if filepath:
        original_image = Image.open(filepath)
        original_image.thumbnail((500, 500))
        photo = ImageTk.PhotoImage(original_image)
        original_label.config(image=photo)
        original_label.image = photo


# Apply filter, display filtered image or save it
def apply_filter(filter_name):
    global original_image, filtered_image
    if original_image:
        if filter_name == "save":
            if filtered_image:
                filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                        filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
                if filepath:
                    filtered_image.save(filepath)
            else:
                messagebox.showerror("Error", "No filtered image to save!")
        else:
            filtered_image = original_image.copy()
            if filter_name == "blur":
                filtered_image = filtered_image.filter(ImageFilter.BLUR)
            elif filter_name == "contour":
                filtered_image = filtered_image.filter(ImageFilter.CONTOUR)
            elif filter_name == "emboss":
                filtered_image = filtered_image.filter(ImageFilter.EMBOSS)
            elif filter_name == "sharpen":
                filtered_image = filtered_image.filter(ImageFilter.SHARPEN)
            elif filter_name == "cartoon":
                filtered_image = Image.fromarray(cartoon_effect(original_image))
            elif filter_name == "glitch":
                filtered_image = Image.fromarray(apply_glitch_filter(original_image))

            photo = ImageTk.PhotoImage(filtered_image)
            filtered_label.config(image=photo)
            filtered_label.image = photo
    else:
        messagebox.showerror("Error", "Please load an image first??")


# Function to apply custom filter
def cartoon_effect(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(img, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon


def apply_glitch_filter(image):
    img = np.array(image)
    blue, green, red = cv2.split(img)
    glitch_blue = np.roll(blue, shift=50, axis=1)
    glitch_green = np.roll(green, shift=-30, axis=0)
    glitch_red = np.roll(red, shift=20, axis=1)
    glitched_image = cv2.merge((glitch_blue, glitch_green, glitch_red))
    return glitched_image


# Function to toggle filter buttons
def toggle_filter_buttons():
    if filter_buttons.winfo_ismapped():
        filter_buttons.grid_forget()
    else:
        filter_buttons.grid(row=3, column=0, columnspan=2, pady=5)


# Function to resize background image
def resize_background(event):
    global background_photo
    background_image = original_background_image.resize((event.width, event.height), Image.LANCZOS)
    background_photo = ImageTk.PhotoImage(background_image)
    background_label.configure(image=background_photo)


# Function to create and display a tooltip
def show_tooltip(widget, text):
    widget.tooltip = tk.Toplevel(widget)
    widget.tooltip.overrideredirect(True)
    x, y, _, _ = widget.bbox("insert")
    x += widget.winfo_rootx() + 25
    y += widget.winfo_rooty() + 25
    widget.tooltip.wm_geometry("+%d+%d" % (x, y))
    label = ttk.Label(widget.tooltip, text=text, background="#dec4f3", foreground="black", padding=(5, 2))
    label.pack()


# Function to bind tooltip to a widget
def bind_tooltip(widget, text):
    def enter(event):
        show_tooltip(widget, text)

    def leave(event):
        widget.tooltip.destroy()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)


# Create the main window
root = tk.Tk()
root.title("Fun Photo Filters")

original_background_image = Image.open("Assets/background.jpg")

background_photo = ImageTk.PhotoImage(original_background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
background_label.bind("<Configure>", resize_background)

# Title
title_text = "From Pixels to Art\n  Crafting Creativity, One Click at a Time!  "
label1 = tk.Label(root, text=title_text, font=("Helvetica", 16), bg="#b59dd1")
label1.grid(row=0, column=0, columnspan=2, pady=10)

# Original image frame
original_frame = tk.Frame(root)
original_frame.grid(row=1, column=0, padx=10, pady=10)
original_label = tk.Label(original_frame, bg="#dec4f3")
original_label.pack()

# Filtered image frame
filtered_frame = tk.Frame(root)
filtered_frame.grid(row=1, column=1, padx=10, pady=10)
filtered_label = tk.Label(filtered_frame, bg="#dec4f3")
filtered_label.pack()

# Import image button
button_image = Image.open("Assets/import.png")
button_photo = ImageTk.PhotoImage(button_image)
import_button = tk.Button(root, image=button_photo, command=open_image, bg="#dec4f3")
import_button.grid(row=2, column=0, columnspan=2, pady=5)
bind_tooltip(import_button, "Import Image")

# Toggle filter buttons button
button_image1 = Image.open("Assets/magic.png")
button_photo1 = ImageTk.PhotoImage(button_image1)
filter_toggle_button = tk.Button(root, image=button_photo1, command=toggle_filter_buttons, bg="#ADD8E6")
filter_toggle_button.grid(row=3, column=0, columnspan=2, pady=5)
bind_tooltip(filter_toggle_button, "Filter Options")

# Load the image for the filter buttons
path_i = Image.open("Assets/filter.png")
button_icon = ImageTk.PhotoImage(path_i)
# Load the image for the download  button
path_save = Image.open("Assets/save.png")
save_icon = ImageTk.PhotoImage(path_save)

# Filter buttons frame
filter_buttons = tk.Frame(root, bg="#dec4f3")
# Blur
filter_button_blur = tk.Button(filter_buttons, image=button_icon, command=lambda: apply_filter("blur"), bg="#FFFDD0")
filter_button_blur.grid(row=0, column=0, padx=5, pady=5)
# Bind tooltip to the button
bind_tooltip(filter_button_blur, "Blur")
# Contour
filter_button_contour = tk.Button(filter_buttons, image=button_icon, command=lambda: apply_filter("contour"),
                                  bg="#FFB6C1")
filter_button_contour.grid(row=0, column=1, padx=5, pady=5)
# Bind tooltip to the button
bind_tooltip(filter_button_contour, "Contour")
# Emboss
filter_button_emboss = tk.Button(filter_buttons, image=button_icon, command=lambda: apply_filter("emboss"),
                                 bg="#90EE90")
filter_button_emboss.grid(row=1, column=0, padx=5, pady=5)
# Bind tooltip to the button
bind_tooltip(filter_button_emboss, "Emboss")
# Sharpen
filter_button_sharpen = tk.Button(filter_buttons, image=button_icon, command=lambda: apply_filter("sharpen"),
                                  bg="#ADD8E6")
filter_button_sharpen.grid(row=1, column=1, padx=5, pady=5)
# Bind tooltip to the button
bind_tooltip(filter_button_sharpen, "Sharpen")
# Cartoon
filter_button_cartoon = tk.Button(filter_buttons, image=button_icon, command=lambda: apply_filter("cartoon"),
                                  bg="#FFA07A")
filter_button_cartoon.grid(row=2, column=0, padx=5, pady=5)
# Bind tooltip to the button
bind_tooltip(filter_button_cartoon, "Cartoon")
# Glitch
filter_button_glitch = tk.Button(filter_buttons, image=button_icon, command=lambda: apply_filter("glitch"),
                                 bg="#20B2AA")
filter_button_glitch.grid(row=2, column=1, padx=5, pady=5)
# Bind tooltip to the button
bind_tooltip(filter_button_glitch, "Glitch")

# Download filtered image button
download_button = tk.Button(root, image=save_icon, command=lambda: apply_filter("save"), bg="#dec4f3")
download_button.grid(row=4, column=0, columnspan=2, pady=5)
# Bind tooltip to the button
bind_tooltip(download_button, "Download")

root.mainloop()