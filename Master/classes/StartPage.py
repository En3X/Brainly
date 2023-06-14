import tkinter as tk
from classes import VoiceControlled, Mannual, AutomatedControl


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)


        self.DRIVING_MODE = "NONE"

        self.title = "Brainly - A Vehicle With a Brain"
        self.width = int(self.winfo_screenwidth() / 1.5)
        self.height = int(self.winfo_screenheight() / 1.5)
        self.resizable(False, False)
        self.geometry(f"{self.width}x{self.height}")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Create different page instances and add them to the frames dictionary
        for PageClass in (HomeScreen, Mannual.ManualControlPage, AutomatedControl.AutomatedControlPage, VoiceControlled.VoiceControlPage):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the home page
        self.show_frame("HomeScreen")

    def show_frame(self, page_name):
        # Raise the desired frame to the front
        frame = self.frames[page_name]
        frame.tkraise()


class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Make a selection", font=("Arial", 24, "bold"))
        label.pack(pady=50)

        # Card 1 - Manual Control
        manual_card = tk.Frame(self, bg="white", relief="solid", bd=1)
        manual_card.pack(fill="both", expand=True, padx=50, pady=20)

        manual_label = tk.Label(manual_card, text="Manual Control", font=("Arial", 16))
        manual_label.pack(pady=10)

        manual_card.bind("<Button-1>", lambda event: self.go_to_page("ManualControlPage"))

        # Card 2 - Automated Control
        automated_card = tk.Frame(self, bg="white", relief="solid", bd=1)
        automated_card.pack(fill="both", expand=True, padx=50, pady=20)

        automated_label = tk.Label(automated_card, text="Automated Control", font=("Arial", 16))
        automated_label.pack(pady=10)

        automated_card.bind("<Button-1>", lambda event: self.go_to_page("AutomatedControlPage"))

        # Card 3 - Voice Control
        voice_card = tk.Frame(self, bg="white", relief="solid", bd=1)
        voice_card.pack(fill="both", expand=True, padx=50, pady=20)

        voice_label = tk.Label(voice_card, text="Voice Control", font=("Arial", 16))
        voice_label.pack(pady=10)

        voice_card.bind("<Button-1>", lambda event: self.go_to_page("VoiceControlPage"))

    def go_to_page(self, page_name):
        self.controller.show_frame(page_name)


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
