import os
import PIL.Image
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

class ImageCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Cropper")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        
        self.input_folder = StringVar()
        self.output_folder = StringVar()
        self.output_name = StringVar()
        self.width_value = IntVar()
        self.height_value = IntVar()
        
        self.create_widgets()

    def create_widgets(self):
        # First screen - Select input and output folders
        self.frame1 = Frame(self.root)
        self.frame1.pack(pady=20)

        label1 = Label(self.frame1, text="Input Folder:")
        label1.grid(row=0, column=0, padx=10, pady=10)

        input_entry = Entry(self.frame1, textvariable=self.input_folder, width=30)
        input_entry.grid(row=0, column=1, padx=10)

        input_browse_btn = Button(self.frame1, text="Browse", command=self.browse_input_folder)
        input_browse_btn.grid(row=0, column=2, padx=10)

        label2 = Label(self.frame1, text="Output Folder:")
        label2.grid(row=1, column=0, padx=10, pady=10)

        output_entry = Entry(self.frame1, textvariable=self.output_folder, width=30)
        output_entry.grid(row=1, column=1, padx=10)

        output_browse_btn = Button(self.frame1, text="Browse", command=self.browse_output_folder)
        output_browse_btn.grid(row=1, column=2, padx=10)

        next_btn = Button(self.root, text="Next", command=self.goto_next_screen)
        next_btn.pack(pady=10)

        # Second screen - Configure output settings
        self.frame2 = Toplevel(self.root)
        self.frame2.withdraw()

        label3 = Label(self.frame2, text="Output Name:")
        label3.grid(row=0, column=0, padx=10, pady=10)

        output_name_entry = Entry(self.frame2, textvariable=self.output_name, width=30)
        output_name_entry.grid(row=0, column=1, padx=10)

        label4 = Label(self.frame2, text="Crop Resolution:")
        label4.grid(row=1, column=0, padx=10, pady=10)

        width_slider = Scale(self.frame2, from_=512, to=1024, orient=HORIZONTAL, variable=self.width_value, length=200, tickinterval=64)
        width_slider.grid(row=1, column=1, padx=10)

        height_slider = Scale(self.frame2, from_=512, to=1024, orient=HORIZONTAL, variable=self.height_value, length=200, tickinterval=64)
        height_slider.grid(row=2, column=1, padx=10)

        back_btn = Button(self.frame2, text="Back", command=self.goto_prev_screen)
        back_btn.grid(row=3, column=0, pady=10)

        process_btn = Button(self.frame2, text="Process", command=self.crop_images)
        process_btn.grid(row=3, column=1, pady=10)

        self.root.bind('<Return>', self.crop_images)


    def browse_input_folder(self):
        folder_path = filedialog.askdirectory()
        self.input_folder.set(folder_path)

    def browse_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder.set(folder_path)

    def goto_next_screen(self):
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()

        if input_folder and output_folder:
            self.root.geometry("400x250")
            self.root.title("Image Cropper - Settings")
            self.root.resizable(False, False)

            self.width_value.set(512)
            self.height_value.set(512)

            self.frame1.pack_forget()
            self.frame2.deiconify()
        else:
            messagebox.showwarning("Warning", "Please select both input and output folders.")

    def goto_prev_screen(self):
        self.root.geometry("400x200")
        self.root.title("Image Cropper")
        self.root.resizable(False, False)

        self.frame1.pack()
        self.frame2.withdraw()

    def crop_images(self, event=None):
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()
        output_name = self.output_name.get()
        width = self.width_value.get()
        height = self.height_value.get()

        if output_name:
            try:
                os.makedirs(output_folder + "/cropped", exist_ok=True)

                image_list = os.listdir(input_folder)

                for i, image_name in enumerate(image_list, start=1):
                    image_path = os.path.join(input_folder, image_name)
                    image = PIL.Image.open(image_path)

                    # Crop and save the image
                    top_left = image.crop((0, 0, width, height))
                    top_right = image.crop((image.width - width, 0, image.width, height))
                    bottom_left = image.crop((0, image.height - height, width, image.height))
                    bottom_right = image.crop((image.width - width, image.height - height, image.width, image.height))

                    top_left.save(f"{output_folder}/cropped/{output_name} ({i * 4 - 3}).jpg")
                    top_right.save(f"{output_folder}/cropped/{output_name} ({i * 4 - 2}).jpg")
                    bottom_left.save(f"{output_folder}/cropped/{output_name} ({i * 4 - 1}).jpg")
                    bottom_right.save(f"{output_folder}/cropped/{output_name} ({i * 4}).jpg")

                images_done = len(image_list) * 4
                messagebox.showinfo("Process Complete", f"{images_done} images cropped and saved successfully.")
            except PermissionError:
                messagebox.showerror("Error", "Permission denied. Please select a different output folder.")
            except FileNotFoundError:
                messagebox.showerror("Error", "Invalid folder path.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showwarning("Warning", "Please enter an output name.")

root = Tk()
app = ImageCropper(root)
root.mainloop()
