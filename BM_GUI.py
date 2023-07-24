import tkinter as tk
from tkinter import PhotoImage, ttk, font
from PIL import ImageTk, Image

root = tk.Tk()
root.title("Boyer Moore Resume Filter")
root.geometry("900x750")

# Image here
backimage_menu = Image.open("bgdaa1.png")
backimage_menu = backimage_menu.resize((900, 750), Image.LANCZOS)
tk_image_menu = ImageTk.PhotoImage(backimage_menu)

def show_page(page):
    if page == "main_menu":
        main_menu.place(x=0, y=0)
        page1.place_forget()
    elif page == "page1":
        main_menu.place_forget()
        page1.place(x=0, y=0)

def mainpage():
    global folder_entry1, folder_entry2, label1, label2, label3, checkbox, log_text, button1

    #Image Calling
    main_menu.config(width=900, height=750)
    main_menu.create_image(0, 0, anchor="nw", image=tk_image_menu)

    label1 = tk.Label(main_menu, text="Select Folder", font=("Arial", 20),bg ="#D4D4D4", bd=0, highlightthickness=0, highlightbackground="SystemButtonFace")
    label1.place(x=50, y=87)

    folder_entry1 = tk.Entry(main_menu, width=70, font=("Arial", 12), bg ="#FFFFFF" ,bd=0, highlightthickness=0, highlightbackground="SystemButtonFace", insertbackground="black")
    folder_entry1.place(x=40, y=137)

    label2 = tk.Label(main_menu, text="Skills", font=("Arial", 20),bg ="#D4D4D4",)
    label2.place(x=40, y=177)

    folder_entry2 = tk.Entry(main_menu, width=70, font=("Arial", 12), bd=0,bg ="#FFFFFF", highlightthickness=0, highlightbackground="SystemButtonFace", insertbackground="black")
    folder_entry2.place(x=40, y=233)

    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(main_menu, width=20, text="Create folder for matches", variable=checkbox_var, bg ="#D4D4D4",font=("Arial", 11))
    checkbox.place(x=40, y=257)

    label3 = tk.Label(main_menu, text="Log:", bg ="#D4D4D4",font=("Arial", 20))
    label3.place(x=40, y=287)
    
    button1 = tk.Button(main_menu, text= "About", height=2, width=17, command=lambda: show_page("page1"), font=("Arial", 13))#, bg="white", fg="black", relief=tk.FLAT, borderwidth=0, highlightthickness=0)
    button1.place(x=40, y=600)
    button1.lift()

    button2 = tk.Button(main_menu, text= "Start", height=2, width=17,  font=("Arial", 13))#,command=lambda: show_page("page1"), bg="white", fg="black", relief=tk.FLAT, borderwidth=0, highlightthickness=0)
    button2.place(x=690, y=600)
    button2.lift()
    # Function for the log
    def add_log_entry(text):
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, text + "\n")
        log_text.config(state=tk.DISABLED)

    canvas_frame = tk.Frame(main_menu)
    canvas_frame.place(x=40, y=327, width=800, height=250)

    
    canvas = tk.Canvas(canvas_frame, bg="white")
    canvas.pack(expand=True, fill=tk.BOTH)

    # Create a text widget inside the canvas
    log_text = tk.Text(canvas, wrap=tk.WORD, bg="white", font=("Arial", 12))
    log_text.pack()

    
    add_log_entry("abcd")

def aboutpage():
    label2 = tk.Label(page1, text="page1!")
    label2.place(x=50, y=10)

    button2 = tk.Button(page1, text="Click Me!", command=lambda: show_page("main_menu"))
    button2.place(x=50, y=50)

# Create a frame for the main menu
main_menu = tk.Canvas(root, width=900, height=750)
main_menu.place(x=0, y=0)

# Create a frame for Page 1
page1 = tk.Frame(root, width=900, height=750)
page1.place(x=0, y=0)

# Call the mainpage function to set up the widgets
mainpage()

# Call the aboutpage function to set up the widgets
aboutpage()

show_page("main_menu")

def disable_minimize_button():
    root.resizable(False, False)

disable_minimize_button()
root.mainloop()
