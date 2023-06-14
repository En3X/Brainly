import tkinter as tk
import tkinter.ttk as ttk
class VoiceControlPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Voice Control Page", font=("Arial", 24, "bold"))
        label.pack(pady=50)

        back_button = ttk.Button(self, text="Back", command=lambda: self.go_to_page("HomeScreen"))
        back_button.pack(pady=10)





    def go_to_page(self, page_name):
        self.controller.show_frame(page_name)
