# PROFESSIONAL PORTFOLIO PROJECT
# PROJECT NAME - Image Watermarking Desktop App
# PROJECT FUNCTIONALITY - A desktop app (implemented with python and tkinter) used for watermarking an image.

from tkinter import *
from tkinter import ttk, filedialog, messagebox, font, colorchooser
from PIL import ImageTk, Image, UnidentifiedImageError, ImageGrab

APP_DEFAULT_IMAGE = "place_photo_here.png"
BG_COL_FOR_CANVAS = None
BG_COL_FOR_WINDOWS = None
MAX_NO_WATERMARK_CHARS = 3
##
FONT_SIZES = [size_num for size_num in range(11, 41)]
FONT_WEIGHTS = [font.BOLD, font.ITALIC, font.NORMAL, font.ROMAN]
WATERMARK_ORIENTATIONS = [angle for angle in range(360)]
##
selected_img_name = None
selected_img = None
watermark_text = None
##
watermark_font_ppts = ["ariel", 20, "bold"]
watermark_position_coordinates = []
##
watermark_x_position_values = [""]
watermark_y_position_values = [""]


# FUNCTIONS
def add_wm_text():
    """Adds a watermark text to the uploaded image."""
    global watermark_text

    if selected_img:
        if watermark_text_entry.get() == "":
            messagebox.showerror(title="Field Empty",
                                 message=f"Field cannot be empty.\nPlease type some text to be used for the watermark."
                                 )
        elif watermark_text_entry.get().strip() == "":
            messagebox.showerror(title="Not Allowed",
                                 message=f"The watermark cannot contain only spaces.\nPlease type some valid character(s)."
                                 )
            watermark_text_entry.delete(first=0, last=END)
        elif len(watermark_text_entry.get()) > MAX_NO_WATERMARK_CHARS:
            messagebox.showerror(title="Maximum Number of Characters Exceeded",
                                 message=f"The watermark cannot contain more than {MAX_NO_WATERMARK_CHARS} characters."
                                 )
            watermark_text_entry.delete(first=0, last=END)
        else:
            watermark_text = watermark_text_entry.get()
            my_canvas.itemconfig(canvas_text, text=watermark_text)
            my_canvas.coords(canvas_text, watermark_position_coordinates)
    else:
        messagebox.showerror(title="No Image Uploaded",
                             message="Please upload an image before adding a watermark text."
                             )
        watermark_text_entry.delete(first=0, last=END)


def choose_wm_colour():
    """Updates the colour of the watermark text."""

    if watermark_text:
        specified_colour = colorchooser.askcolor()
        specified_colour = specified_colour[1]
        my_canvas.itemconfig(canvas_text, fill=specified_colour)
    elif selected_img is None:
        messagebox.showerror(title="No Image Uploaded",
                             message="Please upload an image before updating watermark font colour."
                             )
    elif watermark_text is None:
        messagebox.showerror(title="No Watermark Text",
                             message="Please type a watermark text before updating watermark font colour."
                             )


def choose_wm_font(event):
    """Updates the font type of the watermark text."""
    global watermark_font_ppts

    if watermark_text:
        selected_font = font_type_combobox.get()
        try:
            watermark_font_ppts[0] = selected_font
            my_canvas.itemconfig(canvas_text, font=watermark_font_ppts)
        except TclError:
            messagebox.showerror(title="Incompatible Font",
                                 message=f"The '{selected_font}' font is incompatible with the watermark.\nPlease select another font."
                                 )
            font_type_combobox.set("")
    elif selected_img is None:
        messagebox.showerror(title="No Image Uploaded",
                             message="Please upload an image before updating watermark font type."
                             )
        font_type_combobox.set("")
    elif watermark_text is None:
        messagebox.showerror(title="No Watermark Text",
                             message="Please type a watermark text before updating watermark font type."
                             )
        font_type_combobox.set("")


