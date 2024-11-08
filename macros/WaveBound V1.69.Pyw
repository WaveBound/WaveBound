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
                <textarea placeholder="Enter text here..." style="width: 100%; height: 525px; padding: 8px; background-color: #0d1117; border: 1px solid #30363d; border-radius: 3px; color: #c9d1d9; margin-bottom: 15px; resize: none; font-family: inherit;"></textarea>
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
                        <div style="display: flex; align-items: center;">
                            <p style="margin-right: 10px;">Number of Upgrades:</p>
                            <input type="text" id="upgrade-number" style="
                                height: 35px;
                                font-size: 16px;
                                font-weight: bold;
                                width: 75px;">
                            <button class="button" onclick="setUpgrades()" style="margin-left: 10px; padding: 10px 20px;">Set Upgrades</button>
                            <button class="button" onclick="setUpgradeRegion()" style="margin-left: 10px; padding: 10px 20px;">Set Upgrade Region</button>
                            <button class="button" onclick="setUpgradeClickLocation()" style="margin-left: 10px; padding: 10px 20px;">Set Upgrade Click Location</button>
                        </div>
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
                            <input type="text" id="ability-number" style="
                                height: 35px;
                                font-size: 16px;
                                font-weight: bold;
                                width: 75px;">
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
            <h2 class="settings-title">Anti-AFK</h2>
            <div class="main-content" style="padding-top: 20px;">
                <button class="button" onclick="setAntiAfkClickLocation()">Set Anti-AFK Click Location</button>
                <span id="anti-afk-click-status" style="color: #58a6ff; padding-top: 2px;">Click Location: Not Set</span>
            </div>
        </div>
        <div class="settings-container sub" style="margin-top: 20px;">
            <h2 class="settings-title">Wave</h2>
            <div class="main-content" style="padding-top: 20px;">
                <button class="button" onclick="setWaveRegion()">Set Wave Region</button>
                <span id="wave-region-status" style="color: #58a6ff; padding-top: 2px;">Wave Region: Not Set</span>
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

function showConfigInfo(file) {
    pywebview.api.get_config_info(file).then(description => {
        createInfoDialog(description, [
            {text: 'OK', action: null}
        ]);
    });
}

