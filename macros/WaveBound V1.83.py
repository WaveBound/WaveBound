import webview
import os
import sys
import io
import threading
import time
from screeninfo import get_monitors
import tkinter as tk
import json
import re
import mss
import numpy as np
from PIL import Image
import cv2
import string
import easyocr
import pydirectinput
import queue
import datetime
import requests
import keyboard
import base64
import requests
from tkinter import filedialog
import tkinter as tk
import ssl
import win32api

ssl._create_default_https_context = ssl._create_unverified_context


# Define your HTML content as a string
html_content = """
<html>
<head>
    <title>Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        body {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: Arial, sans-serif;
            overflow: hidden; /* Hides the main window scrollbar */
            margin: 0;
            padding: 0;
            font-weight: bold;
        }
        .container {
            padding: 20px;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 20px;
            background-color: #161b22;
            max-width: 900px;
            margin: 0 auto;
            margin-left: 60px; /* Move the header to the right */
        }
        .header-left {
            display: flex;
            align-items: center;
            width: 100%;
        }
        .header-left h1 {
            font-size: 20px;
            margin: 0;
            margin-left: 0; /* Move the text to the left edge */
        }
        .header-right {
            display: flex;
            align-items: center;
        }
        .header-right i {
            margin-left: 10px;
            cursor: pointer;
            color: #8b949e;
            padding: 5px;  /* Add some padding for better hover area */
            transition: color 0.3s;  /* Smooth color transition */
        }
        .header-right i.fa-times {
            font-size: 20px; /* Makes the X bigger */
            padding: 4px;    /* Increases clickable area */
        }
        .header-right i.fa-window-minimize:hover {
            color: #58a6ff;  /* Same blue as button hover */
        }

        /* Style for close button hover */
        .header-right i.fa-times:hover {
            color: #ff3333;  /* Red color */
        }

        .sidebar {
            width: 60px;
            background-color: #161b22;
            position: fixed;
            top: 0;
            bottom: 0;
            padding-top: 20px;
        }
        .sidebar i {
            display: block;
            text-align: center;
            padding: 20px 0;
            color: #8b949e;
            cursor: pointer;
        }
        .sidebar i.active {
            color: #58a6ff;
        }
        .content {
            margin-left: 60px;
            padding: 20px;
            max-width: 900px;
        }
        .tabs {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .tab-links {
            display: flex;
            border-bottom: 1px solid #30363d;
        }
        .tab-links div {
            padding: 10px 20px;
            cursor: pointer;
            color: #8b949e;
        }
        .tab-links .active {
            border-bottom: 2px solid #58a6ff;
            color: #58a6ff;
        }
        .button {
            background-color: #1b1f23;
            color: #c9d1d9;
            border: 1px solid #30363d;
            padding: 5px 10px;
            cursor: pointer;
            border-radius: 3px;
            font-weight: bold;
            transition: background-color 0.3s, color 0.3s;
        }
        .button:hover {
            background-color: #58a6ff;
            color: #0d1117;
        }
        .card-container {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 15px; /* Increase the gap between cards */
            margin-top: 20px;
            max-width: 900px;
        }
        .card {
            background-color: #161b22;
            padding: 10px;
            text-align: center;
            border-radius: 5px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .card h2 {
            margin: 5px 0;
            font-size: 24px;
        }
        .card p {
            margin: 5px 0;
            color: #8b949e;
        }
        .input-container {
            margin-top: 10px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .input-container input, .input-container select {
            width: 100%;
            padding: 5px;
            background-color: #0d1117;
            color: #c9d1d9;
            border: 1px solid #30363d;
            border-radius: 3px;
        }
        .input-container .wave-input, .input-container .delay-input {
            display: flex;
            align-items: center;
            gap: 10px;
            border: 1px solid #30363d;
            padding: 5px;
            border-radius: 3px;
        }
        .input-container .button {
            border: 1px solid #30363d;
            padding: 5px;
            border-radius: 3px;
        }
        .upgrade-container {
            margin-top: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            max-width: 900px;
            background-color: #161b22;
            padding: 20px;
            border-radius: 5px;
            margin: 0 auto;
        }
        .upgrade-container p {
            display: inline-block;
            margin-right: 10px;
        }
        .upgrade-container input {
            width: 50px; /* Set the width to 50px */
            padding: 5px;
            background-color: #0d1117;
            color: #c9d1d9;
            border: 1px solid #30363d;
            border-radius: 3px;
            display: inline-block;
        }
        .upgrade-settings-container .input-wrapper {
            display: flex;
            align-items: center;
            background-color: #0d1117;
            padding: 0px;
            border-radius: 5px;
            margin-bottom: 0px;
            width: 100%;
        }
        .upgrade-settings-container .upgrade-item {
            background-color: #161b22;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            width: 100%;
        }
        .upgrade-settings-container .upgrade-item input {
            background-color: #0d1117;
            color: #c9d1d9;
            border: 1px solid #30363d;
        }
        .hidden {
            display: none;
        }
        .upgrade-container-wrapper {
            padding-top: 20px;
        }
        .upgrade-settings-container {
            margin-top: 20px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            background-color: #161b22;
            padding: 10px; /* Reduced padding */
            border-radius: 5px;
            margin: 0 auto;
            padding-top: 20px;
            max-width: 900px;
            text-align: center;
        }
        .upgrade-settings-container h2 {
            margin: 0 auto;
            font-size: 20px;
            width: fit-content;
        }
        .scrollable-container {
            max-height: 332px; /* Reduced max height */
            overflow-y: auto;
            margin-top: 20px;
            background-color: #161b22;
            padding: 20px;
            border-radius: 5px;
        }

#upgrade-list.scrollable-container {
    max-height: 290px; /* Adjust this value to your desired height */
}
        

        /* Add this to the existing style section */
        .scrollable-container::-webkit-scrollbar {
            width: 10px;
        }

        .scrollable-container::-webkit-scrollbar-track {
            background: #0d1117;
            border-radius: 5px;
        }

        .scrollable-container::-webkit-scrollbar-thumb {
            background: #30363d;
            border-radius: 5px;
        }

        .scrollable-container::-webkit-scrollbar-thumb:hover {
            background: #58a6ff;
        }


        .scrollable-container .upgrade-item {
            width: calc(100% - 10px); /* Adjusting for padding */
            margin: 0 auto;
            padding-left: 0; /* Remove left padding */
        }

        .custom-scrollbar::-webkit-scrollbar {
            width: 10px;
        }

        .custom-scrollbar::-webkit-scrollbar-track {
            background: #0d1117;
            border-radius: 5px;
        }

        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #30363d;
            border-radius: 5px;
        }

        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: #58a6ff;
        }

        .dropdown-item:hover {
            background-color: #58a6ff;
            color: #0d1117 !important;
        }

        .button:hover {
            background-color: #58a6ff !important;
            color: #0d1117;
        }

.button:hover span {
    color: #0d1117 !important;
}


.ability-container {
    margin: 3px auto;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.ability-number {
    background-color: #1b1f23;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 3px;
    padding: 5px;
}

.ability-container-wrapper {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

.ability-settings-container {
    width: 850px;
    background-color: #161b22;
    margin: 20px auto;
    padding: 20px;
    border-radius: 5px;
}

        .settings-container.main {
            width: 859px;
            height: 376px;
            background-color: #161b22;
            margin: 0px auto;
            border-radius: 5px;
            position: relative;
        }

        .container-wrapper {
            display: flex;
            justify-content: space-between;
            width: 859px;
            margin: 20px auto 0 auto;
        }

        .settings-container.replay {
            width: 419.5px;
            height: 300px;
            background-color: #161b22;
            border-radius: 5px;
            position: relative;
        }

.settings-container.sub {
            width: 419.5px;
            height: 140px;
            background-color: #161b22;
            border-radius: 5px;
            position: relative;
        }

        .settings-container {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .settings-title {
            color: #c9d1d9;
            text-align: center;
            font-size: 20px;
            position: absolute;
            top: -5px;
            left: 50%;
            transform: translateX(-50%);
        }

.settings-container .button {
    height: 35px;
    font-size: 16px;
    font-weight: bold;
}

.settings-container .file-input,
.settings-container .Webhook-input {
    height: 35px;
    font-size: 16px;
    font-weight: bold;
}

.log-container {
    width: 859px;
    height: 696px;
    background-color: #161b22;
    margin: 0px auto;
    border-radius: 5px;
    position: relative;
    overflow-y: auto;
}

.log-container::-webkit-scrollbar {
    width: 10px;
}

.log-container::-webkit-scrollbar-track {
    background: #0d1117;
    border-radius: 5px;
}

.log-container::-webkit-scrollbar-thumb {
    background: #30363d;
    border-radius: 5px;
}

.log-container::-webkit-scrollbar-thumb:hover {
    background: #58a6ff;
}

        .log-container pre {
            color: #c9d1d9;
            margin: 0;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 20px;
            font-weight: bold;
            padding-right: 15px;
            padding-left: 15px;
            padding-top: 15px;
            user-select: text;
        }

        .checkbox {
            appearance: none;
            -webkit-appearance: none;
            -moz-appearance: none;
            width: 20px !important;  /* Force fixed width */
            height: 20px !important; /* Force fixed height */
            border: 1px solid #30363d;
            border-radius: 3px;
            background-color: #0d1117;
            padding: 0;
            cursor: pointer;
            flex-shrink: 0;
            flex-grow: 0;          /* Prevent growing */
            min-width: 20px;       /* Enforce minimum width */
            max-width: 20px;       /* Enforce maximum width */
            min-height: 20px;      /* Enforce minimum height */
            max-height: 20px;      /* Enforce maximum height */
        }

        .checkbox:checked {
            background-color: #58a6ff;
            border-color: #58a6ff;
        }

        .checkbox-label {
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            width: 100%;
            padding: 0px 0;
            gap: 5px;             /* Consistent spacing between checkbox and text */
        }

        .checkbox-label span {
            font-weight: bold;
            font-size: 18px;      /* Control text size */
        }

        .main-content {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
            padding-top: 40px;
        }

        .main-row {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .file-input {
            background-color: #0d1117;
            color: #c9d1d9;
            border: 1px solid #30363d;
            border-radius: 3px;
            padding: 5px 10px;
            width: 200px;
        }

        .Webhook-input {
            background-color: #0d1117;
            color: #c9d1d9;
            border: 1px solid #30363d;
            border-radius: 3px;
            padding: 5px 10px;
            width: 250px;
        }

.dragging {
    opacity: 0.5;
    border: 2px dashed #58a6ff !important;
}

        .main-row span {
            color: #c9d1d9;
            min-width: 0px;
        }

    </style>
</head>
<body>
    <div class="header pywebview-drag-region">
        <div class="header-left" style="padding-left: 0;">
            <h1 id="header-title" style="margin-left: 0;">Dashboard</h1>
        </div>
        <div class="header-right">
            <i class="fas fa-window-minimize" onclick="minimizeWindow()"></i>
            <i class="fas fa-times" onclick="closeWindow()"></i>
        </div>
    </div>
<div class="sidebar">
    <i class="fas fa-home active" onclick="selectTab('dashboard')"></i>
    <i class="fas fa-cog" onclick="selectTab('settings')"></i>
    <i class="fas fa-cloud" onclick="selectTab('cloud')"></i>
    <i class="fas fa-file-alt" onclick="selectTab('logs')"></i>
</div>
    <div class="content">
<div id="cloud" class="tab-content hidden">
    <div class="tabs" style="max-width: 900px;">
        <div class="tab-links">
            <div class="active" onclick="selectCloudSubTab('upload')">Upload</div>
            <div onclick="selectCloudSubTab('download')">Download</div>
        </div>
    </div>
    
<div id="upload" class="cloud-sub-tab-content">
    <div style="display: flex; gap: 20px; justify-content: space-between;">
        <!-- Existing container -->
        <div style="padding: 20px; background-color: #161b22; border-radius: 5px; margin-top: 20px; width: 48%; height: 595px;">
            <h2 style="color: #c9d1d9; margin-bottom: 20px; text-align: center;">Upload Config to GitHub</h2>
<div style="margin-bottom: 20px; display: flex; flex-direction: column; gap: 15px; align-items: center;">
    <p id="selected-folder" style="color: #c9d1d9; margin-bottom: 10px;">No folder selected</p>
    <button class="button" onclick="selectUploadFolder()" style="width: 220px; height: 50px; font-size: 18px; margin-top: 30px;">Select Folder</button>
    <button class="button" onclick="selectLocationImage()" style="width: 220px; height: 50px; font-size: 18px;">Select Location Image</button>
    <button class="button" onclick="startUpload()" style="width: 220px; height: 50px; font-size: 18px;">Upload to GitHub</button>
</div>

            <div style="background-color: #0d1117; border-radius: 3px; height: 30px; width: 100%; margin-top: 10px;"> <!-- Increased height here -->
                <div id="upload-progress" style="background-color: #58a6ff; height: 100%; width: 0%; border-radius: 3px; transition: width 0.3s;"></div>
            </div>
            <p id="upload-status" style="color: #c9d1d9; margin-top: 10px; text-align: center;"></p>
        </div>

        <!-- New container -->
        <div style="padding: 20px; background-color: #161b22; border-radius: 5px; margin-top: 20px; width: 48%; height: 595px;">
            <h2 style="color: #c9d1d9; margin-bottom: 20px; text-align: center;">Config Info</h2>
            <div style="margin-bottom: 20px;">
                <textarea placeholder="Enter text here..." style="width: 100%; height: 525px; padding: 8px; background-color: #0d1117; border: 1px solid #30363d; border-radius: 3px; color: #c9d1d9; margin-bottom: 15px; resize: none; font-family: inherit; font-size: 16px; font-weight: bold;"></textarea>
            </div>
        </div>
    </div>
</div>
    
    <div id="download" class="cloud-sub-tab-content hidden">
        <div style="padding: 20px; background-color: #161b22; border-radius: 5px; margin-top: 20px; max-width: 900px;">
            <h2 style="color: #c9d1d9; margin-bottom: 20px; text-align: center;">Download Configs from GitHub</h2>
            
            <div style="margin-bottom: 20px;">
                <input type="text" id="config-search" 
                       placeholder="Search configs..." 
                       oninput="filterConfigs()"
                       style="width: 100%; padding: 8px; background-color: #0d1117; border: 1px solid #30363d; 
                              border-radius: 3px; color: #c9d1d9; margin-bottom: 15px;">
            </div>

            <div id="config-list" style="max-height: 410px; overflow-y: auto;" class="custom-scrollbar">
                <!-- Configs will be populated here -->
            </div>

            <p id="download-status" style="color: #c9d1d9; margin-top: 15px; text-align: center;">Waiting for Download...</p>
        </div>
    </div>
</div>

<div id="dashboard" class="tab-content" style="max-width: 900px;">
    <div class="tabs" style="max-width: 900px;">
        <div class="tab-links">
            <div class="active" onclick="selectSubTab('units')">Units</div>
            <div onclick="selectSubTab('upgrade')">Upgrade</div>
            <div onclick="selectSubTab('ability')">Ability</div>
            <div onclick="selectSubTab('custom')">Custom</div>
        </div>
        <div id="unit-navigation">
            <button class="button" onclick="previousUnitTab()">Previous</button>
            <button class="button" onclick="nextUnitTab()">Next</button>
        </div>
    </div>
    <div id="units" class="sub-tab-content">
        <div id="unit-tab-1" class="unit-tab">
            <div class="card-container" style="max-width: 900px;">
                <!-- Unit cards for tab 1 will be generated here -->
            </div>
        </div>
        <div id="unit-tab-2" class="unit-tab hidden">
            <div class="card-container" style="max-width: 900px;">
                <!-- Unit cards for tab 2 will be generated here -->
            </div>
        </div>
    </div>
    <div id="upgrade" class="sub-tab-content hidden">
        <div class="upgrade-container-wrapper">
            <div class="upgrade-container" style="max-width: 900px; flex-direction: column;">
                <!-- First row -->
                <div style="display: flex; align-items: center;">
                    <p style="margin: 0; white-space: nowrap;">Number of Upgrades:</p>
                    <input type="text" id="upgrade-number" style="height: 35px; font-size: 16px; font-weight: bold; width: 75px; margin-left: 5px;">
                    <button class="button" onclick="setUpgrades()" style="margin-left: 10px; padding: 10px 20px;">Set Upgrades</button>
                    <button class="button" onclick="setUpgradeRegion()" style="margin-left: 10px; padding: 10px 20px;">Set Upgrade Region</button>
                    <button class="button" onclick="setUpgradeClickLocation()" style="margin-left: 10px; padding: 10px 20px;">Set Upgrade Click Location</button>
                </div>
                <!-- Second row -->
                <div style="display: flex; align-items: center; margin-top: 10px;">
                    <p style="margin: 0; white-space: nowrap;">Default Upgrade Text:</p>
                    <input type="text" id="default-upgrade-text" style="height: 35px; font-size: 16px; font-weight: bold; width: 150px; margin-left: 5px; background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 3px; padding-left: 5px;">
                </div>
                <!-- Status messages row -->
                <div style="display: flex; justify-content: center; gap: 50px; margin-top: 10px;">
                    <p id="upgrade-region-status" style="text-align: center; color: #58a6ff;">Upgrade Region: Not Set</p>
                    <p id="upgrade-click-status" style="text-align: center; color: #58a6ff;">Upgrade Click Location: Not Set</p>
                </div>
            </div>
        </div>
        <div class="upgrade-settings-container" style="padding-top: 20px; margin-top: 20px;">
            <h2>Upgrade Settings</h2>
            <div class="scrollable-container" id="upgrade-list">
                <!-- Upgrade containers will be generated here -->
            </div>
        </div>
    </div>
    <div id="ability" class="sub-tab-content hidden">
        <div class="upgrade-container-wrapper">
            <div class="upgrade-container" style="max-width: 900px; flex-direction: column;">
                <div style="display: flex; align-items: center;">
                    <p style="margin-right: 10px;">Number of Abilities:</p>
                    <input type="text" id="ability-number" style="height: 35px; font-size: 16px; font-weight: bold; width: 75px;">
                    <button class="button" onclick="setAbilities()" style="margin-left: 10px; padding: 10px 20px;">Set Abilities</button>
                    <button class="button" onclick="setAbilityClickLocation()" style="margin-left: 10px; padding: 10px 20px;">Set Ability Click Location</button>
                </div>
                <div style="display: flex; justify-content: center; gap: 50px; margin-top: 10px;">
                    <p id="ability-click-status" style="text-align: center; color: #58a6ff;">Ability Click Location: Not Set</p>
                </div>
            </div>
        </div>
        <div class="upgrade-settings-container" style="padding-top: 20px; margin-top: 20px;">
            <h2>Ability Settings</h2>
            <div class="scrollable-container" id="ability-list">
                <!-- Ability containers will be generated here -->
            </div>
        </div>
    </div>
<div id="custom" class="sub-tab-content hidden">
    <div class="container-wrapper">
        <div class="settings-container sub" style="width: 225px; height: 635px; display: flex; flex-direction: column;">
            <h2 class="settings-title">Controls</h2>
            <div style="padding: 50px 15px 15px 15px; display: flex; flex-direction: column; align-items: center; flex: 1; overflow: hidden;">
                <div style="display: flex; flex-direction: column; gap: 8px; align-items: center; width: 100%;">
                    <label class="checkbox-label" style="transform: scale(1.4); margin-bottom: 15px;">
                        <input type="checkbox" class="checkbox" style="width: 24px; height: 24px;">
                        <span style="font-size: 20px;">Enable</span>
                    </label>

                    <button class="button" draggable="true" ondragstart="drag(event)" style="width: 180px; height: 40px; font-size: 16px;">
                        Key Hold
                    </button>                    

                    <button class="button" draggable="true" ondragstart="drag(event)" style="width: 180px; height: 40px; font-size: 16px;">
                        Key Press
                    </button>

                    <button class="button" draggable="true" ondragstart="drag(event)" style="width: 180px; height: 40px; font-size: 16px;">
                        Move And Click
                    </button>
                    
                    <button class="button" draggable="true" ondragstart="drag(event)" style="width: 180px; height: 40px; font-size: 16px;">
                        Scroll
                    </button>
                    
                    <button class="button" draggable="true" ondragstart="drag(event)" style="width: 180px; height: 40px; font-size: 16px;">
                        Sleep
                    </button>

                    <button class="button" draggable="true" ondragstart="drag(event)" style="width: 180px; height: 40px; font-size: 16px;">
                        Look
                    </button>

                    <button class="button" draggable="true" ondragstart="drag(event)" style="width: 180px; height: 40px; font-size: 16px;">
                        Wait For Wave
                    </button>

                    <button class="button" draggable="true" ondragstart="drag(event)" style="width: 180px; height: 40px; font-size: 16px;">
                        Custom OCR
                    </button>

                    <button class="button" draggable="true" ondragstart="drag(event)" style="width: 180px; height: 40px; font-size: 16px;">
                        Label
                    </button>   

<label class="checkbox-label" style="transform: scale(1.2);">
    <input type="checkbox" class="checkbox" id="onReplayCheck" style="width: 24px; height: 24px;">
    <span style="font-size: 18px;">On Replay</span>
</label>

<label class="checkbox-label" style="transform: scale(1.2);">
    <input type="checkbox" class="checkbox" id="onStartCheck" style="width: 24px; height: 24px;">
    <span style="font-size: 18px;">On Start</span>
</label>
                </div>
            </div>
        </div>
<div class="settings-container replay" style="width: 614px; height: 635px; display: flex; flex-direction: column;" ondrop="drop(event)" ondragover="allowDrop(event)">
    <div id="actionsList" class="custom-scrollbar" style="display: flex; flex-direction: column; gap: 8px; padding: 13px 13px 5px 13px; margin-top: 10px; flex: 1; overflow-y: auto; width: calc(100% - 40px);">
    </div>
</div>
    </div>
</div>
</div>
        <div id="settings" class="tab-content hidden">
                <div class="settings-container main">
                    <h2 class="settings-title">Main</h2>
                    <div class="main-content">
                        <div class="main-row">
                            <span>New File Name:</span>
                            <input type="text" class="file-input">
                            <button class="button" onclick="pywebview.api.create_config()">Create</button>
                        </div>
                        <div class="main-row">
                            <span>Load File:</span>
                            <div class="dropdown" style="margin-right: 15px;">
                                <button class="button" type="button" onclick="toggleSettingsDropdown(event)" style="width: 200px; min-width: 200px; text-align: left; padding-left: 10px; display: flex; justify-content: space-between; align-items: center; background-color: #0d1117; transition: background-color 0.3s;">
                                    <span>Select a file...</span>
                                    <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
                                </button>
                                <ul class="dropdown-menu custom-scrollbar" style="display: none; position: absolute; background-color: #0d1117; border: 1px solid #30363d; max-height: 200px; overflow-y: scroll; z-index: 1000; width: 200px; list-style-type: none; padding: 0; margin: 0;">
                                    <!-- Config Files will be generated here -->
                                </ul>
                            </div>
                            <button class="button" onclick="loadConfig()">Load</button>
                            <button class="button" onclick="saveConfig()">Save</button>
                        </div>
                        <div class="main-row">
                            <span>Start Macro Key:</span>
                            <button class="button" onclick="setKeyBinding(this)">Click To Set</button>
                        </div>
                        <div class="main-row">
                            <span>Stop Macro Key:</span>
                            <button class="button" onclick="setKeyBinding(this)">Click To Set</button>
                        </div>
                        <div class="main-row">
                            <span>Webhook URL:</span>
                            <input type="text" class="Webhook-input">
                        </div>
                    </div>
                </div>
<div class="container-wrapper">
    <div class="settings-container replay">
        <h2 class="settings-title">Replay</h2>
        <div class="main-content" style="padding-top: 20px;">
            <button class="button" onclick="setReplayRegion()">Set Replay Region</button>
            <span id="replay-region-status" style="color: #58a6ff; padding-top: 2px;">Replay Region: Not Set</span>

            <button class="button" onclick="setReplayClickLocation()">Set Replay Click Location</button>
            <span id="replay-click-status" style="color: #58a6ff; padding-top: 2px;">Click Location: Not Set</span>

            <div style="margin-top: 5px;">
                <span>Replay Text:</span>
                <input type="text" class="file-input" style="margin-top: 2px;">
            </div>
        </div>
    </div>
<div style="display: flex; flex-direction: column;">
    <div class="settings-container sub">
        <h2 class="settings-title">Wave</h2>
        <div class="main-content" style="padding-top: 20px;">
            <div style="display: flex; align-items: center;">
                <button class="button" onclick="setWaveRegion()">Set Wave Region</button>
                <div class="dropdown" style="margin-left: 15px;">
                    <button class="button" type="button" onclick="toggleSettingsDropdown(event)" style="width: 175px; min-width: 175px; text-align: left; padding-left: 10px; display: flex; justify-content: space-between; align-items: center; background-color: #0d1117; transition: background-color 0.3s;">
                        <span>Both</span>
                        <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
                    </button>
                    <ul class="dropdown-menu custom-scrollbar" style="display: none; position: absolute; background-color: #0d1117; border: 1px solid #30363d; max-height: 200px; overflow-y: scroll; z-index: 1000; width: 175px; list-style-type: none; padding: 0; margin: 0;">
                        <li><a class="dropdown-item" href="#" onclick="selectSettingsFile(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">Both</a></li>
                        <li><a class="dropdown-item" href="#" onclick="selectSettingsFile(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">Wave+Number</a></li>
                        <li><a class="dropdown-item" href="#" onclick="selectSettingsFile(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">Number</a></li>
                    </ul>
                </div>
            </div>
            <span id="wave-region-status" style="color: #58a6ff; padding-top: 2px;">Wave Region: Not Set</span>
        </div>
    </div>
<div class="settings-container sub" style="margin-top: 20px;">
    <h2 class="settings-title">Anti-AFK</h2>
    <div class="main-content" style="padding-top: 20px;">
        <div style="display: flex; flex-direction: row; align-items: center; gap: 10px;">
<div class="dropdown" style="margin-right: 15px;">
    <button class="button" type="button" onclick="toggleSettingsDropdown(event)" style="width: 50px; min-width: 50px; text-align: left; padding-left: 10px; display: flex; justify-content: space-between; align-items: center; background-color: #0d1117; transition: background-color 0.3s;">
        <span>1</span>
        <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
    </button>
    <ul class="dropdown-menu custom-scrollbar" style="display: none; position: absolute; background-color: #0d1117; border: 1px solid #30363d; max-height: 200px; overflow-y: scroll; z-index: 1000; width: 50px; list-style-type: none; padding: 0; margin: 0;">
        <li><a class="dropdown-item" href="#" onclick="selectSettingsFile(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">1</a></li>
        <li><a class="dropdown-item" href="#" onclick="selectSettingsFile(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">2</a></li>
        <li><a class="dropdown-item" href="#" onclick="selectSettingsFile(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">3</a></li>
        <li><a class="dropdown-item" href="#" onclick="selectSettingsFile(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">4</a></li>
        <li><a class="dropdown-item" href="#" onclick="selectSettingsFile(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">5</a></li>
    </ul>
</div>
            <button class="button" onclick="setAntiAfkClickLocation()">Set Anti-AFK Click Location</button>
        </div>
        <div id="anti-afk-status-container">
            <span id="anti-afk-click-status-1" style="color: #58a6ff; padding-top: 2px;">Click Location 1: Not Set</span>
            <span id="anti-afk-click-status-2" style="color: #58a6ff; padding-top: 2px; display: none;">Click Location 2: Not Set</span>
            <span id="anti-afk-click-status-3" style="color: #58a6ff; padding-top: 2px; display: none;">Click Location 3: Not Set</span>
            <span id="anti-afk-click-status-4" style="color: #58a6ff; padding-top: 2px; display: none;">Click Location 4: Not Set</span>
            <span id="anti-afk-click-status-5" style="color: #58a6ff; padding-top: 2px; display: none;">Click Location 5: Not Set</span>
        </div>
    </div>
</div>
</div>
</div>
                </div>
            <div id="logs" class="tab-content hidden">
                <div class="log-container custom-scrollbar">
                    <pre id="log-content"></pre>
                </div>
            </div>
        </div>
    <script>

const persistentUpgradeData = new Map();
const persistentAbilityData = new Map();

class DialogManager {
    constructor() {
        this.activeDialog = null;
        this.activeOverlay = null;
    }

    create(options) {
        const {
            title = null,
            message,
            content = null,
            buttons,
            isLocation = false,
            isInfo = false,
            isInteractive = false
        } = options;

        // Create new dialog elements
        const dialog = document.createElement('div');
        const overlay = document.createElement('div');

dialog.style.cssText = `
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #161b22;
    padding: 20px;
    border-radius: 5px;
    z-index: 1000;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    ${isLocation ? '' : 'min-width: 300px;'}
    ${isInfo ? 'max-width: 600px; max-height: 400px; overflow-y: auto;' : ''}
`;

        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            z-index: 999;
        `;

        // Add title if provided
        if (title) {
            const titleElement = document.createElement('h3');
            titleElement.textContent = title;
            titleElement.style.color = '#c9d1d9';
            dialog.appendChild(titleElement);
        }

        // Handle different content types
        if (isLocation) {
            const img = document.createElement('img');
            img.src = message;
            img.style.maxWidth = '800px';
            img.style.maxHeight = '600px';
            dialog.appendChild(img);
        } else if (isInfo || isInteractive) {
            const messageElement = document.createElement(isInfo ? 'pre' : 'div');
            if (isInfo) {
                messageElement.textContent = message;
                messageElement.style.cssText = `
                    color: #c9d1d9;
                    margin: 0 0 20px 0;
                    text-align: left;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                    white-space: pre-wrap;
                    word-wrap: break-word;
                `;
            } else {
                messageElement.appendChild(content);
            }
            dialog.appendChild(messageElement);
        } else {
            const messageElement = document.createElement('p');
            messageElement.textContent = message;
            messageElement.style.cssText = `
                color: #c9d1d9;
                margin: 0 0 20px 0;
                text-align: center;
                font-weight: bold;
            `;
            dialog.appendChild(messageElement);
        }

        // Create button container
        const buttonContainer = document.createElement('div');
        buttonContainer.style.cssText = `
            display: flex;
            justify-content: center;
            gap: 10px;
            ${content ? 'margin-top: 20px;' : ''}
        `;

        // Add buttons
buttons.forEach(({text, action}) => {
    const button = document.createElement('button');
    button.textContent = text;
    button.style.cssText = `
        background-color: #0d1117;
        color: #c9d1d9;
        border: 1px solid #30363d;
        padding: 5px 15px;
        cursor: pointer;
        border-radius: 3px;
        font-weight: bold;
        min-width: 60px;
        transition: background-color 0.3s, color 0.3s;
    `;
    
    button.onmouseover = () => {
        button.style.backgroundColor = '#58a6ff';
        button.style.color = '#0d1117';
    };
    
    button.onmouseout = () => {
        button.style.backgroundColor = '#0d1117';
        button.style.color = '#c9d1d9';
    };

    button.onclick = () => {
        if (action) action();  // Execute the action first
        this.closeDialog();    // Then close the dialog
    };

    buttonContainer.appendChild(button);
});

        dialog.appendChild(buttonContainer);

        // Clean up any existing dialog before showing new one
        this.closeDialog();

        // Show new dialog
        document.body.appendChild(overlay);
        document.body.appendChild(dialog);
        
        // Store references
        this.activeDialog = dialog;
        this.activeOverlay = overlay;

        // Handle location dialog click-to-close
        if (isLocation) {
            overlay.onclick = () => this.closeDialog();
        }
    }

    closeDialog() {
        if (this.activeDialog) {
            this.activeDialog.remove();
            this.activeDialog = null;
        }
        if (this.activeOverlay) {
            this.activeOverlay.remove();
            this.activeOverlay = null;
        }
    }
}


// Initialize dialog manager
const dialogManager = new DialogManager();

// Example usage replacements:
function createDialog(message, buttons) {
    dialogManager.create({ message, buttons });
}

function createInteractiveDialog(data, content, buttons) {
    dialogManager.create({
        title: data,
        content: content,
        buttons: buttons,
        isInteractive: true
    });
}

function createInfoDialog(message, buttons) {
    dialogManager.create({ message, buttons, isInfo: true });
}

function createLocationDialog(imageData) {
    dialogManager.create({
        message: `data:image/png;base64,${imageData}`,
        buttons: [],
        isLocation: true
    });
}
    
class DropdownManager {
    constructor() {
        this.activeDropdown = null;
    }

    toggle(event, options = {}) {
        const {
            isAntiAfk = false,
            customWidth = null,
            customHeight = null,
            positionAbove = false,
            onSelect = null
        } = options;

        const dropdownContainer = event.target.closest('.dropdown');
        const dropdownMenu = dropdownContainer.querySelector('.dropdown-menu');
        const buttonRect = dropdownContainer.getBoundingClientRect();
        
        // Set dropdown dimensions
        const dropdownWidth = customWidth || buttonRect.width;
        const dropdownHeight = customHeight || 204;

        // Position the dropdown
        dropdownMenu.style.position = 'fixed';
        dropdownMenu.style.width = `${dropdownWidth}px`;
        dropdownMenu.style.left = `${buttonRect.left}px`;

        if (positionAbove) {
            dropdownMenu.style.top = `${buttonRect.top - dropdownHeight - 2}px`;
        } else {
            dropdownMenu.style.top = `${buttonRect.bottom}px`;
        }

        dropdownMenu.style.maxHeight = `${dropdownHeight}px`;

        // Toggle visibility
        const isVisible = dropdownMenu.style.display !== 'none';
        dropdownMenu.style.display = isVisible ? 'none' : 'block';

        // Handle click outside
        if (!isVisible) {
            setTimeout(() => {
                window.addEventListener('click', (e) => {
                    if (!dropdownContainer.contains(e.target)) {
                        dropdownMenu.style.display = 'none';
                        this.activeDropdown = null;
                    }
                }, { once: true });
            }, 0);
        }

        // Store active dropdown
        this.activeDropdown = dropdownMenu;

        // Handle selection
        dropdownMenu.querySelectorAll('.dropdown-item').forEach(item => {
            item.onclick = (e) => {
                e.preventDefault();
                const selectedText = e.target.textContent;
                const button = dropdownContainer.querySelector('button');
                
                button.innerHTML = `
                    <span>${selectedText}</span>
                    <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
                `;

                if (isAntiAfk) {
                    window.currentAntiAfkNumber = selectedText;
                    this.updateAntiAfkStatus(selectedText);
                }

                if (onSelect) {
                    onSelect(selectedText);
                }

                dropdownMenu.style.display = 'none';
            };
        });
    }

    updateAntiAfkStatus(selectedNumber) {
        const statusElement = document.getElementById('anti-afk-click-status-1');
        if (window.antiAfkClickLocations && window.antiAfkClickLocations[selectedNumber]) {
            const coords = window.antiAfkClickLocations[selectedNumber];
            statusElement.textContent = `Click Location ${selectedNumber}: X=${coords.x}, Y=${coords.y}`;
        } else {
            statusElement.textContent = `Click Location ${selectedNumber}: Not Set`;
        }
    }
}

// Initialize dropdown manager
const dropdownManager = new DropdownManager();

// Replace existing toggle functions with the new unified system
function toggleDropdown(event) {
    dropdownManager.toggle(event);
}

function toggleAbilityDropdown(event) {
    dropdownManager.toggle(event, {
        customHeight: 204
    });
}

function toggleUnitDropdown(event) {
    dropdownManager.toggle(event, {
        customWidth: 135,
        customHeight: 225
    });
}

function toggleSettingsDropdown(event) {
    const isAntiAfk = event.target.closest('.settings-container.sub[style*="margin-top: 20px"]');
    dropdownManager.toggle(event, {
        isAntiAfk: isAntiAfk,
        positionAbove: isAntiAfk,
        customHeight: isAntiAfk ? 170 : 204
    });
}

class DialogDropdownManager {
    constructor() {
        this.activeDropdown = null;
    }

    toggle(event, options = {}) {
        const {
            items = [],
            onSelect = null,
            customWidth = 100,
            customHeight = 200
        } = options;

        const button = event.target.closest('button');
        const dropdownContainer = button.closest('.dropdown');
        const existingMenu = dropdownContainer.querySelector('.dropdown-menu');
        
        if (this.activeDropdown && this.activeDropdown !== existingMenu) {
            this.activeDropdown.style.display = 'none';
        }

        const isVisible = existingMenu.style.display === 'block';
        existingMenu.style.display = isVisible ? 'none' : 'block';

        if (!isVisible) {
            const buttonRect = button.getBoundingClientRect();
            const dialogRect = button.closest('.dialog').getBoundingClientRect();
            
            existingMenu.style.cssText = `
                position: absolute;
                width: ${customWidth}px;
                max-height: ${customHeight}px;
                left: ${buttonRect.left - dialogRect.left}px;
                top: ${buttonRect.bottom - dialogRect.top}px;
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 3px;
                overflow-y: auto;
                z-index: 1001;
                padding: 5px 0;
            `;

            if (!existingMenu.children.length) {
                items.forEach(item => {
                    const option = document.createElement('div');
                    option.className = 'dropdown-item';
                    option.style.cssText = `
                        color: #c9d1d9;
                        padding: 8px 15px;
                        cursor: pointer;
                    `;
                    option.textContent = item;
                    
                    option.onmouseover = () => option.style.backgroundColor = '#1f242b';
                    option.onmouseout = () => option.style.backgroundColor = 'transparent';
                    
                    option.onclick = () => {
                        if (onSelect) onSelect(item);
                        button.querySelector('span:first-child').textContent = item;
                        existingMenu.style.display = 'none';
                        this.activeDropdown = null;
                    };
                    
                    existingMenu.appendChild(option);
                });
            }

            this.activeDropdown = existingMenu;

            setTimeout(() => {
                window.addEventListener('click', (e) => {
                    if (!dropdownContainer.contains(e.target)) {
                        existingMenu.style.display = 'none';
                        this.activeDropdown = null;
                    }
                }, { once: true });
            }, 0);
        } else {
            this.activeDropdown = null;
        }
    }
}

// Initialize dialog dropdown manager
const dialogDropdownManager = new DialogDropdownManager();

class DragAndDropManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.draggingItem = null;
        this.previewItem = null;
        this.activeDropdown = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.container.addEventListener('dragover', this.handleDragOver.bind(this));
        this.container.addEventListener('drop', this.handleDrop.bind(this));
        this.container.addEventListener('dragleave', this.handleDragLeave.bind(this));
        document.addEventListener('dragend', this.handleDragEnd.bind(this));
    }

    createDraggableItem(type, settings = {}) {
        const actionItem = document.createElement('div');
        actionItem.dataset.type = type;
        actionItem.settings = settings;
        actionItem.draggable = true;

        actionItem.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #1b1f23;
            padding: 10px 15px;
            border-radius: 3px;
            border: 1px solid #30363d;
            width: 100%;
            box-sizing: border-box;
            cursor: pointer;
        `;

        const actionText = document.createElement('span');
        actionText.style.color = '#c9d1d9';
        actionText.style.fontSize = '16px';
        
        const deleteButton = document.createElement('button');
        deleteButton.innerHTML = '✕';
        deleteButton.style.cssText = `
            background: none;
            border: none;
            color: #c9d1d9;
            cursor: pointer;
            font-size: 16px;
            padding: 0 5px;
        `;

        deleteButton.onclick = (e) => {
            e.stopPropagation();
            actionItem.isBeingDeleted = true;
            actionItem.remove();
        };

        actionItem.appendChild(actionText);
        actionItem.appendChild(deleteButton);
        
        this.addItemEventListeners(actionItem);
        this.updateActionText(actionItem);
        
        return actionItem;
    }

    handleDragStart(event, item) {
        event.dataTransfer.setData('text/plain', '');
        item.classList.add('dragging');
        this.draggingItem = item;
        
        if (item.dataset.dragText) {
            const formattedText = this.getDisplayText(item.dataset.type, {
                x: '0', y: '0',
                amount: '0', direction: 'up',
                duration: '0',
                wave: '0',
                key: 'None', action: 'down',
                text: 'None'
            });
            item.dataset.dragText = formattedText;
        }
    }

    handleDragOver(event) {
        event.preventDefault();
        if (!this.draggingItem && !this.previewItem) {
            this.createPreviewItem(event);
        }
        this.updateItemPosition(this.draggingItem || this.previewItem, event);
    }

    handleDragEnd() {
        if (this.draggingItem) {
            this.draggingItem.classList.remove('dragging');
            this.draggingItem = null;
        }
        if (this.previewItem) {
            this.previewItem.remove();
            this.previewItem = null;
        }
        const draggedElement = document.querySelector('[data-drag-text]');
        if (draggedElement) {
            delete draggedElement.dataset.dragText;
        }
    }

    handleDragLeave(event) {
        if (!this.container.contains(event.relatedTarget)) {
            if (this.previewItem) {
                this.previewItem.remove();
                this.previewItem = null;
            }
        }
    }

createPreviewItem(event) {
    const draggedElement = document.querySelector('[data-drag-text]');
    const dragText = draggedElement ? draggedElement.dataset.dragText : '';
    const isLabel = draggedElement && draggedElement.textContent.trim() === 'Label';
    
    this.previewItem = document.createElement('div');
    this.previewItem.className = 'dragging';
    this.previewItem.style.cssText = `
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #1b1f23;
        padding: 10px 15px;
        border-radius: 3px;
        border: 1px solid #30363d;
        width: 100%;
        box-sizing: border-box;
        opacity: 0.7;
    `;
    
    this.previewItem.innerHTML = `
        <span style="color: #58a6ff; font-size: 16px;">${isLabel ? 'New Label' : dragText}</span>
        <button style="background: none; border: none; color: #c9d1d9; font-size: 16px; padding: 0 5px;">✕</button>
    `;
    
    this.container.appendChild(this.previewItem);
}


    updateItemPosition(item, event) {
        if (!item) return;

        const closestItem = Array.from(this.container.children)
            .filter(child => child !== item)
            .reduce((closest, child) => {
                const box = child.getBoundingClientRect();
                const offset = event.clientY - box.top - box.height / 2;
                if (!closest || Math.abs(offset) < Math.abs(closest.offset)) {
                    return { offset, element: child };
                }
                return closest;
            }, null);
            
        if (closestItem) {
            const isAfter = closestItem.offset > 0;
            this.container.insertBefore(item, isAfter ? closestItem.element.nextSibling : closestItem.element);
        }
    }

handleDrop(event) {
    event.preventDefault();
    const isNewItem = event.dataTransfer.getData("isNewItem") === "true";
    const type = event.dataTransfer.getData("text");
    
    if (isNewItem) {
        const newItem = type === 'Label' 
            ? this.createLabelItem()
            : this.createDraggableItem(type, {
                x: '0', y: '0',
                amount: '0', direction: 'up',
                duration: '0',
                wave: '0',
                key: 'None', action: 'down',
                text: 'None'
            });
        
        this.updateItemPosition(newItem, event);
    }
    
    if (this.previewItem) {
        this.previewItem.remove();
        this.previewItem = null;
    }
}

    getDisplayText(type, settings) {
        switch(type) {
            case 'Move And Click':
                return `Move And Click (X: ${settings.x || '0'} Y: ${settings.y || '0'} Delay: ${settings.delay || '0'}s)`;
            case 'Scroll':
                return `Scroll (Amount: ${settings.amount || '0'} Direction: ${settings.direction || 'up'} Delay: ${settings.delay || '0'}s)`;
            case 'Sleep':
                return `Sleep (Duration: ${settings.duration || '0'}s)`;
            case 'Wait For Wave':
                return `Wait For Wave (Wave: ${settings.wave || '0'})`;
            case 'Key Press':
                return `Key Press (Key: ${settings.key || 'None'} Action: ${settings.action || 'down'})`;
            case 'Look':
                return `Look (Direction: ${settings.direction || 'up'} Duration: ${settings.duration || '0'}s)`;
            case 'Custom OCR':
                return `Custom OCR (Text: ${settings.text || 'None'})`;
            case 'Key Hold':
                return `Key Hold (Key: ${settings.key || 'None'} Duration: ${settings.duration || '0'}s)`;
            default:
                return type;
        }
    }

    updateActionText(actionItem) {
        const actionText = actionItem.querySelector('span');
        actionText.textContent = this.getDisplayText(actionItem.dataset.type, actionItem.settings);
    }

    addItemEventListeners(item) {
        item.draggable = true;
        
        item.addEventListener('dragstart', (e) => this.handleDragStart(e, item));
        item.addEventListener('dragend', () => item.classList.remove('dragging'));
        
        item.ondblclick = () => {
            if (item.isBeingDeleted) return;
            this.createSettingsDialog(item);
        };
    }

    createSettingsDialog(item) {
        const content = document.createElement('div');
        content.style.cssText = 'display: flex; flex-direction: column; gap: 15px;';

        const dialogContent = this.getDialogContent(item.dataset.type, item.settings);
        content.appendChild(dialogContent);

        dialogManager.create({
            title: item.dataset.type,
            content: content,
            buttons: [
                {
                    text: 'Save',
                    action: () => {
                        const newSettings = this.getUpdatedSettings(item.dataset.type, content);
                        item.settings = { ...item.settings, ...newSettings };
                        this.updateActionText(item);
                    }
                },
                {text: 'Cancel', action: null}
            ],
            isInteractive: true
        });
    }

    getDialogContent(type, settings) {
        const container = document.createElement('div');
        
        switch(type) {
            case 'Move And Click':
                container.appendChild(this.createMoveAndClickContent(settings));
                break;
            case 'Scroll':
                container.appendChild(this.createScrollContent(settings));
                break;
            case 'Sleep':
                container.appendChild(this.createSleepContent(settings));
                break;
            case 'Wait For Wave':
                container.appendChild(this.createWaveContent(settings));
                break;
            case 'Key Press':
                container.appendChild(this.createKeyPressContent(settings));
                break;
            case 'Look':
                container.appendChild(this.createLookContent(settings));
                break;
            case 'Custom OCR':
                container.appendChild(this.createOCRContent(settings));
                break;
            case 'Key Hold':
                container.appendChild(this.createKeyHoldContent(settings));
                break;
        }
        
        return container;
    }

    getUpdatedSettings(type, content) {
        switch(type) {
            case 'Move And Click':
                return {
                    x: content.querySelector('#click-x').value,
                    y: content.querySelector('#click-y').value,
                    delay: content.querySelector('#click-delay').value
                };
            case 'Scroll':
                return {
                    amount: content.querySelector('#scroll-amount').value,
                    direction: content.querySelector('.dropdown button span:first-child').textContent.toLowerCase(),
                    delay: content.querySelector('#scroll-delay').value
                };
            case 'Sleep':
                return {
                    duration: content.querySelector('#sleep-duration').value
                };
            case 'Wait For Wave':
                return {
                    wave: content.querySelector('#wave-number').value
                };
            case 'Key Press':
                return {
                    key: content.querySelector('#key-input').value,
                    action: content.querySelector('.dropdown button span:first-child').textContent.toLowerCase()
                };
            case 'Look':
                return {
                    direction: content.querySelector('.dropdown button span:first-child').textContent.toLowerCase(),
                    duration: content.querySelector('#look-duration').value
                };
            case 'Custom OCR':
                return {
                    text: content.querySelector('#ocr-text').value,
                    x1: content.querySelector('#ocr-x1').value,
                    y1: content.querySelector('#ocr-y1').value,
                    x2: content.querySelector('#ocr-x2').value,
                    y2: content.querySelector('#ocr-y2').value
                };
            case 'Key Hold':
                return {
                    key: content.querySelector('#key-hold-input').value,
                    duration: content.querySelector('#key-hold-duration').value
                };
        }
    }

    createMoveAndClickContent(settings) {
        const container = document.createElement('div');
        container.style.cssText = 'display: flex; flex-direction: column; gap: 15px;';

        const coordContainer = document.createElement('div');
        coordContainer.style.cssText = 'display: flex; align-items: center; gap: 10px;';

        coordContainer.innerHTML = `
            <span style="color: #c9d1d9; width: 20px;">X:</span>
            <input type="text" id="click-x" value="${settings.x || '0'}" style="width: 100px; height: 30px; background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
            <span style="color: #c9d1d9; width: 20px;">Y:</span>
            <input type="text" id="click-y" value="${settings.y || '0'}" style="width: 100px; height: 30px; background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
            <span style="color: #c9d1d9; width: 50px;">Delay:</span>
            <input type="text" id="click-delay" value="${settings.delay || '0'}" style="width: 100px; height: 30px; background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
        `;

        const setLocationBtn = document.createElement('button');
        setLocationBtn.textContent = 'Set Click Location';
        setLocationBtn.className = 'button';
        setLocationBtn.style.cssText = `
            width: 150px;
            height: 35px;
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 3px;
            cursor: pointer;
        `;
        
        setLocationBtn.addEventListener('click', () => {
            pywebview.api.get_click_location('click-location-status', true);
        });

        container.appendChild(coordContainer);
        container.appendChild(setLocationBtn);
        return container;
    }

    createScrollContent(settings) {
        const container = document.createElement('div');
        container.style.cssText = 'display: flex; flex-direction: column; gap: 10px;';

        const scrollAmountContainer = document.createElement('div');
        scrollAmountContainer.innerHTML = `
            <span style="color: #c9d1d9;">Scroll Amount:</span>
            <input type="text" id="scroll-amount" value="${settings.amount || '0'}" style="width: 100px; height: 30px; background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
        `;

        const directionContainer = this.createDropdownContainer('Direction:', settings.direction || 'up', ['Up', 'Down']);
        const delayContainer = document.createElement('div');
        delayContainer.innerHTML = `
            <span style="color: #c9d1d9;">Delay:</span>
            <input type="text" id="scroll-delay" value="${settings.delay || '0'}" style="width: 100px; height: 30px; background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
        `;

        container.appendChild(scrollAmountContainer);
        container.appendChild(directionContainer);
        container.appendChild(delayContainer);
        return container;
    }

    createKeyPressContent(settings) {
        const container = document.createElement('div');
        container.style.cssText = 'display: flex; flex-direction: column; gap: 10px;';

        const keyInput = document.createElement('input');
        keyInput.type = 'text';
        keyInput.id = 'key-input';
        keyInput.readOnly = true;
        keyInput.value = settings.key || 'None';
        keyInput.style.cssText = 'width: 150px; height: 30px; background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;';

        keyInput.onclick = function() {
            keyInput.value = 'Press any key...';
            const handleKeyPress = function(e) {
                e.preventDefault();
                keyInput.value = e.key.toUpperCase();
                document.removeEventListener('keydown', handleKeyPress);
            };
            document.addEventListener('keydown', handleKeyPress);
        };

        const actionContainer = this.createDropdownContainer('Action:', settings.action || 'down', ['Down', 'Up']);

        container.appendChild(keyInput);
        container.appendChild(actionContainer);
        return container;
    }

createDropdownContainer(label, currentValue, options) {
    const container = document.createElement('div');
    container.style.cssText = 'display: flex; align-items: center; gap: 10px;';
    
    const labelElement = document.createElement('span');
    labelElement.textContent = label;
    labelElement.style.color = '#c9d1d9';
    
    const dropdownContainer = document.createElement('div');
    dropdownContainer.className = 'dropdown';
    dropdownContainer.style.position = 'relative';
    
    const button = document.createElement('button');
    button.className = 'button';
    button.style.cssText = `
        width: 120px;
        height: 35px;
        text-align: left;
        padding-left: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #0d1117;
        color: #c9d1d9;
        border: 1px solid #30363d;
        border-radius: 3px;
        cursor: pointer;
        font-weight: bold;
        font-size: 16px;
    `;
    
    button.innerHTML = `
        <span>${currentValue}</span>
        <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
    `;

    const dropdownMenu = document.createElement('ul');
    dropdownMenu.className = 'dropdown-menu custom-scrollbar';
    dropdownMenu.style.cssText = `
        display: none;
        position: absolute;
        background-color: #0d1117;
        border: 1px solid #30363d;
        max-height: 200px;
        overflow-y: auto;
        z-index: 2000;
        width: 120px;
        list-style-type: none;
        padding: 0;
        margin: 0;
        top: 100%;
        left: 0;
    `;

    options.forEach(option => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.className = 'dropdown-item';
        a.href = '#';
        a.style.cssText = `
            color: #c9d1d9;
            display: block;
            padding: 8px 10px;
            text-decoration: none;
            text-align: left;
        `;
        a.textContent = option;
        
        a.onmouseover = () => a.style.backgroundColor = '#58a6ff';
        a.onmouseout = () => a.style.backgroundColor = 'transparent';
        
        a.onclick = (e) => {
            e.preventDefault();
            button.querySelector('span:first-child').textContent = option;
            dropdownMenu.style.display = 'none';
        };
        
        li.appendChild(a);
        dropdownMenu.appendChild(li);
    });

    button.onclick = (e) => {
        e.stopPropagation();
        const isVisible = dropdownMenu.style.display === 'block';
        dropdownMenu.style.display = isVisible ? 'none' : 'block';
        
        if (!isVisible) {
            document.addEventListener('click', function closeDropdown(e) {
                if (!dropdownContainer.contains(e.target)) {
                    dropdownMenu.style.display = 'none';
                    document.removeEventListener('click', closeDropdown);
                }
            });
        }
    };

    dropdownContainer.appendChild(button);
    dropdownContainer.appendChild(dropdownMenu);
    
    container.appendChild(labelElement);
    container.appendChild(dropdownContainer);
    
    return container;
}

    createSleepContent(settings) {
        const container = document.createElement('div');
        container.style.cssText = 'display: flex; align-items: center; gap: 10px;';

        container.innerHTML = `
            <span style="color: #c9d1d9;">Sleep Duration (seconds):</span>
            <input type="text" id="sleep-duration" value="${settings.duration || '0'}"
                style="width: 100px; height: 30px; background-color: #0d1117; color: #c9d1d9;
                border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
        `;

        return container;
    }

    createWaveContent(settings) {
        const container = document.createElement('div');
        container.style.cssText = 'display: flex; align-items: center; gap: 10px;';

        container.innerHTML = `
            <span style="color: #c9d1d9;">Wave Number:</span>
            <input type="text" id="wave-number" value="${settings.wave || '0'}"
                style="width: 100px; height: 30px; background-color: #0d1117; color: #c9d1d9;
                border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
        `;

        return container;
    }

    createLookContent(settings) {
        const container = document.createElement('div');
        container.style.cssText = 'display: flex; flex-direction: column; gap: 10px;';

        const directionContainer = this.createDropdownContainer('Direction:', settings.direction || 'up', ['Up', 'Down']);

        const durationContainer = document.createElement('div');
        durationContainer.style.cssText = 'display: flex; align-items: center; gap: 10px;';
        durationContainer.innerHTML = `
            <span style="color: #c9d1d9;">Duration:</span>
            <input type="text" id="look-duration" value="${settings.duration || '0'}"
                style="width: 100px; height: 30px; background-color: #0d1117; color: #c9d1d9;
                border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
        `;

        container.appendChild(directionContainer);
        container.appendChild(durationContainer);
        return container;
    }

    createOCRContent(settings) {
        const container = document.createElement('div');
        container.style.cssText = 'display: flex; flex-direction: column; gap: 15px;';

        const textContainer = document.createElement('div');
        textContainer.style.cssText = 'display: flex; align-items: center; gap: 10px;';
        textContainer.innerHTML = `
            <span style="color: #c9d1d9;">Target Text:</span>
            <input type="text" id="ocr-text" value="${settings.text || ''}"
                style="width: 200px; height: 30px; background-color: #0d1117; color: #c9d1d9;
                border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
        `;

        const coordsContainer = document.createElement('div');
        coordsContainer.style.cssText = 'display: flex; align-items: center; gap: 10px;';
        
        ['x1', 'y1', 'x2', 'y2'].forEach(coord => {
            const input = document.createElement('div');
            input.style.cssText = 'display: flex; align-items: center; gap: 5px;';
            input.innerHTML = `
                <span style="color: #c9d1d9; width: 25px;">${coord.toUpperCase()}:</span>
                <input type="text" id="ocr-${coord}" value="${settings[coord] || '0'}"
                    style="width: 60px; height: 30px; background-color: #0d1117; color: #c9d1d9;
                    border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
            `;
            coordsContainer.appendChild(input);
        });

        const setRegionBtn = document.createElement('button');
        setRegionBtn.textContent = 'Set OCR Region';
        setRegionBtn.className = 'button';
        setRegionBtn.style.cssText = `
            width: 150px;
            height: 35px;
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 3px;
            cursor: pointer;
        `;
        
        setRegionBtn.addEventListener('click', () => {
            pywebview.api.set_ocr_region();
        });

        container.appendChild(textContainer);
        container.appendChild(coordsContainer);
        container.appendChild(setRegionBtn);
        return container;
    }

    createKeyHoldContent(settings) {
        const container = document.createElement('div');
        container.style.cssText = 'display: flex; flex-direction: column; gap: 10px;';

        const keyInput = document.createElement('input');
        keyInput.type = 'text';
        keyInput.id = 'key-hold-input';
        keyInput.readOnly = true;
        keyInput.value = settings.key || 'None';
        keyInput.style.cssText = 'width: 150px; height: 30px; background-color: #0d1117; color: #c9d1d9; border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;';

        keyInput.onclick = function() {
            keyInput.value = 'Press any key...';
            const handleKeyPress = function(e) {
                e.preventDefault();
                keyInput.value = e.key.toUpperCase();
                document.removeEventListener('keydown', handleKeyPress);
            };
            document.addEventListener('keydown', handleKeyPress);
        };

        const durationContainer = document.createElement('div');
        durationContainer.style.cssText = 'display: flex; align-items: center; gap: 10px;';
        durationContainer.innerHTML = `
            <span style="color: #c9d1d9;">Hold Duration:</span>
            <input type="text" id="key-hold-duration" value="${settings.duration || '0'}"
                style="width: 100px; height: 30px; background-color: #0d1117; color: #c9d1d9;
                border: 1px solid #30363d; border-radius: 3px; padding: 0 10px;">
        `;

        container.appendChild(keyInput);
        container.appendChild(durationContainer);
        return container;
    }

createLabelItem() {
    const labelItem = document.createElement('div');
    labelItem.className = 'label-item';
    labelItem.draggable = true;
    labelItem.style.cssText = `
        display: flex;
        align-items: center;
        background-color: #1b1f23;
        padding: 10px 15px;
        border-radius: 3px;
        border: 1px solid #30363d;
        width: 100%;
        box-sizing: border-box;
        cursor: pointer;
        margin-bottom: 4px;
    `;

    const toggleIcon = document.createElement('span');
    toggleIcon.textContent = '▼'; // Changed from ▶ to ▼
    toggleIcon.style.cssText = 'color: #c9d1d9; margin-right: 10px; cursor: pointer;';

    // Rest of the code remains the same
    const labelText = document.createElement('span');
    labelText.textContent = 'New Label';
    labelText.style.cssText = 'color: #58a6ff; font-size: 16px; flex-grow: 1;';  // Changed color to #58a6ff

    const deleteButton = document.createElement('button');
    deleteButton.innerHTML = '✕';
    deleteButton.style.cssText = `
        background: none;
        border: none;
        color: #c9d1d9;
        cursor: pointer;
        font-size: 16px;
        padding: 0 5px;
    `;

    labelItem.appendChild(toggleIcon);
    labelItem.appendChild(labelText);
    labelItem.appendChild(deleteButton);

    this.addLabelEventListeners(labelItem);
    return labelItem;
}

addLabelEventListeners(labelItem) {
    const toggleIcon = labelItem.querySelector('span');
    const labelText = labelItem.querySelectorAll('span')[1];
    
    labelItem.addEventListener('dragstart', (e) => this.handleDragStart(e, labelItem));
    labelItem.addEventListener('dragend', () => labelItem.classList.remove('dragging'));
    
    toggleIcon.onclick = () => this.toggleLabelGroup(labelItem);
    labelText.ondblclick = (e) => this.editLabelText(e, labelText);
    
    labelItem.querySelector('button').onclick = (e) => {
        e.stopPropagation();
        labelItem.remove();
    };
}

toggleLabelGroup(labelItem) {
    const toggleIcon = labelItem.querySelector('span');
    const isCollapsed = toggleIcon.textContent === '▼';
    toggleIcon.textContent = isCollapsed ? '▶' : '▼';
    
    let groupContent = labelItem.querySelector('.group-content');
    if (!groupContent) {
        groupContent = document.createElement('div');
        groupContent.className = 'group-content';
        groupContent.style.display = 'none';
        labelItem.appendChild(groupContent);
    }
    
    if (!isCollapsed) {
        // Expanding - restore items in original order
        const items = Array.from(groupContent.children);
        items.reverse().forEach(item => {
            this.container.insertBefore(item, labelItem.nextSibling);
        });
    } else {
        // Collapsing - store items while maintaining order
        let nextElement = labelItem.nextElementSibling;
        while (nextElement && !nextElement.classList.contains('label-item')) {
            const currentElement = nextElement;
            nextElement = nextElement.nextElementSibling;
            groupContent.appendChild(currentElement);
        }
    }
}

editLabelText(event, labelText) {
    event.stopPropagation();
    const input = document.createElement('input');
    input.type = 'text';
    input.value = labelText.textContent;
    input.style.cssText = `
        background-color: #0d1117;
        color: #58a6ff;
        border: 1px solid #30363d;
        border-radius: 3px;
        padding: 5px;
        font-size: 16px;
        width: 200px;
    `;

    const handleBlur = () => {
        labelText.textContent = input.value || 'New Label';
        input.replaceWith(labelText);
    };

    input.onblur = handleBlur;
    input.onkeydown = (e) => {
        if (e.key === 'Enter') handleBlur();
        if (e.key === 'Escape') {
            input.value = labelText.textContent;
            handleBlur();
        }
    };

    labelText.replaceWith(input);
    input.focus();
    input.select();
}
}

// Initialize drag and drop manager
const dragDropManager = new DragAndDropManager('actionsList');

// Set up draggable buttons
document.querySelectorAll('.button[draggable="true"]').forEach(button => {
    button.addEventListener('dragstart', (e) => {
        const type = button.textContent.trim();
        const formattedText = dragDropManager.getDisplayText(type, {
            x: '0', y: '0',
            amount: '0', direction: 'up',
            duration: '0',
            wave: '0',
            key: 'None', action: 'down',
            text: 'None'
        });
        e.target.dataset.dragText = formattedText;
        e.dataTransfer.setData("text", type);
        e.dataTransfer.setData("isNewItem", "true");
    });
});

    
function setClickLocationForDialog(xInputId, yInputId) {
    function handleClick(coords) {
        document.getElementById(xInputId).value = coords[0];
        document.getElementById(yInputId).value = coords[1];
    }
    
    overlay = new TransparentOverlay(window, handleClick);
}

function showConfigInfo(file) {
    pywebview.api.get_config_info(file).then(description => {
        createInfoDialog(description, [
            {text: 'OK', action: null}
        ]);
    });
}

function setAntiAfkClickLocation() {
    const statusElement = document.getElementById('anti-afk-click-status-1');
    const selectedNumber = window.currentAntiAfkNumber || '1';
    
    if (!window.antiAfkClickLocations) {
        window.antiAfkClickLocations = {};
    }

    window.addEventListener('click', function clickHandler(e) {
        // Save coordinates for the current selection number
        window.antiAfkClickLocations[selectedNumber] = {
            x: e.screenX,
            y: e.screenY
        };
        
        // Update status display with x= format
        statusElement.textContent = `Click Location ${selectedNumber}: X=${e.screenX}, Y=${e.screenY}`;
        
        window.removeEventListener('click', clickHandler);
    }, { once: true });
}

function selectSettingsFile(event) {
    event.preventDefault();
    const selectedText = event.target.textContent;
    const button = event.target.closest('.dropdown').querySelector('button');
    const buttonContent = `
        <span>${selectedText}</span>
        <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
    `;
    button.innerHTML = buttonContent;
    button.style.marginBottom = '0px';

    const isAntiAfk = event.target.closest('.settings-container.sub[style*="margin-top: 20px"]');
    if (isAntiAfk) {
        window.currentAntiAfkNumber = selectedText;
        
        const statusElement = document.getElementById('anti-afk-click-status-1');
        
        if (window.antiAfkClickLocations && window.antiAfkClickLocations[selectedText]) {
            const coords = window.antiAfkClickLocations[selectedText];
            statusElement.textContent = `Click Location ${selectedText}: X=${coords.x}, Y=${coords.y}`;
        } else {
            statusElement.textContent = `Click Location ${selectedText}: Not Set`;
        }
    }

    event.target.closest('.dropdown-menu').style.display = 'none';
}

function showConfigLocation(file) {
    pywebview.api.get_config_location(file).then(imageData => {
        if (imageData) {
            createLocationDialog(imageData);
        } else {
            createDialog('No location image available', [{text: 'OK', action: null}]);
        }
    });
}

function selectLocationImage() {
    pywebview.api.select_location_image();
}


function startUpload() {
    const selectedPath = document.getElementById('selected-folder').textContent;
    if (selectedPath === 'No folder selected') {
        createDialog('Please select a folder first', [{text: 'OK', action: null}]);
        return;
    }
    
    document.getElementById('upload-progress').style.width = '0%';
    document.getElementById('upload-status').textContent = 'Starting upload...';
    
    pywebview.api.upload_to_github(selectedPath);
}

function loadConfigs() {
    pywebview.api.fetch_github_files().then(files => {
        const configList = document.getElementById('config-list');
        configList.innerHTML = '';
        
        files.forEach(file => {
            const configItem = document.createElement('div');
            configItem.className = 'config-item';
            configItem.style.cssText = `
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px;
                margin: 5px 0;
                background-color: #0d1117;
                border-radius: 3px;
                cursor: pointer;
            `;
            
            configItem.innerHTML = `
                <span style="color: #c9d1d9;">${file.name}</span>
<div style="display: flex; gap: 10px;">
    <button class="button" onclick='showConfigInfo(${JSON.stringify(file)})'><i class="fas fa-info-circle"></i> Info</button>
    <button class="button" onclick='showConfigLocation(${JSON.stringify(file)})'><i class="fas fa-map-marker-alt"></i> Location</button>
    <button class="button" onclick='downloadConfig(${JSON.stringify(file)})'><i class="fas fa-download"></i> Download</button>
</div>
            `;
            
            configList.appendChild(configItem);
        });
    });
}

function filterConfigs() {
    const searchTerm = document.getElementById('config-search').value.toLowerCase();
    const configItems = document.querySelectorAll('.config-item');
    
    configItems.forEach(item => {
        const configName = item.querySelector('span').textContent.toLowerCase();
        item.style.display = configName.includes(searchTerm) ? 'flex' : 'none';
    });
}

function downloadConfig(fileDetails) {
    document.getElementById('download-status').textContent = 'Downloading...';
    pywebview.api.download_github_file(fileDetails);
}

function selectUploadFolder() {
    pywebview.api.select_upload_folder();
}

function startUpload() {
    const selectedPath = document.getElementById('selected-folder').textContent;
    if (selectedPath === 'No folder selected') {
        createDialog('Please select a folder first', [{text: 'OK', action: null}]);
        return;
    }
    
    pywebview.api.upload_to_github(selectedPath);
}

function selectCloudSubTab(subTab) {
    const tabs = document.querySelectorAll('.tabs .tab-links div');
    tabs.forEach(tab => tab.classList.remove('active'));
    document.querySelector(`.tabs .tab-links div[onclick="selectCloudSubTab('${subTab}')"]`).classList.add('active');

    const subContents = document.querySelectorAll('.cloud-sub-tab-content');
    subContents.forEach(content => content.classList.add('hidden'));
    document.getElementById(subTab).classList.remove('hidden');
    
    if(subTab === 'download') {
        loadConfigs();
    }
}

function minimizeWindow() {
    document.body.style.transition = 'transform 0.2s ease-in, opacity 0.2s ease-in';
    document.body.style.transform = 'scale(0.95)';
    document.body.style.opacity = '0';
    setTimeout(() => {
        pywebview.api.minimize_window();
        // Reset transform after minimize
        document.body.style.transform = 'scale(1)';
        document.body.style.opacity = '1';
    }, 200);
}

function setWaveRegion() {
    pywebview.api.set_wave_region();
}

function closeWindow() {
    const selectedFile = document.querySelector('.settings-container.main .dropdown button span').textContent;
    const closeWithAnimation = () => {
        document.body.style.transition = 'transform 0.2s ease-in, opacity 0.2s ease-in';
        document.body.style.transform = 'scale(0.95)';
        document.body.style.opacity = '0';
        setTimeout(() => {
            pywebview.api.close_window();
        }, 200);
    };

    if (selectedFile === 'Select a file...') {
        createDialog('No file selected. Do you want to close?', [
            {text: 'Yes', action: closeWithAnimation},
            {text: 'No', action: null}
        ]);
        return;
    }

    createDialog('Do you want to save before closing?', [
        {text: 'Yes', action: () => {
            saveConfig();
            closeWithAnimation();
        }},
        {text: 'No', action: closeWithAnimation},
        {text: 'Cancel', action: null}
    ]);
}

function selectTab(tab) {
    const icons = document.querySelectorAll('.sidebar i');
    icons.forEach(icon => icon.classList.remove('active'));

    // Store logs scroll position when switching away from logs tab
    if (document.querySelector('#logs:not(.hidden)')) {
        const logContainer = document.querySelector('.log-container');
        logsScrollPosition = logContainer.scrollTop;
    }

    if (tab === 'dashboard') {
        icons[0].classList.add('active');
        document.getElementById('header-title').innerText = 'Dashboard';
        selectSubTab('units'); // Ensure units sub-tab is selected
    } else if (tab === 'settings') {
        icons[1].classList.add('active');
        document.getElementById('header-title').innerText = 'Settings';
    } else if (tab === 'cloud') {
        icons[2].classList.add('active');
        document.getElementById('header-title').innerText = 'Upload/Download';
        selectCloudSubTab('upload'); // Ensure upload sub-tab is selected
    } else if (tab === 'logs') {
        icons[3].classList.add('active');
        document.getElementById('header-title').innerText = 'Logs';
        // Restore logs scroll position 
        requestAnimationFrame(() => {
            const logContainer = document.querySelector('.log-container');
            logContainer.scrollTop = logsScrollPosition;
        });
    }

    const contents = document.querySelectorAll('.tab-content');
    contents.forEach(content => content.classList.add('hidden'));
    document.getElementById(tab).classList.remove('hidden');
}

        function selectSubTab(subTab) {
            const tabs = document.querySelectorAll('.tabs .tab-links div');
            tabs.forEach(tab => tab.classList.remove('active'));
            document.querySelector(`.tabs .tab-links div[onclick="selectSubTab('${subTab}')"]`).classList.add('active');

            const subContents = document.querySelectorAll('.sub-tab-content');
            subContents.forEach(content => content.classList.add('hidden'));
            document.getElementById(subTab).classList.remove('hidden');

            // Show or hide the unit navigation buttons based on the selected sub-tab
            const unitNavigation = document.getElementById('unit-navigation');
            if (subTab === 'units') {
                unitNavigation.classList.remove('hidden');
            } else {
                unitNavigation.classList.add('hidden');
            }
        }

function setUpgrades() {
    const upgradeNumber = document.getElementById('upgrade-number').value;
    const upgradeList = document.getElementById('upgrade-list');
    
    // Store current data in persistent storage
    const currentUpgrades = upgradeList.querySelectorAll('.upgrade-item');
    currentUpgrades.forEach((item, index) => {
        persistentUpgradeData.set(index + 1, {
            unit: item.querySelector('button span').textContent,
            wave: item.querySelector('input[type="text"]').value,
            upgradeText: item.querySelectorAll('input[type="text"]')[1].value
        });
    });

    upgradeList.innerHTML = '';

    for (let i = 1; i <= upgradeNumber; i++) {
        const upgradeItem = document.createElement('div');
        upgradeItem.className = 'upgrade-item';
        
        const savedData = persistentUpgradeData.get(i) || {
            unit: 'Select Unit',
            wave: '',
            upgradeText: ''
        };

        upgradeItem.innerHTML = `
            <div class="input-wrapper" style="width: 100%; max-width: 800px; padding-left: 0; display: flex; align-items: center; overflow: hidden;">
                <p style="margin: 0 0px 0 15px; font-weight: bold; min-width: fit-content;">Upgrade ${i}</p>
                <div style="width: 2px; height: 30px; background-color: #ffffff; margin: 0 15px; min-width: 2px;"></div>
                <p style="margin-right: 10px; font-weight: bold; min-width: fit-content;">Unit:</p>
                <div class="dropdown" style="margin-right: 15px;">
                    <button class="button" type="button" onclick="toggleDropdown(event)" style="width: 150px; min-width: 150px; height: 35px; text-align: left; padding-left: 10px; display: flex; justify-content: space-between; align-items: center; font-weight: bold; font-size: 16px;">
                        <span>${savedData.unit}</span>
                        <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
                    </button>
                    <ul class="dropdown-menu custom-scrollbar" style="display: none; position: absolute; background-color: #1b1f23; border: 1px solid #30363d; max-height: 200px; overflow-y: scroll; z-index: 1000; width: 150px; list-style-type: none; padding: 0; margin: 0;">
                        ${Array.from({length: 20}, (_, i) => 
                            `<li><a class="dropdown-item" href="#" onclick="selectUnit(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">Unit ${i + 1}</a></li>`
                        ).join('')}
                    </ul>
                </div>
                <p style="margin-right: 10px; font-weight: bold; min-width: fit-content;">Wave:</p>
                <input type="text" value="${savedData.wave}" style="
                    background-color: #1b1f23;
                    color: #c9d1d9;
                    border: 1px solid #30363d;
                    border-radius: 3px;
                    padding-left: 5px;
                    font-size: 16px;
                    font-weight: bold;
                    height: 35px;
                    width: 80px;
                    margin-right: 15px;
                    min-width: 80px;">
                <p style="margin-right: 10px; font-weight: bold; min-width: fit-content;">Upgrade Text:</p>
                <input type="text" value="${savedData.upgradeText}" style="
                    background-color: #1b1f23;
                    color: #c9d1d9;
                    border: 1px solid #30363d;
                    border-radius: 3px;
                    padding-left: 5px;
                    margin-right: 15px;
                    font-size: 16px;
                    font-weight: bold;
                    height: 35px;
                    width: 175px;
                    min-width: 100px;">
            </div>
        `;
        upgradeList.appendChild(upgradeItem);
    }
}

function selectUnit(event) {
    event.preventDefault();
    const selectedText = event.target.textContent;
    const button = event.target.closest('.dropdown').querySelector('button');
    const buttonContent = `
        <span>${selectedText}</span>
        <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
    `;
    button.innerHTML = buttonContent;
    event.target.closest('.dropdown-menu').style.display = 'none';
}

        function generateUnitOptions(numUnits) {
            let options = '';
            for (let i = 1; i <= numUnits; i++) {
                options += `<option value="${i}">Unit ${i}</option>`;
            }
            return options;
        }

function setAbilities() {
    const abilityNumber = document.getElementById('ability-number').value;
    const abilityList = document.getElementById('ability-list');
    
    // Store current data in persistent storage
    const currentAbilities = abilityList.querySelectorAll('.upgrade-item');
    currentAbilities.forEach((item, index) => {
        persistentAbilityData.set(index + 1, {
            unit: item.querySelector('button span').textContent,
            wave: item.querySelector('input[type="text"]').value,
            abilityText: item.querySelectorAll('input[type="text"]')[1].value
        });
    });

    abilityList.innerHTML = '';

    for (let i = 1; i <= abilityNumber; i++) {
        const abilityItem = document.createElement('div');
        abilityItem.className = 'upgrade-item';
        
        const savedData = persistentAbilityData.get(i) || {
            unit: 'Select Unit',
            wave: '',
            abilityText: ''
        };

        abilityItem.innerHTML = `
            <div class="input-wrapper" style="width: 100%; max-width: 800px; padding-left: 0; display: flex; align-items: center; overflow: hidden;">
                <p style="margin: 0 0px 0 15px; font-weight: bold; min-width: fit-content;">Ability ${i}</p>
                <div style="width: 2px; height: 30px; background-color: #ffffff; margin: 0 15px; min-width: 2px;"></div>
                <p style="margin-right: 10px; font-weight: bold; min-width: fit-content;">Unit:</p>
                <div class="dropdown" style="margin-right: 15px;">
                    <button class="button" type="button" onclick="toggleAbilityDropdown(event)" style="width: 150px; min-width: 150px; height: 35px; text-align: left; padding-left: 10px; display: flex; justify-content: space-between; align-items: center; font-weight: bold; font-size: 16px;">
                        <span>${savedData.unit}</span>
                        <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
                    </button>
                    <ul class="dropdown-menu custom-scrollbar" style="display: none; position: absolute; background-color: #1b1f23; border: 1px solid #30363d; max-height: 200px; overflow-y: scroll; z-index: 1000; width: 150px; list-style-type: none; padding: 0; margin: 0;">
                        ${Array.from({length: 20}, (_, i) => 
                            `<li><a class="dropdown-item" href="#" onclick="selectUnit(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">Unit ${i + 1}</a></li>`
                        ).join('')}
                    </ul>
                </div>
                <p style="margin-right: 10px; font-weight: bold; min-width: fit-content;">Wave:</p>
                <input type="text" value="${savedData.wave}" style="
                    background-color: #1b1f23;
                    color: #c9d1d9;
                    border: 1px solid #30363d;
                    border-radius: 3px;
                    padding-left: 5px;
                    font-size: 16px;
                    font-weight: bold;
                    height: 35px;
                    width: 80px;
                    margin-right: 15px;
                    min-width: 80px;">
                <p style="margin-right: 10px; font-weight: bold; min-width: fit-content;">Delay:</p>
                <input type="text" value="${savedData.abilityText}" style="
                    background-color: #1b1f23;
                    color: #c9d1d9;
                    border: 1px solid #30363d;
                    border-radius: 3px;
                    padding-left: 5px;
                    margin-right: 15px;
                    font-size: 16px;
                    font-weight: bold;
                    height: 35px;
                    width: 175px;
                    min-width: 100px;">
            </div>
        `;
        abilityList.appendChild(abilityItem);
    }
}

function setKeyBinding(button) {
    button.textContent = 'Press a key...';
    
    // Tell Python we're setting a key
    pywebview.api.set_key_setting_state(true);
    
    function handleKeyPress(e) {
        e.preventDefault();
        const keyPressed = e.key.toUpperCase();
        button.textContent = keyPressed;
        
        // Log the button press
        pywebview.api.log_key_binding(button.previousElementSibling.textContent.replace(':', ''), keyPressed);
        
        // Add keyboard hotkey
        pywebview.api.set_keyboard_binding(keyPressed, button.previousElementSibling.textContent.replace(':', ''));
        
        // Tell Python we're done setting the key
        pywebview.api.set_key_setting_state(false);
        
        document.removeEventListener('keydown', handleKeyPress);
    }
    
    document.addEventListener('keydown', handleKeyPress);
}


function setClickLocation(button) {
    const locationElement = button.nextElementSibling;
    locationElement.id = 'click-location-' + Math.random().toString(36);
    pywebview.api.get_click_location(locationElement.id, true);
}

function setUpgradeClickLocation() {
    pywebview.api.get_click_location('upgrade-click-status');
}

function setAbilityClickLocation() {
    pywebview.api.get_click_location('ability-click-status');
}

function setAntiAfkClickLocation() {
    // Target specifically the anti-AFK container's dropdown
    const locationNumber = document.querySelector('.settings-container.sub[style*="margin-top: 20px"] .dropdown button span').textContent;
    console.log("Selected Anti-AFK location number:", locationNumber);
    pywebview.api.get_click_location(`anti-afk-click-status-${locationNumber}`, false, locationNumber);
}


function setReplayClickLocation() {
    pywebview.api.get_click_location('replay-click-status');
}

function setReplayRegion() {
    pywebview.api.set_replay_region();
}

function setUpgradeRegion() {
    pywebview.api.set_upgrade_region();
}

function generateUnitCards() {
    const cardContainer1 = document.querySelector('#unit-tab-1 .card-container');
    const cardContainer2 = document.querySelector('#unit-tab-2 .card-container');
    for (let i = 1; i <= 20; i++) {
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <h2 style="margin-top: 0;">Unit ${i}</h2>
            <div class="input-container">
                <div class="dropdown">
                    <button class="button" type="button" onclick="toggleUnitDropdown(event)" style="width: 100%; text-align: left; padding-left: 10px; display: flex; justify-content: space-between; align-items: center; background-color: #0d1117; transition: background-color 0.3s;">
                        <span>Select Unit Slot</span>
                        <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
                    </button>
                    <ul class="dropdown-menu custom-scrollbar" style="display: none; position: absolute; background-color: #0d1117; border: 1px solid #30363d; max-height: 225px; overflow-y: scroll; z-index: 1000; width: 135px; list-style-type: none; padding: 0; margin: 0;">
                        ${Array.from({length: 6}, (_, i) => 
                            `<li><a class="dropdown-item" href="#" onclick="selectUnit(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">Unit slot ${i + 1}</a></li>`
                        ).join('')}
                    </ul>
                </div>
                <label class="checkbox-label">
                    <input type="checkbox" id="enable-${i}" class="checkbox">
                    <span>Enable</span>
                </label>
                <div class="wave-input">
                    Wave:
                    <input type="text">
                </div>
                <div class="delay-input">
                    Delay:
                    <input type="text">
                </div>
                <button class="button" onclick="setClickLocation(this)" style="padding: 12px 0; width: 100%;">Set Click Location</button>
                <p class="click-location" style="font-size: 12px; color: #58a6ff;">Click location: not set</p>
            </div>
        `;
        if (i <= 10) {
            cardContainer1.appendChild(card);
        } else {
            cardContainer2.appendChild(card);
        }
    }
}

        function previousUnitTab() {
            document.getElementById('unit-tab-1').classList.remove('hidden');
            document.getElementById('unit-tab-2').classList.add('hidden');
        }

        function nextUnitTab() {
            document.getElementById('unit-tab-1').classList.add('hidden');
            document.getElementById('unit-tab-2').classList.remove('hidden');
        }

function saveConfig() {
    const selectedFile = document.querySelector('.settings-container.main .dropdown button span').textContent;
    
    if (selectedFile === 'Select a file...') {
        createDialog('No File Selected. Select A File', [
            {text: 'OK', action: null}
        ]);
        return;
    }

    const webhookUrl = document.querySelector('.settings-container.main .Webhook-input').value;
    pywebview.api.save_webhook(selectedFile, webhookUrl);

    const unitData = [];
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        const unitSlot = card.querySelector('.dropdown button span').textContent;
        const enabled = card.querySelector('.checkbox').checked;
        const wave = card.querySelector('.wave-input input').value;
        const delay = card.querySelector('.delay-input input').value;
        const clickLocation = card.querySelector('.click-location').textContent;
        
        unitData.push({
            unitNumber: index + 1,
            unitSlot: unitSlot,
            enabled: enabled,
            wave: wave,
            delay: delay,
            clickLocation: clickLocation
        });
    });

    const upgradeData = {
        numberOfUpgrades: document.getElementById('upgrade-number').value,
        upgradeRegionStatus: document.getElementById('upgrade-region-status').textContent,
        upgradeClickStatus: document.getElementById('upgrade-click-status').textContent,
        upgrades: []
    };

    const upgradeItems = document.querySelectorAll('#upgrade-list .upgrade-item');
    upgradeItems.forEach((item, index) => {
        upgradeData.upgrades.push({
            upgradeNumber: index + 1,
            unit: item.querySelector('.dropdown button span').textContent,
            wave: item.querySelectorAll('input[type="text"]')[0].value,
            upgradeText: item.querySelectorAll('input[type="text"]')[1].value
        });
    });

    const abilityData = {
        numberOfAbilities: document.getElementById('ability-number').value,
        abilityClickStatus: document.getElementById('ability-click-status').textContent,
        abilities: []
    };

    const abilityItems = document.querySelectorAll('#ability-list .upgrade-item');
    abilityItems.forEach((item, index) => {
        abilityData.abilities.push({
            abilityNumber: index + 1,
            unit: item.querySelector('.dropdown button span').textContent,
            wave: item.querySelectorAll('input[type="text"]')[0].value,
            delay: item.querySelectorAll('input[type="text"]')[1].value
        });
    });

    const replayData = {
        replayRegionStatus: document.getElementById('replay-region-status').textContent,
        replayClickStatus: document.getElementById('replay-click-status').textContent,
        replayText: document.querySelector('.settings-container.replay .file-input').value
    };

    const antiAfkData = {
        clickLocations: window.antiAfkClickLocations || {}
    };

    const waveData = {
        waveRegionStatus: document.getElementById('wave-region-status').textContent,
        waveFormat: document.querySelector('.settings-container.sub .dropdown button span').textContent
    };

    const customData = {
        enabled: document.querySelector('#custom .checkbox').checked,
        onReplay: document.getElementById('onReplayCheck').checked,
        onStart: document.getElementById('onStartCheck').checked,
        actions: []
    };

    const actionItems = document.querySelectorAll('#actionsList > div');
    actionItems.forEach(item => {
        if (item.classList.contains('label-item')) {
            const labelData = {
                type: 'Label',
                text: item.querySelector('span:nth-child(2)').textContent,
                isCollapsed: item.querySelector('span:first-child').textContent === '▶',
                nestedActions: []
            };

            const groupContent = item.querySelector('.group-content');
            if (groupContent) {
                Array.from(groupContent.children).forEach(nestedItem => {
                    labelData.nestedActions.push({
                        type: nestedItem.dataset.type,
                        settings: nestedItem.settings
                    });
                });
            }
            customData.actions.push(labelData);
        } else {
            customData.actions.push({
                type: item.dataset.type,
                settings: item.settings
            });
        }
    });

    const configData = {
        units: unitData,
        upgrades: upgradeData,
        abilities: abilityData,
        replay: replayData,
        antiAfk: antiAfkData,
        wave: waveData,
        custom: customData,
        macroKeys: {
            startKey: document.querySelector('.main-row:nth-child(3) .button').textContent,
            stopKey: document.querySelector('.main-row:nth-child(4) .button').textContent
        },
        defaultUpgradeText: document.getElementById('default-upgrade-text').value
    };

    pywebview.api.save_config(selectedFile, JSON.stringify(configData));
    
    createDialog(`Config saved to ${selectedFile}`, [
        {text: 'OK', action: null}
    ]);
}

function loadConfig() {
    const selectedFile = document.querySelector('.settings-container.main .dropdown button span').textContent;
   
    if (selectedFile === 'Select a file...') {
        createDialog('No File Selected. Select A File', [
            {text: 'OK', action: null}
        ]);
        return;
    }

    pywebview.api.load_webhook(selectedFile).then(webhookUrl => {
        document.querySelector('.settings-container.main .Webhook-input').value = webhookUrl;
    });    

    pywebview.api.load_config(selectedFile).then(data => {
        const config = JSON.parse(data);
        
        if (config.units && Array.isArray(config.units)) {
            const cards = document.querySelectorAll('.card');
            config.units.forEach((unit, index) => {
                if (index < cards.length) {
                    const card = cards[index];
                    card.querySelector('.dropdown button span').textContent = unit.unitSlot || 'Select Unit Slot';
                    card.querySelector('.checkbox').checked = unit.enabled;
                    card.querySelector('.wave-input input').value = unit.wave || '';
                    card.querySelector('.delay-input input').value = unit.delay || '';
                    card.querySelector('.click-location').textContent = unit.clickLocation || 'Click location: not set';
                }
            });
        }

        if (config.upgrades) {
            document.getElementById('upgrade-number').value = config.upgrades.numberOfUpgrades || '0';
            setUpgrades();
            
            document.getElementById('upgrade-region-status').textContent = config.upgrades.upgradeRegionStatus || 'Upgrade Region: Not Set';
            document.getElementById('upgrade-click-status').textContent = config.upgrades.upgradeClickStatus || 'Upgrade Click Location: Not Set';
            
            setTimeout(() => {
                const upgradeItems = document.querySelectorAll('#upgrade-list .upgrade-item');
                config.upgrades.upgrades.forEach((upgrade, index) => {
                    if (index < upgradeItems.length) {
                        const item = upgradeItems[index];
                        item.querySelector('.dropdown button span').textContent = upgrade.unit || 'Select Unit';
                        item.querySelectorAll('input[type="text"]')[0].value = upgrade.wave || '';
                        item.querySelectorAll('input[type="text"]')[1].value = upgrade.upgradeText || '';
                    }
                });
            }, 100);
        }

        if (config.defaultUpgradeText) {
            document.getElementById('default-upgrade-text').value = config.defaultUpgradeText;
        }

        if (config.abilities) {
            document.getElementById('ability-number').value = config.abilities.numberOfAbilities || '0';
            setAbilities();
            
            document.getElementById('ability-click-status').textContent = config.abilities.abilityClickStatus || 'Ability Click Location: Not Set';
            
            setTimeout(() => {
                const abilityItems = document.querySelectorAll('#ability-list .upgrade-item');
                config.abilities.abilities.forEach((ability, index) => {
                    if (index < abilityItems.length) {
                        const item = abilityItems[index];
                        item.querySelector('.dropdown button span').textContent = ability.unit || 'Select Unit';
                        item.querySelectorAll('input[type="text"]')[0].value = ability.wave || '';
                        item.querySelectorAll('input[type="text"]')[1].value = ability.delay || '';
                    }
                });
            }, 100);
        }

        if (config.replay) {
            document.getElementById('replay-region-status').textContent = config.replay.replayRegionStatus || 'Replay Region: Not Set';
            document.getElementById('replay-click-status').textContent = config.replay.replayClickStatus || 'Click Location: Not Set';
            document.querySelector('.settings-container.replay .file-input').value = config.replay.replayText || '';
        }

        if (config.antiAfk && config.antiAfk.clickLocations) {
            window.antiAfkClickLocations = config.antiAfk.clickLocations;
            const currentNumber = window.currentAntiAfkNumber || '1';
            const statusElement = document.getElementById('anti-afk-click-status-1');
            
            if (window.antiAfkClickLocations[currentNumber]) {
                const coords = window.antiAfkClickLocations[currentNumber];
                statusElement.textContent = `Click Location ${currentNumber}: X=${coords.x}, Y=${coords.y}`;
            } else {
                statusElement.textContent = `Click Location ${currentNumber}: Not Set`;
            }
        }

        if (config.wave) {
            document.getElementById('wave-region-status').textContent = config.wave.waveRegionStatus || 'Wave Region: Not Set';
            if (config.wave.waveFormat) {
                document.querySelector('.settings-container.sub .dropdown button').innerHTML = `
                    <span>${config.wave.waveFormat}</span>
                    <span style="transform: rotate(90deg); margin-right: 5px; font-size: 18px;">&gt;</span>
                `;
            }
        }

        if (config.custom) {
            document.querySelector('#custom .checkbox').checked = config.custom.enabled;
            document.getElementById('onReplayCheck').checked = config.custom.onReplay;
            document.getElementById('onStartCheck').checked = config.custom.onStart;
            
            const actionsList = document.getElementById('actionsList');
            actionsList.innerHTML = '';
            
            config.custom.actions.forEach(action => {
                if (action.type === 'Label') {
                    const labelItem = dragDropManager.createLabelItem();
                    const labelText = labelItem.querySelector('span:nth-child(2)');
                    const toggleIcon = labelItem.querySelector('span:first-child');
                    
                    labelText.textContent = action.text;
                    
                    // Set initial state based on nested actions
                    const hasNestedActions = action.nestedActions && action.nestedActions.length > 0;
                    toggleIcon.textContent = hasNestedActions ? '▶' : '▼';
                    
                    actionsList.appendChild(labelItem);

                    if (action.nestedActions && action.nestedActions.length > 0) {
                        const groupContent = document.createElement('div');
                        groupContent.className = 'group-content';
                        groupContent.style.display = hasNestedActions ? 'none' : 'block';
                        
                        action.nestedActions.forEach(nestedAction => {
                            const nestedItem = dragDropManager.createDraggableItem(
                                nestedAction.type, 
                                nestedAction.settings
                            );
                            groupContent.appendChild(nestedItem);
                        });
                        
                        labelItem.appendChild(groupContent);
                    }
                } else {
                    const actionItem = dragDropManager.createDraggableItem(
                        action.type, 
                        action.settings
                    );
                    actionsList.appendChild(actionItem);
                }
            });
        }

        if (config.macroKeys) {
            document.querySelector('.main-row:nth-child(3) .button').textContent = config.macroKeys.startKey || 'Click To Set';
            document.querySelector('.main-row:nth-child(4) .button').textContent = config.macroKeys.stopKey || 'Click To Set';
        }

        createDialog(`Config loaded from ${selectedFile}`, [
            {text: 'OK', action: null}
        ]);
    }).catch(error => {
        console.error('Error loading config:', error);
        createDialog(`Error loading config from ${selectedFile}`, [
            {text: 'OK', action: null}
        ]);
    });
}


        document.addEventListener('DOMContentLoaded', () => {
            generateUnitCards();
            selectSubTab('units'); // Ensure the units tab is selected by default
        });
        
    </script>
</body>
</html>
"""

