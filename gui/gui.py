import ctypes
import tkinter as tk
from tkinter import ttk

from middleware import (amount_given,
                        authenticate,
                        get_patient,
                        get_drug,
                        update_last_login)

def check_login_info(username, password):
    name = username.get()
    password = password.get()
    if authenticate(
            username= name,
            pswd= password
    ):
        load_menu_screen(name)
        update_last_login(name)
    else:
        show_error()

def show_error():
    error_label = ttk.Label(
        root,
        text='Incorrect password or username',
        font=("Segui", 14),
        foreground='red'
    )
    error_label.grid(
        column=1,
        row=1,
        sticky='S',
        columnspan=2
    )

# load login screen
def load_login_screen():
    # styles
    style = ttk.Style()
    style.configure(
        "Modern.TEntry",
        padding=5,
        font=("Segui", 16)
    )

    # wipe the screen
    for widget in root.winfo_children():
        widget.destroy()

    # load the main screen
    root.title('Username_info')

    # grid
    root.rowconfigure(
        0,
        weight=2
    )
    root.rowconfigure(
        1,
        weight=2
    )
    root.rowconfigure(
        2,
        weight=1
    )
    root.rowconfigure(
        3,
        weight=1
    )
    root.columnconfigure(
        0,
        weight=1,
        minsize=root.winfo_width() / 4
    )
    root.columnconfigure(
        1,
        weight=1,
        minsize=root.winfo_width() / 4
    )
    root.columnconfigure(
        2,
        weight=1,
        minsize=root.winfo_width() / 4
    )
    root.columnconfigure(
        3,
        weight=1,
        minsize=root.winfo_width() / 4
    )

    # wlc logo
    wlc_nursing_logo_img = tk.PhotoImage(file="./images/WLC_Nursing_Logo.png")
    wlc_nursing_logo = ttk.Label(
        root,
        image=wlc_nursing_logo_img
    )
    wlc_nursing_logo.grid(
        column=1,
        row=0,
        padx=5,
        pady=5,
        columnspan=2
    )

    root.wlc_nursing_logo_img = wlc_nursing_logo_img

    # name box
    username_label = ttk.Label(
        root,
        text='Name  ',
        font=("Segui", 14)
    )
    username_label.grid(
        column=1,
        row=1,
        sticky='NE'
    )

    username = ttk.Entry(
        root,
        style="Modern.TEntry"
    )
    username.grid(
        column=2,
        row=1,
        sticky='NW'
    )
    username.focus()

    # password box
    password_label = ttk.Label(
        root,
        text='Password  ',
        font=("Segui", 14)
    )
    password_label.grid(
        column=1,
        row=1,
        sticky='E'
    )

    password = ttk.Entry(
        root,
        show='*'
    )
    password.grid(
        column=2,
        row=1,
        sticky='W'
    )

    # Login button -> new window with user info
    enter = ttk.Button(
        root,
        text='Login',
        command=lambda: check_login_info(username, password)
    )
    enter.grid(
        column=1,
        row=2,
        sticky='N',
        columnspan=2
    )

