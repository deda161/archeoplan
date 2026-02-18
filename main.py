import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import threading

from data_parser import DataParser
from graphic_creator import GraphicCreator

ctk.set_appearance_mode("system")

how_to_text = "Will be added soon..."

class ArcheoplanGUI:
    def __init__(self):
        """
        Initialize main window
        """
        self.thread = None
        self.north_direction = 'top'
        self.root = ctk.CTk()
        self.root.title("Arheoplan")

        self._configure_main_frame()

        self.root.update_idletasks()

        width = self.main_frame.winfo_reqwidth() + 40
        height = self.main_frame.winfo_reqheight() + 40

        self.root.geometry(f"{width}x{height}")
        self.root.resizable(False, False)

        self.data_parsing_done = False

    def _configure_main_frame(self):
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

        directions = ["Top", "Bottom", "Left", "Right"]
        self.combobox_label = ctk.CTkLabel(self.main_frame, text="Choose North direction:", font=("Arial", 12))
        self.combobox_label.grid(row=2, column=0, padx=10)

        self.combobox = ctk.CTkComboBox(
            self.main_frame,
            values=directions,
            command=self.on_combobox_select,
            border_color="#3498db",
            button_color="#3498db",
            button_hover_color="#2980b9",
            dropdown_fg_color="#2b2b2b",
            dropdown_hover_color="#3498db",
            dropdown_text_color="white"
        )
        self.combobox.grid(row=3, column=0, padx=20, pady=10)

        self.combobox.set("Top")

        ctk.CTkButton(
            self.main_frame,
            text="Generate",
            command=self._generate_cb
        ).grid(row=4, column=0, padx=20, pady=10)

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

        self.how_to_window.transient(self)
        self.how_to_window.update_idletasks()
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
        file_path = filedialog.askopenfilename(
                    title="Choose Excel file...",
                    filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
                )

        if file_path:

            if not file_path.lower().endswith(('.xlsx', '.xls')):
                self._draw_error_or_info_dialog_window('Error', '❌ Not Excel format!')
                return

            data_parser = DataParser(file_path)
            data_parser.read_data_from_file()
            data_parser.prepare_data()

            self.rows, self.conlumns = data_parser.get_squares_matrix_size()
            self.matrix = data_parser.get_squares_matrix()
            self.raw_data = data_parser.get_processed_data()

            self.data_parsing_done = True
        else:
            self._draw_error_or_info_dialog_window('Error', '❌ Please, choose Excel file!')

    def _generate_cb(self):
        """
        Generate callback
        """
        if self.data_parsing_done:
            graphic_creator = GraphicCreator()
            self.thread = threading.Thread(target=graphic_creator.make_plots(self.rows, self.conlumns, self.matrix, self.raw_data, self.north_direction))
            self.thread.start()
        else:
            self._draw_error_or_info_dialog_window('Error', '❌ Please, load and parse data first!')

    def _check_thread(self):
        if self.thread.is_alive():
                self.root.after(100, self._check_thread, self.thread)

    def on_combobox_select(self, choice):
        self.north_direction = choice

    def _draw_error_or_info_dialog_window(self, title_text, message_text):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title_text)
        dialog.resizable(False, False)

        # Make the dialog modal
        dialog.grab_set()

        # Label text
        label = ctk.CTkLabel(
            dialog,
            text=message_text,
            font=("Arial", 14)
        )
        label.pack(pady=20)

        # Close button
        btn_ok = ctk.CTkButton(
            dialog,
            text="Close",
            command=dialog.destroy,
            width=100
        )
        btn_ok.pack(pady=10)

        dialog.transient(self)
        dialog.update_idletasks()
        dialog.geometry("")
        dialog.wait_window()

    def run(self):
        """Start the App"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ArcheoplanGUI()
    app.run()