import tkinter as tk
from modes.k2_ui import launch_k2
from modes.g35_ui import launch_g35
from modes.g68_ui import launch_g68


def main():
    root = tk.Tk()
    root.title("Wandering Woods")
    root.geometry("860x560")
    root.minsize(760, 500)
    root.configure(bg="#eef4ea")

    title_font = ("Segoe UI", 34, "bold")
    subtitle_font = ("Segoe UI", 13)
    button_font = ("Segoe UI", 16, "bold")

    hero = tk.Frame(root, bg="#2f5d45", padx=28, pady=24)
    hero.pack(fill="x", padx=20, pady=(20, 12))

    title_label = tk.Label(
        hero,
        text="Wandering in the Woods",
        font=title_font,
        fg="#f4f8f0",
        bg="#2f5d45",
    )
    title_label.pack(anchor="w")

    subtitle_label = tk.Label(
        hero,
        text="Pick a grade band to start a guided forest simulation.",
        font=subtitle_font,
        fg="#dbe9db",
        bg="#2f5d45",
    )
    subtitle_label.pack(anchor="w", pady=(8, 0))

    content = tk.Frame(root, bg="#eef4ea")
    content.pack(fill="both", expand=True, padx=24, pady=(8, 24))

    label = tk.Label(
        content,
        text="Choose Game Mode",
        font=("Segoe UI", 20, "bold"),
        fg="#2b3d2e",
        bg="#eef4ea",
    )
    label.pack(pady=(8, 20))

    button_box = tk.Frame(content, bg="#eef4ea")
    button_box.pack(fill="both", expand=True)

    button_style = {
        "font": button_font,
        "fg": "#f8fbf8",
        "bg": "#3f7a58",
        "activeforeground": "#ffffff",
        "activebackground": "#2f5d45",
        "relief": "flat",
        "bd": 0,
        "cursor": "hand2",
        "width": 26,
        "height": 2,
    }

    btn1 = tk.Button(button_box, text="K-2 Mode", command=lambda: launch_k2(root), **button_style)
    btn1.pack(pady=10)

    btn2 = tk.Button(button_box, text="Grades 3-5", command=lambda: launch_g35(root), **button_style)
    btn2.pack(pady=10)

    btn3 = tk.Button(button_box, text="Grades 6-8", command=lambda: launch_g68(root), **button_style)
    btn3.pack(pady=10)

    tip = tk.Label(
        content,
        text="Tip: Start with K-2 mode for the simplest controls.",
        font=("Segoe UI", 11),
        fg="#56695b",
        bg="#eef4ea",
    )
    tip.pack(pady=(12, 0))

    root.mainloop()


if __name__ == "__main__":
    main()