def choose_wm_fontsize(event):
    """Updates the font size of the watermark text."""
    global watermark_font_ppts

    if watermark_text:
        selected_fontsize = font_size_combobox.get()
        watermark_font_ppts[1] = selected_fontsize
        my_canvas.itemconfig(canvas_text, font=watermark_font_ppts)
    elif selected_img is None:
        messagebox.showerror(title="No Image Uploaded",
                             message="Please upload an image before updating watermark font size."
                             )
        font_size_combobox.set("")
    elif watermark_text is None:
        messagebox.showerror(title="No Watermark Text",
                             message="Please type a watermark text before updating watermark font size."
                             )
        font_size_combobox.set("")


def choose_wm_fontweight(event):
    """Updates the font weight of the watermark text."""
    global watermark_font_ppts

    if watermark_text:
        selected_fontweight = font_weight_combobox.get()
        watermark_font_ppts[2] = selected_fontweight
        my_canvas.itemconfig(canvas_text, font=watermark_font_ppts)
    elif selected_img is None:
        messagebox.showerror(title="No Image Uploaded",
                             message="Please upload an image before updating watermark font weight."
                             )
        font_weight_combobox.set("")
    elif watermark_text is None:
        messagebox.showerror(title="No Watermark Text",
                             message="Please type a watermark text before updating watermark font weight."
                             )
        font_weight_combobox.set("")


def choose_wm_orientation(event):
    """Updates the orientation of the watermark text."""

    if watermark_text:
        selected_wm_orientation = watermark_orientation_combobox.get()
        my_canvas.itemconfig(canvas_text, angle=selected_wm_orientation)
    elif selected_img is None:
        messagebox.showerror(title="No Image Uploaded",
                             message="Please upload an image before updating watermark orientation."
                             )
        watermark_orientation_combobox.set("")
    elif watermark_text is None:
        messagebox.showerror(title="No Watermark Text",
                             message="Please type a watermark text before updating watermark orientation."
                             )
        watermark_orientation_combobox.set("")


def choose_wm_position(event):
    """Updates the (x- and y- axes) position of the watermark text."""
    global watermark_position_coordinates

    if watermark_text:
        if watermark_x_position_combobox.get():
            selected_x_position = watermark_x_position_combobox.get()
            watermark_position_coordinates[0] = selected_x_position
            my_canvas.coords(canvas_text, watermark_position_coordinates)
        if watermark_y_position_combobox.get():
            selected_y_position = watermark_y_position_combobox.get()
            watermark_position_coordinates[1] = selected_y_position
            my_canvas.coords(canvas_text, watermark_position_coordinates)
    elif selected_img is None:
        messagebox.showerror(title="No Image Uploaded",
                             message="Please upload an image before updating watermark position."
                             )
        watermark_x_position_combobox.set("")
        watermark_y_position_combobox.set("")
    elif watermark_text is None:
        messagebox.showerror(title="No Watermark Text",
                             message="Please type a watermark text before updating watermark position."
                             )
        watermark_x_position_combobox.set("")
        watermark_y_position_combobox.set("")


def do_delete():
    """Deletes the uploaded image from the canvas."""
    global watermark_position_coordinates, watermark_x_position_values, watermark_y_position_values, selected_img, selected_img_name

    widgets_clear()

    selected_img_name = None
    selected_img = None

    watermark_position_coordinates = []
    watermark_x_position_values = [""]
    watermark_y_position_values = [""]



    watermark_features_prompt_label.config(text="")

    my_canvas.config(width=app_default_img.width(), height=app_default_img.height())
    my_canvas.itemconfig(canvas_img, image=app_default_img)
    my_canvas.coords(canvas_img, [app_default_img.width() / 2, app_default_img.height() / 2])
    my_canvas.itemconfig(canvas_text, text="", font=watermark_font_ppts, fill="black", angle="0")
    my_canvas.coords(canvas_text, [app_default_img.width() / 2, app_default_img.height() / 2])

    watermark_x_position_combobox.config(values=watermark_x_position_values)
    watermark_y_position_combobox.config(values=watermark_y_position_values)