# load menu screen
def load_menu_screen(name):
    username = name

    # wipe the screen
    for widget in root.winfo_children():
        widget.destroy()

    # load menu
    root.rowconfigure(
        0,
        weight=1
    )
    root.rowconfigure(
        1,
        weight=2
    )
    root.rowconfigure(
        2,
        weight=1
    )
    root.columnconfigure(
        0,
        weight=1,
        minsize=root.winfo_width()/4
    )
    root.columnconfigure(
        1,
        weight=2,
        minsize=root.winfo_width()/2
    )
    root.columnconfigure(
        2,
        weight=1,
        minsize=root.winfo_width()/4
    )

    label = tk.Label(
        font=('Segoe UI', 16),
        text='Hello ' + username
    )
    label.grid(
        column=0,
        row=0,
        sticky='NW',
        columnspan=3
    )

    # create the frame for the menu
    menu_frame = ttk.Frame(root)
    menu_frame.grid(
        column=1,
        row=1,
        padx=5,
        pady=5
    )

    menu_frame.grid_rowconfigure(
        0,
        weight=1
    )
    menu_frame.grid_columnconfigure(
        0,
        weight=1
    )

    # create a canvas for scrolling in
    canvas = tk.Canvas(menu_frame)
    canvas.grid(
        column=0,
        row=0
    )

    # scrollbar on the side
    scrollbar = ttk.Scrollbar(
        menu_frame,
        orient='vertical',
        command=canvas.yview
    )
    scrollbar.grid(
        column=1,
        row=0,
        sticky='ns'
    )
    canvas.configure(yscrollcommand=scrollbar.set)

    # frame for holding the patient widgets inside the canvas
    patient_frame = ttk.Frame(canvas)

    patient_window = canvas.create_window(
        (0, 0),
        window=patient_frame,
        anchor="nw"
    )

    # Sample patients
    patients = get_patient(username)

    # Create a button for each patient
    for patient in patients:
        button = ttk.Button(
            patient_frame,
            text=f"{patient['first_name']}, "
                 f"{patient['last_name']} | "
                 f"ID: {patient['ID']}, | "
                 f"DOB: {patient['date_of_birth']}",
            command=lambda p=patient, u=username: load_patient_screen(p, u)
        )
        button.pack(
            fill="x",
            padx=20,
            pady=20,
            ipady=20
        )

    # Login button -> new window with user info
    logout = ttk.Button(
        root,
        text='Logout',
        command=lambda: load_login_screen()
    )
    logout.grid(
        column=1,
        row=2,
        sticky=''
    )