class MacroBuilder:
    def __init__(self):
        self.macro_sequence = []
    
    def get_dropped_items(self):
        return window.evaluate_js("""
            function getAllItems() {
                const items = [];
                const allElements = document.querySelectorAll('#actionsList > div');
            
                allElements.forEach(element => {
                    if (element.classList.contains('label-item')) {
                        // Get items from group content if it exists
                        const groupContent = element.querySelector('.group-content');
                        if (groupContent) {
                            Array.from(groupContent.children).forEach(item => {
                                items.push({
                                    type: item.dataset.type,
                                    settings: item.settings || {}
                                });
                            });
                        }
                    } else {
                        items.push({
                            type: element.dataset.type,
                            settings: element.settings || {}
                        });
                    }
                });
                return items;
            }
            getAllItems();
        """)

class MacroActions:
    @staticmethod
    def move_and_click(x, y, delay):
        pydirectinput.moveTo(x, y)
        time.sleep(0.025)
        pydirectinput.moveTo(x, y - 1)
        time.sleep(0.025)
        pydirectinput.click(x, y - 2)
        time.sleep(float(delay))
    
    @staticmethod
    def scroll(amount, direction, delay):
        scroll_amount = int(amount)
        wheel_delta = 120 if direction == 'up' else -120
    
        for _ in range(scroll_amount):
            win32api.mouse_event(0x0800, 0, 0, wheel_delta, 0)
            time.sleep(0.05)
        time.sleep(float(delay))
    
    @staticmethod
    def key_press(key, action):
        if action == 'down':
            keyboard.press(key)
        else:
            keyboard.release(key)
            
    @staticmethod
    def sleep(duration):
        time.sleep(float(duration))
        
    @staticmethod
    def look(direction, duration):
        pydirectinput.PAUSE = 0.0
        start_x, start_y = win32api.GetCursorPos()
        move_amount = -5 if direction == 'up' else 5
        pydirectinput.mouseDown(button='right')
    
        for _ in range(15):
            win32api.SetCursorPos((start_x, start_y))
            time.sleep(0.001)
    
        start_time = time.time()
        while time.time() - start_time < float(duration):
            pydirectinput.moveRel(0, move_amount, relative=True)
            time.sleep(0.001)
    
        pydirectinput.mouseUp(button='right')

    @staticmethod
    def key_hold(key, duration):
        keyboard.press(key.lower())
        time.sleep(float(duration))
        keyboard.release(key.lower())
 
    @staticmethod
    def wait_for_wave(wave_number, api_instance):
        while not api_instance.stop_event.is_set():
            current_wave, _ = api_instance.check_wave_change(custom_wave=wave_number)
            if current_wave and int(current_wave) >= int(wave_number):
                api_instance.handle_wave(wave_number, is_custom=True)
                return True
            time.sleep(0.5)
        
            if api_instance.stop_event.is_set():
                print("Stop signal received during wave wait")
                return False

    @staticmethod
    def custom_ocr(settings, api_instance):
        while not api_instance.stop_event.is_set():
            if api_instance.check_custom_ocr(settings):
                return True
            time.sleep(0.5)
        
            if api_instance.stop_event.is_set():
                print("Stop signal received during OCR check")
                return False