def do_refresh():
    """Clears all the watermark features from the uploaded image which is retained on the canvas."""
    global watermark_position_coordinates

    if selected_img:
        widgets_clear()

        watermark_position_coordinates = [selected_img.width() / 2, selected_img.height() / 2]
        my_canvas.itemconfig(canvas_text, text="", font=watermark_font_ppts, fill="black", angle="0")
        my_canvas.coords(canvas_text, watermark_position_coordinates)

        my_window.after(500)
        messagebox.showinfo(title="Refresh Successful",
                            message="Continue using the app by first typing in a watermark text, or close the app if you are done using it."
                            )
    else:
        messagebox.showinfo(title="No Image Available to Refresh",
                            message="Continue using the app by first uploading an image, or close the app if you are done using it."
                            )


def do_save():
    """Saves a watermarked image to a location in the local disk."""
    if watermark_text:
        image_name_before_wm = selected_img_name.split(".")[0]
        image_name_after_wm = image_name_before_wm + "_watermarked"

        x0 = my_canvas.winfo_rootx()
        y0 = my_canvas.winfo_rooty()
        x1 = x0 + my_canvas.winfo_width()
        y1 = y0 + my_canvas.winfo_height()

        file_to_save = filedialog.asksaveasfilename(initialdir="/", title="Save File", defaultextension=".jpg",
                                                    initialfile=image_name_after_wm,
                                                    filetypes=[("jpg file", "*.jpg"), ("png file", "*.png")],
                                                    )
        watermarked_img = ImageGrab.grab(bbox=[x0, y0, x1, y1])
        watermarked_img.save(file_to_save)

        messagebox.showinfo(title="File Saved", message="The file has been saved successfully.")
        do_delete()


    elif selected_img is None:
        messagebox.showerror(title="Image Unavailable", message="Please upload an image and add a watermark to it before saving it.")
    elif watermark_text is None:
        messagebox.showerror(title="No Watermark Text", message="Please add a watermark text to the image before saving it.")


def do_upload():
    """Uploads an image from the local disk to the canvas."""
    global selected_img_name, selected_img, watermark_position_coordinates

    if selected_img:
        prompt_for_re_upload = messagebox.askyesno(title="Image Already Uploaded",
                                               message="Do you want to replace the already-uploaded image?")
        if prompt_for_re_upload:
            do_delete()
            do_upload()
    else:
        image_file_location = filedialog.askopenfilename(initialdir="/", title="Select a file",
                                                         filetypes=[("all files", "*.*"), ("jpg files", "*.jpg"), ("png files", "*.png")]
                                                         )
        try:
            the_image_file = Image.open(image_file_location)
        except UnidentifiedImageError as error_message:
            messagebox.showerror(title="Unidentified Image", message=f"{error_message}.\nPlease select another image.")
        else:
            selected_img_name = image_file_location.split("/")[-1]
            selected_img = ImageTk.PhotoImage(the_image_file)

            watermark_position_coordinates = [selected_img.width() / 2, selected_img.height() / 2]

            my_canvas.config(width=selected_img.width(), height=selected_img.height())
            my_canvas.itemconfig(canvas_img, image=selected_img)
            my_canvas.coords(canvas_img, watermark_position_coordinates)

            get_wm_position_coordinates(image=selected_img)
            widgets_enable()


def get_wm_position_coordinates(image):
    """From an input image, derives a range of integer values to be used as options for each of the watermark positions
    (x and y), and loads same into their respective combo boxes."""
    global watermark_x_position_values, watermark_y_position_values

    max_x_pos_val = round(image.width())
    max_y_pos_val = round(image.height())
    watermark_x_position_values = [x_pos_value for x_pos_value in range(max_x_pos_val + 1) if x_pos_value % 5 == 0]
    watermark_y_position_values = [y_pos_value for y_pos_value in range(max_y_pos_val + 1) if y_pos_value % 5 == 0]

    watermark_x_position_combobox.config(values=watermark_x_position_values)
    watermark_y_position_combobox.config(values=watermark_y_position_values)