function createInfoDialog(message, buttons) {
    const dialog = document.createElement('div');
    dialog.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #1b1f23;
        padding: 20px;
        border-radius: 5px;
        z-index: 1000;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        min-width: 300px;
        max-width: 600px;
        max-height: 400px;
        overflow-y: auto; /* Enable scrolling */
    `;

    const messageElement = document.createElement('pre'); // Use <pre> for preserving whitespace
    messageElement.textContent = message; // Set text content
    messageElement.style.cssText = `
        color: #c9d1d9;
        margin: 0 0 20px 0;
        text-align: left; /* Align text to the left */
        font-weight: bold; /* Make text bold */
        font-family: Arial, sans-serif; /* Match the font style */
    `;

    const buttonContainer = document.createElement('div');
    buttonContainer.style.cssText = `
        display: flex;
        justify-content: center;
        gap: 10px;
    `;

    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
    `;

    buttons.forEach(({ text, action }) => {
        const button = document.createElement('button');
        button.textContent = text;
        button.style.cssText = `
            background-color: #1b1f23;
            color: #c9d1d9;
            border: 1px solid #30363d;
            padding: 5px 15px;
            cursor: pointer;
            border-radius: 3px;
            font-weight: bold; /* Make button text bold */
            font-family: Arial, sans-serif; /* Match the font style */
            min-width: 60px;
            transition: background-color 0.3s, color 0.3s;
        `;

        button.onmouseover = () => {
            button.style.backgroundColor = '#58a6ff';
            button.style.color = '#0d1117';
        };

        button.onmouseout = () => {
            button.style.backgroundColor = '#1b1f23';
            button.style.color = '#c9d1d9';
        };

        button.onclick = () => {
            document.body.removeChild(overlay);
            document.body.removeChild(dialog);
            if (action) action();
        };

        buttonContainer.appendChild(button);
    });

    dialog.appendChild(messageElement);
    dialog.appendChild(buttonContainer);
    document.body.appendChild(overlay);
    document.body.appendChild(dialog);
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

function toggleSettingsDropdown(event) {
    const dropdownContainer = event.target.closest('.dropdown');
    const dropdownMenu = dropdownContainer.querySelector('.dropdown-menu');
    
    // Get the button's position
    const buttonRect = dropdownContainer.getBoundingClientRect();

    // Position the dropdown menu
    dropdownMenu.style.position = 'fixed';  // Changed to fixed positioning
    dropdownMenu.style.width = `${buttonRect.width}px`;
    dropdownMenu.style.left = `${buttonRect.left}px`;
    dropdownMenu.style.top = `${buttonRect.bottom}px`;  // Position directly under the button
    dropdownMenu.style.maxHeight = '200px';  // Fixed height

    // Toggle visibility
    dropdownMenu.style.display = dropdownMenu.style.display === 'none' ? 'block' : 'none';

    // Add click outside listener to close dropdown
    if (dropdownMenu.style.display === 'block') {
        setTimeout(() => {
            window.addEventListener('click', function closeDropdown(e) {
                if (!dropdownContainer.contains(e.target)) {
                    dropdownMenu.style.display = 'none';
                    window.removeEventListener('click', closeDropdown);
                }
            });
        }, 0);
    }
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
    event.target.closest('.dropdown-menu').style.display = 'none';
}

let logsScrollPosition = 0;

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

function toggleDropdown(event) {
    const dropdownContainer = event.target.closest('.dropdown');
    const dropdownMenu = dropdownContainer.querySelector('.dropdown-menu');
    const scrollableContainer = document.querySelector('#upgrade-list.scrollable-container');
    
    // Get the necessary measurements
    const buttonRect = dropdownContainer.getBoundingClientRect();
    const windowHeight = window.innerHeight;
    const scrollTop = scrollableContainer.scrollTop;

    // Calculate available space within the window
    const spaceBelow = windowHeight - buttonRect.bottom;
    const spaceAbove = buttonRect.top;
    const dropdownHeight = 204;

    // Position the dropdown menu
    dropdownMenu.style.position = 'fixed';
    dropdownMenu.style.width = `${buttonRect.width}px`;
    dropdownMenu.style.left = `${buttonRect.left}px`;

    // Determine whether to show above or below
    if (spaceBelow >= dropdownHeight || spaceBelow > spaceAbove) {
        dropdownMenu.style.top = `${buttonRect.bottom}px`;
        dropdownMenu.style.maxHeight = `${Math.min(dropdownHeight, spaceBelow)}px`;
    } else {
        dropdownMenu.style.top = `${buttonRect.top - Math.min(dropdownHeight, spaceAbove)}px`;
        dropdownMenu.style.maxHeight = `${Math.min(dropdownHeight, spaceAbove)}px`;
    }

    // Toggle visibility
    dropdownMenu.style.display = dropdownMenu.style.display === 'none' ? 'block' : 'none';

    // Add click outside listener
    if (dropdownMenu.style.display === 'block') {
        setTimeout(() => {
            window.addEventListener('click', function closeDropdown(e) {
                if (!dropdownContainer.contains(e.target)) {
                    dropdownMenu.style.display = 'none';
                    window.removeEventListener('click', closeDropdown);
                }
            });
        }, 0);
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

function toggleAbilityDropdown(event) {
    const dropdownContainer = event.target.closest('.dropdown');
    const dropdownMenu = dropdownContainer.querySelector('.dropdown-menu');
    const scrollableContainer = document.querySelector('#ability-list.scrollable-container');
    
    // Get the necessary measurements
    const buttonRect = dropdownContainer.getBoundingClientRect();
    const windowHeight = window.innerHeight;
    const scrollTop = scrollableContainer.scrollTop;

    // Calculate available space within the window
    const spaceBelow = windowHeight - buttonRect.bottom;
    const spaceAbove = buttonRect.top;
    const dropdownHeight = 204;

    // Position the dropdown menu
    dropdownMenu.style.position = 'fixed';
    dropdownMenu.style.width = `${buttonRect.width}px`;
    dropdownMenu.style.left = `${buttonRect.left}px`;

    // Determine whether to show above or below
    if (spaceBelow >= dropdownHeight || spaceBelow > spaceAbove) {
        dropdownMenu.style.top = `${buttonRect.bottom}px`;
        dropdownMenu.style.maxHeight = `${Math.min(dropdownHeight, spaceBelow)}px`;
    } else {
        dropdownMenu.style.top = `${buttonRect.top - Math.min(dropdownHeight, spaceAbove)}px`;
        dropdownMenu.style.maxHeight = `${Math.min(dropdownHeight, spaceAbove)}px`;
    }

    // Toggle visibility
    dropdownMenu.style.display = dropdownMenu.style.display === 'none' ? 'block' : 'none';

    // Add click outside listener
    if (dropdownMenu.style.display === 'block') {
        setTimeout(() => {
            window.addEventListener('click', function closeDropdown(e) {
                if (!dropdownContainer.contains(e.target)) {
                    dropdownMenu.style.display = 'none';
                    window.removeEventListener('click', closeDropdown);
                }
            });
        }, 0);
    }
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
    
    function handleKeyPress(e) {
        e.preventDefault();
        const keyPressed = e.key.toUpperCase();
        button.textContent = keyPressed;
        
        // Log the button press
        pywebview.api.log_key_binding(button.previousElementSibling.textContent.replace(':', ''), keyPressed);
        
        // Add keyboard hotkey
        pywebview.api.set_keyboard_binding(keyPressed, button.previousElementSibling.textContent.replace(':', ''));
        
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
    pywebview.api.get_click_location('anti-afk-click-status');
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

function toggleUnitDropdown(event) {
    const dropdownContainer = event.target.closest('.dropdown');
    const dropdownMenu = dropdownContainer.querySelector('.dropdown-menu');
    
    dropdownMenu.style.display = dropdownMenu.style.display === 'none' ? 'block' : 'none';

    if (dropdownMenu.style.display === 'block') {
        setTimeout(() => {
            window.addEventListener('click', function closeDropdown(e) {
                if (!dropdownContainer.contains(e.target)) {
                    dropdownMenu.style.display = 'none';
                    window.removeEventListener('click', closeDropdown);
                }
            });
        }, 0);
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

function createDialog(message, buttons) {
    const dialog = document.createElement('div');
    dialog.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: #1b1f23;
        padding: 20px;
        border-radius: 5px;
        z-index: 1000;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        min-width: 300px;
    `;

    const messageElement = document.createElement('p');
    messageElement.textContent = message;
    messageElement.style.cssText = `
        color: #c9d1d9;
        margin: 0 0 20px 0;
        text-align: center;
        font-weight: bold;
    `;

    const buttonContainer = document.createElement('div');
    buttonContainer.style.cssText = `
        display: flex;
        justify-content: center;
        gap: 10px;
    `;

    const overlay = document.createElement('div');
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        z-index: 999;
    `;

    buttons.forEach(({text, action}) => {
        const button = document.createElement('button');
        button.textContent = text;
        button.style.cssText = `
            background-color: #1b1f23;
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
            button.style.backgroundColor = '#1b1f23';
            button.style.color = '#c9d1d9';
        };

        button.onclick = () => {
            document.body.removeChild(overlay);
            document.body.removeChild(dialog);
            if (action) action();
        };

        buttonContainer.appendChild(button);
    });

    dialog.appendChild(messageElement);
    dialog.appendChild(buttonContainer);
    document.body.appendChild(overlay);
    document.body.appendChild(dialog);
}


function saveConfig() {
    const selectedFile = document.querySelector('.settings-container.main .dropdown button span').textContent;
    
    if (selectedFile === 'Select a file...') {
        createDialog('No File Selected. Select A File', [
            {text: 'OK', action: null}
        ]);
        return;
    }

    // Save webhook separately
    const webhookUrl = document.querySelector('.settings-container.main .Webhook-input').value;
    pywebview.api.save_webhook(selectedFile, webhookUrl);

    // Get unit data
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

    // Get upgrade data
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

    // Get ability data
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

    // Get replay data
    const replayData = {
        replayRegionStatus: document.getElementById('replay-region-status').textContent,
        replayClickStatus: document.getElementById('replay-click-status').textContent,
        replayText: document.querySelector('.settings-container.replay .file-input').value
    };

    // Get anti-afk data
    const antiAfkData = {
        antiAfkClickStatus: document.getElementById('anti-afk-click-status').textContent
    };

    const configData = {
        units: unitData,
        upgrades: upgradeData,
        abilities: abilityData,
        replay: replayData,
        antiAfk: antiAfkData,
    wave: {
        waveRegionStatus: document.getElementById('wave-region-status').textContent
    },
    macroKeys: {
        startKey: document.querySelector('.main-row:nth-child(3) .button').textContent,
        stopKey: document.querySelector('.main-row:nth-child(4) .button').textContent
    }
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

    // Load webhook data
    pywebview.api.load_webhook(selectedFile).then(webhookUrl => {
        document.querySelector('.settings-container.main .Webhook-input').value = webhookUrl;
    });    

    pywebview.api.load_config(selectedFile).then(data => {
        const config = JSON.parse(data);
        
        // Load unit data
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

        // Load upgrade data
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

        // Load ability data
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

        // Load replay data
        if (config.replay) {
            document.getElementById('replay-region-status').textContent = config.replay.replayRegionStatus || 'Replay Region: Not Set';
            document.getElementById('replay-click-status').textContent = config.replay.replayClickStatus || 'Click Location: Not Set';
            document.querySelector('.settings-container.replay .file-input').value = config.replay.replayText || '';
        }

        // Load anti-afk data
        if (config.antiAfk) {
            document.getElementById('anti-afk-click-status').textContent = config.antiAfk.antiAfkClickStatus || 'Click Location: Not Set';
        }

        // Load wave region status
        if (config.wave) {
            document.getElementById('wave-region-status').textContent = config.wave.waveRegionStatus || 'Wave Region: Not Set';
        }

        // Load macro keys
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

class TransparentOverlay:
    def __init__(self, window, callback, region_select=False):
        # Minimize window using the actual window minimize
        window.minimize()
        time.sleep(0.2)  # Wait for minimize
        
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
        
        # Configure overlay window
        self.root.attributes('-alpha', 0.1)
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        # Set window size to cover all screens
        self.root.geometry(f"{total_width}x{total_height}+{self.min_x}+{self.min_y}")
        
        # Create canvas for drawing selection rectangle
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        if region_select:
            # Bind drag events for region selection
            self.canvas.bind('<Button-1>', self.start_selection)
            self.canvas.bind('<B1-Motion>', self.update_selection)
            self.canvas.bind('<ButtonRelease-1>', self.end_selection)
        else:
            # Bind single click event
            self.canvas.bind('<Button-1>', self.on_click)
        
        # Focus the overlay
        self.root.focus_force()
        
        # Start the tkinter main loop
        self.root.mainloop()

    def restore_window(self):
        # Restore window to normal state
        self.window.restore()
        time.sleep(0.2)  # Wait for restore

    def start_selection(self, event):
        self.start_x = event.x_root - self.min_x
        self.start_y = event.y_root - self.min_y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=2
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

        self.macro_running = False
        self.stop_event = threading.Event()

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
        print("Starting macro...")
        self.reader = easyocr.Reader(['en'])
        self.macro_running = True
        self.stop_event.clear()
    
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
    
        print("Macro stopped successfully")

    def set_keyboard_binding(self, key, binding_type):
        if binding_type.strip() == 'Start Macro Key':
            keyboard.on_press_key(key.lower(), lambda _: self.start_macro())
        elif binding_type.strip() == 'Stop Macro Key':
            keyboard.on_press_key(key.lower(), lambda _: self.stop_macro())

    def run_macro_loop(self):
        while self.macro_running and not self.stop_event.is_set():
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
                    print(f"Ability timer ready - pausing macro loop for ability activation")
                    if self.current_upgrade:
                        print("Waiting for current upgrade to complete...")
                        while self.current_upgrade:
                            time.sleep(0.1)
                    
                    self.activate_ability(unit, number)
                    self.ability_timers.remove((timer, unit, number))
                    time.sleep(0.5)
  
            # Regular macro operations
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

    def handle_wave(self, wave):
        print(f"Processing wave {wave}")

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
        
                # Skip if wave, text, or unit is empty/not set
                if not upgrade_wave or not upgrade['text'].strip() or upgrade_unit == 'Select Unit':
                    continue

                upgrade_unit = int(upgrade_unit)
                if (upgrade_number not in self.completed_upgrades.get(upgrade_unit, set()) and
                    not any(u == (upgrade_unit, upgrade['text'], upgrade_number) 
                           for u in list(self.upgrade_queue.queue))):
            
                    if ((upgrade_wave.isdigit() and int(upgrade_wave) == wave) or 
                        (not upgrade_wave.isdigit())):
                        print(f"Queueing upgrade {upgrade_number} for unit {upgrade_unit}")
                        self.upgrade_queue.put((upgrade_unit, upgrade['text'], upgrade_number))
            except ValueError:
                continue

    
        # Handle abilities - Modified logic
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
                # Skip if wave, delay, or unit is empty/not set
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
    
    def check_wave_change(self):
        wave_region_text = window.evaluate_js("document.getElementById('wave-region-status').textContent")
        if "Not Set" in wave_region_text:
            print("Wave region not set, skipping wave check")
            return None, self.highest_wave_seen

        # Get all wave numbers from unit settings
        wave_numbers = window.evaluate_js("""
            Array.from(new Set(
                Array.from(document.querySelectorAll('.wave-input input, #upgrade-list input[type="text"]:first-of-type, #ability-list input[type="text"]:first-of-type'))
                    .map(input => input.value)
                    .filter(value => value !== '')
                    .map(Number)
            ))
        """)
        print(f"Looking for waves: {wave_numbers}")
    
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
        all_text = [text.lower() for (_, text, _) in results]

        # Check for separate "wave" and number
        if "wave" in all_text:
            wave_index = all_text.index("wave")
            # Look for numbers in adjacent texts
            for i in range(max(0, wave_index - 1), min(len(all_text), wave_index + 2)):
                if all_text[i].isdigit():
                    # Create combined text and replace original texts
                    combined_text = f"wave {all_text[i]}"
                    all_text = [combined_text]  # Replace all_text with just the combined text
                    print(f"Text detected in wave region: {all_text}")
                    break
        else:
            print(f"Text detected in wave region: {all_text}")
    
        current_wave = None
        for wave_num in wave_numbers:
            wave_patterns = [f"wave {wave_num}", str(wave_num)]
            for pattern in wave_patterns:
                for text in all_text:
                    if pattern in text:
                        print(f"Found wave {wave_num} in text: {text}")
                        current_wave = wave_num
                        break
                if current_wave:
                    break
            if current_wave:
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

    def upgrade_macro(self, unit_number, upgrade_text, upgrade_number):
        if self.stop_event.is_set():
            return False
        print(f"Attempting upgrade {upgrade_number} for Unit {unit_number}")

        unit_data = window.evaluate_js(f"""
            document.querySelectorAll('.card')[{unit_number - 1}].querySelector('.checkbox').checked
        """)

        if not unit_data or upgrade_number in self.completed_upgrades.get(unit_number, set()):
            print(f"Unit {unit_number} not placed or upgrade {upgrade_number} already completed")
            return True

        upgrade_texts = [text.strip().lower() for text in upgrade_text.split(',')]
        print(f"Looking for upgrade texts: {upgrade_texts}")

        while True:
            if self.stop_event.is_set():
                return False
        
            # Process ability queue here
            while not self.ability_queue.empty():
                ability_unit, ability_delay, ability_number = self.ability_queue.get()
                if ability_number not in self.completed_abilities:
                    start_time = time.time()
                    timer_entry = (start_time + ability_delay, ability_unit, ability_number)
                    if timer_entry not in self.ability_timers:
                        self.ability_timers.append(timer_entry)
                        print(f"Added ability {ability_number} to timer list with delay {ability_delay}")
        
            # Check for ability timers
            current_time = time.time()
            for timer, ability_unit, ability_number in self.ability_timers[:]:
                if current_time >= timer:
                    print("Pausing upgrade to execute ability macro")
                    self.activate_ability(ability_unit, ability_number)
                    self.ability_timers.remove((timer, ability_unit, ability_number))
                    print("Ability executed, resuming upgrade macro")
        
            if self.check_for_replay():
                break

            # Check for any of the upgrade texts
            found_upgrade = False
            for text in upgrade_texts:
                if self.check_for_upgrade(text):
                    found_upgrade = True
                    break

            if found_upgrade:
                self.completed_upgrades.setdefault(unit_number, set()).add(upgrade_number)
                print(f"Unit {unit_number} successfully upgraded to level {upgrade_number}")

                anti_afk_status = window.evaluate_js("document.getElementById('anti-afk-click-status').textContent")
                if "Not Set" not in anti_afk_status:
                    coords = re.findall(r'X=(\d+), Y=(\d+)', anti_afk_status)[0]
                    x, y = map(int, coords)
                    pydirectinput.moveTo(x, y)
                    time.sleep(0.025)
                    pydirectinput.moveTo(x, y - 1)
                    time.sleep(0.025)
                    pydirectinput.click(x, y - 2)
                    print("Anti-AFK click performed after upgrade")

                return True
    
            # Click unit
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
                time.sleep(0.025)
    
            # Click upgrade button
            upgrade_click_status = window.evaluate_js("document.getElementById('upgrade-click-status').textContent")
            if "Not Set" not in upgrade_click_status:
                coords = re.findall(r'X=(\d+), Y=(\d+)', upgrade_click_status)[0]
                upgrade_x, upgrade_y = map(int, coords)
                pydirectinput.moveTo(upgrade_x, upgrade_y)
                time.sleep(0.025)
                pydirectinput.moveTo(upgrade_x, upgrade_y - 1)
                time.sleep(0.025)
                pydirectinput.click(upgrade_x, upgrade_y - 1)
                time.sleep(1.5)
    
            current_wave, _ = self.check_wave_change()
            if current_wave:
                print(f"Wave {current_wave} detected during upgrade attempt")
                self.handle_wave(current_wave)

        print("Replay detected during upgrade attempt")
        return True

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
                    pydirectinput.click(ability_x, ability_y - 1)
                    time.sleep(0.250)
    
                    anti_afk_status = window.evaluate_js("document.getElementById('anti-afk-click-status').textContent")
                    if "Not Set" not in anti_afk_status:
                        coords = re.findall(r'X=(\d+), Y=(\d+)', anti_afk_status)[0]
                        x, y = map(int, coords)
                        pydirectinput.moveTo(x, y)
                        time.sleep(0.025)
                        pydirectinput.click(x, y - 1)
                        time.sleep(0.50)
    
                    self.completed_abilities.setdefault(ability_unit, set()).add(ability_number)
                    print(f"Unit {ability_unit} successfully activated ability {ability_number}")

    def replay_macro(self):
        replay_click_status = window.evaluate_js("document.getElementById('replay-click-status').textContent")
        if "Not Set" not in replay_click_status:
            coords = re.findall(r'X=(\d+), Y=(\d+)', replay_click_status)[0]
            x, y = map(int, coords)
            pydirectinput.moveTo(x, y)
            time.sleep(0.025)
            pydirectinput.click(x, y - 1)
            time.sleep(5)
        
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
            
            self.current_upgrade = None
            print("Replay macro executed and all tracking variables reset")
            return True
        return False

    def anti_afk_macro(self):
        anti_afk_status = window.evaluate_js("document.getElementById('anti-afk-click-status').textContent")
        if "Not Set" not in anti_afk_status:
            coords = re.findall(r'X=(\d+), Y=(\d+)', anti_afk_status)[0]
            x, y = map(int, coords)
            pydirectinput.moveTo(x, y)
            time.sleep(0.025)
            pydirectinput.click(x, y - 1)
            print("Anti-AFK macro executed")
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
        pydirectinput.click(click_x, click_y - 1)
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
            
    def get_click_location(self, element_id, is_unit_card=False):
        def handle_click(coords):
            if is_unit_card:
                js_code = f"""
                    const element = document.getElementById('{element_id}');
                    if (element) {{
                        element.innerText = 'X={coords[0]}, Y={coords[1]}';
                    }}
                """
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