class ExecuteMacro:
    def __init__(self, api_instance):
        self.builder = MacroBuilder()
        self.actions = MacroActions()
        self.api = api_instance
    
    def run_macro_sequence(self):
        self.api.custom_macro_running = True
        items = self.builder.get_dropped_items()
        for item in items:
            if self.api.stop_event.is_set():
                print("Stopping custom macro sequence")
                return False
                
            if item['type'] == 'Move And Click':
                self.actions.move_and_click(
                    int(item['settings']['x']), 
                    int(item['settings']['y']),
                    item['settings']['delay']
                )
            
            elif item['type'] == 'Scroll':
                self.actions.scroll(
                    item['settings']['amount'], 
                    item['settings']['direction'],
                    item['settings']['delay']
                )
            
            elif item['type'] == 'Key Press':
                self.actions.key_press(item['settings']['key'].lower(), item['settings']['action'])
            
            elif item['type'] == 'Sleep':
                start_time = time.time()
                while time.time() - start_time < float(item['settings']['duration']):
                    if self.api.stop_event.is_set():
                        return False
                    time.sleep(0.1)
            
            elif item['type'] == 'Look':
                self.actions.look(item['settings']['direction'], item['settings']['duration'])
            
            elif item['type'] == 'Wait For Wave':
                if not self.actions.wait_for_wave(item['settings']['wave'], self.api):
                    return False

            elif item['type'] == 'Custom OCR':
                while not self.actions.custom_ocr(item['settings'], self.api):
                    if self.api.stop_event.is_set():
                        return False
                    time.sleep(0.5)

            elif item['type'] == 'Key Hold':
                self.actions.key_hold(item['settings']['key'], item['settings']['duration'])
        
        self.api.custom_macro_running = False
        return True