def widgets_clear():
    """Re-initialises the variables and widgets of the app"""
    global watermark_text, watermark_font_ppts

    watermark_text = None
    watermark_font_ppts = ["ariel", 20, "bold"]

    watermark_text_entry.delete(first=0, last=END)
    font_type_combobox.set("")
    font_size_combobox.set("")
    font_weight_combobox.set("")
    watermark_x_position_combobox.set("")
    watermark_y_position_combobox.set("")
    watermark_orientation_combobox.set("")


def widgets_enable():
    """Enables the widgets used for specifying and updating the properties of the watermark that is added to an image
    which has been uploaded to the canvas."""

    refresh_img_button.config(state="enabled") #

    watermark_features_prompt_label.config(text="Select Watermark Features")

    watermark_text_prompt_label.config(state="enabled")

    watermark_text_entry.config(state="enabled")

    add_watermark_button.config(state="enabled") #

    font_type_prompt_label.config(state="enabled")

    font_type_combobox.config(state="readonly")

    font_size_prompt_label.config(state="enabled")

    font_size_combobox.config(state="readonly")

    font_weight_prompt_label.config(state="enabled")

    font_weight_combobox.config(state="readonly")

    font_colour_button.config(state="enabled")

    watermark_x_position_prompt_label.config(state="enabled")

    watermark_x_position_combobox.config(state="readonly")

    watermark_y_position_prompt_label.config(state="enabled")

    watermark_y_position_combobox.config(state="readonly")

    watermark_orientation_prompt_label.config(state="enabled")

    watermark_orientation_combobox.config(state="readonly")

    delete_img_button.config(state="enabled")

    save_img_button.config(state="enabled")


# USER INTERFACE
my_window = Tk()
my_window.title("Watermark Desktop App")
my_window.geometry("400x680")
my_window.minsize(width=400, height=680)
my_window.config(padx=25, pady=25, bg=BG_COL_FOR_WINDOWS)

# Styles for the ttk widgets
style = ttk.Style()
style.configure("TButton", padding=2)
style.configure("TCombobox", padding=1)
style.configure("TEntry", padding=1)
style.configure("TLabel", padding=1)

# Widgets
##
welcome_msg_label = ttk.Label()
welcome_msg_label.config(text="*** WELCOME TO THE WATERMARK DESKTOP APP ***")
welcome_msg_label.grid(column=0, row=0, columnspan=5)
##
upload_prompt_msg_label = ttk.Label()
upload_prompt_msg_label.config(text="Click 'Upload Image' to get an image")
upload_prompt_msg_label.grid(column=0, row=1, columnspan=5)
##
app_default_img = ImageTk.PhotoImage(Image.open(APP_DEFAULT_IMAGE))

my_canvas = Canvas()
my_canvas.config(width=app_default_img.width(), height=app_default_img.height(), bg=BG_COL_FOR_CANVAS, highlightthickness=0)
canvas_img = my_canvas.create_image([app_default_img.width() / 2, app_default_img.height() / 2], image=app_default_img)
canvas_text = my_canvas.create_text([app_default_img.width() / 2, app_default_img.height() / 2], text="",
                                    font=watermark_font_ppts, fill="black", angle="0")
my_canvas.grid(column=0, row=2, columnspan=5, padx=25, pady=15)
##
upload_img_button = ttk.Button()
upload_img_button.config(text="Upload Image", command=do_upload)
upload_img_button.grid(column=1, row=3)

refresh_img_button = ttk.Button()
refresh_img_button.config(text="Refresh Image", command=do_refresh, state=DISABLED)
refresh_img_button.grid(column=3, row=3)
##
watermark_features_prompt_label = ttk.Label()
watermark_features_prompt_label.config(text="", foreground="red")
watermark_features_prompt_label.grid(column=0, row=4, columnspan=5, pady=10)
##
watermark_text_prompt_label = ttk.Label()
watermark_text_prompt_label.config(text="Watermark Text", state=DISABLED)
watermark_text_prompt_label.grid(column=0, row=5, columnspan=2, pady=1, sticky="e")

watermark_text_entry = ttk.Entry()
watermark_text_entry.config(width=20, state=DISABLED)
watermark_text_entry.grid(column=2, row=5, pady=1)

