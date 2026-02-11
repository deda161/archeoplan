import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

from data_parser import DataParser
from graphic_creator import GraphicCreator

ctk.set_appearance_mode("system")

how_to_text = " Arheoplan - это программа для работы с данными о строительных объектах.\n" \
    "Она предоставляет возможность загрузки и обработки данных о строительных объектах,\n" \
    "а также создания и сохранения графических представлений данных в виде карты."

class ArcheoplanGUI:
    def __init__(self):
        """
        Initialize main window
        """
        self.root = ctk.CTk()
        self.root.title("Arheoplan")

        self._confidure_main_frame()

        self.root.update_idletasks()

        width = self.main_frame.winfo_reqwidth() + 40
        height = self.main_frame.winfo_reqheight() + 40

        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)

        self.data_parsing_done = False

    def _confidure_main_frame(self):
        """
        Configure main frame widget
        """
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure
        ctk.CTkButton(
            self.main_frame,
            text="How to...",
            command=self._show_how_to_cb
        ).grid(row=0, column=0, padx=20, pady=10)

        ctk.CTkButton(
            self.main_frame,
            text="Load and parse data",
            command=self._load_and_parse_data_cb
        ).grid(row=1, column=0, padx=20, pady=10)

        ctk.CTkButton(
            self.main_frame,
            text="Configure",
            command=None
        ).grid(row=2, column=0, padx=20, pady=10)

        ctk.CTkButton(
            self.main_frame,
            text="Generate",
            command=self._generate_cb
        ).grid(row=3, column=0, padx=20, pady=10)

    def _show_how_to_cb(self):
        """
        Show how to window with program description and how to use it
        """
        self.how_to_window = ctk.CTkToplevel(self.root)
        self.how_to_window.title("How to use Arheoplan")
        self.how_to_frame = ctk.CTkFrame(self.how_to_window, corner_radius=10)
        self.how_to_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.how_to_frame.grid_columnconfigure

        self.text_label = ctk.CTkLabel(
            self.how_to_frame,
            text = how_to_text,
            font=("Arial", 16),
            wraplength=400,
            justify="left"
        ).grid(row=0, column=0, padx=20, pady=20)

        ctk.CTkButton(
            self.how_to_frame,
            text="Close",
            command=self._close_how_to_cb
        ).grid(row=1, column=0, padx=20, pady=10)

        self.how_to_window.update_idletasks()

        width = self.how_to_frame.winfo_reqwidth() + 40
        height = self.how_to_frame.winfo_reqheight() + 40

        self.how_to_window.geometry(f"{width}x{height}")
        self.how_to_window.resizable(False, False)

    def _close_how_to_cb(self):
        """
        Close how to window callback
        """
        self.how_to_window.destroy()
        self.how_to_window = None
        self.text_label = None
        self.how_to_frame = None

    def _load_and_parse_data_cb(self):
        """
        Load and parse data callback
        """
        data_parser = DataParser('data/test_simple.xlsx')
        data_parser.read_data_from_file()
        data_parser.prepare_data()

        self.rows, self.conlumns = data_parser.get_squares_matrix_size()
        self.matrix = data_parser.get_squares_matrix()
        self.raw_data = data_parser.get_processed_data()

        self.data_parsing_done = True
        print('done')

    def _generate_cb(self):
        """
        Generate callback
        """
        if self.data_parsing_done:
            graphic_creator = GraphicCreator()
            graphic_creator.make_plots(self.rows, self.conlumns, self.matrix, self.raw_data)
            print('generated')

    def run(self):
        """Start the App"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ArcheoplanGUI()
    app.run()