import customtkinter as ctk
import threading
from screenshot import Screenshot
import totxt
from gpt import send_prompt
from tkinter.scrolledtext import ScrolledText
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import mss
from screeninfo import get_monitors
import numpy as np


class CustomGUI(tk.Tk):
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.geometry("1200x800")  # Increased window size for better spacing
        self.app.title("CaseSpy")
        
        # Add last_response tracking
        self.last_response = None

        self.setup_widgets()

    def add_log(self, message):
        """Add a log message to the log text box"""
        self.log_text_box.config(state='normal')
        self.log_text_box.insert(tk.END, f"{message}\n")
        self.log_text_box.see(tk.END)  # Scroll to the end
        self.log_text_box.config(state='disabled')

    def setup_widgets(self):
        # API Key section
        api_label = ctk.CTkLabel(self.app, text="API Configuration", font=("Helvetica", 14, "bold"))
        api_label.place(x=50, y=30)
        
        self.api_key_entry = ctk.CTkEntry(self.app, width=400, placeholder_text="API Key:")
        self.api_key_entry.place(x=50, y=70)

        self.solve_button = ctk.CTkButton(self.app, text="Solve", command=self.sendToApi, width=100, height=40)
        self.solve_button.place(x=470, y=70)

        # First Screenshot section
        first_shot_label = ctk.CTkLabel(self.app, text="First Screenshot Configuration", font=("Helvetica", 14, "bold"))
        first_shot_label.place(x=50, y=140)
        
        # First Screenshot coordinates
        self.topleftLabel_X = ctk.CTkLabel(self.app, text="Top-right x")
        self.topleftLabel_X.place(x=50, y=180)

        self.topleft_x1 = ctk.CTkEntry(self.app, width=100, placeholder_text="topLeft x1 (px)")
        self.topleft_x1.place(x=50, y=210)
        self.topleft_x1.insert(0,"0")

        self.topleftLabel_Y = ctk.CTkLabel(self.app, text="Top-right y")
        self.topleftLabel_Y.place(x=170, y=180)

        self.topleft_y1 = ctk.CTkEntry(self.app, width=100, placeholder_text="topLeft y1 (px)")
        self.topleft_y1.place(x=170, y=210)
        self.topleft_y1.insert(0,"0")

        self.bottomleftLabel_X = ctk.CTkLabel(self.app, text="Bottom-Left X")
        self.bottomleftLabel_X.place(x=290, y=180)

        self.bottomRight_x1 = ctk.CTkEntry(self.app, width=100, placeholder_text="bottomRight x1 (px)")
        self.bottomRight_x1.place(x=290, y=210)
        self.bottomRight_x1.insert(0,"0")

        self.bottomleftLabel_Y = ctk.CTkLabel(self.app, text="Bottom-Left Y")
        self.bottomleftLabel_Y.place(x=410, y=180)

        self.bottomRight_y1 = ctk.CTkEntry(self.app, width=100, placeholder_text="bottomRight y1 (px)")
        self.bottomRight_y1.place(x=410, y=210)
        self.bottomRight_y1.insert(0,"0")

        self.screenshotBTN1 = ctk.CTkButton(self.app, width=100, height=35, corner_radius=20, text="TakeShot1", command=lambda: self.sendScreenShotData1())
        self.screenshotBTN1.place(x=530, y=210)

        # Second Screenshot section
        second_shot_label = ctk.CTkLabel(self.app, text="Second Screenshot Configuration", font=("Helvetica", 14, "bold"))
        second_shot_label.place(x=50, y=280)
        
        # Second Screenshot coordinates
        self.topleft_x2 = ctk.CTkEntry(self.app, width=100, placeholder_text="topLeft x2 (px)")
        self.topleft_x2.place(x=50, y=320)
        self.topleft_x2.insert(0,"0")

        self.topleft_y2 = ctk.CTkEntry(self.app, width=100, placeholder_text="topLeft y2 (px)")
        self.topleft_y2.place(x=170, y=320)
        self.topleft_y2.insert(0,"0")

        self.bottomRight_x2 = ctk.CTkEntry(self.app, width=100, placeholder_text="bottomRight x2 (px)")
        self.bottomRight_x2.place(x=290, y=320)
        self.bottomRight_x2.insert(0,"0")

        self.bottomRight_y2 = ctk.CTkEntry(self.app, width=100, placeholder_text="bottomRight y2 (px)")
        self.bottomRight_y2.place(x=410, y=320)
        self.bottomRight_y2.insert(0,"0")

        self.screenshotBTN2 = ctk.CTkButton(self.app, width=100, height=35, corner_radius=20, text="TakeShot2", command=lambda: self.sendScreenShotData2())
        self.screenshotBTN2.place(x=530, y=320)

        # Logs section
        logs_label = ctk.CTkLabel(self.app, text="Logs", font=("Helvetica", 14, "bold"))
        logs_label.place(x=50, y=400)  # Placed just above the log text box

        # Log text box
        self.log_text_box = ScrolledText(self.app, width=100, height=20, wrap='word', state='disabled', font=("Helvetica", 10))
        self.log_text_box.place(x=50, y=540)

        # Results section
        results_label = ctk.CTkLabel(self.app, text="Results", font=("Helvetica", 14, "bold"))
        results_label.place(x=880, y=30)
        

        # Output text box
        self.result_text_box = ScrolledText(self.app, width=80, height=45, wrap='word', state='disabled', font=("Helvetica", 10))
        self.result_text_box.place(x=850, y=70)

        self.previous_button = ctk.CTkButton(self.app, text="Solve", width=100, height=40)

        # Add initial log message
        self.add_log("Application started...")

    def sendScreenShotData1(self):
        self.screenshot = Screenshot()
        self.add_log("Taking first screenshot...")
        threading.Thread(target=self.screenshot.take_shot1, args=(int(self.topleft_x1.get()), int(self.topleft_y1.get()), int(self.bottomRight_x1.get()), int(self.bottomRight_y1.get()))).start()
        self.add_log("First screenshot taken successfully")

    def sendScreenShotData2(self):
        self.screenshot = Screenshot()
        self.add_log("Taking second screenshot...")
        threading.Thread(target=self.screenshot.take_shot2, args=(int(self.topleft_x2.get()), int(self.topleft_y2.get()), int(self.bottomRight_x2.get()), int(self.bottomRight_y2.get()))).start()
        self.add_log("Second screenshot taken successfully")

    def sendToApi(self, model_choice=None):
        self.result_text_box.config(state='normal')
        self.result_text_box.delete(1.0, tk.END)
        self.result_text_box.insert(tk.END, "Loading...")
        self.result_text_box.config(state='disabled')
        self.add_log("Processing request...")
        
        self.totxt = totxt.Totxt()  
        prompt_text = self.totxt.imgToTxt()  
        
        if(prompt_text == "no screenshot found"):
            self.result_text_box.config(state='normal')
            self.result_text_box.delete(1.0, tk.END)
            self.result_text_box.insert(tk.END, prompt_text)
            self.result_text_box.config(state='disabled')
            self.last_response = prompt_text
            self.add_log("Error: No screenshot found")
            return prompt_text

        else:
            api_key = self.api_key_entry.get()
            self.add_log("Sending request to API...")

            def thread_target(prompt_text, api_key, model_choice):
                model = model_choice if model_choice is not None else 1  # Default to Grok
                response = send_prompt(prompt_text, api_key, api_key, model)
                self.app.after(0, self.showApiResponse, response)
                self.last_response = response
                self.add_log("Response received from API")
                return response

            thread = threading.Thread(target=thread_target, args=(prompt_text, api_key, model_choice))
            thread.start()
            return "Processing request..."

    def showApiResponse(self, response):
        print("Response SUCCESSFUL!")
        self.result_text_box.config(state='normal')
        self.result_text_box.delete(1.0, tk.END)
        self.result_text_box.insert(tk.END, response)
        self.result_text_box.config(state='disabled')
        self.last_response = response
        self.add_log("Response displayed successfully")

    def run(self):
        self.app.mainloop()

