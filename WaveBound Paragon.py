import customtkinter as ctk
from tkinter import messagebox
import cv2
import mss
import re
import numpy as np
import requests
import io
import datetime
import string
import sys
import json
from PIL import Image
import os
import time
import keyboard
from screeninfo import get_monitors
import easyocr
import logging
import threading
import configparser
import pydirectinput
import difflib
import warnings
from queue import Queue

warnings.filterwarnings("ignore", message="CTkLabel Warning: Given image is not CTkImage")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')

# Customization section
BUTTON_COLOR = "#696969"
BUTTON_HOVER_COLOR = "#005999"
LABEL_COLOR = "#FFFFFF"
ENTRY_COLOR = "#2E2E2E"
CHECKBOX_COLOR = "#007ACC"
FRAME_COLOR = "#1E1E1E"
FONT = ("Arial", 16, "bold")
FONTUNITS = ("Arial", 14, "bold")
BUTTON_FONT = ("Arial", 16, "bold")
BUTTON2_FONT = ("Arial", 13, "bold")
BOLD_FONT = ("Arial", 18, "bold")
TAB_FONT = ("Arial", 14, "bold")
STATUS_FONT = ("Arial", 16, "bold")
RESETBUTTON_FONT = ("Arial", 18, "bold")

class UnitWidget(ctk.CTkFrame):
    def __init__(self, master, unit, app, row, col, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.unit = unit
        self.app = app
        self.row = row
        self.col = col

        self.grid(row=self.row, column=self.col, pady=2, padx=2, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.canvas = ctk.CTkCanvas(self, bg=self._apply_appearance_mode(FRAME_COLOR), highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        coords = self.get_layout_coords()

        # Draw border rectangle
        self.border_rect = self.create_clipped_rectangle(*coords["border_rect"], outline="gray50", width=2)

        # Draw all elements on canvas
        self.unit_text = self.canvas.create_text(*coords["unit_text"], text=f"Unit {unit.number}", anchor="n", font=FONTUNITS, fill="white")
    
        self.canvas.create_text(*coords["slot_text"], text="Slot:", anchor="w", font=FONTUNITS, fill="white", tags="slot_text")
        self.slot_var = ctk.StringVar(value=str(unit.slot))
        self.slot_dropdown = ctk.CTkComboBox(self, variable=self.slot_var, values=list(map(str, range(1, 7))), width=50, bg_color=FRAME_COLOR)
        self.canvas.create_window(*coords["slot_dropdown"], window=self.slot_dropdown, anchor="w", tags="slot_dropdown")
    
        self.enabled_var = ctk.BooleanVar(value=unit.enabled)
        self.enable_checkbox = ctk.CTkCheckBox(self, variable=self.enabled_var, command=lambda: self.app.toggle_unit(unit), text="", width=20, bg_color=FRAME_COLOR)
        self.canvas.create_window(*coords["enable_checkbox"], window=self.enable_checkbox, anchor="w", tags="enable_checkbox")
        self.canvas.create_text(*coords["enable_text"], text="Enable", anchor="w", font=FONTUNITS, fill="white", tags="enable_text")
    
        self.set_click_button = ctk.CTkButton(self, text="Set Click Location", command=self.set_click_location, width=140, height=28, fg_color=BUTTON_COLOR, bg_color=FRAME_COLOR, text_color="white", hover_color=BUTTON_HOVER_COLOR)
        self.canvas.create_window(*coords["set_click_button"], window=self.set_click_button, anchor="center", tags="set_click_button")
    
        self.canvas.create_text(*coords["wave_text"], text="Wave:", anchor="e", font=FONTUNITS, fill="white", tags="wave_text")
        self.wave_entry = ctk.CTkEntry(self, width=50, bg_color=FRAME_COLOR)
        self.canvas.create_window(*coords["wave_entry"], window=self.wave_entry, anchor="w", tags="wave_entry")
        self.wave_entry.insert(0, str(unit.wave_number) if unit.wave_number else "")
    
        self.canvas.create_text(*coords["delay_text"], text="Delay:", anchor="e", font=FONTUNITS, fill="white", tags="delay_text")
        self.delay_entry = ctk.CTkEntry(self, width=50, bg_color=FRAME_COLOR)
        self.canvas.create_window(*coords["delay_entry"], window=self.delay_entry, anchor="w", tags="delay_entry")
        self.delay_entry.insert(0, str(unit.sleep_time))
    
        self.click_location_text = ctk.CTkLabel(self, text="Click location: Not set", font=("Arial", 11, "bold"), text_color="white", bg_color=FRAME_COLOR)
        self.canvas.create_window(*coords["click_location_text"], window=self.click_location_text, anchor="center", tags="click_location_text")
        self.unit.location_label = self.click_location_text
    
        self.bind("<Configure>", self.update_layout)

        self.slot_dropdown.configure(command=self.update_slot)
        self.wave_entry.configure(textvariable=self.unit.wave_entry)
        self.delay_entry.configure(textvariable=self.unit.delay_entry)
    
    def get_layout_coords(self):
        center_x = self.winfo_width() / 2
        return {
            "unit_text": (center_x, 5),
            "border_rect": (5, 35, self.winfo_width() - 5, self.winfo_height() - 5),
            "slot_text": (center_x - 50, 60),
            "slot_dropdown": (center_x, 60),
            "enable_checkbox": (center_x - 50, 90),
            "enable_text": (center_x - 20, 90),
            "set_click_button": (center_x, 125),
            "wave_text": (center_x, 160),
            "wave_entry": (center_x + 5, 160),
            "delay_text": (center_x, 195),
            "delay_entry": (center_x + 5, 195),
            "click_location_text": (center_x, 230)
        }

    def create_clipped_rectangle(self, x1, y1, x2, y2, clip_size=5, **kwargs):
            points = [
                x1 + clip_size, y1,
                x2 - clip_size, y1,
                x2, y1 + clip_size,
                x2, y2 - clip_size,
                x2 - clip_size, y2,
                x1 + clip_size, y2,
                x1, y2 - clip_size,
                x1, y1 + clip_size
            ]
            return self.canvas.create_polygon(points, **kwargs, smooth=False, fill='')

    def update_layout(self, event):
        coords = self.get_layout_coords()
    
        self.canvas.coords(self.unit_text, *coords["unit_text"])
        self.canvas.delete(self.border_rect)
        self.border_rect = self.create_clipped_rectangle(*coords["border_rect"], clip_size=5, outline="gray50", width=2)
        self.canvas.coords(self.canvas.find_withtag("slot_text"), *coords["slot_text"])
        self.canvas.coords(self.canvas.find_withtag("slot_dropdown"), *coords["slot_dropdown"])
        self.canvas.coords(self.canvas.find_withtag("enable_checkbox"), *coords["enable_checkbox"])
        self.canvas.coords(self.canvas.find_withtag("enable_text"), *coords["enable_text"])
        self.canvas.coords(self.canvas.find_withtag("set_click_button"), *coords["set_click_button"])
        self.canvas.coords(self.canvas.find_withtag("wave_text"), *coords["wave_text"])
        self.canvas.coords(self.canvas.find_withtag("wave_entry"), *coords["wave_entry"])
        self.canvas.coords(self.canvas.find_withtag("delay_text"), *coords["delay_text"])
        self.canvas.coords(self.canvas.find_withtag("delay_entry"), *coords["delay_entry"])
        self.canvas.coords(self.canvas.find_withtag("click_location_text"), *coords["click_location_text"])

    def update_slot(self, value):
        self.unit.slot = int(value)
        self.unit.slot_var.set(value)

    def update_wave(self, *args):
        self.unit.wave_number = self.wave_entry.get()

    def update_delay(self, *args):
        self.unit.sleep_time = self.delay_entry.get()

    def set_click_location(self):
        overlay = TransparentOverlay(self.app.master, self.on_click_location_set)
        self.app.master.wait_window(overlay)

    def on_click_location_set(self, location):
        self.unit.click_location = location
        self.update_click_location_display()
        logging.info(f"Location set for Unit {self.unit.number}")

    def update_click_location_display(self):
        if self.unit.click_location:
            self.click_location_text.configure(text=f"Click location: {self.unit.click_location[0]}, {self.unit.click_location[1]}")
        else:
            self.click_location_text.configure(text="Click location: Not set")

class ClippedCornerFrame(ctk.CTkFrame):
    def __init__(self, master, corner_radius=10, **kwargs):
        super().__init__(master, **kwargs)
        self.corner_radius = corner_radius
        self.bind('<Configure>', self._draw_clipped_corners)

    def _draw_clipped_corners(self, event=None):
        self.delete('corner')
        width, height = self.winfo_width(), self.winfo_height()
        
        # Create corner shapes
        self.create_polygon((0, self.corner_radius, self.corner_radius, 0, 0, 0),
                            fill=self._apply_appearance_mode(self.cget("fg_color")), tags='corner')
        self.create_polygon((width-self.corner_radius, 0, width, 0, width, self.corner_radius),
                            fill=self._apply_appearance_mode(self.cget("fg_color")), tags='corner')
        self.create_polygon((0, height-self.corner_radius, 0, height, self.corner_radius, height),
                            fill=self._apply_appearance_mode(self.cget("fg_color")), tags='corner')
        self.create_polygon((width, height-self.corner_radius, width-self.corner_radius, height, width, height),
                            fill=self._apply_appearance_mode(self.cget("fg_color")), tags='corner')

class Unit:
    def __init__(self, number):
        self.number = number
        self.slot = 1
        self.enabled = False
        self.click_location = None
        self.wave_number = None
        self.placed = False
        self.upgraded = False
        self.queued_upgrades = set()
        self.completed_upgrades = set()
        self.queued_abilities = set()
        self.completed_abilities = set()
        self.sleep_time = 1  # Default sleep time

        # Add these new attributes
        # Add these new attributes
        self.slot_var = ctk.StringVar(value=str(self.slot))
        self.enabled_var = ctk.BooleanVar(value=self.enabled)
        self.wave_entry = ctk.StringVar(value=str(self.wave_number) if self.wave_number else "")
        self.delay_entry = ctk.StringVar(value=str(self.sleep_time))
        self.location_label = None

    def toggle(self):
        self.enabled = not self.enabled
        self.enabled_var.set(self.enabled)

class RegionSelector(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.parent = parent
        
        # Store the original alpha value
        self.original_alpha = self.parent.attributes("-alpha")
        
        # Make the parent window fully transparent
        self.parent.attributes("-alpha", 0.0)
        
        # Set up the region selector as before
        monitors = get_monitors()
        self.min_x = min(m.x for m in monitors)
        self.min_y = min(m.y for m in monitors)
        max_x = max(m.x + m.width for m in monitors)
        max_y = max(m.y + m.height for m in monitors)
        self.geometry(f"{max_x - self.min_x}x{max_y - self.min_y}+{self.min_x}+{self.min_y}")
        
        self.attributes("-alpha", 0.3)
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.configure(bg='white')

        self.canvas = ctk.CTkCanvas(self, cursor="cross")
        self.canvas.pack(fill=ctk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red", width=2)

    def on_release(self, event):
        x1, y1 = min(self.start_x, event.x), min(self.start_y, event.y)
        x2, y2 = max(self.start_x, event.x), max(self.start_y, event.y)
        self.callback({"top": y1 + self.min_y, "left": x1 + self.min_x, 
                       "width": x2 - x1, "height": y2 - y1})
        self.destroy()
        # Restore the parent window's original opacity
        self.parent.attributes("-alpha", self.original_alpha)

class TransparentOverlay(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.parent = parent
        
        # Store the original alpha value
        self.original_alpha = self.parent.attributes("-alpha")
        
        # Make the parent window fully transparent
        self.parent.attributes("-alpha", 0.0)
        
        # Set up the overlay as before
        monitors = get_monitors()
        self.min_x = min(m.x for m in monitors)
        self.min_y = min(m.y for m in monitors)
        max_x = max(m.x + m.width for m in monitors)
        max_y = max(m.y + m.height for m in monitors)
        self.geometry(f"{max_x - self.min_x}x{max_y - self.min_y}+{self.min_x}+{self.min_y}")
        
        self.attributes("-alpha", 0.3)
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.configure(bg='white')
        self.bind("<Button-1>", self.on_click)

    def on_click(self, event):
        x = event.x_root - self.min_x
        y = event.y_root - self.min_y
        self.callback((x, y))
        self.destroy()
        # Restore the parent window's original opacity
        self.parent.attributes("-alpha", self.original_alpha)

class TDMacro:
    def __init__(self, master, config_file=None):
        self.master = master
        self.master.title("WaveBound OCR")
        self.master.geometry("825x625")

        self.reader = easyocr.Reader(['en'])
        self.num_upgrades = 0
        self.num_abilities = 0
        self.units = [Unit(i) for i in range(1, 21)]
        self.upgrade_unit = None
        self.wave_screenshots = {}
        self.total_waves = 0
        self.highest_wave_seen = 0
        self.total_runs = 0
        self.similarity_threshold = float(config.get('Settings', 'similarity_threshold', fallback='1'))
        self.upgrade_click_location = None
        self.replay_click_location = None
        self.anti_afk_click_location = None
        self.upgrade_queue = Queue()
        self.current_upgrade = None
        self.ability_queue = Queue()
        self.scroll_refresh_rate = 60
        self.dropdown_cache = {}
        self.place_macro_running = False
        self.upgrade_macro_paused = False
        self.replay_macro_running = False
        
        self.wave_screenshot_labels = {}
        self.wave_screenshot_visibility = {}
        self.macro_running = False
        self.macro_loop_interval = int(config.get('Settings', 'macro_loop_interval', fallback='100'))
        
        self.setup_gui()
        self.update_file_list()
        self.macro_event = threading.Event()
        self.macro_thread = None

        self.file_var = ctk.StringVar()
        self.file_var.trace_add("write", self.on_file_selection_change)

        if config_file:
            self.load_config(config_file)

    def setup_gui(self):
        notebook = ctk.CTkTabview(self.master)
        notebook.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        main_tab = notebook.add("Main")
        units_tab = notebook.add("Units")
        wave_tab = notebook.add("Wave")
        upgrade_tab = notebook.add("Upgrade")
        ability_tab = notebook.add("Ability")
        replay_tab = notebook.add("Replay")
        paragon_tab = notebook.add("Paragon")
        anti_afk_tab = notebook.add("Anti-AFK")

        # Set the font for each tab individually
        for tab_name in ["Main", "Units", "Wave", "Upgrade", "Ability", "Replay", "Anti-AFK"]:
            notebook._segmented_button.configure(font=TAB_FONT)

        self.setup_main_tab(main_tab)
        self.setup_units_tab(units_tab)
        self.setup_wave_tab(wave_tab)
        self.setup_upgrade_tab(upgrade_tab)
        self.setup_ability_tab(ability_tab)
        self.setup_replay_tab(replay_tab)
        self.setup_paragon_tab(paragon_tab)
        self.setup_anti_afk_tab(anti_afk_tab)

    def setup_main_tab(self, parent):
        ctk.CTkLabel(parent, text="File Management", font=BOLD_FONT, text_color=LABEL_COLOR).pack(pady=(10, 5))

        new_file_frame = ctk.CTkFrame(parent)
        new_file_frame.pack(pady=5)
        ctk.CTkLabel(new_file_frame, text="New File Name:", font=FONT, text_color=LABEL_COLOR).pack(side=ctk.LEFT, padx=(0, 5))
        self.new_file_entry = ctk.CTkEntry(new_file_frame, width=175, height=35, fg_color=ENTRY_COLOR)
        self.new_file_entry.pack(side=ctk.LEFT)
        ctk.CTkButton(new_file_frame, text="Create", command=self.create_new_file, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT, width=100, height=35).pack(side=ctk.LEFT, padx=(5, 0))

        load_file_frame = ctk.CTkFrame(parent)
        load_file_frame.pack(pady=5)
        ctk.CTkLabel(load_file_frame, text="Load File:", font=FONT, text_color=LABEL_COLOR).pack(side=ctk.LEFT, padx=(0, 5))
        self.file_var = ctk.StringVar()
        self.file_dropdown = ctk.CTkComboBox(load_file_frame, variable=self.file_var, state="readonly", width=200, height=35)
        self.file_dropdown.pack(side=ctk.LEFT)
        self.update_file_list()
        ctk.CTkButton(load_file_frame, text="Load", command=self.load_selected_file, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT, width=80, height=35).pack(side=ctk.LEFT, padx=(5, 0))
        ctk.CTkButton(load_file_frame, text="Save", command=self.save_selected_file, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT, width=80, height=35).pack(side=ctk.LEFT, padx=(5, 0))

        ctk.CTkLabel(parent, text="Macro Keys", font=BOLD_FONT, text_color=LABEL_COLOR).pack(pady=(20, 5))

        start_frame = ctk.CTkFrame(parent)
        start_frame.pack(pady=5)
        ctk.CTkLabel(start_frame, text="Start Macro Key:", font=FONT, text_color=LABEL_COLOR).pack(side=ctk.LEFT, padx=(0, 5))
        self.start_macro_key_entry = ctk.CTkButton(start_frame, text="Click to set", width=100, height=35, 
                                                   command=lambda: self.capture_next_key(self.start_macro_key_entry),
                                                   fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT)
        self.start_macro_key_entry.pack(side=ctk.LEFT)

        stop_frame = ctk.CTkFrame(parent)
        stop_frame.pack(pady=5)
        ctk.CTkLabel(stop_frame, text="Stop Macro Key:", font=FONT, text_color=LABEL_COLOR).pack(side=ctk.LEFT, padx=(0, 5))
        self.stop_macro_key_entry = ctk.CTkButton(stop_frame, text="Click to set", width=100, height=35, 
                                                  command=lambda: self.capture_next_key(self.stop_macro_key_entry),
                                                  fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT)
        self.stop_macro_key_entry.pack(side=ctk.LEFT)

        ctk.CTkLabel(parent, text="Macro Status", font=BOLD_FONT, text_color=LABEL_COLOR).pack(pady=(20, 5))
        self.macro_status_label = ctk.CTkLabel(parent, text="Stopped", font=STATUS_FONT, text_color=LABEL_COLOR)
        self.macro_status_label.pack(pady=5)

        ctk.CTkLabel(parent, text="Discord Webhook", font=BOLD_FONT, text_color=LABEL_COLOR).pack(pady=(5, 0))

        webhook_frame = ctk.CTkFrame(parent)
        webhook_frame.pack(pady=5)
        ctk.CTkLabel(webhook_frame, text="Webhook URL:", font=FONT, text_color=LABEL_COLOR).pack(side=ctk.LEFT, padx=(0, 5))
        self.webhook_url_entry = ctk.CTkEntry(webhook_frame, width=300, fg_color=ENTRY_COLOR)
        self.webhook_url_entry.pack(side=ctk.LEFT)

        ctk.CTkButton(parent, text="Reset Configuration", command=self.reset_configuration, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=RESETBUTTON_FONT, width=200, height=40).pack(pady=20)

        self.update_file_list()

    def capture_next_key(self, button):
        def on_key(event):
            key = event.keysym
            button.configure(text=key)
            self.master.unbind('<Key>')
            if button == self.start_macro_key_entry:
                self.set_start_macro_key()
            elif button == self.stop_macro_key_entry:
                self.set_stop_macro_key()

        self.master.bind('<Key>', on_key)
        button.configure(text="Press a key...")

    def setup_units_tab(self, parent):
        self.current_units_page = 1
        self.units_pages = {}

        for page in range(1, 3):  # 2 pages for 20 units
            frame = ctk.CTkFrame(parent)
            self.units_pages[page] = frame

            for i in range((page-1)*10, page*10):
                unit = self.units[i]
                row = (i % 10) // 5
                col = (i % 10) % 5
                unit_widget = UnitWidget(frame, unit, self, row, col, fg_color="gray86")
                unit_widget.grid(row=row, column=col, pady=2, padx=2, sticky="nsew")

            # Configure grid to expand properly
            for i in range(2):  # 2 rows
                frame.grid_rowconfigure(i, weight=1)
            for i in range(5):  # 5 columns
                frame.grid_columnconfigure(i, weight=1)

        # Add navigation buttons
        nav_frame = ctk.CTkFrame(parent)
        nav_frame.pack(side=ctk.BOTTOM, fill=ctk.X)
        self.prev_page_button = ctk.CTkButton(nav_frame, text="Previous", command=self.prev_units_page, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR)
        self.prev_page_button.pack(side=ctk.LEFT, padx=5, pady=5)
        self.next_page_button = ctk.CTkButton(nav_frame, text="Next", command=self.next_units_page, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR)
        self.next_page_button.pack(side=ctk.RIGHT, padx=5, pady=5)
    
        self.show_units_page(1)

    def show_units_page(self, page):
        for p, frame in self.units_pages.items():
            if p == page:
                frame.pack(fill=ctk.BOTH, expand=True)
            else:
                frame.pack_forget()
        self.current_units_page = page
        self.update_nav_buttons()

    def next_units_page(self):
        if self.current_units_page < len(self.units_pages):
            self.show_units_page(self.current_units_page + 1)

    def prev_units_page(self):
        if self.current_units_page > 1:
            self.show_units_page(self.current_units_page - 1)

    def update_nav_buttons(self):
        self.prev_page_button.configure(state=ctk.NORMAL if self.current_units_page > 1 else ctk.DISABLED)
        self.next_page_button.configure(state=ctk.NORMAL if self.current_units_page < len(self.units_pages) else ctk.DISABLED)

    def setup_wave_tab(self, parent):
        ctk.CTkButton(parent, text="Set Wave Search Region", command=self.set_wave_search_region, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT, width=250, height=35).pack(pady=10)
        self.wave_search_region_label = ctk.CTkLabel(parent, text="Wave Search Region: Not Set", font=FONT, text_color=LABEL_COLOR)
        self.wave_search_region_label.pack(pady=5)

        wave_frame = ctk.CTkFrame(parent)
        wave_frame.pack(pady=10)

    def set_wave_search_region(self):
        region = self.capture_region()
        if region:
            self.wave_search_region = (region['left'], region['top'], region['left'] + region['width'], region['top'] + region['height'])
            self.wave_search_region_label.configure(text=f"Wave Search Region: Set")
            logging.info(f"Wave search region set to: {self.wave_search_region}")
            messagebox.showinfo("Success", "Wave region set successfully")
        else:
            messagebox.showerror("Error", "Failed to set wave region")

    def setup_upgrade_tab(self, parent):
        upgrade_frame = ctk.CTkFrame(parent)
        upgrade_frame.pack(pady=10)

        ctk.CTkLabel(upgrade_frame, text="Number of Upgrades:", font=FONT, text_color=LABEL_COLOR).pack(side=ctk.LEFT, padx=(0, 5))
        self.num_upgrades_entry = ctk.CTkEntry(upgrade_frame, width=50, fg_color=ENTRY_COLOR)
        self.num_upgrades_entry.pack(side=ctk.LEFT)
        self.num_upgrades_entry.insert(0, str(self.num_upgrades))
        ctk.CTkButton(upgrade_frame, text="Set Upgrades", command=self.set_num_upgrades, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT).pack(side=ctk.LEFT, padx=(5, 0))

        ctk.CTkButton(upgrade_frame, text="Set Region", command=self.set_upgrade_region, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT).pack(side=ctk.LEFT, padx=(5, 0))

        ctk.CTkButton(parent, text="Set Upgrade Click Location", command=self.set_upgrade_click_location, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT, width=250, height=35).pack(pady=10)
        self.upgrade_click_location_label = ctk.CTkLabel(parent, text="Upgrade Click Location: Not Set", font=FONT, text_color=LABEL_COLOR)
        self.upgrade_click_location_label.pack(pady=5)

        self.upgrade_region_label = ctk.CTkLabel(parent, text="Upgrade Search Region: Not Set", font=FONT, text_color=LABEL_COLOR)
        self.upgrade_region_label.pack(pady=5)
    
        self.upgrade_scrollable_frame = ctk.CTkScrollableFrame(parent, label_text="Upgrade Settings", label_font=("Arial", 16, "bold"))
        self.upgrade_scrollable_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        self.upgrade_settings = []
        self.update_upgrade_frame()

    def set_upgrade_region(self):
        region = self.capture_region()
        if region:
            self.upgrade_region = (region['left'], region['top'], region['left'] + region['width'], region['top'] + region['height'])
            self.upgrade_region_label.configure(text="Upgrade Search Region: Set")
            logging.info(f"Upgrade search region set to: {self.upgrade_region}")
            messagebox.showinfo("Success", "Upgrade region set successfully")
        else:
            messagebox.showerror("Error", "Failed to set upgrade region")

    def set_upgrade_click_location(self):
        overlay = TransparentOverlay(self.master, self.set_upgrade_click)
        self.master.wait_window(overlay)

    def set_upgrade_click(self, location):
        self.upgrade_click_location = location
        self.upgrade_click_location_label.configure(text=f"Upgrade Click Location: {location[0]}, {location[1]}")
        logging.info(f"Upgrade click location set to: {location}")

    def get_upgrade_settings(self):
        return self.upgrade_settings

    def set_num_upgrades(self):
        try:
            new_num_upgrades = int(self.num_upgrades_entry.get())
            if new_num_upgrades >= 0:
                if new_num_upgrades > self.num_upgrades:
                    # Add new upgrade settings
                    for _ in range(new_num_upgrades - self.num_upgrades):
                        self.upgrade_settings.append({
                            "number": ctk.StringVar(),
                            "unit": ctk.StringVar(),
                            "wave": ctk.StringVar(),
                            "text": ctk.StringVar()
                        })
                elif new_num_upgrades < self.num_upgrades:
                    # Remove excess upgrade settings
                    self.upgrade_settings = self.upgrade_settings[:new_num_upgrades]
            
                self.num_upgrades = new_num_upgrades
                self.update_upgrade_frame()
                messagebox.showinfo("Success", f"Number of upgrades set to {new_num_upgrades}")
            else:
                messagebox.showerror("Invalid Input", "Please enter a non-negative number for upgrades")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for upgrades")

    def update_upgrade_frame(self):
        for widget in self.upgrade_scrollable_frame.winfo_children():
            widget.destroy()

        updates = []
        for i, upgrade in enumerate(self.upgrade_settings):
            upgrade_frame = ctk.CTkFrame(self.upgrade_scrollable_frame, fg_color=FRAME_COLOR)
            content_frame = ctk.CTkFrame(upgrade_frame, fg_color=FRAME_COLOR)
        
            updates.append((upgrade_frame.pack, {'pady': 5, 'fill': ctk.X, 'padx': 10}))
            updates.append((content_frame.pack, {'pady': 5, 'padx': 5, 'fill': ctk.X}))

            label = ctk.CTkLabel(content_frame, text=f"Upgrade {i+1}", font=("Arial", 16, "bold"), text_color=LABEL_COLOR)
            updates.append((label.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
    
            unit_label = ctk.CTkLabel(content_frame, text="Unit:", font=("Arial", 16, "bold"))
            updates.append((unit_label.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
        
            unit_dropdown = ctk.CTkComboBox(content_frame, variable=upgrade["unit"], width=60, state="readonly")
            updates.append((unit_dropdown.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))

            unit_values = [str(i) for i in range(1, 21)]
            CTkScrollableDropdown(unit_dropdown, 
                                  values=unit_values,
                                  command=lambda value, u=upgrade["unit"]: u.set(value),
                                  width=100,
                                  height=150,
                                  frame_corner_radius=5,
                                  button_color=BUTTON_COLOR,
                                  hover_color=BUTTON_HOVER_COLOR,
                                  font=("Arial", 14))

            wave_label = ctk.CTkLabel(content_frame, text="Wave:", font=("Arial", 16, "bold"))
            updates.append((wave_label.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
        
            wave_entry = ctk.CTkEntry(content_frame, textvariable=upgrade["wave"], width=50, font=("Arial", 16, "bold"))
            updates.append((wave_entry.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
    
            text_label = ctk.CTkLabel(content_frame, text="Upgrade Text:", font=("Arial", 16, "bold"))
            updates.append((text_label.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
        
            text_entry = ctk.CTkEntry(content_frame, textvariable=upgrade["text"], width=150, font=("Arial", 16, "bold"))
            updates.append((text_entry.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))

            upgrade["number"].set(str(i+1))  # Set the upgrade number

        # Apply all updates at once
        for widget_method, kwargs in updates:
            widget_method(**kwargs)
    
        self.upgrade_scrollable_frame.update_idletasks()

    def on_upgrade_frame_configure(self, event):
        self.upgrade_canvas.configure(scrollregion=self.upgrade_canvas.bbox("all"))

    def on_upgrade_canvas_configure(self, event):
        canvas_width = event.width
        self.upgrade_canvas.itemconfig(self.upgrade_canvas_frame, width=canvas_width)

    def custom_upgrade_scroll(self, *args):
        self.upgrade_canvas.yview_moveto(args[1])
        self.upgrade_canvas.after(1 // self.scroll_refresh_rate, self.update_upgrade_scroll_region)

    def update_upgrade_scroll_region(self):
        self.upgrade_canvas.configure(scrollregion=self.upgrade_canvas.bbox("all"))

    def setup_ability_tab(self, parent):
        ability_frame = ctk.CTkFrame(parent)
        ability_frame.pack(pady=10)

        ctk.CTkLabel(ability_frame, text="Number of Abilities:", font=FONT, text_color=LABEL_COLOR).pack(side=ctk.LEFT, padx=(0, 5))
        self.num_abilities_entry = ctk.CTkEntry(ability_frame, width=50, fg_color=ENTRY_COLOR)
        self.num_abilities_entry.pack(side=ctk.LEFT)
        self.num_abilities_entry.insert(0, str(self.num_abilities))
        ctk.CTkButton(ability_frame, text="Set Abilities", command=self.set_num_abilities, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT).pack(side=ctk.LEFT, padx=(5, 0))

        ctk.CTkButton(parent, text="Set Ability Click Location", command=self.set_ability_click_location, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT, width=250, height=35).pack(pady=10)

        self.ability_click_location_label = ctk.CTkLabel(parent, text="Ability Click Location: Not Set", font=FONT, text_color=LABEL_COLOR)
        self.ability_click_location_label.pack(pady=5)

        self.ability_scrollable_frame = ctk.CTkScrollableFrame(parent, label_text="Ability Settings", label_font=("Arial", 16, "bold"))
        self.ability_scrollable_frame.pack(fill=ctk.BOTH, expand=True, padx=10, pady=10)

        self.ability_settings = []
        self.update_ability_frame()
        
    def set_ability_click_location(self):
        overlay = TransparentOverlay(self.master, self.set_ability_click)
        self.master.wait_window(overlay)

    def set_ability_click(self, location):
        self.ability_click_location = location
        self.ability_click_location_label.configure(text=f"Ability Click Location: {location[0]}, {location[1]}")
        logging.info(f"Ability click location set to: {location}")

    def set_num_abilities(self):
        try:
            new_num_abilities = int(self.num_abilities_entry.get())
            if new_num_abilities >= 0:
                if new_num_abilities > self.num_abilities:
                    for _ in range(new_num_abilities - self.num_abilities):
                        self.ability_settings.append({
                            "number": ctk.StringVar(),
                            "unit": ctk.StringVar(),
                            "wave": ctk.StringVar(),
                            "delay": ctk.StringVar()  # Add this line
                        })
                elif new_num_abilities < self.num_abilities:
                    self.ability_settings = self.ability_settings[:new_num_abilities]
            
                self.num_abilities = new_num_abilities
                self.update_ability_frame()
                messagebox.showinfo("Success", f"Number of abilities set to {new_num_abilities}")
            else:
                messagebox.showerror("Invalid Input", "Please enter a non-negative number for abilities")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for abilities")

    def update_ability_frame(self):
        for widget in self.ability_scrollable_frame.winfo_children():
            widget.destroy()

        updates = []
        for i, ability in enumerate(self.ability_settings):
            ability_frame = ctk.CTkFrame(self.ability_scrollable_frame, fg_color=FRAME_COLOR)
            updates.append((ability_frame.pack, {'pady': 5, 'fill': ctk.X, 'padx': 10}))
    
            content_frame = ctk.CTkFrame(ability_frame, fg_color=FRAME_COLOR)
            updates.append((content_frame.pack, {'pady': 5, 'padx': 5, 'fill': ctk.X}))

            label = ctk.CTkLabel(content_frame, text=f"Ability {i+1}", font=("Arial", 16, "bold"), text_color=LABEL_COLOR)
            updates.append((label.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
    
            unit_label = ctk.CTkLabel(content_frame, text="Unit:", font=("Arial", 16, "bold"))
            updates.append((unit_label.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
        
            unit_dropdown = ctk.CTkComboBox(content_frame, variable=ability["unit"], width=60, state="readonly")
            updates.append((unit_dropdown.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))

            unit_values = [str(i) for i in range(1, 21)]
            CTkScrollableDropdown(unit_dropdown, 
                                  values=unit_values,
                                  command=lambda value, u=ability["unit"]: u.set(value),
                                  width=100,
                                  height=150,
                                  frame_corner_radius=5,
                                  button_color=BUTTON_COLOR,
                                  hover_color=BUTTON_HOVER_COLOR,
                                  font=("Arial", 14))
    
            wave_label = ctk.CTkLabel(content_frame, text="Wave:", font=("Arial", 16, "bold"))
            updates.append((wave_label.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
            
            wave_entry = ctk.CTkEntry(content_frame, textvariable=ability["wave"], width=50, font=("Arial", 16, "bold"))
            updates.append((wave_entry.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
    
            delay_label = ctk.CTkLabel(content_frame, text="Delay:", font=("Arial", 16, "bold"))
            updates.append((delay_label.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
            
            delay_entry = ctk.CTkEntry(content_frame, textvariable=ability["delay"], width=50, font=("Arial", 16, "bold"))
            updates.append((delay_entry.pack, {'side': ctk.LEFT, 'padx': (0, 5)}))
    
            ability["number"].set(str(i+1))
    
        # Apply all updates at once
        for widget_method, kwargs in updates:
            widget_method(**kwargs)
        
        self.ability_scrollable_frame.update_idletasks()
    
    def setup_replay_tab(self, parent):
        ctk.CTkButton(parent, text="Set Replay Region", command=self.set_replay_region, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT, width=200, height=35).pack(pady=10)
        self.replay_region_label = ctk.CTkLabel(parent, text="Replay Region: Not Set", font=FONT, text_color=LABEL_COLOR)
        self.replay_region_label.pack(pady=5)

        ctk.CTkButton(parent, text="Set Replay Click Location", command=self.set_replay_click_location, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT, width=250, height=35).pack(pady=10)
        self.replay_click_location_label = ctk.CTkLabel(parent, text="Replay Click Location: Not Set", font=FONT, text_color=LABEL_COLOR)
        self.replay_click_location_label.pack(pady=5)

        replay_text_frame = ctk.CTkFrame(parent)
        replay_text_frame.pack(pady=10)
        ctk.CTkLabel(replay_text_frame, text="Replay Text:", font=FONT, text_color=LABEL_COLOR).pack(side=ctk.LEFT, padx=(0, 5))
        self.replay_text_entry = ctk.CTkEntry(replay_text_frame, width=150, fg_color=ENTRY_COLOR)
        self.replay_text_entry.pack(side=ctk.LEFT)

    def set_replay_region(self):
        region = self.capture_region()
        if region:
            self.replay_region = (region['left'], region['top'], region['left'] + region['width'], region['top'] + region['height'])
            self.replay_region_label.configure(text="Replay Region: Set")
            logging.info(f"Replay region set to: {self.replay_region}")
            messagebox.showinfo("Success", "Replay region set successfully")
        else:
            messagebox.showerror("Error", "Failed to set replay region")

    def setup_anti_afk_tab(self, parent):
        ctk.CTkButton(parent, text="Set Anti-AFK Click Location", command=self.set_anti_afk_click_location, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT, width=250, height=35).pack(pady=10)
        self.anti_afk_click_location_label = ctk.CTkLabel(parent, text="Anti-AFK Click Location: Not Set", font=FONT, text_color=LABEL_COLOR)
        self.anti_afk_click_location_label.pack(pady=5)

    def setup_paragon_tab(self, parent):
        # Create a frame for regions and buttons
        region_frame = ctk.CTkFrame(parent, fg_color=FRAME_COLOR)
        region_frame.pack(side="left", padx=10, pady=(50, 10), fill="y")

        # Add padding to the frame
        region_inner_frame = ctk.CTkFrame(region_frame, fg_color=FRAME_COLOR)
        region_inner_frame.pack(padx=5, pady=5)

        ctk.CTkButton(region_inner_frame, text="Set Paragon Region 1", command=self.set_paragon_region_1, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT).pack(pady=5, padx=5)
        ctk.CTkButton(region_inner_frame, text="Set Paragon Region 2", command=self.set_paragon_region_2, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT).pack(pady=5, padx=5)
        ctk.CTkButton(region_inner_frame, text="Set Paragon Region 3", command=self.set_paragon_region_3, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR, font=BUTTON_FONT).pack(pady=5, padx=5)

        self.paragon_region_1_label = ctk.CTkLabel(region_inner_frame, text="Region 1: Not Set", font=FONT, text_color=LABEL_COLOR)
        self.paragon_region_1_label.pack(pady=2)

        self.paragon_region_2_label = ctk.CTkLabel(region_inner_frame, text="Region 2: Not Set", font=FONT, text_color=LABEL_COLOR)
        self.paragon_region_2_label.pack(pady=2)

        self.paragon_region_3_label = ctk.CTkLabel(region_inner_frame, text="Region 3: Not Set", font=FONT, text_color=LABEL_COLOR)
        self.paragon_region_3_label.pack(pady=2)

        priority_frame = ctk.CTkFrame(parent)
        priority_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        ctk.CTkLabel(priority_frame, text="Paragon Priority", font=BOLD_FONT, text_color=LABEL_COLOR).pack(pady=5)

        self.paragon_priorities = [
            "SHIELDED", "REGEN ENEMIES","IMMUNITY", "CHAMPIONS", "THRICE", "DODGE", "STRONG ENEMIES", "FAST ENEMIES", "EXPLOSION", "REVITALIZE", "DROWSY", "QUAKE"
    ]
    
        self.priority_frames = []
    
        for word in self.paragon_priorities:
            frame = ctk.CTkFrame(priority_frame, fg_color=FRAME_COLOR)
            frame.pack(fill="x", pady=2)
            ctk.CTkLabel(frame, text=word, font=FONT, text_color=LABEL_COLOR, bg_color=FRAME_COLOR).pack(side="left", padx=(5, 0))
            down_button = ctk.CTkButton(frame, text="▼", command=lambda w=word: self.move_priority_down(w), 
                                        width=30, height=30, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR)
            down_button.pack(side="right", padx=(0, 5))
            up_button = ctk.CTkButton(frame, text="▲", command=lambda w=word: self.move_priority_up(w), 
                                      width=30, height=30, fg_color=BUTTON_COLOR, hover_color=BUTTON_HOVER_COLOR)
            up_button.pack(side="right", padx=(0, 5))
            self.priority_frames.append(frame)

    def move_priority_up(self, word):
        index = self.paragon_priorities.index(word)
        if index > 0:
            self.paragon_priorities[index], self.paragon_priorities[index-1] = self.paragon_priorities[index-1], self.paragon_priorities[index]
            self.priority_frames[index], self.priority_frames[index-1] = self.priority_frames[index-1], self.priority_frames[index]
            self.update_priority_display()

    def move_priority_down(self, word):
        index = self.paragon_priorities.index(word)
        if index < len(self.paragon_priorities) - 1:
            self.paragon_priorities[index], self.paragon_priorities[index+1] = self.paragon_priorities[index+1], self.paragon_priorities[index]
            self.priority_frames[index], self.priority_frames[index+1] = self.priority_frames[index+1], self.priority_frames[index]
            self.update_priority_display()

    def update_priority_display(self):
        for frame in self.priority_frames:
            frame.pack_forget()
        for word in self.paragon_priorities:
            for frame in self.priority_frames:
                if frame.winfo_children()[0].cget("text") == word:
                    frame.pack(fill="x", pady=2)
                    break

    def set_paragon_region_1(self):
        region = self.capture_region()
        if region:
            self.paragon_region_1 = (region['left'], region['top'], region['left'] + region['width'], region['top'] + region['height'])
            self.paragon_region_1_label.configure(text="Region 1: Set")
            logging.info(f"Paragon region 1 set to: {self.paragon_region_1}")
            messagebox.showinfo("Success", "Paragon region 1 set successfully")
        else:
            messagebox.showerror("Error", "Failed to set paragon region 1")

    def set_paragon_region_2(self):
        region = self.capture_region()
        if region:
            self.paragon_region_2 = (region['left'], region['top'], region['left'] + region['width'], region['top'] + region['height'])
            self.paragon_region_2_label.configure(text="Region 2: Set")
            logging.info(f"Paragon region 2 set to: {self.paragon_region_2}")
            messagebox.showinfo("Success", "Paragon region 2 set successfully")
        else:
            messagebox.showerror("Error", "Failed to set paragon region 2")

    def set_paragon_region_3(self):
        region = self.capture_region()
        if region:
            self.paragon_region_3 = (region['left'], region['top'], region['left'] + region['width'], region['top'] + region['height'])
            self.paragon_region_3_label.configure(text="Region 3: Set")
            logging.info(f"Paragon region 3 set to: {self.paragon_region_3}")
            messagebox.showinfo("Success", "Paragon region 3 set successfully")
        else:
            messagebox.showerror("Error", "Failed to set paragon region 3")

    def set_start_macro_key(self):
        new_key = self.start_macro_key_entry.cget("text")
        if hasattr(self, 'start_macro_key'):
            keyboard.remove_hotkey(self.start_macro_key)
        self.start_macro_key = new_key
        keyboard.add_hotkey(self.start_macro_key, self.start_macro)
        logging.info(f"Start macro key set to: {self.start_macro_key}")

    def set_stop_macro_key(self):
        new_key = self.stop_macro_key_entry.cget("text")
        if hasattr(self, 'stop_macro_key'):
            keyboard.remove_hotkey(self.stop_macro_key)
        self.stop_macro_key = new_key
        keyboard.add_hotkey(self.stop_macro_key, self.stop_macro)
        logging.info(f"Stop macro key set to: {self.stop_macro_key}")

    def toggle_unit(self, unit):
        unit.toggle()
        logging.info(f"Unit {unit.number} {'enabled' if unit.enabled else 'disabled'}")

    def start_click_listener(self, unit):
        self.current_unit = unit
        overlay = TransparentOverlay(self.master, self.set_click_location)
        self.master.wait_window(overlay)

    def set_click_location(self, location):
        self.current_unit.click_location = location
        self.update_click_location_display(self.current_unit)
        logging.info(f"Location set for Unit {self.current_unit.number}")

    def update_click_location_display(self, unit):
        if unit.click_location:
            unit.location_label.configure(text=f"Click location: {unit.click_location[0]}, {unit.click_location[1]}")
        else:
            unit.location_label.configure(text="Click location: Not set")
        
    def capture_region(self):
        self.temp_region = None
        selector = RegionSelector(self.master, self.set_region)
        self.master.wait_window(selector)
        return self.temp_region

    def set_region(self, region):
        self.temp_region = region

    def set_replay_click_location(self):
        overlay = TransparentOverlay(self.master, self.set_replay_click)
        self.master.wait_window(overlay)

    def set_replay_click(self, location):
        self.replay_click_location = location
        self.replay_click_location_label.configure(text=f"Replay Click Location: {location[0]}, {location[1]}")
        logging.info(f"Replay click location set to: {location}")

    def set_anti_afk_click_location(self):
        overlay = TransparentOverlay(self.master, self.set_anti_afk_click)
        self.master.wait_window(overlay)

    def set_anti_afk_click(self, location):
       self.anti_afk_click_location = location
       self.anti_afk_click_location_label.configure(text=f"Anti-AFK Click Location: {location[0]}, {location[1]}")
       logging.info(f"Anti-AFK click location set to: {location}")
       
    def start_macro(self):
        if self.macro_thread and self.macro_thread.is_alive():
            logging.info("Macro is already running")
            return

        # Check for unset regions
        unset_regions = []
        if not hasattr(self, 'wave_search_region'):
            unset_regions.append("Wave")
        if not hasattr(self, 'upgrade_region'):
            unset_regions.append("Upgrade")
        if not hasattr(self, 'replay_region'):
            unset_regions.append("Replay")

        if unset_regions:
            regions_str = "/".join(unset_regions)
            message = f"{regions_str} region{'s' if len(unset_regions) > 1 else ''} not set. Do you wish to start anyway?"
            result = messagebox.askyesno("Warning", message, icon='warning')
            if not result:
                return

        # Reset unit placement and clear upgrade queues before starting the macro
        self.reset_unit_placement()

        self.macro_event = threading.Event()
        self.macro_event.set()
        self.macro_status_label.configure(text="Running")

        if self.highest_wave_seen != 0:
            self.highest_wave_seen = 0
            logging.info("Highest wave reset to 0")

        if self.total_runs != 0:
            self.total_runs = 0
            logging.info("Total runs reset to 0")

        self.macro_thread = threading.Thread(target=self.run_macro_loop, daemon=True)
        self.macro_thread.start()
        logging.info("Macro started")

    def stop_macro(self):
        if self.macro_thread and self.macro_thread.is_alive():
            self.macro_event.clear()
            self.anti_afk_event.clear()
            self.macro_thread.join(timeout=2)  # Wait for the thread to finish
            self.macro_thread = None
        self.macro_status_label.configure(text="Stopped")
        self.reset_unit_placement()
        logging.info("Macro stopped")

    def run_macro_loop(self):
        self.anti_afk_event = threading.Event()
        ability_events = []

        while self.macro_event.is_set():
            self.anti_afk_event.clear()

            current_wave, _ = self.check_wave_change()
            if current_wave:
                logging.info(f"Wave {current_wave} detected in run_macro_loop")
                self.handle_wave(current_wave)

            # Check for upgrades
            while not self.current_upgrade and not self.upgrade_queue.empty():
                self.current_upgrade = self.upgrade_queue.get()
                if not self.upgrade_macro(*self.current_upgrade):
                    return
                self.current_upgrade = None

            # Handle ability activations
            if not self.place_macro_running and not self.replay_macro_running:
                ability_events = [event_tuple for event_tuple in ability_events if not event_tuple[0].is_set()]
                if not self.ability_queue.empty():
                    ability_unit, ability_delay, ability_number = self.ability_queue.get()
                    ability_events.append(self.ability_macro(ability_unit, ability_delay, ability_number))

                for event, unit_number, ability_number in ability_events:
                    if event.is_set():
                        self.activate_ability(unit_number, ability_number)
                        ability_events.remove((event, unit_number, ability_number))

            if self.check_for_replay():
                logging.info("Replay Text Detected")
                if not self.replay_macro():
                    return
                self.reset_unit_placement()

            if self.paragon_macro():
                time.sleep(0.25)

            self.anti_afk_event.set()
            if not self.anti_afk_macro():
                return

            time.sleep(self.macro_loop_interval / 100)

    def handle_wave(self, wave):
        for unit in self.units:
            if unit.enabled and unit.wave_entry.get() and int(unit.wave_entry.get()) == wave and not unit.placed:
                if not self.place_macro(unit.number):
                    return False

        if not hasattr(self, 'upgrade_region'):
            logging.info("Upgrade region not set, skipping upgrade queueing")
            return True

        # Sort upgrades by their number before queueing
        upgrade_settings = sorted(self.get_upgrade_settings(), key=lambda x: int(x['number'].get()))

        for upgrade in upgrade_settings:
            try:
                upgrade_wave = upgrade["wave"].get().lower()
                upgrade_unit = int(upgrade['unit'].get())
                upgrade_number = int(upgrade['number'].get())
                upgrade_text = upgrade['text'].get()
                unit = self.units[upgrade_unit - 1]
        
                # Check if upgrade_wave is a number or any text
                if (upgrade_wave.isdigit() and int(upgrade_wave) == wave) or (not upgrade_wave.isdigit()):
                    if upgrade_number not in unit.queued_upgrades and upgrade_number not in unit.completed_upgrades:
                        logging.info(f"Queueing upgrade {upgrade_number} for unit {upgrade_unit} on wave {wave}")
                        self.upgrade_queue.put((upgrade_unit, upgrade_text, upgrade_number))
                        unit.queued_upgrades.add(upgrade_number)
            except ValueError:
                continue

    # Handle abilities (unchanged)
        for ability in self.ability_settings:
            try:
                ability_wave = int(ability["wave"].get())
                ability_unit = int(ability['unit'].get())
                ability_delay = float(ability['delay'].get())
                ability_number = int(ability['number'].get())
                unit = self.units[ability_unit - 1]
                if (ability_wave == wave and 
                    ability_number not in unit.queued_abilities and 
                    ability_number not in unit.completed_abilities and 
                    hasattr(self, 'ability_click_location') and
                    unit.placed):
                    threading.Timer(ability_delay, self.activate_ability, args=[ability_unit, ability_number]).start()
                    unit.queued_abilities.add(ability_number)
            except ValueError:
                continue

        return True

    def save_config(self, file_name=None):
        if not file_name:
            file_name = self.file_var.get()
    
        if not file_name:
            messagebox.showerror("Error", "No file selected")
            return

        config_dir = os.path.join("configs", file_name)
        os.makedirs(config_dir, exist_ok=True)
    
        config = {
            "units": [],
            "upgrade_click_location": self.upgrade_click_location,
            "replay_click_location": self.replay_click_location,
            "anti_afk_click_location": self.anti_afk_click_location,
            "wave_search_region": self.wave_search_region if hasattr(self, 'wave_search_region') else None,
            "upgrade_region": self.upgrade_region if hasattr(self, 'upgrade_region') else None,
            "replay_region": self.replay_region if hasattr(self, 'replay_region') else None,
            "replay_text": self.replay_text_entry.get(),
            "start_macro_key": self.start_macro_key_entry.cget("text"),
            "stop_macro_key": self.stop_macro_key_entry.cget("text"),
            "num_upgrades": self.num_upgrades,
            "upgrade_settings": [],
            "num_abilities": self.num_abilities,
            "ability_settings": [],
            "ability_click_location": self.ability_click_location if hasattr(self, 'ability_click_location') else None,
            "paragon_region_1": self.paragon_region_1 if hasattr(self, 'paragon_region_1') else None,
            "paragon_region_2": self.paragon_region_2 if hasattr(self, 'paragon_region_2') else None,
            "paragon_region_3": self.paragon_region_3 if hasattr(self, 'paragon_region_3') else None,
            "paragon_priorities": self.paragon_priorities
        }
    
        for upgrade in self.upgrade_settings:
            config["upgrade_settings"].append({
                "number": upgrade["number"].get(),
                "unit": upgrade["unit"].get(),
                "wave": upgrade["wave"].get(),
                "text": upgrade["text"].get()
            })
        
        for ability in self.ability_settings:
            config["ability_settings"].append({
                "number": ability["number"].get(),
                "unit": ability["unit"].get(),
                "wave": ability["wave"].get(),
                "delay": ability["delay"].get()
            })
    
        for unit in self.units:
            unit_config = {
                "number": unit.number,
                "slot": unit.slot_var.get(),
                "enabled": unit.enabled_var.get(),
                "click_location": unit.click_location,
                "wave_number": unit.wave_entry.get(),
                "sleep_time": unit.delay_entry.get(),
            }
            config["units"].append(unit_config)
    
        with open(os.path.join(config_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=4)
    
        self.save_webhook_url(file_name)
    
        logging.info(f"Configuration saved to {file_name}")

    def load_config(self, file_name=None):
        if file_name is None:
            return
        self.file_var.set(file_name)
        config_dir = os.path.join("configs", file_name)
        config_file = os.path.join(config_dir, "config.json")

        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    config = json.load(f)

                self.upgrade_click_location = config.get("upgrade_click_location")
                self.replay_click_location = config.get("replay_click_location")
                self.anti_afk_click_location = config.get("anti_afk_click_location")

                self.wave_search_region = config.get("wave_search_region")
                self.upgrade_region = config.get("upgrade_region")
                self.replay_region = config.get("replay_region")

                self.paragon_region_1 = config.get("paragon_region_1")
                self.paragon_region_2 = config.get("paragon_region_2")
                self.paragon_region_3 = config.get("paragon_region_3")
                self.paragon_priorities = [priority.upper() for priority in config.get("paragon_priorities", self.paragon_priorities)]

                if self.wave_search_region:
                    self.wave_search_region_label.configure(text="Wave Search Region: Set")
                else:
                    self.wave_search_region_label.configure(text="Wave Search Region: Not Set")
    
                if self.upgrade_region:
                    self.upgrade_region_label.configure(text="Upgrade Search Region: Set")
                else:
                    self.upgrade_region_label.configure(text="Upgrade Search Region: Not Set")

                if self.replay_region:
                    self.replay_region_label.configure(text="Replay Region: Set")
                else:
                    self.replay_region_label.configure(text="Replay Region: Not Set")

                if self.paragon_region_1:
                    self.paragon_region_1_label.configure(text="Region 1: Set")
                else:
                    self.paragon_region_1_label.configure(text="Replay Region: Not Set")

                if self.paragon_region_2:
                    self.paragon_region_2_label.configure(text="Region 2: Set")
                else:
                    self.paragon_region_2_label.configure(text="Replay Region: Not Set")

                if self.paragon_region_3:
                    self.paragon_region_3_label.configure(text="Region 3: Set")
                else:
                    self.paragon_region_3_label.configure(text="Replay Region: Not Set")

                start_macro_key = config.get("start_macro_key")
                if start_macro_key and start_macro_key != "Click to set":
                    self.start_macro_key_entry.configure(text=start_macro_key)
                    self.set_start_macro_key()

                stop_macro_key = config.get("stop_macro_key")
                if stop_macro_key and stop_macro_key != "Click to set":
                    self.stop_macro_key_entry.configure(text=stop_macro_key)
                    self.set_stop_macro_key()

                self.num_upgrades = config.get("num_upgrades", 1)
                self.num_upgrades_entry.delete(0, ctk.END)
                self.num_upgrades_entry.insert(0, str(self.num_upgrades))
    
                upgrade_settings = config.get("upgrade_settings", [])
                self.upgrade_settings = []
                for upgrade in upgrade_settings:
                    number_var = ctk.StringVar(value=upgrade.get("number", ""))
                    unit_var = ctk.StringVar(value=upgrade.get("unit", ""))
                    wave_var = ctk.StringVar(value=upgrade.get("wave", ""))
                    text_var = ctk.StringVar(value=upgrade.get("text", ""))
                    self.upgrade_settings.append({
                        "number": number_var,
                        "unit": unit_var,
                        "wave": wave_var,
                        "text": text_var
                    })

                self.ability_click_location = config.get("ability_click_location")
                if self.ability_click_location:
                    self.ability_click_location_label.configure(text=f"Ability Click Location: {self.ability_click_location[0]}, {self.ability_click_location[1]}")
                else:
                    self.ability_click_location_label.configure(text="Ability Click Location: Not Set")

                self.num_abilities = config.get("num_abilities", 0)
                self.num_abilities_entry.delete(0, ctk.END)
                self.num_abilities_entry.insert(0, str(self.num_abilities))

                ability_settings = config.get("ability_settings", [])
                self.ability_settings = []
                for ability in ability_settings:
                    number_var = ctk.StringVar(value=ability.get("number", ""))
                    unit_var = ctk.StringVar(value=ability.get("unit", ""))
                    wave_var = ctk.StringVar(value=ability.get("wave", ""))
                    delay_var = ctk.StringVar(value=ability.get("delay", ""))
                    self.ability_settings.append({
                        "number": number_var,
                        "unit": unit_var,
                        "wave": wave_var,
                        "delay": delay_var
                    })

                replay_text = config.get("replay_text", "")
                self.replay_text_entry.delete(0, ctk.END)
                self.replay_text_entry.insert(0, replay_text)

                webhook_url = self.load_webhook_url(file_name)
                self.webhook_url_entry.delete(0, ctk.END)
                self.webhook_url_entry.insert(0, webhook_url)

                self.update_upgrade_frame()
                self.update_ability_frame()
                self.update_priority_display()

                for unit_config in config.get("units", []):
                    unit_number = unit_config.get("number")
                    if 1 <= unit_number <= len(self.units):
                        unit = self.units[unit_number - 1]
                        unit.slot = unit_config.get("slot", unit_number)
                        unit.slot_var.set(str(unit.slot))
                        unit.enabled = unit_config.get("enabled", False)
                        unit.enabled_var.set(unit.enabled)
                        unit.click_location = unit_config.get("click_location")
                        unit.wave_number = unit_config.get("wave_number")
                        unit.wave_entry.set(str(unit.wave_number) if unit.wave_number else "")
                        unit.sleep_time = unit_config.get("sleep_time", 1.5)
                        unit.delay_entry.set(str(unit.sleep_time))

                        # Update UI elements
                        for widget in self.units_pages[1].winfo_children() + self.units_pages[2].winfo_children():
                            if isinstance(widget, UnitWidget) and widget.unit.number == unit_number:
                                widget.slot_dropdown.set(str(unit.slot))
                                widget.enable_checkbox.select() if unit.enabled else widget.enable_checkbox.deselect()
                                widget.wave_entry.delete(0, ctk.END)
                                widget.wave_entry.insert(0, str(unit.wave_number) if unit.wave_number else "")
                                widget.delay_entry.delete(0, ctk.END)
                                widget.delay_entry.insert(0, str(unit.sleep_time))
                                widget.update_click_location_display()
                                break

                self.update_upgrade_click_location_display()
                self.update_replay_click_location_display()
                self.update_anti_afk_click_location_display()

                logging.info(f"Configuration loaded from {file_name}")
                messagebox.showinfo("Success", f"Configuration loaded from {file_name}")
            except Exception as e:
                logging.error(f"Error loading configuration: {str(e)}")
                messagebox.showerror("Load Error", f"Failed to load configuration from {file_name}. Error: {str(e)}")
        else:
            messagebox.showerror("Load Error", f"Configuration file not found: {file_name}")
            
    def create_new_file(self):
        new_file_name = self.new_file_entry.get()
        if new_file_name:
            os.makedirs(os.path.join("configs", new_file_name), exist_ok=True)
            self.save_config(new_file_name)
            self.update_file_list()
            messagebox.showinfo("Success", f"Created new configuration: {new_file_name}")
        else:
            messagebox.showerror("Error", "Please enter a file name")

    def update_file_list(self):
        if not os.path.exists("configs"):
            os.makedirs("configs")
        config_files = [d for d in os.listdir("configs") if os.path.isdir(os.path.join("configs", d))]
        self.file_dropdown.configure(values=config_files)
        self.file_var.set("")  # Set to an empty string instead of the first config file
        logging.info(f"Available config files: {config_files}")

    def load_selected_file(self):
        selected_file = self.file_dropdown.get()
        logging.info(f"Attempting to load file: {selected_file}")
        if selected_file:
            try:
                self.load_config(selected_file)
            except Exception as e:
                logging.error(f"Error loading file: {str(e)}")
                messagebox.showerror("Load Error", f"Failed to load configuration: {str(e)}")
        else:
            logging.error("No file selected for loading")
            messagebox.showerror("Error", "Please select a file to load")

    def save_selected_file(self):
        selected_file = self.file_dropdown.get()
        logging.info(f"Attempting to save file: {selected_file}")
        if selected_file:
            confirm = messagebox.askyesno("Confirm Save", "Are you sure you want to save this configuration?")
            if confirm:
                try:
                    self.save_config(selected_file)
                    messagebox.showinfo("Success", f"Configuration saved to {selected_file}")
                except Exception as e:
                    logging.error(f"Error saving file: {str(e)}")
                    messagebox.showerror("Save Error", f"Failed to save configuration: {str(e)}")
            else:
                logging.info("Save cancelled by user")
        else:
            logging.error("No file selected for saving")
            messagebox.showerror("Error", "Please select a file to save")

    def on_file_selection_change(self, *args):
        selected_file = self.file_var.get()
        logging.info(f"File selection changed to: {selected_file}")
        self.update_upgrade_frame()

    def update_upgrade_click_location_display(self):
        if self.upgrade_click_location:
            self.upgrade_click_location_label.configure(text=f"Upgrade Click Location: {self.upgrade_click_location[0]}, {self.upgrade_click_location[1]}")
        else:
            self.upgrade_click_location_label.configure(text="Upgrade Click Location: Not set")

    def update_replay_click_location_display(self):
        if self.replay_click_location:
            self.replay_click_location_label.configure(text=f"Replay Click Location: {self.replay_click_location[0]}, {self.replay_click_location[1]}")
        else:
            self.replay_click_location_label.configure(text="Replay Click Location: Not set")

    def update_anti_afk_click_location_display(self):
        if self.anti_afk_click_location:
            self.anti_afk_click_location_label.configure(text=f"Anti-AFK Click Location: {self.anti_afk_click_location[0]}, {self.anti_afk_click_location[1]}")
        else:
            self.anti_afk_click_location_label.configure(text="Anti-AFK Click Location: Not set")


    def reset_configuration(self):
        if messagebox.askyesno("Reset Configuration", "Are you sure you want to reset all settings?"):
            # Clear all existing widgets
            for widget in self.master.winfo_children():
                widget.destroy()

            # Reinitialize the application
            self.__init__(self.master)

            # Update the GUI
            self.master.update()

            logging.info("Configuration reset to default settings")
            messagebox.showinfo("Reset Complete", "Configuration has been reset to default settings.")


    def on_closing(self):
        selected_file = self.file_dropdown.get()
        if selected_file:
            save_choice = messagebox.askyesnocancel("Save Configuration", "Do you want to save the current configuration?")
            if save_choice is None:  # User clicked Cancel
                return
            elif save_choice:  # User clicked Yes
                self.save_config(selected_file)
                messagebox.showinfo("Save Successful", "Configuration saved successfully.")
        self.master.destroy()

    def place_macro(self, unit_number):
        self.place_macro_running = True
        unit = self.units[unit_number - 1]
        if unit.enabled and unit.click_location and not unit.placed:
            slot_key = unit.slot_var.get()
            keyboard.press_and_release(slot_key)
            logging.debug(f"Pressed key: {slot_key} for Unit {unit_number}")

            # Use the unit-specific sleep time
            sleep_time = float(unit.delay_entry.get())
            time.sleep(sleep_time)
        
            if not self.macro_event.is_set():
                return False

            click_x, click_y = unit.click_location
            pydirectinput.moveTo(click_x, click_y)
            time.sleep(0.025)
            pydirectinput.moveTo(click_x, click_y - 1)
            time.sleep(0.025)
        
            if not self.macro_event.is_set():
                return False
            pydirectinput.click(click_x, click_y - 2)
            unit.placed = True
            logging.info(f"Placed Unit {unit_number} using slot {slot_key}")
        self.place_macro_running = False
        return True

    def upgrade_macro(self, unit_number, upgrade_text, upgrade_number):
        ability_events = []
        unit = self.units[unit_number - 1]
        if not unit.placed or upgrade_number in unit.completed_upgrades:
            logging.info(f"Unit {unit_number} not placed or upgrade {upgrade_number} already completed, skipping")
            unit.queued_upgrades.discard(upgrade_number)
            return True

        logging.info(f"Attempting upgrade {upgrade_number} for Unit {unit_number}")

        while True:
            if self.upgrade_macro_paused:
                time.sleep(0.025)
                continue

            if self.check_for_replay():
                break

            # Rest of the upgrade logic
            ability_events = [event_tuple for event_tuple in ability_events if not event_tuple[0].is_set()]

            if not self.ability_queue.empty():
                ability_unit, ability_delay, ability_number = self.ability_queue.get()
                ability_events.append(self.ability_macro(ability_unit, ability_delay, ability_number))

            for event, ability_unit, ability_number in ability_events:
                if event.is_set():
                    self.activate_ability(ability_unit, ability_number)
                    ability_events.remove((event, ability_unit, ability_number))
                    continue

            if self.check_for_upgrade(upgrade_text):
                unit.upgraded = True
                unit.queued_upgrades.discard(upgrade_number)
                unit.completed_upgrades.add(upgrade_number)
                logging.info(f"Unit {unit_number} successfully upgraded to level {upgrade_number}")
                self.current_upgrade = None

                if self.anti_afk_click_location:
                    x, y = self.anti_afk_click_location
                    pydirectinput.moveTo(x, y)
                    time.sleep(0.025)
                    pydirectinput.moveTo(x, y - 1)
                    time.sleep(0.025)
                    pydirectinput.click(x, y - 2)
                    logging.info("Anti-AFK click performed after upgrade")
    
                return True

            # Click on the unit
            unit_x, unit_y = unit.click_location
            pydirectinput.moveTo(unit_x, unit_y - 5)
            time.sleep(0.025)
            pydirectinput.moveTo(unit_x, unit_y - 6)
            time.sleep(0.025)

            if not self.macro_event.is_set():
                return False
            pydirectinput.click(unit_x, unit_y - 7)
            time.sleep(0.025)

            # Click on the upgrade button
            upgrade_x, upgrade_y = self.upgrade_click_location
            pydirectinput.moveTo(upgrade_x, upgrade_y)
            time.sleep(0.025)
            pydirectinput.moveTo(upgrade_x, upgrade_y - 1)
            time.sleep(0.025)
            if not self.macro_event.is_set():
                return False
            pydirectinput.click(upgrade_x, upgrade_y - 1)
            time.sleep(1.5)

            # Check for wave change
            current_wave, _ = self.check_wave_change()  # Only use the current_wave
            if current_wave:
                logging.info(f"Wave {current_wave} detected during upgrade attempt")
                self.handle_wave(current_wave)
                if not self.macro_event.is_set():
                    return False

        logging.info("Replay detected during upgrade attempt, exiting upgrade macro")
        return True

    def activate_ability(self, ability_unit, ability_number):
        self.upgrade_macro_paused = True
        unit = self.units[ability_unit - 1]
        if unit.enabled and unit.click_location and unit.placed:
            # Click on the unit
            unit_x, unit_y = unit.click_location
            pydirectinput.moveTo(unit_x, unit_y - 5)
            time.sleep(0.025)
            pydirectinput.moveTo(unit_x, unit_y - 6)
            time.sleep(0.025)
            pydirectinput.click(unit_x, unit_y - 7)
            time.sleep(0.025)

            # Click on the ability
            ability_x, ability_y = self.ability_click_location
            pydirectinput.moveTo(ability_x, ability_y)
            time.sleep(0.025)
            pydirectinput.moveTo(ability_x, ability_y - 1)
            time.sleep(0.025)
            pydirectinput.click(ability_x, ability_y - 2)


            # Perform anti-AFK click to deselect the unit
            if self.anti_afk_click_location:
                x, y = self.anti_afk_click_location
                pydirectinput.moveTo(x, y)
                time.sleep(0.025)
                pydirectinput.moveTo(x, y - 1)
                time.sleep(0.025)
                pydirectinput.click(x, y - 2)
                time.sleep(0.25)

            self.upgrade_macro_paused = False
            unit.queued_abilities.discard(ability_number)
            unit.completed_abilities.add(ability_number)
            logging.info(f"Activated ability {ability_number} for Unit {ability_unit}")

    def replay_macro(self):
        self.replay_macro_running = True
        # Cancel any pending ability activations
        self.ability_queue.queue.clear()

        if self.replay_click_location:
            x, y = self.replay_click_location
            pydirectinput.moveTo(x, y)
            time.sleep(0.025)
            pydirectinput.moveTo(x, y - 1)
            time.sleep(0.025)
            if not self.macro_event.is_set():
                return False
            pydirectinput.click(x, y - 2)
            time.sleep(5)
            logging.info("Replay macro executed")
        self.replay_macro_running = False
        return True
    
    def paragon_macro(self):
        highest_priority = float('inf')
        target_region = None
        target_word = None
    
        for i, region in enumerate([self.paragon_region_1, self.paragon_region_2, self.paragon_region_3]):
            if not region:
                continue

            # Convert region tuple to dictionary format
            monitor = {"top": region[1], "left": region[0], "width": region[2] - region[0], "height": region[3] - region[1]}
        
            # Capture the region
            with mss.mss() as sct:
                screenshot = np.array(sct.grab(monitor))
        
            # Convert to grayscale
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        
            # Use the processed image for OCR
            text = self.reader.readtext(gray)
            text_lower = [re.sub(r'[^a-zA-Z\s]', '', t[1]).lower() for t in text]
        
            logging.info(f"Text found in Paragon Region {i+1}: {text_lower}")
            for priority, word in enumerate(self.paragon_priorities):
                if word.lower() in text_lower and priority < highest_priority:
                    highest_priority = priority
                    target_region = region
                    target_word = word
    
        if target_region and target_word:
            # Calculate the center of the target region
            center_x = (target_region[0] + target_region[2]) // 2
            center_y = (target_region[1] + target_region[3]) // 2
        
            pydirectinput.moveTo(center_x, center_y)
            time.sleep(0.025)
            pydirectinput.moveTo(center_x - 1, center_y - 1)
            time.sleep(0.025)
            pydirectinput.click(center_x - 1, center_y - 1)
            logging.info(f"Paragon macro executed for '{target_word}' at center of region: ({center_x}, {center_y})")
            return True
        return False
    
    def anti_afk_macro(self):
        if self.anti_afk_click_location:
            x, y = self.anti_afk_click_location
            pydirectinput.moveTo(x, y)
            time.sleep(0.025)
            pydirectinput.moveTo(x, y - 1)
            time.sleep(0.025)
            if not self.macro_event.is_set() or not self.anti_afk_event.is_set():
                return False
            pydirectinput.click(x, y - 2)
            logging.info("Anti-AFK macro executed")
        return True

    def reset_unit_placement(self):
        for unit in self.units:
            unit.placed = False
            unit.upgraded = False
            unit.queued_upgrades.clear()
            unit.completed_upgrades.clear()
            unit.queued_abilities.clear()
            unit.completed_abilities.clear()  # Add this line

        self.current_upgrade = None
        self.current_ability = None

        logging.info("Reset unit placement, upgrade status, and ability status")

    def search_text(self, text_to_find, region=None, return_text=False, return_all_text=False):
        with mss.mss() as sct:
            if region:
                monitor = {"top": region[1], "left": region[0], "width": region[2] - region[0], "height": region[3] - region[1]}
            else:
                monitor = sct.monitors[0]
            screenshot = np.array(sct.grab(monitor))

        results = self.reader.readtext(screenshot)
    
        # Define valid characters (letters and numbers)
        valid_chars = string.ascii_letters + string.digits + ' '
    
        # Filter the results
        filtered_results = []
        for bbox, text, prob in results:
            filtered_text = ''.join(char for char in text if char in valid_chars)
            filtered_results.append((bbox, filtered_text, prob))
    
        all_text = [text for _, text, _ in filtered_results]

        for (bbox, text, prob) in filtered_results:
            if text.lower() == text_to_find.lower() and prob > self.similarity_threshold:
                (top_left, top_right, bottom_right, bottom_left) = bbox
                center_x = int((top_left[0] + bottom_right[0]) / 2)
                center_y = int((top_left[1] + bottom_right[1]) / 2)
                if return_text:
                    return text, (center_x, center_y)
                elif return_all_text:
                    return all_text, (center_x, center_y)
                else:
                    return (center_x, center_y)
        if return_text:
            return None, None
        elif return_all_text:
            return all_text, None
        return None

    def check_for_upgrade(self, upgrade_text):
        if not hasattr(self, 'upgrade_region'):
            logging.info("Upgrade region not set, skipping upgrade check")
            return False

        with mss.mss() as sct:
            monitor = {"top": self.upgrade_region[1], "left": self.upgrade_region[0],
                       "width": self.upgrade_region[2] - self.upgrade_region[0],
                       "height": self.upgrade_region[3] - self.upgrade_region[1]}
            screenshot = np.array(sct.grab(monitor))

        # Increase resolution and scale
        scale_factor = 2
        dpi = 192 * scale_factor

        screenshot_pil = Image.fromarray(screenshot)
        screenshot_pil.info['dpi'] = (dpi, dpi)

        width = int(screenshot.shape[1] * scale_factor)
        height = int(screenshot.shape[0] * scale_factor)
        screenshot = np.array(screenshot_pil.resize((width, height), Image.LANCZOS))

        upgrade_texts = [text.strip().lower() for text in upgrade_text.split(',')]
        all_text, location = self.search_text("", self.upgrade_region, return_all_text=True)
        all_text_lower = [text.lower() for text in all_text]
        logging.info(f"All text found in upgrade region: {all_text_lower}")

        for upgrade_text in upgrade_texts:
            for text in all_text_lower:
                if upgrade_text in text:
                    logging.info(f"Upgrade text '{upgrade_text}' found at location: {location}")
                    return True

        logging.info(f"Upgrade texts {upgrade_texts} not found in region")
        return False

    def check_for_replay(self):
        if not hasattr(self, 'replay_region'):
            logging.info("Replay region not set, skipping replay check")
            return False

        with mss.mss() as sct:
            monitor = {"top": self.replay_region[1], "left": self.replay_region[0],
                       "width": self.replay_region[2] - self.replay_region[0],
                       "height": self.replay_region[3] - self.replay_region[1]}
            screenshot = np.array(sct.grab(monitor))

        # Increase resolution and scale
        scale_factor = 2
        dpi = 192 * scale_factor

        screenshot_pil = Image.fromarray(screenshot)
        screenshot_pil.info['dpi'] = (dpi, dpi)

        width = int(screenshot.shape[1] * scale_factor)
        height = int(screenshot.shape[0] * scale_factor)
        screenshot = np.array(screenshot_pil.resize((width, height), Image.LANCZOS))

        replay_texts = [text.strip().lower() for text in self.replay_text_entry.get().split(',')]
        all_text, location = self.search_text("", self.replay_region, return_all_text=True)
        all_text_lower = [text.lower() for text in all_text]
        logging.info(f"All text found in replay region: {all_text_lower}")

        for replay_text in replay_texts:
            for text in all_text_lower:
                if replay_text in text:
                    logging.info(f"Replay text '{replay_text}' found at location: {location}")

                    # Add a small delay here
                    time.sleep(0.5)  # You can adjust this value as needed

                    # Webhook logic
                    if self.webhook_url_entry.get():
                        current_time = time.time()
                
                        if hasattr(self, 'last_replay_time'):
                            elapsed_time = current_time - self.last_replay_time
                            if elapsed_time >= 60:
                                elapsed_time_str = str(datetime.timedelta(seconds=int(elapsed_time)))
                                self.capture_and_send_screenshot(elapsed_time_str)
                                self.last_replay_time = current_time
                            else:
                                logging.info("Less than 1 minute since last screenshot, skipping image capture")
                        else:
                            self.capture_and_send_screenshot("N/A")
                            self.last_replay_time = current_time
                    else:
                        logging.info("Webhook URL not set, skipping screenshot capture and send")

                    # Reset highest wave seen after sending webhook
                    if self.highest_wave_seen != 0:
                        self.highest_wave_seen = 0
                        logging.info("Highest wave seen reset to 0")

                    return True

        logging.info(f"Replay text {replay_texts} not found in region")
        return False

    def save_webhook_url(self, file_name):
        webhook_data = {"webhook_url": self.webhook_url_entry.get()}
        webhook_file = os.path.join("configs", file_name, "webhook.json")
        with open(webhook_file, "w") as f:
            json.dump(webhook_data, f)

    def load_webhook_url(self, file_name):
        webhook_file = os.path.join("configs", file_name, "webhook.json")
        try:
            with open(webhook_file, "r") as f:
                webhook_data = json.load(f)
            return webhook_data.get("webhook_url", "")
        except FileNotFoundError:
            return ""

    def capture_and_send_screenshot(self, elapsed_time_str):
        with mss.mss() as sct:
            for monitor in sct.monitors[1:]:  # Skip the first monitor (entire virtual screen)
                if (monitor["left"] <= self.replay_region[0] < monitor["left"] + monitor["width"] and
                    monitor["top"] <= self.replay_region[1] < monitor["top"] + monitor["height"]):
                    screenshot = np.array(sct.grab(monitor))
                    self.send_discord_webhook(screenshot, elapsed_time_str)
                    break
            else:
                logging.error("Could not determine which monitor contains the replay region")

    def send_discord_webhook(self, screenshot, elapsed_time):
        webhook_url = self.webhook_url_entry.get()
        if not webhook_url:
            logging.warning("Discord webhook URL not set")
            return

        self.total_runs += 1

        _, img_encoded = cv2.imencode('.png', screenshot)
        img_bytes = io.BytesIO(img_encoded.tobytes())

        files = {
            'file': ('screenshot.png', img_bytes, 'image/png')
        }

        embed = {
            "title": "WaveBound Alert",
            "description": (
                "The macro has detected a replay and is attempting to restart.\n\n"
                f"**Highest Wave Detected**\n{self.highest_wave_seen}\n\n"
                f"**Elapsed Time**\n{elapsed_time}\n\n"
                f"**Total Runs**\n{self.total_runs}"
            ),
            "color": 0x0066ff,  # Blue color
            "image": {"url": "attachment://screenshot.png"},
            "footer": {
                "text": "WaveBound OCR"
            }
        }

        payload = {
            "embeds": [embed]
        }

        response = requests.post(webhook_url, files=files, data={"payload_json": json.dumps(payload)})
        if response.status_code == 200:
            logging.info(f"Discord webhook sent successfully. Total runs: {self.total_runs}")
        else:
            logging.error(f"Failed to send Discord webhook. Status code: {response.status_code}")


    def check_wave_change(self):
        if not hasattr(self, 'wave_search_region'):
            logging.info("Wave search region not set, skipping wave check")
            return None, self.highest_wave_seen

        with mss.mss() as sct:
            monitor = {"top": self.wave_search_region[1], "left": self.wave_search_region[0],
                       "width": self.wave_search_region[2] - self.wave_search_region[0],
                       "height": self.wave_search_region[3] - self.wave_search_region[1]}
            screenshot = np.array(sct.grab(monitor))

        # Increase resolution and scale
        scale_factor = 2
        dpi = 192 * scale_factor

        screenshot_pil = Image.fromarray(screenshot)
        screenshot_pil.info['dpi'] = (dpi, dpi)

        width = int(screenshot.shape[1] * scale_factor)
        height = int(screenshot.shape[0] * scale_factor)
        screenshot = np.array(screenshot_pil.resize((width, height), Image.LANCZOS))

        hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0,0,200])
        upper_white = np.array([180,30,255])
        mask = cv2.inRange(hsv, lower_white, upper_white)
        kernel = np.ones((2,2),np.uint8)
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        results = self.reader.readtext(opening)
        all_text = [text.lower() for (_, text, _) in results]

        # Post-processing step to combine "wave" and number
        combined_text = []
        i = 0
        while i < len(all_text):
            if all_text[i] == "wave" and i + 1 < len(all_text) and all_text[i + 1].isdigit():
                combined_text.append(f"wave {all_text[i + 1]}")
                i += 2
            else:
                combined_text.append(all_text[i])
                i += 1

        all_text = combined_text

        logging.info(f"All text found in region after combining: {all_text}")


        # Collect unique wave numbers from units, upgrades, and abilities
        unique_waves = set()
        for unit in self.units:
            if unit.enabled and unit.wave_entry.get().isdigit():
                unique_waves.add(int(unit.wave_entry.get()))

        for upgrade in self.upgrade_settings:
            if upgrade["wave"].get().isdigit():
                unique_waves.add(int(upgrade["wave"].get()))

        for ability in self.ability_settings:
            if ability["wave"].get().isdigit():
                unique_waves.add(int(ability["wave"].get()))

        current_wave = None
        for wave in sorted(unique_waves):
            wave_text = f"wave {wave}"
            wave_str = str(wave)
            logging.info(f"Searching for '{wave_text}' or '{wave_str}' in region. Text found: {wave_text if wave_text in all_text else wave_str if wave_str in all_text else 'Not found'}")
            for text in all_text:
                if re.search(rf'\bwave\s+{wave}\b', text, re.IGNORECASE) or re.search(rf'\b{wave}\b', text):
                    logging.info(f"Wave {wave} detected in text: {text}")
                    current_wave = wave
                    break
            if current_wave:
                break

        if current_wave is None:
            logging.info("No wave change detected")

        highest_wave = 0
        for text in all_text:
            numbers = [int(num) for num in re.findall(r'\d+', text)]
            if numbers:
                highest_wave = max(highest_wave, max(numbers))

        if highest_wave > self.highest_wave_seen:
            self.highest_wave_seen = highest_wave

        logging.info(f"Highest wave detected: {self.highest_wave_seen}")

        return current_wave, self.highest_wave_seen
    
class CTkScrollableDropdown(ctk.CTkToplevel):
    
    def __init__(self, attach, x=None, y=None, button_color=None, height: int = 200, width: int = None,
                 fg_color=None, button_height: int = 20, justify="center", scrollbar_button_color=None,
                 scrollbar=True, scrollbar_button_hover_color=None, frame_border_width=2, values=[],
                 command=None, image_values=[], alpha: float = 0.97, frame_corner_radius=20, double_click=False,
                 resize=True, frame_border_color=None, text_color=None, autocomplete=False, 
                 hover_color=None, **button_kwargs):
        
        super().__init__(master=attach.winfo_toplevel(), takefocus=1)
        
        self.focus()
        self.lift()
        self.alpha = alpha
        self.attach = attach
        self.corner = frame_corner_radius
        self.padding = 0
        self.focus_something = False
        self.disable = True
        self.update()
        
        if sys.platform.startswith("win"):
            self.after(100, lambda: self.overrideredirect(True))
            self.transparent_color = self._apply_appearance_mode(self._fg_color)
            self.attributes("-transparentcolor", self.transparent_color)
        elif sys.platform.startswith("darwin"):
            self.overrideredirect(True)
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
            self.focus_something = True
        else:
            self.overrideredirect(True)
            self.transparent_color = '#000001'
            self.corner = 0
            self.padding = 18
            self.withdraw()

        self.hide = True
        self.attach.bind('<Configure>', lambda e: self._withdraw() if not self.disable else None, add="+")
        self.attach.winfo_toplevel().bind('<Configure>', lambda e: self._withdraw() if not self.disable else None, add="+")
        self.attach.winfo_toplevel().bind("<ButtonPress>", lambda e: self._withdraw() if not self.disable else None, add="+")        
        self.bind("<Escape>", lambda e: self._withdraw() if not self.disable else None, add="+")
        
        self.attributes('-alpha', 0)
        self.disable = False
        self.fg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"] if fg_color is None else fg_color
        self.scroll_button_color = ctk.ThemeManager.theme["CTkScrollbar"]["button_color"] if scrollbar_button_color is None else scrollbar_button_color
        self.scroll_hover_color = ctk.ThemeManager.theme["CTkScrollbar"]["button_hover_color"] if scrollbar_button_hover_color is None else scrollbar_button_hover_color
        self.frame_border_color = ctk.ThemeManager.theme["CTkFrame"]["border_color"] if frame_border_color is None else frame_border_color
        self.button_color = ctk.ThemeManager.theme["CTkFrame"]["top_fg_color"] if button_color is None else button_color
        self.text_color = ctk.ThemeManager.theme["CTkLabel"]["text_color"] if text_color is None else text_color
        self.hover_color = ctk.ThemeManager.theme["CTkButton"]["hover_color"] if hover_color is None else hover_color
        
        
        if scrollbar is False:
            self.scroll_button_color = self.fg_color
            self.scroll_hover_color = self.fg_color
            
        self.frame = ctk.CTkScrollableFrame(self, bg_color=self.transparent_color, fg_color=self.fg_color,
                                        scrollbar_button_hover_color=self.scroll_hover_color,
                                        corner_radius=self.corner, border_width=frame_border_width,
                                        scrollbar_button_color=self.scroll_button_color,
                                        border_color=self.frame_border_color)
        self.frame._scrollbar.grid_configure(padx=3)
        self.frame.pack(expand=True, fill="both")
        self.dummy_entry = ctk.CTkEntry(self.frame, fg_color="transparent", border_width=0, height=1, width=1)
        self.no_match = ctk.CTkLabel(self.frame, text="No Match")
        self.height = height
        self.height_new = height
        self.width = width
        self.command = command
        self.fade = False
        self.resize = resize
        self.autocomplete = autocomplete
        self.var_update = ctk.StringVar()
        self.appear = False
        
        if justify.lower()=="left":
            self.justify = "w"
        elif justify.lower()=="right":
            self.justify = "e"
        else:
            self.justify = "c"
            
        self.button_height = button_height
        self.values = values
        self.button_num = len(self.values)
        self.image_values = None if len(image_values)!=len(self.values) else image_values
        
        self.resizable(width=False, height=False)
        self.transient(self.master)
        self._init_buttons(**button_kwargs)

        # Add binding for different ctk widgets
        if double_click or type(self.attach) is ctk.CTkEntry or type(self.attach) is ctk.CTkComboBox:
            self.attach.bind('<Double-Button-1>', lambda e: self._iconify(), add="+")
        else:
            self.attach.bind('<Button-1>', lambda e: self._iconify(), add="+")

        if type(self.attach) is ctk.CTkComboBox:
            self.attach._canvas.tag_bind("right_parts", "<Button-1>", lambda e: self._iconify())
            self.attach._canvas.tag_bind("dropdown_arrow", "<Button-1>", lambda e: self._iconify())
            if self.command is None:
                self.command = self.attach.set
              
        if type(self.attach) is ctk.CTkOptionMenu:
            self.attach._canvas.bind("<Button-1>", lambda e: self._iconify())
            self.attach._text_label.bind("<Button-1>", lambda e: self._iconify())
            if self.command is None:
                self.command = self.attach.set
                
        self.attach.bind("<Destroy>", lambda _: self._destroy(), add="+")
        
        self.update_idletasks()
        self.x = x
        self.y = y

        if self.autocomplete:
            self.bind_autocomplete()
            
        self.withdraw()

        self.attributes("-alpha", self.alpha)

    def _destroy(self):
        self.after(500, self.destroy_popup)
        
    def _withdraw(self):
        if not self.winfo_exists():
            return
        if self.winfo_viewable() and self.hide:
            self.withdraw()
        
        self.event_generate("<<Closed>>")
        self.hide = True

    def _update(self, a, b, c):
        self.live_update(self.attach._entry.get())
        
    def bind_autocomplete(self, ):
        def appear(x):
            self.appear = True
            
        if type(self.attach) is ctk.CTkComboBox:
            self.attach._entry.configure(textvariable=self.var_update)
            self.attach._entry.bind("<Key>", appear)
            self.attach.set(self.values[0])
            self.var_update.trace_add('write', self._update)
            
        if type(self.attach) is ctk.CTkEntry:
            self.attach.configure(textvariable=self.var_update)
            self.attach.bind("<Key>", appear)
            self.var_update.trace_add('write', self._update)
        
    def fade_out(self):
        for i in range(100,0,-10):
            if not self.winfo_exists():
                break
            self.attributes("-alpha", i/100)
            self.update()
            time.sleep(1/100)
            
    def fade_in(self):
        for i in range(0,100,10):
            if not self.winfo_exists():
                break
            self.attributes("-alpha", i/100)
            self.update()
            time.sleep(1/100)
            
    def _init_buttons(self, **button_kwargs):
        self.i = 0
        self.widgets = {}
        for row in self.values:
            self.widgets[self.i] = ctk.CTkButton(self.frame,
                                                          text=row,
                                                          height=self.button_height,
                                                          fg_color=self.button_color,
                                                          text_color=self.text_color,
                                                          image=self.image_values[self.i] if self.image_values is not None else None,
                                                          anchor=self.justify,
                                                          hover_color=self.hover_color,
                                                          command=lambda k=row: self._attach_key_press(k), **button_kwargs)
            self.widgets[self.i].pack(fill="x", pady=2, padx=(self.padding, 0))
            self.i+=1
 
        self.hide = False
            
    def destroy_popup(self):
        self.destroy()
        self.disable = True

    def place_dropdown(self):
        self.x_pos = self.attach.winfo_rootx() if self.x is None else self.x + self.attach.winfo_rootx()
        self.y_pos = self.attach.winfo_rooty() + self.attach.winfo_reqheight() + 5 if self.y is None else self.y + self.attach.winfo_rooty()
        self.width_new = self.attach.winfo_width() if self.width is None else self.width
        
        if self.resize:
            if self.button_num<=5:      
                self.height_new = self.button_height * self.button_num + 55
            else:
                self.height_new = self.button_height * self.button_num + 35
            if self.height_new>self.height:
                self.height_new = self.height

        self.geometry('{}x{}+{}+{}'.format(self.width_new, self.height_new,
                                           self.x_pos, self.y_pos))
        self.fade_in()
        self.attributes('-alpha', self.alpha)
        self.attach.focus()

    def _iconify(self):
        if self.attach.cget("state") == "disabled":
            return
        if self.disable:
            return
        if self.winfo_exists():  # Check if the widget still exists
            if self.hide:
                self.event_generate("<<Opened>>")
                self.focus()
                self.hide = False
                self.place_dropdown()
                self._deiconify()  
                if self.focus_something:
                    self.dummy_entry.pack()
                    self.dummy_entry.focus_set()
                    self.after(100, self.dummy_entry.pack_forget)
            else:
                self.withdraw()
                self.hide = True
            
    def _attach_key_press(self, k):
        self.event_generate("<<Selected>>")
        self.fade = True
        if self.command:
            self.command(k)
        self.fade = False
        self.fade_out()
        self.withdraw()
        self.hide = True
            
    def live_update(self, string=None):
        if not self.appear: return
        if self.disable: return
        if self.fade: return
        if string:
            string = string.lower()
            self._deiconify()
            i=1
            for key in self.widgets.keys():
                s = self.widgets[key].cget("text").lower()
                text_similarity = difflib.SequenceMatcher(None, s[0:len(string)], string).ratio()
                similar = s.startswith(string) or text_similarity > 0.75
                if not similar:
                    self.widgets[key].pack_forget()
                else:
                    self.widgets[key].pack(fill="x", pady=2, padx=(self.padding, 0))
                    i+=1
                    
            if i==1:
                self.no_match.pack(fill="x", pady=2, padx=(self.padding, 0))
            else:
                self.no_match.pack_forget()
            self.button_num = i
            self.place_dropdown()
            
        else:
            self.no_match.pack_forget()
            self.button_num = len(self.values)
            for key in self.widgets.keys():
                self.widgets[key].destroy()
            self._init_buttons()
            self.place_dropdown()
            
        self.frame._parent_canvas.yview_moveto(0.0)
        self.appear = False
        
    def insert(self, value, **kwargs):
        self.widgets[self.i] = ctk.CTkButton(self.frame,
                                                       text=value,
                                                       height=self.button_height,
                                                       fg_color=self.button_color,
                                                       text_color=self.text_color,
                                                       hover_color=self.hover_color,
                                                       anchor=self.justify,
                                                       command=lambda k=value: self._attach_key_press(k), **kwargs)
        self.widgets[self.i].pack(fill="x", pady=2, padx=(self.padding, 0))
        self.i+=1
        self.values.append(value)
        
    def _deiconify(self):
        if len(self.values)>0:
            self.deiconify()

    def popup(self, x=None, y=None):
        self.x = x
        self.y = y
        self.hide = True
        self._iconify()

    def hide(self):
        self._withdraw()
        
    def configure(self, **kwargs):
        if "height" in kwargs:
            self.height = kwargs.pop("height")
            self.height_new = self.height
            
        if "alpha" in kwargs:
            self.alpha = kwargs.pop("alpha")
            
        if "width" in kwargs:
            self.width = kwargs.pop("width")
            
        if "fg_color" in kwargs:
            self.frame.configure(fg_color=kwargs.pop("fg_color"))
            
        if "values" in kwargs:
            self.values = kwargs.pop("values")
            self.image_values = None
            self.button_num = len(self.values)
            for key in self.widgets.keys():
                self.widgets[key].destroy()
            self._init_buttons()
 
        if "image_values" in kwargs:
            self.image_values = kwargs.pop("image_values")
            self.image_values = None if len(self.image_values)!=len(self.values) else self.image_values
            if self.image_values is not None:
                i=0
                for key in self.widgets.keys():
                    self.widgets[key].configure(image=self.image_values[i])
                    i+=1
                    
        if "button_color" in kwargs:
            button_color = kwargs.pop("button_color")
            for key in self.widgets.keys():
                self.widgets[key].configure(fg_color=button_color)

        if "font" in kwargs:
            font = kwargs.pop("font")
            for key in self.widgets.keys():
                self.widgets[key].configure(font=font)
                
        if "hover_color" not in kwargs:
            kwargs["hover_color"] = self.hover_color
        
        for key in self.widgets.keys():
            self.widgets[key].configure(**kwargs)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.resizable(False, False)  # Add this line
    app = TDMacro(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
