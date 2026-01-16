import tkinter as tk
from tkinter import messagebox, filedialog
import random

data = [
    " ***  ****   ***  ****  ***** *****  ***  *   * ***** ***** *   * *     *   * *   *  ***  ****   ***  ****   **** ***** *   * *   * *   * *   * *   * *****        ***                     ***  ***   ****  ****  *   * *****  ***  *****  ***  ***** ",
    "*   * *   * *   * *   * *     *     *     *   *   *      *  *  *  *     ** ** **  * *   * *   * *   * *   * *       *   *   * *   * *   *  * *   * *     *        * ***                   *   *   *       *     * *   * *     *         * *   * *   * ",
    "*   * ****  *     *   * ***   ****  *  ** *****   *      *  ***   *     * * * * * * *   * ****  *   * ****  *****   *   *   * *   * * * *   *     *     *         * * *       *****       *   *   *       *   **  ***** ****  ****      *  ***  ***** ",
    "***** *   * *   * *   * *     *     *   * *   *   *   *  *  *  *  *     *   * *  ** *   * *     *   * *  *      *   *   *   *  * *  ** **  * *    *    *          * * *              ***  *   *   *   ***       *     *     * *   *     * *   *     * ",
    "*   * ****   ***  ****  ***** *      ***  *   * *****  ***  *   * ***** *   * *   *  ***  *      ***  *   * ****    *   *****   *   *   * *   *   *   *****        ***  *****        ***   ***  ***** ***** ****      * ****   ***      *  ***      * "
]
data1 =[
    "  **** *               *                   *     *         * *     *                      *     ***   * **   ****   *                                        ",  
    " *   * *     *****     * *****  **** ***** *               * *     *          *   *  ***  ****  * *   **  * *       *                           *   *  ***** ",  
    "   * * ***** *     ***** * * *  *  * ***** ***** *         * *  ** *    *   * * * * *   * *   * *** * *     ***** ***** *   * *   * *   * ** ** *****     *  ", 
    " *   * *   * *     *   * *     ***       * *   * *     *   * * *   *    * * * *  ** *   * ****     ** *         *   *   *   *  * *  * * *   *       *    *   ",
    " ***** ***** ***** ***** *****  *    ***** *   * *     ***** *  ** **** *   * *   *  ***  *         * *     ****    *** *****   *   ** ** ** ** *****  ***** ",
]

def get_block_start_for_char(ch: str) -> int:
    ch_ord = ord(ch)
    if 48 <= ch_ord <= 57: return (ch_ord - 17) * 6
    if ch == " ": return 26 * 6
    if ch == "@": return 27 * 6
    if ch == "_": return 28 * 6
    if ch == "-": return 29 * 6
    if ch == ".": return 30 * 6
    if "A" <= ch <= "Z": return ((ord(ch) - 64) - 1) * 6
    raise KeyError(f"Character not supported: '{ch}'")


def render_text_to_lines(text: str):
    lines = ["", "", "", "", ""]

    for ch in text:
        # Decide which dataset to use
        if ch.islower():
            dataset = data1
            ch = ch.upper()   # reuse same index logic
        else:
            dataset = data

        for row_index, row in enumerate(dataset):
            try:
                n = get_block_start_for_char(ch)
                seg = row[n:n + 6].ljust(6, " ")
            except KeyError:
                seg = " " * 6
            lines[row_index] += seg

    return lines



def save_lines_to_file(lines, filename):
    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n\n")


class Particle:
    def __init__(self, canvas, x, y, r, vx, vy):
        self.canvas = canvas
        self.x, self.y, self.r, self.vx, self.vy = x, y, r, vx, vy


class SoftCyberASCIIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ASCII ART")
        self.root.geometry("1150x750")
        self.root.minsize(900, 600)

        self.canvas = tk.Canvas(root, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.control_frame = tk.Frame(root, bg="#001f3f")
        self.control_frame.place(relx=0.5, rely=0.05, anchor="n")

        self.title_label = tk.Label(self.control_frame, text="ASCII ART",
                                    font=("Consolas", 20, "bold"),
                                    bg="#001f3f", fg="#00d9ff")
        self.title_label.grid(row=0, column=0, columnspan=6, pady=8)

        self.input_entry = tk.Entry(self.control_frame, font=("Consolas", 14),
                                    width=36, bg="#003366", fg="#00eaff",
                                    insertbackground="cyan")
        self.input_entry.grid(row=1, column=0, columnspan=4, padx=8, ipady=4)

        btn_font = ("Consolas", 11, "bold")
        btn_style = dict(font=btn_font, bg="#004d99", fg="white",
                         activebackground="#0077ff")

        self.btn_one_char = tk.Button(self.control_frame, text="Single Char", command=self.one_character, **btn_style)
        self.btn_words = tk.Button(self.control_frame, text="Word <=15", command=self.words_module, **btn_style)
        self.btn_range = tk.Button(self.control_frame, text="Range A-D format", command=self.range_module, **btn_style)
        self.btn_alpha = tk.Button(self.control_frame, text="Only A-Z", command=self.only_alpha, **btn_style)
        self.btn_num = tk.Button(self.control_frame, text="Only 0-9", command=self.only_num, **btn_style)
        self.btn_exit = tk.Button(self.control_frame, text="EXIT", command=root.quit, **btn_style)

        buttons = [self.btn_one_char, self.btn_words, self.btn_range, self.btn_alpha, self.btn_num, self.btn_exit]
        for i, btn in enumerate(buttons):
            btn.grid(row=2, column=i, padx=6, pady=8)

        self.output_frame = tk.Frame(root, bg="black")
        self.output_frame.place(relx=0.5, rely=0.22, anchor="n")

        self.preview_label = tk.Label(self.output_frame, text="OUTPUT PREVIEW",
                                      font=("Consolas", 12, "bold"),
                                      bg="black", fg="#00c8ff")
        self.preview_label.pack(pady=4)

        self.text_widget = tk.Text(self.output_frame, width=100, height=22,
                                   font=("Courier New", 12), wrap="none",
                                   bd=2, relief="groove", bg="#00172e",
                                   fg="#00f0ff", insertbackground="cyan")
        self.text_widget.pack(padx=12, pady=8)

        self.save_btn = tk.Button(self.output_frame, text="SAVE OUTPUT",
                                  command=self.save_output,
                                  font=("Consolas", 11, "bold"),
                                  bg="#0055cc", fg="#ffffff",
                                  activebackground="#0088ff")
        self.save_btn.pack(pady=6)

        self.gradient_colors = [(0, 0, 20), (0, 80, 200), (0, 255, 255)]
        self.particles = []
        self._create_particles()
        self.last_rendered_lines = []
        self._running = True

        self.root.after(30, self._animate)
        self.root.bind("<Configure>", self._on_resize)

    # ---------- Modules ----------
    def one_character(self):
        text = self.input_entry.get()

        if len(text) != 1:
            return messagebox.showinfo("Error", "Enter Only One Character")
        self._show(render_text_to_lines(text))

    def words_module(self):
        text = self.input_entry.get()
        if not (1 <= len(text) <= 15):
            return messagebox.showinfo("Error", "Length must be 1-15")
        self._show(render_text_to_lines(text))

    def range_module(self):
        text = self.input_entry.get()

        if len(text) != 3 or text[1] != "-":
            return messagebox.showinfo("Error", "A-D Format Required!")

        start, end = text[0], text[2]
        letters = "".join(chr(c) for c in range(ord(start), ord(end) + 1))
        self._show(render_text_to_lines(letters))


    def only_alpha(self):
        text = self.input_entry.get()

        if not text.isalpha():
            return messagebox.showinfo("Error", "Only Alphabets")
        self._show(render_text_to_lines(text))

    def only_num(self):
        t = self.input_entry.get()
        if not t.isdigit():
            return messagebox.showinfo("Error", "Only Numbers")
        self._show(render_text_to_lines(t.upper()))

    # ---------- Display ----------
    def _show(self, lines):
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, "\n".join(lines))
        self.last_rendered_lines = lines

    def save_output(self):
        if not self.last_rendered_lines:
            return messagebox.showinfo("Error", "Nothing to Save")
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            save_lines_to_file(self.last_rendered_lines, path)
            messagebox.showinfo("Saved", "File Saved Successfully!")

    # ---------- Animation Background ----------
    def _draw_gradient(self):
        self.canvas.delete("gradient")
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()

        for i in range(h):
            t = i / h
            r = int(self.gradient_colors[0][0] * (1 - t) + self.gradient_colors[2][0] * t)
            g = int(self.gradient_colors[0][1] * (1 - t) + self.gradient_colors[2][1] * t)
            b = int(self.gradient_colors[0][2] * (1 - t) + self.gradient_colors[2][2] * t)
            self.canvas.create_line(0, i, w, i,
                                    fill=f"#{r:02x}{g:02x}{b:02x}",
                                    tags="gradient")

    def _create_particles(self):
        w, h = 1150, 750
        self.particles = [
            Particle(self.canvas,
                     random.randint(0, w), random.randint(0, h),
                     random.randint(6, 15),
                     random.uniform(-0.4, 0.4),
                     random.uniform(-0.3, 0.3))
            for _ in range(30)
        ]

    def _animate(self):
        if not self._running: return

        self._draw_gradient()
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()

        self.canvas.delete("particle")
        for p in self.particles:
            p.x += p.vx
            p.y += p.vy
            if p.x < 0: p.x = w
            if p.y < 0: p.y = h

            self.canvas.create_oval(p.x - p.r, p.y - p.r, p.x + p.r, p.y + p.r,
                                    fill="#00ffff", outline="", tags="particle")
        self.root.after(50, self._animate)

    def _on_resize(self, event):
        self.canvas.config(width=event.width, height=event.height)


def main():
    root = tk.Tk()
    app = SoftCyberASCIIApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()



