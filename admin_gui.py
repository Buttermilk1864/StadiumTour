import customtkinter as ctk
from tkinter import messagebox
import csv
import googlemaps
import os

# --- CONFIG ---
API_KEY = "AIzaSyAoo4zXBVWd7A_o6Q348qWwKraEV09OAQs"
gmaps = googlemaps.Client(key=API_KEY)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") # Looks sharp with baseball colors

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("⚾ Stadium Tour - Scouting Report Control Center")
        self.geometry("600x850")

        # Header
        self.header = ctk.CTkLabel(self, text="GAME DAY ITINERARY", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(pady=20)

        # Scrollable Frame for Fields
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=550, height=600)
        self.scroll_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.entries = {}
        
        # Define our Scouting Report Fields
        self.setup_field("Date", "e.g. 2026-06-10")
        self.setup_dropdown("Action", ["Travel", "Activity", "Food"])
        self.setup_dropdown("Method", ["Drive", "Fly", "Bus", "Train", "Subway", "Walk"])
        self.setup_field("Destination", "e.g. PNC Park")
        self.setup_field("Starting Time", "e.g. 08:00 AM")
        self.setup_field("Starting Location", "e.g. Home")
        self.setup_field("Starting Address", "Full Address for GPS")
        self.setup_field("Ending Time", "e.g. 05:00 PM")
        self.setup_field("Ending Location", "e.g. Hotel")
        self.setup_field("Ending Address", "Full Address for GPS")

        # Action Buttons
        self.save_btn = ctk.CTkButton(self, text="SAVE TO LOG", fg_color="#2d5a27", hover_color="#1e3d1a", command=self.save_data)
        self.save_btn.pack(pady=10, padx=40, fill="x")

        self.push_btn = ctk.CTkButton(self, text="PUSH TO LIVE DASHBOARD 🚀", fg_color="#3b3b3b", command=self.push_live)
        self.push_btn.pack(pady=10, padx=40, fill="x")

    def setup_field(self, label, placeholder):
        lbl = ctk.CTkLabel(self.scroll_frame, text=label)
        lbl.pack(pady=(10, 0), padx=20, anchor="w")
        entry = ctk.CTkEntry(self.scroll_frame, placeholder_text=placeholder, width=450)
        entry.pack(pady=(0, 10), padx=20)
        self.entries[label] = entry

    def setup_dropdown(self, label, options):
        lbl = ctk.CTkLabel(self.scroll_frame, text=label)
        lbl.pack(pady=(10, 0), padx=20, anchor="w")
        combo = ctk.CTkComboBox(self.scroll_frame, values=options, width=450)
        combo.pack(pady=(0, 10), padx=20)
        self.entries[label] = combo

    def save_data(self):
        # Fetch Google Data automatically
        start_addr = self.entries["Starting Address"].get()
        end_addr = self.entries["Ending Address"].get()
        dist, dur = "N/A", "N/A"

        if start_addr and end_addr:
            try:
                res = gmaps.distance_matrix(start_addr, end_addr, mode="driving")
                dist = res['rows'][0]['elements'][0]['distance']['text']
                dur = res['rows'][0]['elements'][0]['duration']['text']
            except:
                pass

        row = [self.entries[k].get() for k in self.entries.keys()] + [dist, dur]
        
        with open('itinerary.csv', 'a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        
        messagebox.showinfo("Logged", "The play has been recorded!")

    def push_live(self):
        os.system('git add .')
        os.system('git commit -m "Itinerary Update"')
        os.system('git push')
        messagebox.showinfo("Sent", "The Dashboard has been updated!")

if __name__ == "__main__":
    app = App()
    app.mainloop()