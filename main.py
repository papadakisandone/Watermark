import pathlib
import tkinter
from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageDraw, ImageFont
import glob

from tqdm import tqdm  # progress bar for the terminal


def choose_directory():
    window.directory = tkinter.filedialog.askdirectory()
    FOLDER_PATH = window.directory

    # print(FOLDER_PATH)
    label_choose['text'] = FOLDER_PATH
    button_folder['text'] = "Change Folder Path"
    load_images_from_folder(FOLDER_PATH)

    labeltext = 'Choose the Folder with the Images -->'
    if label_choose['text'] != labeltext and label_choose['text'] != '':
        #                                                     top, bottom space
        label_watermark.grid(column=0, row=1, sticky=W, pady=(20, 2))
        entry_watermark.grid(column=0, row=2, sticky=W, pady=2)
        button_start.grid(column=0, row=3, sticky=W, pady=2)
    else:
        label_choose['text'] = labeltext
        button_folder['text'] = 'Select Folder'


def load_images_from_folder(FOLDER_PATH):
    FOLDER_PATH = FOLDER_PATH + '/'
    ext = ['png', 'jpg', ]  # Add image formats here

    # create list with paths, that contains extensions from ext list
    [files.extend(glob.glob(FOLDER_PATH + '*.' + e)) for e in ext]
    # print(files)


def start_to_add_watermark():
    # Gets text from the entry
    watermark_text = entry_watermark.get()
    print(watermark_text)

    for img_path in tqdm(files, desc='wait', colour='blue'):
        img = Image.open(img_path)
        width, height = img.size

        draw = ImageDraw.Draw(img)
        text = watermark_text

        font = ImageFont.truetype('arial.ttf', 26)
        textwidth, textheight = draw.textsize(text, font)

        # calculate the x,y coordinates of the text
        margin = 10
        x = width - textwidth - margin
        y = height - textheight - margin

        # draw watermark in the bottom right corner
        draw.text((x, y), text, font=font)

        # create the directory if not exist
        pathlib.Path('img/img_watermark').mkdir(parents=True, exist_ok=True)
        # Save watermarked image
        img.save(f"img/img_watermark/{img_path.split('img')[1]}")

        label_info.grid(column=0, row=5, sticky=W, pady=2)
        label_info.config(text='WaterMark Completed!!!')
    print("WaterMark Completed!!!")


if __name__ == '__main__':
    FOLDER_PATH = ""
    # images = []
    files = []
    img_names = []

    window = Tk()
    window.title("Add Watermark")
    window.minsize(width=500, height=300)
    window.config(padx=10, pady=10)

    # ---------------------------UI------------------------------------------------------------
    # -----------------Select folder-------------
    label_choose = tkinter.Label(text="Choose the Folder with the Images -->", font=("Arial", 10, 'italic'))
    label_choose.grid(column=0, row=0, sticky=W, pady=2)

    button_folder = Button(text="Select Folder", command=choose_directory)
    button_folder.grid(column=1, row=0, sticky=W, pady=2)
    # -----------------------------------------------------------

    # -----------------WaterMark--------------------------------
    label_watermark = tkinter.Label(text="Add your text for the watermark", font=("Arial", 10))

    # WaterMark Text
    entry_watermark = Entry(width=60, fg='grey')

    # Add some text to begin with
    entry_watermark.insert(END, string="example: Papadakis.Com")

    button_start = Button(text="Start ", command=start_to_add_watermark, width=20)

    label_info = tkinter.Label(text="In Progress, Please Wait", font=("Arial", 16, 'bold'))
    # -----------------------------------------------------

window.mainloop()