class TransparentOverlay:
    def __init__(self, window, callback, region_select=False):
        window.minimize()
        time.sleep(0.2)  
        
        self.root = tk.Tk()
        self.window = window
        self.callback = callback
        self.region_select = region_select
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        # Get all monitors info
        self.monitors = get_monitors()
        
        # Calculate total screen dimensions
        self.min_x = min(monitor.x for monitor in self.monitors)
        self.min_y = min(monitor.y for monitor in self.monitors)
        self.max_x = max(monitor.x + monitor.width for monitor in self.monitors)
        self.max_y = max(monitor.y + monitor.height for monitor in self.monitors)
        
        total_width = self.max_x - self.min_x
        total_height = self.max_y - self.min_y
        
        # Configure base overlay window
        self.root.attributes('-alpha', 0.1)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        self.root.geometry(f"{total_width}x{total_height}+{self.min_x}+{self.min_y}")
        
        # Create canvas on root window if not region select
        if not region_select:
            self.canvas = tk.Canvas(self.root, highlightthickness=0)
            self.canvas.bind('<Button-1>', self.on_click)
        else:
            # Create top window and its canvas for region selection
            self.top_window = tk.Toplevel(self.root)
            self.top_window.attributes('-alpha', 1.0)
            self.top_window.attributes('-topmost', True)
            self.top_window.overrideredirect(True)
            self.top_window.geometry(f"{total_width}x{total_height}+{self.min_x}+{self.min_y}")
            self.top_window.attributes('-transparentcolor', 'black')
            self.canvas = tk.Canvas(self.top_window, highlightthickness=0, bg='black')
            
            # Bind events to root window for region selection
            self.root.bind('<Button-1>', self.start_selection)
            self.root.bind('<B1-Motion>', self.update_selection)
            self.root.bind('<ButtonRelease-1>', self.end_selection)
        
        self.canvas.pack(fill='both', expand=True)
        self.root.focus_force()
        self.root.mainloop()

    def restore_window(self):
        self.window.restore()
        time.sleep(0.2)

    def start_selection(self, event):
        self.start_x = event.x_root - self.min_x
        self.start_y = event.y_root - self.min_y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='#00FF00', width=2
        )

    def update_selection(self, event):
        cur_x = event.x_root - self.min_x
        cur_y = event.y_root - self.min_y
        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def end_selection(self, event):
        end_x = event.x_root - self.min_x
        end_y = event.y_root - self.min_y
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        self.root.destroy()
        self.callback((x1, y1, x2, y2))
        self.restore_window()

    def on_click(self, event):
        x = event.x_root - self.min_x
        y = event.y_root - self.min_y
        self.root.destroy()
        self.callback((x, y))
        self.restore_window()

