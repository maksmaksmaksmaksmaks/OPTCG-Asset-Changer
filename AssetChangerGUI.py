import os
import shutil
import time
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import AssetChanger


# pyinstaller --onefile --collect-all UnityPy --collect-all archspec TESTING_FOLDER/AssetChangerGUI.py


class Asset:
    def __init__(self, name: str, h: int, w: int, desc: str, path: str = ""):
        self.name = name
        self.h = h
        self.w = w
        self.desc = desc
        self.path = path

    def show(self):
        return f"{self.name} |{self.w}x{self.h}| {self.desc}"

    def __str__(self):
        return f"{self.name} |{self.w}x{self.h}| {self.desc} | {self.path}"


class ItemEditor:
    def __init__(self, root):
        self.edit_item_name = tk.StringVar()
        self.edit_item_name.set("")

        self.current_item = None
        self.current_path = tk.StringVar()
        self.current_path.set("")

        # automatic image updates
        self.current_path.trace('w', self.update_image)

        self.image_label = None

        self.root = root
        self.root.title("OPTCGSim Asset-Changer")
        self.root.geometry("700x500")

        self.items = [
            Asset("buttonLong_beige", 49, 190, "the button for everything, it gets stretched"),
            Asset("HighlightSquare", 178, 178, "highlight on selected cards and don"),
            Asset("Arrow", 30, 60, "the red arrow showing who attacks and where"),
            Asset("AttackArrow", 100, 200, "the wide power is displayed over"),
            Asset("panel_beige", 100, 100, "background for choosing game and some labels"),
            Asset("arrow_beige", 100, 100, "arrows for checking trash"),
            Asset("Background", 32, 32, "chat background"),
            Asset("YouLose", 90, 391, "you lose screen"),
            Asset("YouWin", 88, 377, "you win screen"),
            Asset("toppng.com-download-blue-glow-effect-1024x1024", 835, 835,
                  "the glow effect for prio - it has a blue filter over :3"),
            Asset("Checkmark", 64, 64, "checkmark in deck builder and timed lobby"),
            Asset("ClydeBanner", 500, 1500, "ad banner - transparency doesn't work"),
            Asset("ImpactBanner", 500, 1500, "ad banner - transparency doesn't work"),
            Asset("CrossBanner", 400, 1000, "ad banner"),
            Asset("DropdownArrow", 64, 64, "arrow on all dropdowns"),
            Asset("InputFieldBackground", 32, 32, "just for the deck name"),
            Asset("Launch_bounty", 133, 500, "- transparency doesn't work"),
            Asset("MatchHistory", 133, 500, "- transparency doesn't work"),
            Asset("TCGMM_discord", 139, 488, "- transparency doesn't work"),
            Asset("PatronAsk", 270, 1080, "/"),
            Asset("UIMask", 32, 32, "deck editor background for where you pick cards from"),
            Asset("UISprite", 32, 32, "dropdowns, checkboxes and game select buttons"),
            Asset("audioOff", 50, 50, "/"),
            Asset("audioOn", 50, 50, "/"),
            Asset("musicOff", 50, 50, "/"),
            Asset("musicOn", 50, 50, "/"),
        ]
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self.root, text="Select Items to Edit", font=("Arial", 14, "bold")).pack(pady=5)

        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left side - Item selection
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side='left', fill='y', padx=(0, 10))

        tk.Label(left_frame, text="Items:", font=("Arial", 10, "bold")).pack(anchor='w')

        # Listbox with scrollbar
        listbox_frame = tk.Frame(left_frame)
        listbox_frame.pack(fill='both', expand=True)

        self.listbox = tk.Listbox(listbox_frame, selectmode='single', width=35)
        scrollbar = tk.Scrollbar(listbox_frame, orient='vertical', command=self.listbox.yview)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # load pre existing
        if os.path.isfile('changes.txt'):
            with open('changes.txt', 'r') as f:
                lines = f.readlines()
                print(lines)
            for line in lines:
                if line[0] == '#':
                    continue
                try:
                    for item in self.items:
                        if item.name == line.split(':')[0].strip():
                            item.path = line.split(':')[1].strip()
                except Exception as e:
                    print(e)

        # Populate listbox
        for asset in self.items:
            self.listbox.insert('end', f"{asset.name}: {'-' if asset.path == '' else asset.path}")

        self.listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Bind selection event
        self.listbox.bind('<<ListboxSelect>>', self.on_selection_change)

        # Buttons for selection
        button_frame = tk.Frame(left_frame)
        button_frame.pack(fill='x', pady=5)

        # Right side - Edit area
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)

        tk.Label(right_frame, text=f"Edit Selected Item:", ).pack()
        tk.Label(right_frame, textvariable=self.edit_item_name, ).pack()

        canvas = tk.Canvas(right_frame, bg='white')
        self.edit_frame = tk.Frame(canvas)

        canvas.pack(side='left', fill='both', expand=True)

        canvas.create_window((0, 0), window=self.edit_frame, anchor='nw')
        self.entry_widgets = {}

        # Bottom frm
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill='x', padx=10, pady=5)

        tk.Button(bottom_frame, text="Make Changes", command=self.change_assets,
                  bg="#4CAF50", fg="white").pack(side='left', padx=5)

    def on_selection_change(self, event=None):
        # Clear existing entry widgets
        for widget in self.edit_frame.winfo_children():
            widget.destroy()
        self.entry_widgets.clear()

        # Get selected items
        if not self.listbox.curselection():
            return
        selected_index = self.listbox.curselection()[0]
        self.current_item = self.items[selected_index]
        self.current_path.set(self.current_item.path)
        # print(selected_index)
        top_frame = tk.Frame(self.edit_frame)
        top_frame.pack(fill='x')

        # Label
        self.edit_item_name.set(self.items[selected_index].show())
        # Entry
        entry = tk.Entry(top_frame, textvariable=self.current_path)
        entry.config(state='disabled')
        entry.pack(side='right', fill='x', expand=True)

        # filename = askopenfilename()
        # button2 = tk.Button(top_frame, text=f"Save", command=self.save_changes)
        # button2.pack(side='right')

        button = tk.Button(top_frame, text=f"Pick an image", command=self.get_image)
        button.pack(side='left')
        button = tk.Button(top_frame, text=f"Reset", command=self.reset_image)
        button.pack(side='left')

        # print(f"images/{self.current_path.get()}")
        bottom_frame = tk.Frame(self.edit_frame)
        bottom_frame.pack(fill='both', expand=True)

        self.image_label = tk.Label(bottom_frame, text="No image selected")
        self.image_label.pack()

        self.current_path.set(self.current_item.path)

        self.entry_widgets[selected_index] = entry

    def update_image(self, *args):
        # Check if image_label exists AND is still a valid widget
        if (not hasattr(self, 'image_label') or
                self.image_label is None or
                not self.image_label.winfo_exists()):
            return

        path = self.current_path.get()
        if not path:
            self.image_label.configure(image='', text="No image selected")
            return

        try:
            image = tk.PhotoImage(file=f"images/{path}")
            self.image_label.configure(image=image, text='')
            self.image_label.image = image
        except (tk.TclError, FileNotFoundError) as e:
            print(f"Error loading image '{path}': {e}")
            self.image_label.configure(image='', text=f"Error loading: {path}")
        except tk.TclError as widget_error:
            # Handle case where widget was destroyed
            print(f"Widget no longer exists: {widget_error}")
            self.image_label = None

    def save_changes(self):
        # Update items with new values
        self.items[self.items.index(self.current_item)].path = self.current_path.get()
        self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for asset in self.items:
            self.listbox.insert('end', f"{asset.name}: {'-' if asset.path == '' else asset.path}")

    def get_image(self):
        imgpath = askopenfilename(title=f"{self.current_item.name} |{self.current_item.w}x{self.current_item.h}|",
                                  filetypes=[
                                      ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                                  ])
        if imgpath == '':
            return

        if not os.path.exists("images/"):
            os.makedirs("images/")
        try:
            shutil.copy(imgpath, f"images/{imgpath.split('/')[-1]}")
        except shutil.SameFileError:
            pass
        except Exception as e:
            print(e)
        self.current_path.set(imgpath.split('/')[-1])
        self.save_changes()

        print(f"{self.current_path.get()} -> {self.current_item.name}")

    def reset_image(self):
        self.current_path.set("")
        self.save_changes()
    def change_assets(self):
        changes = ""
        for asset in self.items:
            if asset.path != "":
                changes += f"{asset.name} : {asset.path}\n"

        with open('changes.txt', 'w') as f:
            f.write(changes)

        # print(changes)
        time.sleep(1)
        AssetChanger.main()
        print("\n")
        messagebox.showinfo("Finished", "Asset changer finished, if there are any problems check what the console says")

if __name__ == "__main__":

    #so it fakes running from the folder
    if not os.path.isdir("AssetChanger"):
        os.mkdir("AssetChanger")
    os.chdir("AssetChanger")

    root = tk.Tk()
    app = ItemEditor(root)
    root.mainloop()
