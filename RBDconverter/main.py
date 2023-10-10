import tkinter
from tkinter import font as tkFont  # for convenience
from tkinter import ttk
from tkinter import filedialog
import rbd_converter


def main():
    window = tkinter.Tk()
    window.title('RBD converter')
    # This coefficient used to preserve the proportions fo 4 and 8k monitors
    cof = round(window.winfo_screenwidth() / 1920)

    window_width = 600 * cof
    window_height = 300 * cof

    # get the screen dimension
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    # print(screen_width, screen_height)

    # find the center point
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)

    # set the position of the window to the center of the screen
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    window.resizable(False, False)
    window.attributes('-topmost', 1)
    window.iconbitmap('logo.ico')

    tkFont.nametofont('TkDefaultFont').configure(size=20)

    button1 = ttk.Button(
        window,
        text='Single PGS directory',
        command=lambda: rbd_converter.convert(get_dir(), ''))

    button2 = ttk.Button(
        window,
        text="Directory with multiple PGS subdirectories",
        command=lambda: rbd_converter.multi_convert(get_dir()))

    button1.place(x=0, y=0, width=window_width, height=window_height / 2)
    button2.place(x=0, y=window_height / 2, width=window_width, height=window_height / 2)
    window.mainloop()


def get_dir():
    directory = filedialog.askdirectory()
    return directory


main()
