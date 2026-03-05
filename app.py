import os

from dotenv import load_dotenv

import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
from pypdf import PdfReader, PdfWriter
from tkinter import filedialog

selected_file = None
total_pages = 0

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
load_dotenv()  # .env dosyasını okur

os.environ["TCL_LIBRARY"] = os.getenv("TCL_LIBRARY")
os.environ["TK_LIBRARY"] = os.getenv("TK_LIBRARY")

class App(TkinterDnD.Tk):

    def __init__(self):
        super().__init__()

        self.title("PDF Page Extractor")
        self.geometry("500x400")

        self.label = ctk.CTkLabel(
            self,
            text="PDF Page Extractor",
            font=("Arial", 20),
            text_color="black"
        )

        self.label.pack(pady=30)

        self.drop_area = ctk.CTkFrame(
            self,
            width=400,
            height=120,
            fg_color="#1f1f1f",
            border_width=2,
            border_color="#444444"
        )
        self.drop_area.pack(pady=10)

        self.drop_label = ctk.CTkLabel(
            self.drop_area,
            text="Drag & Drop PDF Here",
            text_color="red",
            font=("Arial", 16)
        )
        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        self.drop_label.place(relx=0.5, rely=0.5, anchor="center")

        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.drop)

        self.file_label = ctk.CTkLabel(self, text="", text_color="white")
        self.file_label.pack()

        self.page_label = ctk.CTkLabel(self, text="", text_color="white")
        self.page_label.pack()

        self.calc_label = ctk.CTkLabel(self, text="", text_color="lightgreen")
        self.calc_label.pack()

        self.start_entry = ctk.CTkEntry(
            self,
            placeholder_text="Start Page",
            text_color="white",
            fg_color="#2b2b2b",
            border_color="#555555"
        )
        self.start_entry.pack(pady=10)

        self.end_entry = ctk.CTkEntry(
            self,
            placeholder_text="End Page",
            text_color="white",
            fg_color="#2b2b2b",
            border_color="#555555"
        )
        self.end_entry.pack(pady=10)

        self.start_entry.bind("<KeyRelease>", self.calculate_pages)
        self.end_entry.bind("<KeyRelease>", self.calculate_pages)

        self.extract_button = ctk.CTkButton(self, text="Extract PDF", command=self.extract)
        self.extract_button.pack(pady=20)

    def drop(self, event):
        global selected_file, total_pages

        selected_file = event.data.strip("{}")

        reader = PdfReader(selected_file)
        total_pages = len(reader.pages)

        filename = os.path.basename(selected_file)

        self.file_label.configure(text=f"Loaded: {filename}", text_color="black")
        self.page_label.configure(text=f"Total Pages: {total_pages}", text_color="black")

    def calculate_pages(self, event=None):
        try:
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())

            if end < start:
                self.calc_label.configure(text="Error: End page cannot be less than start page", text_color="red")
                return
            
            if start < 1 or end > total_pages:
                self.calc_label.configure(text=f"Error: Pages must be between 1 and {total_pages}", text_color="red")
                return

            pages = end - start + 1

            self.calc_label.configure(text=f"Extracting {pages} pages", text_color="black")

        except ValueError:
            self.calc_label.configure(text="")
        except:
            self.calc_label.configure(text="")

    def extract(self):
        try:
            if not selected_file:
                self.calc_label.configure(text="Error: No PDF file loaded", text_color="red")
                return
                
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())

            if end < start:
                self.calc_label.configure(text="Error: End page cannot be less than start page", text_color="red")
                return
            
            if start < 1 or end > total_pages:
                self.calc_label.configure(text=f"Error: Pages must be between 1 and {total_pages}", text_color="red")
                return

            reader = PdfReader(selected_file)
            writer = PdfWriter()

            for i in range(start - 1, end):
                writer.add_page(reader.pages[i])

            output = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
            )

            if not output:
                return

            with open(output, "wb") as f:
                writer.write(f)

            self.calc_label.configure(text="PDF created successfully!", text_color="lightgreen")

        except ValueError:
            self.calc_label.configure(text="Error: Please enter valid page numbers", text_color="red")
        except Exception as e:
            self.calc_label.configure(text=f"Error: {str(e)}", text_color="red")


app = App()
app.mainloop()
