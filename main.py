import tkinter as tk
from k2_ui import launch_k2
from g35_ui import launch_g35
from g68_ui import launch_g68


def main():

    root = tk.Tk()
    root.title("Wandering Woods")

    label = tk.Label(root, text="Choose Game Mode")
    label.pack(pady=10)

    btn1 = tk.Button(root, text="K-2 Mode", command=lambda: launch_k2(root))
    btn1.pack(pady=5)

    btn2 = tk.Button(root, text="Grades 3-5", command=lambda: launch_g35(root))
    btn2.pack(pady=5)

    btn3 = tk.Button(root, text="Grades 6-8", command=lambda: launch_g68(root))
    btn3.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()