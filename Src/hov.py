import tkinter as tk
import tkinter.ttk as ttk


# Function to create and display a tooltip
def show_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.overrideredirect(True)
    x, y, _, _ = widget.bbox("insert")
    x += widget.winfo_rootx() + 25
    y += widget.winfo_rooty() + 25
    tooltip.wm_geometry("+%d+%d" % (x, y))
    label = ttk.Label(tooltip, text=text, background="#ffffe0", foreground="black", padding=(5, 2))
    label.pack()


# Function to bind tooltip to a widget
def bind_tooltip(widget, text):
    def enter(event):
        show_tooltip(widget, text)

    def leave(event):
        widget.unbind("<Motion>")
        widget.unbind("<Leave>")
        widget.tooltip.destroy()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)


# Example usage
root = tk.Tk()

# Create a button
button = tk.Button(root, text="Hover over me")
button.pack()

# Bind tooltip to the button
bind_tooltip(button, "This is a tooltip")

root.mainloop()