class LogRedirect(io.StringIO):
    def __init__(self, api):
        super().__init__()
        self.api = api
    
    def write(self, text):
        if text.strip():
            # Clean up the text by removing carets and extra whitespace
            cleaned_text = text.replace('^', '').strip()
            if cleaned_text:
                self.api.update_logs(cleaned_text.replace('"', '\\"'))
    
    def flush(self):
        pass


class Api:
    def __init__(self):
        self.handled_waves = set()
        self.handled_custom_waves = set()
        self.file_monitor_thread = threading.Thread(target=self.monitor_files, daemon=True)
        self.file_monitor_thread.start()
        self.highest_wave_seen = 0
        self.total_runs = 0
        self.completed_placements = set()
        self.placement_queue = queue.Queue()
        self.units = []
        self.upgrade_settings = []
        self.ability_settings = []
        self.upgrade_queue = queue.Queue()
        self.ability_queue = queue.Queue()
        self.placement_queue = queue.Queue()
        self.macro_event = threading.Event()
        self.anti_afk_event = threading.Event()
        self.ability_events = {}
        self.ability_timers = []
        self.current_upgrade_text = None

        self.start_key = None
        self.stop_key = None
        self.is_setting_key = False

        self.macro_running = False
        self.custom_macro_running = False
        self.stop_event = threading.Event()

    def select_location_image(self):
        def open_file_dialog():
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
            root.destroy()
            return file_path

        # Run the file dialog in the main thread
        file_path = webview.windows[0].evaluate_js(
            'new Promise(resolve => setTimeout(resolve, 0))'
        )
        file_path = open_file_dialog()

        if file_path:
            folder_path = window.evaluate_js("document.getElementById('selected-folder').textContent")
            if folder_path != 'No folder selected':
                destination = os.path.join(folder_path, "location.png")
                with open(file_path, 'rb') as src, open(destination, 'wb') as dst:
                    dst.write(src.read())
                print("Location image saved successfully")


    def get_config_location(self, file_details):
        try:
            url = file_details['url']
            response = requests.get(url)
            response.raise_for_status()
            items = response.json()

            location_file = next((item for item in items if item['name'] == 'location.png'), None)
            if location_file and 'download_url' in location_file:
                image_response = requests.get(location_file['download_url'])
                image_response.raise_for_status()
                return base64.b64encode(image_response.content).decode('utf-8')
            return None
        except Exception as e:
            print(f'Error fetching location image: {str(e)}')
            return None

    def monitor_files(self):
        while True:
            if not os.path.exists("configs"):
                os.makedirs("configs")
            config_files = [d for d in os.listdir("configs") if os.path.isdir(os.path.join("configs", d))]
        
            js_code = f"""
                const settingsDropdown = document.querySelector('.settings-container.main .dropdown-menu');
                const fileList = {config_files};
                settingsDropdown.innerHTML = fileList.map(file => 
                    `<li><a class="dropdown-item" href="#" onclick="selectSettingsFile(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">${{file}}</a></li>`
                ).join('');
            """
            window.evaluate_js(js_code)
        
            time.sleep(5)

    def log_key_binding(self, binding_type, key):
        print(f"Set {binding_type} to: {key}")

    def start_macro(self):
        if self.macro_running:
            print("Macro is already running!")
            return

        # Check if custom macro is enabled and set to run on start
        custom_settings = window.evaluate_js("""
            ({
                enabled: document.querySelector('#custom .checkbox').checked,
                onStart: document.getElementById('onStartCheck').checked
            })
        """)

        print("Starting macro...")
        self.reader = easyocr.Reader(['en'])
        self.macro_running = True
        self.stop_event.clear()

        # Run custom macro in separate thread if enabled
        if custom_settings['enabled'] and custom_settings['onStart']:
            print("Running custom macro sequence on start")
            threading.Thread(target=lambda: ExecuteMacro(self).run_macro_sequence(), daemon=True).start()

        # Reset time tracking and run counter
        self.last_replay_time = time.time()
        self.total_runs = 0

        # Reset all tracking variables
        self.completed_upgrades = {}
        self.completed_abilities = {}
        self.completed_placements = set()
    
        # Clear all queues
        while not self.upgrade_queue.empty():
            self.upgrade_queue.get()
        while not self.ability_queue.empty():
            self.ability_queue.get()
        while not self.placement_queue.empty():
            self.placement_queue.get()
        
        self.highest_wave_seen = 0
        self.current_upgrade = None
        self.macro_loop_interval = 10  # milliseconds
    
        # Run the macro loop in a separate thread
        threading.Thread(target=self.run_macro_loop, daemon=True).start()
        print("Macro started successfully")

    def stop_macro(self):
        print("Stopping macro...")
        self.stop_event.set()
        self.macro_running = False
    
        # Clear all queues
        while not self.upgrade_queue.empty():
            self.upgrade_queue.get()
        while not self.ability_queue.empty():
            self.ability_queue.get()
        while not self.placement_queue.empty():
            self.placement_queue.get()
        
        # Reset tracking variables
        self.current_upgrade = None
        self.completed_placements.clear()
        self.completed_upgrades.clear()
        self.completed_abilities.clear()
        self.handled_waves.clear()
        self.handled_custom_waves.clear()
    
        print("Macro stopped successfully")

    def set_keyboard_binding(self, key, binding_type):
        # Remove existing binding first
        keyboard.unhook_all()  # Clear all bindings
    
        # Store the new key and create new binding
        if binding_type.strip() == 'Start Macro Key':
            self.start_key = key.lower()
            keyboard.on_press(self.handle_key_press)
        elif binding_type.strip() == 'Stop Macro Key':
            self.stop_key = key.lower()
        keyboard.on_press(self.handle_key_press)
        
    def set_key_setting_state(self, state):
        self.is_setting_key = state

    def handle_key_press(self, event):
        if self.is_setting_key:
            return
        
        if event.name == self.start_key:
            self.start_macro()
        elif event.name == self.stop_key:
            self.stop_macro()
            
    def run_macro_loop(self):
        while self.macro_running and not self.stop_event.is_set():
            if self.custom_macro_running:
                time.sleep(0.1)
                continue
            
            if not self.current_upgrade:
                current_wave, _ = self.check_wave_change()
                if current_wave:
                    print(f"Wave {current_wave} detected in run_macro_loop")
                    self.handle_wave(current_wave)

                # Only add new timers from queue if they don't exist yet
                while not self.ability_queue.empty():
                    ability_unit, ability_delay, ability_number = self.ability_queue.get()
                    if ability_number not in self.completed_abilities:
                        start_time = time.time()
                        timer_entry = (start_time + ability_delay, ability_unit, ability_number)
                        if timer_entry not in self.ability_timers:
                            self.ability_timers.append(timer_entry)
                            print(f"Added ability {ability_number} to timer list with delay {ability_delay}")
        
                # Check if any ability timer is ready
                current_time = time.time()
                for timer, unit, number in self.ability_timers[:]:
                    if current_time >= timer:
                        print(f"Ability timer ready - executing ability macro")
                        self.activate_ability(unit, number)
                        self.ability_timers.remove((timer, unit, number))
                        time.sleep(0.5)
      
                # Process upgrades when no current upgrade is running
                while not self.current_upgrade and not self.upgrade_queue.empty():
                    self.current_upgrade = self.upgrade_queue.get()
                    if not self.upgrade_macro(*self.current_upgrade):
                        return
                    self.current_upgrade = None
        
                if self.check_for_replay():
                    print("Replay detected - executing replay macro")
                    if not self.replay_macro():
                        return
                    self.completed_placements.clear()
                    self.completed_upgrades.clear()
                    self.completed_abilities.clear()
        
                if not self.anti_afk_event.is_set():
                    self.anti_afk_macro()
        
                for _ in range(10):
                    if self.stop_event.is_set():
                        print("Stop signal received, ending macro loop")
                        return
                    time.sleep(self.macro_loop_interval / 10000)

    def handle_wave(self, wave, is_custom=False):
        # Skip if wave already handled in the appropriate set
        if is_custom:
            if wave in self.handled_custom_waves:
                print(f"Custom wave {wave} already handled, skipping...")
                return
        else:
            if wave in self.handled_waves:
                print(f"Wave {wave} already handled, skipping...")
                return
    
        print(f"Processing {'custom ' if is_custom else ''}wave {wave}")

        # Get unit data from UI
        units_data = window.evaluate_js("""
           Array.from(document.querySelectorAll('.card')).map((card, index) => ({
                number: index + 1,
                enabled: card.querySelector('.checkbox').checked,
                wave: card.querySelector('.wave-input input').value,
                delay: card.querySelector('.delay-input input').value,
                slot: card.querySelector('.dropdown button span').textContent,
                location: card.querySelector('.click-location').textContent,
                placed: false
            }))
        """)
    
        # Handle unit placement
        for unit in units_data:
            if (unit['enabled'] and 
                unit['wave'] and 
                unit['delay'] and 
                unit['slot'] != 'Select Unit Slot' and
                "not set" not in unit['location'].lower() and
                int(unit['wave']) == wave and 
                unit['number'] not in self.completed_placements):
                if not self.place_macro(unit['number']):
                    return False
    
        # Get and sort upgrade settings
        upgrades_data = window.evaluate_js("""
            Array.from(document.querySelectorAll('#upgrade-list .upgrade-item'))
                .map(item => ({
                    number: item.querySelector('p').textContent.replace('Upgrade ', ''),
                    unit: item.querySelector('.dropdown button span').textContent.replace('Unit ', ''),
                    wave: item.querySelectorAll('input[type="text"]')[0].value,
                    text: item.querySelectorAll('input[type="text"]')[1].value
                }))
                .sort((a, b) => parseInt(a.number) - parseInt(b.number))
        """)
    
        for upgrade in upgrades_data:
            try:
                upgrade_wave = upgrade['wave'].lower().strip()
                upgrade_unit = upgrade['unit'].strip()
                upgrade_number = int(upgrade['number'])
    
                if not upgrade_wave or not upgrade['text'].strip() or upgrade_unit == 'Select Unit':
                    continue
    
                upgrade_unit = int(upgrade_unit)
        
                if upgrade_unit not in self.completed_placements:
                    continue
    
                if (upgrade_number not in self.completed_upgrades.get(upgrade_unit, set()) and
                    not any(u == (upgrade_unit, upgrade['text'], upgrade_number) 
                           for u in list(self.upgrade_queue.queue))):
        
                    if ((upgrade_wave.isdigit() and int(upgrade_wave) == wave) or 
                        (not upgrade_wave.isdigit())):
                        print(f"Queueing upgrade {upgrade_number} for unit {upgrade_unit}")
                        self.upgrade_queue.put((upgrade_unit, upgrade['text'], upgrade_number))
            except ValueError:
                continue
        
        # Handle abilities
        abilities_data = window.evaluate_js("""
            Array.from(document.querySelectorAll('#ability-list .upgrade-item')).map(item => ({
                number: item.querySelector('p').textContent.replace('Ability ', ''),
                unit: item.querySelector('.dropdown button span').textContent.replace('Unit ', ''),
                wave: item.querySelectorAll('input[type="text"]')[0].value,
                delay: item.querySelectorAll('input[type="text"]')[1].value
            }))
        """)
        
        cumulative_delay = 0
        for ability in abilities_data:
            try:
                if not ability['wave'].strip() or not ability['delay'].strip() or ability['unit'].strip() == 'Select Unit':
                    continue
    
                ability_wave = int(ability['wave'])
                ability_unit = int(ability['unit'])
                ability_number = int(ability['number'])
                ability_delay = float(ability['delay'])
    
                if (ability_wave == wave and
                    ability_unit in self.completed_placements and
                    ability_number not in self.completed_abilities and
                    not any(a[2] == ability_number for a in list(self.ability_queue.queue)) and
                    not any(t[2] == ability_number for t in self.ability_timers)):
        
                    cumulative_delay += ability_delay
                    start_time = time.time()
                    timer_entry = (start_time + cumulative_delay, ability_unit, ability_number)
                    self.ability_timers.append(timer_entry)
                    print(f"Queueing ability {ability_number} for unit {ability_unit} with cumulative delay {cumulative_delay}")
            except ValueError:
                continue
    
        # Add wave to appropriate handled set
        if is_custom:
            self.handled_custom_waves.add(wave)
        else:
            self.handled_waves.add(wave)

    def check_custom_ocr(self, settings):
        coords = (int(settings['x1']), int(settings['y1']), int(settings['x2']), int(settings['y2']))
        target_text = settings['text'].lower()

        with mss.mss() as sct:
            monitor = {
                "top": coords[1],
                "left": coords[0],
                "width": coords[2] - coords[0],
                "height": coords[3] - coords[1]
            }
            screenshot = np.array(sct.grab(monitor))

        scale_factor = 2
        dpi = 192 * scale_factor
        screenshot_pil = Image.fromarray(screenshot)
        screenshot_pil.info['dpi'] = (dpi, dpi)
        width = int(screenshot.shape[1] * scale_factor)
        height = int(screenshot.shape[0] * scale_factor)
        screenshot = np.array(screenshot_pil.resize((width, height), Image.LANCZOS))

        all_text, location = self.search_text("", coords, return_all_text=True)
        all_text_lower = [text.lower() for text in all_text]
        print(f"All text found in OCR region: {all_text_lower}")

        for text in all_text_lower:
            if target_text in text:
                print(f"Target text '{target_text}' found")
                return True
    
        print(f"Target text '{target_text}' not found in region")
        return False

    def check_wave_change(self, custom_wave=None):
        wave_region_text = window.evaluate_js("document.getElementById('wave-region-status').textContent")
        wave_format = window.evaluate_js("document.querySelector('.settings-container.sub .dropdown button span').textContent")

        if "Not Set" in wave_region_text:
            print("Wave region not set, skipping wave check")
            return None, self.highest_wave_seen

        # Use custom wave if provided, otherwise use unit waves
        if custom_wave:
            wave_numbers = [custom_wave]
            print(f"Looking for custom wave: {wave_numbers}")
            handled_set = self.handled_custom_waves
        else:
            wave_numbers = window.evaluate_js("""
                Array.from(new Set(
                    Array.from(document.querySelectorAll('.wave-input input, #upgrade-list input[type="text"]:first-of-type, #ability-list input[type="text"]:first-of-type'))
                        .map(input => input.value)
                        .filter(value => value !== '')
                        .map(Number)
                ))
            """)
            print(f"Looking for waves: {wave_numbers}")
            handled_set = self.handled_waves
    
        coords = re.findall(r'X1=(\d+), Y1=(\d+), X2=(\d+), Y2=(\d+)', wave_region_text)[0]
        wave_region = tuple(map(int, coords))
    
        with mss.mss() as sct:
            monitor = {
                "top": wave_region[1],
                "left": wave_region[0],
                "width": wave_region[2] - wave_region[0],
                "height": wave_region[3] - wave_region[1]
            }
            screenshot = np.array(sct.grab(monitor))
    
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
        valid_chars = string.ascii_letters + string.digits + ' '
        filtered_results = []
        for bbox, text, prob in results:
            filtered_text = ''.join(char for char in text if char in valid_chars)
            if filtered_text.strip():
                filtered_results.append((bbox, filtered_text, prob))
    
        all_text = [text.lower() for (_, text, _) in filtered_results]
    
        # Handle split text detection for Wave+Number and Both modes
        if wave_format in ["Wave+Number", "Both"]:
            if "wave" in all_text:
                wave_index = all_text.index("wave")
                for i in range(max(0, wave_index - 1), min(len(all_text), wave_index + 2)):
                    if all_text[i].isdigit():
                        combined_text = f"wave {all_text[i]}"
                        all_text = [combined_text]
                        print(f"Text detected in wave region: {all_text}")
                        break
        
        print(f"Text detected in wave region: {all_text}")
    
        current_wave = None
        for wave_num in wave_numbers:
            wave_str = str(wave_num)
            if wave_format == "Both":
                if any(text.strip() == wave_str for text in all_text) or any(text.strip() == f"wave {wave_str}" for text in all_text):
                    if wave_num not in handled_set:
                        current_wave = wave_num
                        break
            elif wave_format == "Wave+Number":
                if any(text.strip() == f"wave {wave_str}" for text in all_text):
                    if wave_num not in handled_set:
                        current_wave = wave_num
                        break
            elif wave_format == "Number":
                if any(text.strip() == wave_str for text in all_text):
                    if wave_num not in handled_set:
                        current_wave = wave_num
                        break
    
        highest_wave = max([int(num) for num in re.findall(r'\d+', ' '.join(all_text))] or [0])
        if highest_wave > self.highest_wave_seen:
            self.highest_wave_seen = highest_wave
            print(f"New highest wave reached: {self.highest_wave_seen}")
    
        return current_wave, self.highest_wave_seen

    def capture_and_send_screenshot(self, elapsed_time_str):
        # Get replay region from UI to determine which monitor it's on
        replay_region_text = window.evaluate_js("document.getElementById('replay-region-status').textContent")
        coords = re.findall(r'X1=(\d+), Y1=(\d+), X2=(\d+), Y2=(\d+)', replay_region_text)[0]
        replay_x = int(coords[0])
    
        with mss.mss() as sct:
            # Find the correct monitor containing the replay region
            target_monitor = None
            for monitor in sct.monitors[1:]:  # Skip first monitor (combined virtual screen)
                if monitor["left"] <= replay_x < monitor["left"] + monitor["width"]:
                    target_monitor = monitor
                    break
        
            if target_monitor:
                # Capture entire monitor
                screenshot = np.array(sct.grab(target_monitor))
                self.send_discord_webhook(screenshot, elapsed_time_str)
            else:
                print("Could not determine which monitor contains the replay region")

    def send_discord_webhook(self, screenshot, elapsed_time):
        webhook_url = window.evaluate_js("document.querySelector('.settings-container.main .Webhook-input').value")
        if not webhook_url:
            print("Discord webhook URL not set")
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
            print(f"Discord webhook sent successfully. Total runs: {self.total_runs}")
        else:
            print(f"Failed to send Discord webhook. Status code: {response.status_code}")
    
    
    def check_for_replay(self):
        replay_region_text = window.evaluate_js("document.getElementById('replay-region-status').textContent")
        if "Not Set" in replay_region_text:
            print("Replay region not set, skipping replay check")
            return False

        coords = re.findall(r'X1=(\d+), Y1=(\d+), X2=(\d+), Y2=(\d+)', replay_region_text)[0]
        replay_region = tuple(map(int, coords))
    
        with mss.mss() as sct:
            monitor = {
                "top": replay_region[1],
                "left": replay_region[0],
                "width": replay_region[2] - replay_region[0],
                "height": replay_region[3] - replay_region[1]
            }
            screenshot = np.array(sct.grab(monitor))

        scale_factor = 2
        dpi = 192 * scale_factor
        screenshot_pil = Image.fromarray(screenshot)
        screenshot_pil.info['dpi'] = (dpi, dpi)
        width = int(screenshot.shape[1] * scale_factor)
        height = int(screenshot.shape[0] * scale_factor)
        screenshot = np.array(screenshot_pil.resize((width, height), Image.LANCZOS))
    
        replay_text = window.evaluate_js("document.querySelector('.settings-container.replay .file-input').value")
        replay_texts = [text.strip().lower() for text in replay_text.split(',')]
        all_text, location = self.search_text("", replay_region, return_all_text=True)
        all_text_lower = [text.lower() for text in all_text]
        print(f"All text found in replay region: {all_text_lower}")
    
        for replay_text in replay_texts:
            for text in all_text_lower:
                if replay_text in text:
                    print(f"Replay text '{replay_text}' found")
                    time.sleep(0.5)
                    
                    webhook_url = window.evaluate_js("document.querySelector('.settings-container.main .Webhook-input').value")
                    if webhook_url:
                        current_time = time.time()
                        if hasattr(self, 'last_replay_time'):
                            elapsed_time = current_time - self.last_replay_time
                            if elapsed_time >= 60:
                                elapsed_time_str = str(datetime.timedelta(seconds=int(elapsed_time)))
                                self.capture_and_send_screenshot(elapsed_time_str)
                                self.last_replay_time = current_time
                            else:
                                print("Less than 1 minute since last screenshot, skipping image capture")
                        else:
                            self.capture_and_send_screenshot("N/A")
                            self.last_replay_time = current_time
    
                    if self.highest_wave_seen != 0:
                        self.highest_wave_seen = 0
                        print("Highest wave seen reset to 0")
    
                    return True
    
        print(f"Replay text {replay_texts} not found in region")
        return False
    
    def check_for_upgrade(self, upgrade_text):
        upgrade_region_status = window.evaluate_js("document.getElementById('upgrade-region-status').textContent")
        if "Not Set" in upgrade_region_status:
            print("Upgrade region not set, skipping upgrade check")
            return False

        coords = re.findall(r'X1=(\d+), Y1=(\d+), X2=(\d+), Y2=(\d+)', upgrade_region_status)[0]
        upgrade_region = tuple(map(int, coords))

        with mss.mss() as sct:
            monitor = {
                "top": upgrade_region[1],
                "left": upgrade_region[0],
                "width": upgrade_region[2] - upgrade_region[0], 
               "height": upgrade_region[3] - upgrade_region[1]
            }
            screenshot = np.array(sct.grab(monitor))

        scale_factor = 2
        dpi = 192 * scale_factor
        screenshot_pil = Image.fromarray(screenshot)
        screenshot_pil.info['dpi'] = (dpi, dpi)
        width = int(screenshot.shape[1] * scale_factor)
        height = int(screenshot.shape[0] * scale_factor)
        screenshot = np.array(screenshot_pil.resize((width, height), Image.LANCZOS))
    
        upgrade_texts = [text.strip().lower() for text in upgrade_text.split(',') if text.strip()]
        all_text, location = self.search_text("", upgrade_region, return_all_text=True)
        all_text_lower = [text.lower() for text in all_text]
        print(f"All text found in upgrade region: {all_text_lower}")
    
        for upgrade_text in upgrade_texts:
            for text in all_text_lower:
                if upgrade_text in text:
                    print(f"Upgrade text '{upgrade_text}' found")
                    return True
    
        print(f"Upgrade texts {upgrade_texts} not found in region")
        return False

    def search_text(self, text_to_find, region=None, return_text=False, return_all_text=False):
        with mss.mss() as sct:
            if region:
                monitor = {"top": region[1], "left": region[0], "width": region[2] - region[0], "height": region[3] - region[1]}
            else:
                monitor = sct.monitors[0]
            screenshot = np.array(sct.grab(monitor))

        # Process screenshot with OCR
        results = self.reader.readtext(screenshot)
    
        # Filter results to only include valid characters
        valid_chars = string.ascii_letters + string.digits + ' '
        filtered_results = []
        for bbox, text, prob in results:
            filtered_text = ''.join(char for char in text if char in valid_chars)
            filtered_results.append((bbox, filtered_text, prob))
    
        all_text = [text for _, text, _ in filtered_results]
    
        # Check for matching text
        for (bbox, text, prob) in filtered_results:
            if text.lower() == text_to_find.lower():
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

    def get_first_valid_anti_afk_location(self):
        anti_afk_locations = window.evaluate_js("window.antiAfkClickLocations")
        if anti_afk_locations:
            locations = sorted(anti_afk_locations.items(), 
                             key=lambda x: int(''.join(filter(str.isdigit, x[0]))))
        
            for location_num, coords in locations:
                if coords and 'x' in coords and 'y' in coords:
                    return coords['x'], coords['y']
        return None
    
    def upgrade_macro(self, unit_number, upgrade_text, upgrade_number):
        if self.stop_event.is_set():
            return False

        print(f"Attempting upgrade {upgrade_number} for Unit {unit_number}")

        # Check if unit enabled and upgrade not completed
        unit_data = window.evaluate_js(f"""
            document.querySelectorAll('.card')[{unit_number - 1}].querySelector('.checkbox').checked
        """)
        if not unit_data or upgrade_number in self.completed_upgrades.get(unit_number, set()):
            print(f"Unit {unit_number} not placed or upgrade {upgrade_number} already completed")
            return True

        # Get default and completed upgrade texts
        default_upgrade_text = window.evaluate_js("document.getElementById('default-upgrade-text').value")
        completed_upgrade_text = None
        previous_upgrade_number = max(self.completed_upgrades.get(unit_number, set()), default=0)
        if previous_upgrade_number > 0:
            previous_upgrades = window.evaluate_js(f"""
                Array.from(document.querySelectorAll('#upgrade-list .upgrade-item'))
                    .find(item => item.querySelector('p').textContent === 'Upgrade {previous_upgrade_number}' && 
                                 item.querySelector('.dropdown button span').textContent === 'Unit {unit_number}')
                    ?.querySelectorAll('input[type="text"]')[1].value
            """)
            if previous_upgrades:
                completed_upgrade_text = previous_upgrades
    
        # Initialize tracking variables
        check_text = completed_upgrade_text if completed_upgrade_text else default_upgrade_text
        found_initial_text = False
        menu_open = False
        previous_interruption_text = None
        interruption_text = None  # Tracks the most recently seen text in upgrade region
    
        while True:
            if self.stop_event.is_set():
                return False

            # Check for any text in upgrade region
            if menu_open:
                all_text, _ = self.search_text("", self.get_upgrade_region(), return_all_text=True)
                if all_text and len(all_text) > 0:
                    interruption_text = all_text[0]  # Take first text found
                    # Only log if text actually changed
                    if interruption_text != previous_interruption_text:
                        print(f"Updated interruption text to: {interruption_text}")
                        previous_interruption_text = interruption_text
    
            # Handle ability interruptions
            while not self.ability_queue.empty():
                ability_unit, ability_delay, ability_number = self.ability_queue.get()
                if ability_number not in self.completed_abilities:
                    print(f"Pausing upgrade for ability activation")
                    print(f"Current interruption text: {interruption_text}")
                    self.activate_ability(ability_unit, ability_number)
                    found_initial_text = False
                    menu_open = False
                    check_text = interruption_text if interruption_text else check_text
                    continue
    
            # Check for replay
            if self.check_for_replay():
                print("Replay detected, ending upgrade attempt")
                return True
    
            # Handle wave changes
            current_wave, _ = self.check_wave_change()
            if current_wave and current_wave not in self.handled_waves:
                print(f"Wave {current_wave} detected, handling wave first")
                print(f"Current interruption text: {interruption_text}")
                self.handle_wave(current_wave)
                found_initial_text = False
                menu_open = False
                if interruption_text:
                    check_text = interruption_text
                    print(f"Resuming with interruption text: {check_text}")
                continue
    
            # Initial text finding phase
            if not found_initial_text:
                unit_click_location = window.evaluate_js(f"""
                    document.querySelectorAll('.card')[{unit_number - 1}].querySelector('.click-location').textContent
                """)
                
                if "not set" not in unit_click_location.lower():
                    coords = re.findall(r'X=(\d+), Y=(\d+)', unit_click_location)[0]
                    unit_x, unit_y = map(int, coords)
                    pydirectinput.moveTo(unit_x, unit_y - 18)
                    time.sleep(0.025)
                    pydirectinput.moveTo(unit_x, unit_y - 19)
                    time.sleep(0.025)
                    pydirectinput.click(unit_x, unit_y - 20)
                    time.sleep(1.5)
    
                    if self.check_for_upgrade(check_text):
                        found_initial_text = True
                        menu_open = True
                        print(f"Menu opened, found initial text: {check_text}")
                        continue
    
            # Upgrade phase
            elif menu_open:
                upgrade_click_status = window.evaluate_js("document.getElementById('upgrade-click-status').textContent")
                if "Not Set" not in upgrade_click_status:
                    coords = re.findall(r'X=(\d+), Y=(\d+)', upgrade_click_status)[0]
                    upgrade_x, upgrade_y = map(int, coords)
        
                    pydirectinput.moveTo(upgrade_x, upgrade_y)
                    time.sleep(0.025)
                    pydirectinput.moveTo(upgrade_x, upgrade_y - 1)
                    time.sleep(0.025)
                    pydirectinput.click(upgrade_x, upgrade_y - 1)
                    time.sleep(0.25)
    
                    if self.check_for_upgrade(upgrade_text):
                        self.completed_upgrades.setdefault(unit_number, set()).add(upgrade_number)
                        print(f"Unit {unit_number} successfully upgraded to level {upgrade_number}")
                            
                        coords = self.get_first_valid_anti_afk_location()
                        if coords:
                            x, y = coords
                            pydirectinput.moveTo(x, y)
                            time.sleep(0.025)
                            pydirectinput.moveTo(x, y - 1)
                            time.sleep(0.025)
                            pydirectinput.click(x, y - 2)
                            print("Anti-AFK click performed after upgrade using first valid location")
                        return True
    
            time.sleep(0.1)

    def get_upgrade_region(self):
        upgrade_region_text = window.evaluate_js("document.getElementById('upgrade-region-status').textContent")
        if "Not Set" not in upgrade_region_text:
            coords = re.findall(r'X1=(\d+), Y1=(\d+), X2=(\d+), Y2=(\d+)', upgrade_region_text)[0]
            return tuple(map(int, coords))
        return None

    def activate_ability(self, ability_unit, ability_number):
        if self.stop_event.is_set():
            return False

        if ability_number in self.completed_abilities:
            return True

        print(f"Attempting ability {ability_number} for Unit {ability_unit}")

        unit_data = window.evaluate_js(f"""
            document.querySelectorAll('.card')[{ability_unit - 1}].querySelector('.checkbox').checked
        """)
    
        if unit_data:
            unit_click_location = window.evaluate_js(f"""
                document.querySelectorAll('.card')[{ability_unit - 1}].querySelector('.click-location').textContent
            """)
        
            if "not set" not in unit_click_location.lower():
                coords = re.findall(r'X=(\d+), Y=(\d+)', unit_click_location)[0]
                unit_x, unit_y = map(int, coords)
                pydirectinput.moveTo(unit_x, unit_y - 18)
                time.sleep(0.025)
                pydirectinput.moveTo(unit_x, unit_y - 19)
                time.sleep(0.025)
                pydirectinput.click(unit_x, unit_y - 20)
                time.sleep(0.025)
    
                ability_click_status = window.evaluate_js("document.getElementById('ability-click-status').textContent")
                if "Not Set" not in ability_click_status:
                    coords = re.findall(r'X=(\d+), Y=(\d+)', ability_click_status)[0]
                    ability_x, ability_y = map(int, coords)
                    pydirectinput.moveTo(ability_x, ability_y)
                    time.sleep(0.025)
                    pydirectinput.moveTo(ability_x, ability_y - 1)
                    time.sleep(0.025)
                    pydirectinput.click(ability_x, ability_y - 2)
                    time.sleep(0.250)
    
                    coords = self.get_first_valid_anti_afk_location()
                    if coords:
                        x, y = coords
                        pydirectinput.moveTo(x, y)
                        time.sleep(0.025)
                        pydirectinput.moveTo(x, y - 1)
                        time.sleep(0.025)
                        pydirectinput.click(x, y - 2)
                        print("Anti-AFK click performed after ability using first valid location")
                        time.sleep(0.50)
    
                    self.completed_abilities.setdefault(ability_unit, set()).add(ability_number)
                    print(f"Unit {ability_unit} successfully activated ability {ability_number}")

    def replay_macro(self):
        replay_click_status = window.evaluate_js("document.getElementById('replay-click-status').textContent")

        if "Not Set" not in replay_click_status:
            coords = re.findall(r'X=(\d+), Y=(\d+)', replay_click_status)[0]
            x, y = map(int, coords)

            # Keep clicking replay until it's no longer detected
            while self.check_for_replay():
                pydirectinput.moveTo(x, y)
                time.sleep(0.025)
                pydirectinput.moveTo(x, y - 1)
                time.sleep(0.025)
                pydirectinput.click(x, y - 2)
                time.sleep(2)

            # Check if custom macro is enabled and set to run on replay
            custom_settings = window.evaluate_js("""
                ({
                    enabled: document.querySelector('#custom .checkbox').checked,
                    onReplay: document.getElementById('onReplayCheck').checked
                })
            """)

            # Execute custom macro sequence in a thread if enabled and set to run on replay
            if custom_settings['enabled'] and custom_settings['onReplay']:
                print("Running custom macro sequence on replay")
                threading.Thread(target=lambda: ExecuteMacro(self).run_macro_sequence(), daemon=True).start()

            # Reset all tracking variables
            self.completed_upgrades = {}
            self.completed_abilities = {}
            self.completed_placements = set()
            self.handled_waves.clear()
            self.handled_custom_waves.clear()
            self.current_upgrade_text = None

            # Clear all queues
            while not self.upgrade_queue.empty():
                self.upgrade_queue.get()
            while not self.ability_queue.empty():
                self.ability_queue.get()
            while not self.placement_queue.empty():
                self.placement_queue.get()
            
            self.current_upgrade = None
            print("Replay macro executed and all tracking variables reset")
            return True
        return False

    def anti_afk_macro(self):
        # Get all saved anti-afk locations from the window's antiAfkClickLocations object
        anti_afk_locations = window.evaluate_js("window.antiAfkClickLocations")
    
        if anti_afk_locations:
            # Extract number from location string and sort
            locations = sorted(anti_afk_locations.items(), 
                             key=lambda x: int(''.join(filter(str.isdigit, x[0]))))
        
            for location_num, coords in locations:
                # Skip if coordinates aren't properly set
                if not coords or 'x' not in coords or 'y' not in coords:
                    continue
                
                x, y = coords['x'], coords['y']
                pydirectinput.moveTo(x, y)
                time.sleep(0.025)
                pydirectinput.moveTo(x, y - 1)
                time.sleep(0.025)
                pydirectinput.click(x, y - 2)
                print(f"Anti-AFK macro executed for location {location_num}")
                time.sleep(0.1)
            
            return True
        
        return False

    def place_macro(self, unit_number):
        if self.stop_event.is_set():
            return False
    
        if unit_number in self.completed_placements:
            return True

        unit_data = window.evaluate_js(f"""
            (function() {{
                const card = document.querySelectorAll('.card')[{unit_number - 1}];
                return {{
                    slot: card.querySelector('.dropdown button span').textContent,
                    delay: card.querySelector('.delay-input input').value,
                    location: card.querySelector('.click-location').textContent
                }};
            }})();
        """)

        slot_number = unit_data['slot'].replace('Unit slot ', '')
        keyboard.press_and_release(slot_number)
        print(f"Pressed key: {slot_number} for Unit {unit_number}")
    
        sleep_time = float(unit_data['delay'])
        time.sleep(sleep_time)
    
        coords = re.findall(r'X=(\d+), Y=(\d+)', unit_data['location'])[0]
        click_x, click_y = map(int, coords)
        pydirectinput.moveTo(click_x, click_y)
        time.sleep(0.025)
        pydirectinput.moveTo(click_x, click_y - 1)
        time.sleep(0.025)
        pydirectinput.click(click_x, click_y - 2)
        print(f"Placed Unit {unit_number} using slot {slot_number}")
        
        self.completed_placements.add(unit_number)
        return True

    def save_config(self, filename, data):
        config_path = os.path.join("configs", filename, "config.json")
        config_data = json.loads(data)
    
        with open(config_path, "w") as f:
            json.dump(config_data, f, indent=4)
    
        print(f"Config saved to: {config_path}")

    def load_config(self, filename):
        config_path = os.path.join("configs", filename, "config.json")
        try:
            with open(config_path, "r") as f:
                config_data = json.load(f)
                print(f"Config loaded from: {config_path}")
            
                # Set up keyboard bindings if they exist in config
                if isinstance(config_data, dict) and 'macroKeys' in config_data:
                    start_key = config_data['macroKeys'].get('startKey')
                    stop_key = config_data['macroKeys'].get('stopKey')
                
                    if start_key:
                        self.set_keyboard_binding(start_key, 'Start Macro Key')
                    if stop_key:
                        self.set_keyboard_binding(stop_key, 'Stop Macro Key')
            
                if not isinstance(config_data, dict):
                    config_data = {
                        "units": config_data,
                        "upgrades": {
                            "numberOfUpgrades": "0",
                            "upgradeRegionStatus": "Upgrade Region: Not Set",
                            "upgradeClickStatus": "Upgrade Click Location: Not Set",
                            "upgrades": []
                        },
                        "abilities": {
                            "numberOfAbilities": "0",
                            "abilityClickStatus": "Ability Click Location: Not Set",
                            "abilities": []
                        },
                        "replay": {
                            "replayRegionStatus": "Replay Region: Not Set",
                            "replayClickStatus": "Click Location: Not Set",
                            "replayText": ""
                        },
                        "antiAfk": {
                            "antiAfkClickStatus": "Click Location: Not Set"
                        }
                    }
                return json.dumps(config_data)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            return json.dumps({
                "units": [],
                "upgrades": {
                    "numberOfUpgrades": "0",
                    "upgradeRegionStatus": "Upgrade Region: Not Set",
                    "upgradeClickStatus": "Upgrade Click Location: Not Set",
                    "upgrades": []
                },
                "abilities": {
                    "numberOfAbilities": "0",
                    "abilityClickStatus": "Ability Click Location: Not Set",
                    "abilities": []
                },
                "replay": {
                    "replayRegionStatus": "Replay Region: Not Set",
                    "replayClickStatus": "Click Location: Not Set",
                    "replayText": ""
                },
                "antiAfk": {
                    "antiAfkClickStatus": "Click Location: Not Set"
                }
            })

    def save_webhook(self, filename, webhook_url):
        webhook_path = os.path.join("configs", filename, "webhook.json")
        with open(webhook_path, "w") as f:
            json.dump({"webhook": webhook_url}, f, indent=4)
        print(f"Webhook saved to: {webhook_path}")

    def load_webhook(self, filename):
        webhook_path = os.path.join("configs", filename, "webhook.json")
        try:
            with open(webhook_path, "r") as f:
                webhook_data = json.load(f)
                return webhook_data.get("webhook", "")
        except FileNotFoundError:
            print(f"Webhook file not found: {webhook_path}")
            return ""

    def create_config(self):
        js_code = """ 
            (function() { 
                const fileInput = document.querySelector('.settings-container.main .file-input'); 
                const webhookInput = document.querySelector('.settings-container.main .Webhook-input'); 
                return { 
                    fileName: fileInput.value, 
                    webhook: webhookInput.value 
                }; 
            })(); 
        """ 
        result = window.evaluate_js(js_code)
    
        if result['fileName']:
            config_dir = os.path.join("configs", result['fileName'])
            os.makedirs(config_dir, exist_ok=True)

            # Create config.json 
            config_path = os.path.join(config_dir, "config.json")
            with open(config_path, "w") as f:
                json.dump({}, f, indent=4)

            # Create webhook.json 
            webhook_path = os.path.join(config_dir, "webhook.json")
            with open(webhook_path, "w") as f:
                json.dump({"webhook": result['webhook']}, f, indent=4)
    
            # Immediately update the dropdown
            config_files = [d for d in os.listdir("configs") if os.path.isdir(os.path.join("configs", d))]
            js_update_code = f""" 
                const settingsDropdown = document.querySelector('.settings-container.main .dropdown-menu');
                const fileList = {config_files};
                settingsDropdown.innerHTML = fileList.map(file => 
                    `<li><a class="dropdown-item" href="#" onclick="selectSettingsFile(event)" style="color: #c9d1d9; display: block; padding: 8px 10px; text-decoration: none; text-align: left;">${{file}}</a></li>`
                ).join('');
            """
            window.evaluate_js(js_update_code)
    
            # Show success dialog
            window.evaluate_js(f""" 
                createDialog('Configuration "{result['fileName']}" created successfully', [{{ 
                    'text': 'OK', 'action': null 
                }}]); 
            """)
        else:
            # Show error dialog if no filename is entered
            window.evaluate_js(""" 
                createDialog('Please enter a file name', [{ 
                    'text': 'OK', 'action': null 
                }]); 
            """)
            
    def get_click_location(self, element_id, is_unit_card=False, location_number=None):
        def handle_click(coords):
            if element_id == 'click-location-status':
                # Update x and y input boxes in Move and Click dialog
                js_code = f"""
                    document.getElementById('click-x').value = '{coords[0]}';
                    document.getElementById('click-y').value = '{coords[1]}';
                """
                window.evaluate_js(js_code)
            elif 'anti-afk-click-status' in element_id:
                location_num = element_id.split('-')[-1]
                js_save_coords = f"""
                    if (!window.antiAfkClickLocations) {{
                        window.antiAfkClickLocations = {{}};
                    }}
                    window.antiAfkClickLocations['{location_num}'] = {{
                        x: {coords[0]},
                        y: {coords[1]}
                    }};
                """
                window.evaluate_js(js_save_coords)
                
                js_update_status = f"""
                    const statusElement = document.getElementById('anti-afk-click-status-1');
                    if (statusElement) {{
                        statusElement.textContent = 'Click Location {location_num}: X={coords[0]}, Y={coords[1]}';
                    }}
                """
                window.evaluate_js(js_update_status)
            elif is_unit_card:
                js_code = f"""
                    const element = document.getElementById('{element_id}');
                    if (element) {{
                        element.innerText = 'X={coords[0]}, Y={coords[1]}';
                    }}
                """
                window.evaluate_js(js_code)
            else:
                js_code = f"""
                    const element = document.getElementById('{element_id}');
                    if (element) {{
                        element.innerText = 'Click location: X={coords[0]}, Y={coords[1]}';
                    }}
                """
                window.evaluate_js(js_code)
                   
        overlay = TransparentOverlay(window, handle_click)


    def close_window(self):
        window.destroy()
    
    def minimize_window(self):
        window.minimize()

    def set_ocr_region(self):
        def handle_region(coords):
            x1, y1, x2, y2 = coords
            js_code = f"""
                document.getElementById('ocr-x1').value = '{x1}';
                document.getElementById('ocr-y1').value = '{y1}';
                document.getElementById('ocr-x2').value = '{x2}';
                document.getElementById('ocr-y2').value = '{y2}';
            """
            window.evaluate_js(js_code)
    
        overlay = TransparentOverlay(window, handle_region, region_select=True)


    def set_replay_region(self):
        def handle_region(coords):
            js_code = f"""
                const element = document.getElementById('replay-region-status');
                if (element) {{
                    element.innerText = 'Replay Region: X1={coords[0]}, Y1={coords[1]}, X2={coords[2]}, Y2={coords[3]}';
                }}
            """
            window.evaluate_js(js_code)
        
        overlay = TransparentOverlay(window, handle_region, region_select=True)

    def set_upgrade_region(self):
        def handle_region(coords):
            js_code = f"""
                const element = document.getElementById('upgrade-region-status');
                if (element) {{
                    element.innerText = 'Upgrade Region: X1={coords[0]}, Y1={coords[1]}, X2={coords[2]}, Y2={coords[3]}';
                }}
            """
            window.evaluate_js(js_code)
    
        overlay = TransparentOverlay(window, handle_region, region_select=True)

    def set_wave_region(self):
        def handle_region(coords):
            js_code = f"""
                const element = document.getElementById('wave-region-status');
                if (element) {{
                    element.innerText = 'Wave Region: X1={coords[0]}, Y1={coords[1]}, X2={coords[2]}, Y2={coords[3]}';
                }}
            """
            window.evaluate_js(js_code)
        
        overlay = TransparentOverlay(window, handle_region, region_select=True)

    def update_logs(self, log_text):
        escaped_text = log_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')

        js_code = f"""
            const logContent = document.getElementById("log-content");
            const logsTab = document.getElementById("logs");
            const logContainer = document.querySelector(".log-container");

            const wasHidden = logsTab.classList.contains('hidden');
            if (wasHidden) {{
                logsTab.classList.remove('hidden');
            }}

            // Store current scroll position and max scroll
            const currentScroll = logContainer.scrollTop;
            const maxScroll = logContainer.scrollHeight - logContainer.clientHeight;
        
            // Check if user is actively scrolling (within 75px of current position)
            const isUserScrolling = maxScroll - currentScroll > 75;

            let messages = logContent.innerText.split("\\n")
                .map(msg => msg.trim())
                .filter(msg => msg.length > 0);
            
            if (messages.length > 250) {{
                messages = messages.slice(-250);
            }}
        
            messages.push(`{escaped_text}`);
    
            logContent.innerText = messages.join("\\n");
            logContent.style.paddingLeft = "15px";
            logContent.style.paddingRight = "15px";
            logContent.style.paddingTop = "15px";
    
            // Only auto-scroll if user isn't actively scrolling
            if (!isUserScrolling) {{
                requestAnimationFrame(() => {{
                    logContainer.scrollTop = logContainer.scrollHeight;
                }});
            }}
    
            if (wasHidden) {{
                logsTab.classList.add('hidden');
            }}
        """
        window.evaluate_js(js_code)

    def upload_to_github(self, folder_path):
        try:
            # Get folder name
            folder_name = os.path.basename(folder_path)

            # Check if the folder already exists on GitHub
            existing_folders = self.fetch_github_files()
            if any(folder['name'] == folder_name for folder in existing_folders):
                # Show a dialog to inform the user
                window.evaluate_js(f""" 
                    createDialog('The folder "{folder_name}" already exists on GitHub. Skipping upload. Rename To Upload', [{{ 
                        'text': 'OK', 'action': null 
                    }}]); 
                """)

                # Update the upload status
                window.evaluate_js(f""" 
                    document.getElementById('upload-progress').style.width = '0%'; 
                   document.getElementById('upload-status').textContent = 'Skipping upload'; 
                """)
                return  # Skip the upload
    
            # Update the status before starting the upload
            window.evaluate_js(f""" 
                document.getElementById('upload-progress').style.width = '0%'; 
                document.getElementById('upload-status').textContent = 'Starting upload...'; 
            """)
    
            # Get the text from the entry box
            info_text = window.evaluate_js(""" 
                document.querySelector('#upload textarea').value; 
            """)
    
            # Create info.json file
            info_json_path = os.path.join(folder_path, "info.json")
            with open(info_json_path, 'w') as f:
                json.dump({"description": info_text}, f, indent=4)
    
            # Get all files in the selected folder
            files_to_upload = []
            # Add info.json as first file to upload
            files_to_upload.append((info_json_path, f"{folder_name}/info.json"))
    
            # Add remaining files, skipping webhook.json
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    if file != "info.json" and file != "webhook.json":  # Skip info.json and webhook.json
                        full_path = os.path.join(root, file)
                        relative_path = os.path.join(folder_name, file).replace(os.path.sep, '/')
                        files_to_upload.append((full_path, relative_path))
    
            total_files = len(files_to_upload)
    
            for index, (full_path, relative_path) in enumerate(files_to_upload):
                self.upload_single_file(full_path, relative_path)
                progress = ((index + 1) / total_files) * 100
    
                # Update progress in UI
                window.evaluate_js(f""" 
                    document.getElementById('upload-progress').style.width = '{progress}%'; 
                    document.getElementById('upload-status').textContent = 'Uploaded {index + 1}/{total_files} files'; 
                """)
    
            # Remove the temporary info.json if it didn't exist before
            if not os.path.exists(info_json_path):
                os.remove(info_json_path)
    
            window.evaluate_js(""" 
                document.getElementById('upload-status').textContent = 'Upload completed successfully! '; 
            """)
    
        except Exception as e:
            window.evaluate_js(f""" 
                document.getElementById('upload-status').textContent = 'Error: {str(e)}'; 
            """)

    def upload_single_file(self, full_path, relative_path):
        try:
            with open(full_path, 'rb') as file:
                file_content = file.read()
    
            payload = {
                'filename': relative_path,
                'content': base64.b64encode(file_content).decode('utf-8')
            }
    
            response = requests.post("https://wavebound-uploader.onrender.com/upload", json=payload)
            if response.status_code != 200:
                raise Exception(f"Failed to upload {relative_path}: {response.text}")
    
        except Exception as e:
            print(f"Error uploading {relative_path}: {str(e)}")

    def select_upload_folder(self):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        selected_path = filedialog.askdirectory()
        root.destroy()
    
        if selected_path:
            window.evaluate_js(f"""
                document.getElementById('selected-folder').textContent = '{selected_path}';
            """)
            return selected_path

    def fetch_github_files(self):
        repo_owner = "WaveBound"
        repo_name = "WaveBound_Configs"
        path = "Configs"
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    
        try:
            response = requests.get(url)
            if response.status_code == 200:
                files = response.json()
                return files
            return []
        except:
            return []

    def get_config_info(self, file_details):
        try:
            url = file_details['url']
            response = requests.get(url)
            response.raise_for_status()
            items = response.json()

            # Look for info.json 
            info_file = next((item for item in items if item['name'] == 'info.json'), None)

            if info_file and 'download_url' in info_file:
                info_response = requests.get(info_file['download_url'])
                info_response.raise_for_status()
                info_data = info_response.json()
                description = info_data.get('description', 'No description available')
            
                # If description is empty, return the default message
                return description if description.strip() else 'No description available'

            return 'No description available'

        except Exception as e:
            return f'Error fetching config info: {str(e)}'


    def download_github_file(self, file_details):
        try:
            url = file_details['url']
            response = requests.get(url)
            response.raise_for_status()
            items = response.json()

            # Create folder in configs directory
            folder_name = os.path.join("configs", file_details['name'])
            os.makedirs(folder_name, exist_ok=True)

            if isinstance(items, list):
                for item in items:
                    if 'download_url' in item and item['download_url']:
                        file_response = requests.get(item['download_url'])
                        file_response.raise_for_status()
                        
                        filepath = os.path.join(folder_name, item['name'])
                        with open(filepath, 'wb') as f:
                            f.write(file_response.content)
                        print(f"Downloaded: {item['name']} to {folder_name}")
            
            elif 'download_url' in items and items['download_url']:
                filepath = os.path.join(folder_name, items['name'])
                file_response = requests.get(items['download_url'])
                file_response.raise_for_status()
                
                with open(filepath, 'wb') as f:
                    f.write(file_response.content)
                print(f"Downloaded: {items['name']} to {folder_name}")
    
            window.evaluate_js(f"""
                document.getElementById('download-status').textContent = 'Successfully downloaded {file_details["name"]}';
            """)
            
        except Exception as e:
            window.evaluate_js(f"""
                document.getElementById('download-status').textContent = 'Error downloading file: {str(e)}';
            """)
            
if __name__ == '__main__':
    api = Api()
    window = webview.create_window("WaveBound", html=html_content, width=975, height=825, frameless=True, js_api=api)
    sys.stdout = LogRedirect(api)
    sys.stderr = LogRedirect(api)  # This captures error logs too
    webview.start()
