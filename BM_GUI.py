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

    # Create a canvas widget for main_menu
    main_menu = tk.Canvas(root, width=900, height=750)
    main_menu.place(x=0, y=0)

    #Image Calling
    main_menu.config(width=900, height=750)
    main_menu.create_image(0, 0, anchor="nw", image=tk_image_menu)

    label1 = tk.Label(main_menu, text="Select Folder", font=("Arial", 20),bg ="#D4D4D4", bd=0, highlightthickness=0, highlightbackground="SystemButtonFace")
    label1.place(x=50, y=87)

    folder_entry1 = tk.Entry(main_menu, width=70, font=("Arial", 12), bg ="#FFFFFF" ,bd=0, highlightthickness=0, highlightbackground="SystemButtonFace", insertbackground="black")
    folder_entry1.place(x=45, y=140)

    label2 = tk.Label(main_menu, text="Skills", font=("Arial", 20),bg ="#D4D4D4",)
    label2.place(x=40, y=177)

    folder_entry2 = tk.Entry(main_menu, width=70, font=("Arial", 12), bd=0,bg ="#FFFFFF", highlightthickness=0, highlightbackground="SystemButtonFace", insertbackground="black")
    folder_entry2.place(x=45, y=228)

    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(main_menu, width=20, text="Create folder for matches", variable=checkbox_var, bg ="#D4D4D4",font=("Arial", 11))
    checkbox.place(x=40, y=257)

    label3 = tk.Label(main_menu, text="Log:", bg ="#D4D4D4",font=("Arial", 20))
    label3.place(x=40, y=287)

    button1 = tk.Button(main_menu, text= "About", height=2, width=17, command=lambda: show_page("page1"), font=("Arial", 13))
    button1.place(x=40, y=600)
    button1.lift()

    button2 = tk.Button(main_menu, text= "Start", height=2, width=17,  font=("Arial", 13))
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
    global log_text, page1, tk_image_about
    
    # Create a frame for the About page
    page1 = tk.Frame(root, width=900, height=750)

    # Load the background image for aboutpage
    backimage_about = Image.open("daaabout.png")
    backimage_about = backimage_about.resize((900, 750), Image.LANCZOS)
    tk_image_about = ImageTk.PhotoImage(backimage_about)
    background_label = tk.Label(page1, image=tk_image_about)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # Create a canvas widget for page1 and set the background image
    label1 = tk.Label(page1, text="About", font=("Arial", 20),bg ="#D4D4D4", bd=0, highlightthickness=0, highlightbackground="SystemButtonFace")
    label1.place(x=50, y=87)

    # Function for the log
    def add_log_entry(text):
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, text + "\n")
        log_text.config(state=tk.DISABLED)

    canvas_frame = tk.Frame(page1)
    canvas_frame.place(x=40, y=150, width=800, height=450)

    canvas = tk.Canvas(canvas_frame, bg="white")
    canvas.grid(row=0, column=0, sticky="nsew")  # Use grid instead of pack
    canvas_frame.rowconfigure(0, weight=3)       # Make canvas expand vertically
    canvas_frame.columnconfigure(0, weight=3)

    # Create a text widget inside the canvas
    log_text = tk.Text(canvas, wrap=tk.WORD, bg="white", font=("Arial", 12))
    log_text.pack()

    add_log_entry("abcd")

    # Add any other widgets specific to aboutpage...

    button2 = tk.Button(page1, text="Back to Main Menu",height=2, width=17, command=lambda: show_page("main_menu"))
    button2.place(x=40, y=620)


# Create a frame for the main menu
main_menu = tk.Canvas(root, width=900, height=750)
main_menu.place(x=0, y=0)



# Call the mainpage function to set up the widgets
mainpage()
aboutpage()
# Call the aboutpage function to set up the widgets, but don't show it initially
# Instead, show the main_menu page initially
show_page("main_menu")

def disable_minimize_button():
    root.resizable(False, False)

disable_minimize_button()
root.mainloop()
