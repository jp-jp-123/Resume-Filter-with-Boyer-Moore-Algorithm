import tkinter as tk
import threading
from boyermoore import BoyerMoore
from tkinter import PhotoImage, ttk, font, filedialog
from PIL import ImageTk, Image
from logger import logger

class ResumeFilterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Boyer Moore Resume Filter")
        self.geometry("900x750")
        self.disable_minimize_button()
        self.setup_images()
        self.show_main_menu()
        self.after(1, self.check_new_log_entries)
        #
        self.boyer_moore = BoyerMoore()
    def check_new_log_entries(self):
        self.autoscroll()
        self.after(1, self.check_new_log_entries)
    def set_path(self):
        path = self.entry_folder.get()
        self.boyer_moore.set_path(path)

    def set_patterns(self):
        patterns = self.entry_skills.get()
        self.boyer_moore.parse(patterns)

    def start_boyer_moore(self):
        self.boyer_moore.start()
        self.boyer_moore.set_low_level_logging(False)
        self.boyer_moore.set_low_level_logging(True)
        self.boyer_moore.start()
        self.boyer_moore.segregate_pdf()
        logger.make_logfile(self.boyer_moore.filepath)

    def start(self):
        self.set_path()
        self.set_patterns()
    
        boyer_moore_thread = threading.Thread(target=self.start_boyer_moore)
        boyer_moore_thread.start()

    def disable_minimize_button(self):
        self.resizable(False, False)

    def setup_images(self):
        # Image for main_menu
        backimage_menu = Image.open("bgdaa1.png")
        backimage_menu = backimage_menu.resize((900, 750), Image.LANCZOS)
        self.tk_image_menu = ImageTk.PhotoImage(backimage_menu)

        # Image for about page
        backimage_about = Image.open("daaabout.png")
        backimage_about = backimage_about.resize((900, 750), Image.LANCZOS)
        self.tk_image_about = ImageTk.PhotoImage(backimage_about)
    def add_log_entry(self, text):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.config(state=tk.DISABLED)
    def autoscroll(self):
        self.canvas.yview_moveto(1.0)
    def show_main_menu(self):
        main_menu = tk.Canvas(self, width=900, height=750)
        main_menu.place(x=0, y=0)
        main_menu.config(width=900, height=750)
        main_menu.create_image(0, 0, anchor="nw", image=self.tk_image_menu)

        label1 = tk.Label(main_menu, text="Select Folder", font=("Arial", 20), bg="#D4D4D4", bd=0, highlightthickness=0, highlightbackground="SystemButtonFace")
        label1.place(x=50, y=87)

        self.entry_folder = tk.Entry(main_menu, width=70, font=("Arial", 12), bg="#FFFFFF", bd=0, highlightthickness=0, highlightbackground="SystemButtonFace", insertbackground="black")
        self.entry_folder.place(x=45, y=140)
        self.entry_folder.bind("<Button-1>", self.select_folder)

        label2 = tk.Label(main_menu, text="Skills", font=("Arial", 20), bg="#D4D4D4")
        label2.place(x=40, y=177)

        self.entry_skills = tk.Entry(main_menu, width=70, font=("Arial", 12), bd=0, bg="#FFFFFF", highlightthickness=0, highlightbackground="SystemButtonFace", insertbackground="black")
        self.entry_skills.place(x=45, y=228)

        label3 = tk.Label(main_menu, text="Log:", bg="#D4D4D4", font=("Arial", 20))
        label3.place(x=40, y=265)

        button1 = tk.Button(main_menu, text="About", height=2, width=17, command=self.show_about_page, font=("Arial", 13))
        button1.place(x=40, y=600)
        button1.lift()

        button2 = tk.Button(main_menu, text="Start", height=2, width=17, command=self.start, font=("Arial", 13))
        button2.place(x=690, y=600)
        button2.lift()

        canvas_frame = tk.Frame(main_menu)
        canvas_frame.place(x=40, y=327, width=800, height=250)
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.log_text = tk.Text(self.canvas, wrap=tk.WORD, bg="white", font=("Arial", 12))
        self.log_text.pack()
        logger.set_field(self.log_text)
        self.scrollbar = tk.Scrollbar(canvas_frame, command=self.log_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=self.scrollbar.set)
        self.main_menu = main_menu
    def show_about_page(self):
        page1 = tk.Frame(self, width=900, height=750)
        background_label = tk.Label(page1, image=self.tk_image_about)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        label1 = tk.Label(page1, text="About", font=("Arial", 20), bg="#D4D4D4", bd=0, highlightthickness=0, highlightbackground="SystemButtonFace")
        label1.place(x=50, y=87)

        canvas_frame = tk.Frame(page1)
        canvas_frame.place(x=40, y=150, width=800, height=450)

        canvas = tk.Canvas(canvas_frame, bg="white")
        canvas.grid(row=0, column=0, sticky="nsew")
        canvas_frame.rowconfigure(0, weight=3)
        canvas_frame.columnconfigure(0, weight=3)

        self.log_text = tk.Text(canvas, wrap=tk.WORD, bg="white", font=("Arial", 12))
        self.log_text.pack()

        # self.add_log_entry("abcd")

        button2 = tk.Button(page1, text="Back to Main Menu", height=2, width=17, command=self.show_main_menu)
        button2.place(x=40, y=620)

        self.page1 = page1
        self.main_menu.place_forget()
        self.page1.place(x=0, y=0)

    def autoscroll(self):
        self.log_text.yview(tk.END)

    def select_folder(self, event):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.entry_folder.delete(0, tk.END)
            self.entry_folder.insert(0, folder_selected)

if __name__ == "__main__":
    app = ResumeFilterApp()
    app.mainloop()