add_watermark_button = ttk.Button()
add_watermark_button.config(text="Add Text", command=add_wm_text, state=DISABLED)
add_watermark_button.grid(column=3, row=5, pady=1)
##
font_type_prompt_label = ttk.Label()
font_type_prompt_label.config(text="Font", state=DISABLED)
font_type_prompt_label.grid(column=0, row=6, columnspan=2, pady=1, sticky="e")

font_type_combobox = ttk.Combobox()
font_type_combobox.config(values=font.families(), width=32, state=DISABLED)
font_type_combobox.bind("<<ComboboxSelected>>", choose_wm_font)
font_type_combobox.grid(column=2, row=6, columnspan=3, pady=1)
##
font_size_prompt_label = ttk.Label()
font_size_prompt_label.config(text="Font Size", state=DISABLED)
font_size_prompt_label.grid(column=0, row=7, columnspan=2, pady=1, sticky="e")

font_size_combobox = ttk.Combobox()
font_size_combobox.config(values=FONT_SIZES, width=10, state=DISABLED)
font_size_combobox.bind("<<ComboboxSelected>>", choose_wm_fontsize)
font_size_combobox.grid(column=2, row=7, columnspan=3, pady=1)
##
font_weight_prompt_label = ttk.Label()
font_weight_prompt_label.config(text="Font Weight", state=DISABLED)
font_weight_prompt_label.grid(column=0, row=8, columnspan=2, pady=1, sticky="e")

font_weight_combobox = ttk.Combobox()
font_weight_combobox.config(values=FONT_WEIGHTS, width=10, state=DISABLED)
font_weight_combobox.bind("<<ComboboxSelected>>", choose_wm_fontweight)
font_weight_combobox.grid(column=2, row=8, pady=1)

font_colour_button = ttk.Button()
font_colour_button.config(text="Font Colour", command=choose_wm_colour, state=DISABLED)
font_colour_button.grid(column=3, row=8, pady=1)
##
watermark_x_position_prompt_label = ttk.Label()
watermark_x_position_prompt_label.config(text="X-Position", state=DISABLED)
watermark_x_position_prompt_label.grid(column=0, row=9, columnspan=2, pady=1, sticky="e")

watermark_x_position_combobox = ttk.Combobox()
watermark_x_position_combobox.config(values=watermark_x_position_values, width=10, state=DISABLED)
watermark_x_position_combobox.bind("<<ComboboxSelected>>", choose_wm_position)
watermark_x_position_combobox.grid(column=2, row=9, columnspan=3, pady=1)
##
watermark_y_position_prompt_label = ttk.Label()
watermark_y_position_prompt_label.config(text="Y-Position", state=DISABLED)
watermark_y_position_prompt_label.grid(column=0, row=10, columnspan=2, pady=1, sticky="e")

watermark_y_position_combobox = ttk.Combobox()
watermark_y_position_combobox.config(values=watermark_y_position_values, width=10, state=DISABLED)
watermark_y_position_combobox.bind("<<ComboboxSelected>>", choose_wm_position)
watermark_y_position_combobox.grid(column=2, row=10, columnspan=3, pady=1)
##
watermark_orientation_prompt_label = ttk.Label()
watermark_orientation_prompt_label.config(text="Orientation (°)", state=DISABLED)
watermark_orientation_prompt_label.grid(column=0, row=11, columnspan=2, pady=1, sticky="e")

watermark_orientation_combobox = ttk.Combobox()
watermark_orientation_combobox.config(values=WATERMARK_ORIENTATIONS, width=10, state=DISABLED)
watermark_orientation_combobox.bind("<<ComboboxSelected>>", choose_wm_orientation)
watermark_orientation_combobox.grid(column=2, row=11, columnspan=3, pady=1)
##
delete_img_button = ttk.Button()
delete_img_button.config(text="Delete Image", command=do_delete, state=DISABLED)
delete_img_button.grid(column=1, row=12, pady=5)

save_img_button = ttk.Button()
save_img_button.config(text="Save Image", command=do_save, state=DISABLED)
save_img_button.grid(column=3, row=12, pady=5)
##

my_window.mainloop()