# Update the scrollable area when content changes
    def update_scroll_region(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    patient_frame.bind(
        "<Configure>",
        update_scroll_region
    )

# Keep the inner frame the same width as the canvas
    def resize_patient_frame(event):
        canvas.itemconfigure(
            patient_window,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        resize_patient_frame
    )

# load patient screen
def load_patient_screen(patient, name):
    patient_name = patient["first_name"]
    username = name

    # wipe the screen
    for widget in root.winfo_children():
        widget.destroy()

    # load menu
    root.rowconfigure(
        0,
        weight=1
    )
    root.rowconfigure(
        1,
        weight=2
    )
    root.rowconfigure(
        2,
        weight=2
    )
    root.rowconfigure(
        3,
        weight=2
    )
    root.rowconfigure(
        4,
        weight=1
    )
    root.columnconfigure(
        0,
        weight=1,
        minsize=root.winfo_width()/4
    )
    root.columnconfigure(
        1,
        weight=1,
        minsize=root.winfo_width()/4
    )
    root.columnconfigure(
        2,
        weight=2,
        minsize=root.winfo_width()/4
    )
    root.columnconfigure(
        3,
        weight=1,
        minsize=root.winfo_width()/4
    )
    root.columnconfigure(
        4,
        weight=1,
        minsize=root.winfo_width()/4
    )

    # back button
    back_botton = ttk.Button(
        root,
        text='Back',
        command=lambda: load_menu_screen(username)
    )
    back_botton.grid(
        column=1,
        row=3,
        sticky='NW'
    )

    # drug menu creation
    # create the left frame for the menu
    left_menu_frame = ttk.Frame(root)
    left_menu_frame.grid(
        column=0,
        row=2,
        padx=5,
        pady=5,
        columnspan= 2,
        sticky= ''
    )

    left_menu_frame.grid_rowconfigure(
        0,
        weight=1
    )
    left_menu_frame.grid_columnconfigure(
        0,
        weight=1
    )

    # create a canvas for scrolling in
    left_canvas = tk.Canvas(left_menu_frame)
    left_canvas.grid(
        column=0,
        row=0
    )

    # scrollbar on the side
    left_scrollbar = ttk.Scrollbar(
        left_menu_frame,
        orient='vertical',
        command=left_canvas.yview
    )
    left_scrollbar.grid(
        column=1,
        row=0,
        sticky='ns'
    )
    left_canvas.configure(yscrollcommand=left_scrollbar.set)

    # frame for holding the drugs widgets inside the canvas
    left_drug_frame = ttk.Frame(left_canvas)

    left_drug_window = left_canvas.create_window(
        (0, 0),
        window=left_drug_frame,
        anchor="nw"
    )

    # Sample patients
    drugs = get_drug(patient_name)

    # list for drugs that will be dispensed
    dispense_table = []

    # Create a button for each patient
    def refresh_drug_frame():
        for widget in left_drug_frame.winfo_children():
            widget.destroy()

        for drug in drugs:
            def on_click(d=drug):
                # nonlocal dispense_table

                dispense_table.append(d)
                amount_given(d["name"])
                drugs.remove(d)

                # refresh the screen
                refresh_drug_frame()
                refresh_dispense_frame()

            button = ttk.Button(
                left_drug_frame,
                text=drug["name"],
                command=on_click
            )
            button.pack(
                fill="x",
                padx=20,
                pady=20,
                ipady=20
            )

    refresh_drug_frame()

    # create the right frame for the menu
    right_menu_frame = ttk.Frame(root)
    right_menu_frame.grid(
        column=2,
        row=2,
        padx=5,
        pady=5,
        columnspan=2,
        sticky=''
    )

    right_menu_frame.grid_rowconfigure(
        0,
        weight=1
    )
    right_menu_frame.grid_columnconfigure(
        0,
        weight=1
    )

    # create a canvas for scrolling in
    right_canvas = tk.Canvas(right_menu_frame)
    right_canvas.grid(
        column=0,
        row=0
    )

    # scrollbar on the side
    right_scrollbar = ttk.Scrollbar(
        right_menu_frame,
        orient='vertical',
        command=right_canvas.yview
    )
    right_scrollbar.grid(
        column=1,
        row=0,
        sticky='ns'
    )
    right_canvas.configure(yscrollcommand=right_scrollbar.set)

    # frame for holding the drugs widgets inside the canvas
    right_drug_frame = ttk.Frame(right_canvas)

    right_drug_window = right_canvas.create_window(
        (0, 0),
        window=right_drug_frame,
        anchor="nw"
    )

    def refresh_dispense_frame():
        for widget in right_drug_frame.winfo_children():
            widget.destroy()

        for drug in dispense_table:
            def on_click(d=drug):

                drugs.append(d)
                dispense_table.remove(d)

                refresh_dispense_frame()
                refresh_drug_frame()

            button = ttk.Button(
                right_drug_frame,
                text=drug["name"],
                command=on_click
            )
            button.pack(
                fill="x",
                padx=20,
                pady=20,
                ipady=20
            )

    refresh_dispense_frame()

    # Update the scrollable area when content changes
    def update_scroll_region(event=None):
        left_canvas.configure(
            scrollregion=left_canvas.bbox("all")
        )
        right_canvas.configure(
            scrollregion=right_canvas.bbox("all")
        )

    left_drug_frame.bind(
        "<Configure>",
        update_scroll_region
    )
    right_drug_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    # Keep the inner frame the same width as the canvas
    def resize_drug_frame(event):
        left_canvas.itemconfigure(
            left_drug_window,
            width=event.width
        )
        right_canvas.itemconfigure(
            right_drug_window,
            width=event.width
        )

    left_canvas.bind(
        "<Configure>",
        resize_drug_frame
    )
    right_canvas.bind(
        "<Configure>",
        resize_drug_frame
    )

ctypes.windll.shcore.SetProcessDpiAwareness(1)

# create main window
root = tk.Tk()
root.attributes(
    '-fullscreen',
    True
)

load_login_screen()

root.mainloop()