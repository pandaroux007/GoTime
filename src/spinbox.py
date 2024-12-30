# based on https://customtkinter.tomschimansky.com/tutorial/spinbox
import customtkinter as ctk
from typing import Callable

class Spinbox(ctk.CTkFrame):
    def __init__(self, *args, value_from: tuple[int, None]=None,
                value_to: tuple[int, None]=None,
                width: int=100, height: int=32,
                enter_key_command: Callable=None,
                placeholder: str, text_variable=None, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        
        self.grid_columnconfigure(0, weight=1) # entry expands
        self.grid_columnconfigure((1, 2), weight=0) # buttons don't expand
        
        self.entry = ctk.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, textvariable=text_variable)
        self.entry.grid(row=0, column=0, columnspan=1, padx=(3, 0), pady=3, sticky="ew")
        if placeholder:
            self.entry.configure(placeholder_text=placeholder)
        else:
            self._write_value_in_entry(0) # default value
        # https://stackoverflow.com/questions/55184324/why-is-calling-register-required-for-tkinter-input-validation
        self.entry.configure(validate="key", validatecommand=(self.entry.register(self._validate_numeric_input), "%P"))

        self.subtract_button = ctk.CTkButton(self, text="-", width=height-6, height=height-6, command=self._subtract_button_callback)
        self.subtract_button.grid(row=0, column=1, padx=3, pady=3)

        self.add_button = ctk.CTkButton(self, text="+", width=height-6, height=height-6, command=self._add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # ------------------------ internal values
        if isinstance(value_from, int):
            self._from = value_from
        else:
            self._from = None
        if isinstance(value_to, int):
            self._to = value_to
        else: self._to = None

        if enter_key_command:
            self.enter_key_command = enter_key_command
            self.entry.bind(sequence='<Return>', command=lambda event: self.enter_key_command())
        else:
            self.enter_key_command = None

    # ------------------------ public methods
    def get(self) -> int:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value):
        self._write_value_in_entry(value)

    def clear(self): self._write_value_in_entry(0)

    def desabled(self):
        self.add_button.configure(state=ctk.DISABLED)
        self.subtract_button.configure(state=ctk.DISABLED)
        self.entry.configure(state=ctk.DISABLED)

    def enable(self):
        self.add_button.configure(state=ctk.NORMAL)
        self.subtract_button.configure(state=ctk.NORMAL)
        self.entry.configure(state=ctk.NORMAL)

    # ------------------------ private methods of internal operation
    def _write_value_in_entry(self, value):
        self.entry.delete(0, ctk.END)
        self.entry.insert(0, str(value))
    
    def _add_button_callback(self):
        try:
            if self.entry.get() != "":
                value = int(self.entry.get()) + 1
            else: value = 1
            if self._to is not None:
                if self._to >= value:
                    self._write_value_in_entry(value)
            else:
                self._write_value_in_entry(value)
        except ValueError:
            return

    def _subtract_button_callback(self):
        try:
            if self.entry.get() != "":
                value = int(self.entry.get()) - 1
            else: value = 0
            if self._from is not None:
                if self._from <= value:
                    self._write_value_in_entry(value)
            else:
                self._write_value_in_entry(value)
        except ValueError:
            return
        
    def _validate_numeric_input(self, text):
        return text.isdigit() or text.startswith("-") or text == ""

""" app = ctk.CTk()

box = Spinbox(app, width=200, enter_key_command=lambda: foo(10), placeholder="bar")
box.pack(padx = 10, pady = 10)

def foo(value: int):
    print("value: " + (str(value - box.get())))

app.mainloop() """