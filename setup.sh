#!/bin/bash

echo "Updating Termux..."
pkg update -y && pkg upgrade -y

echo "Installing Python..."
pkg install python -y

echo "Installing Termux API..."
pkg install termux-api -y

echo "Requesting Storage Permissions..."
termux-setup-storage

echo " "
echo "Setup Complete!"
echo "IMPORTANT: Make sure you have installed the 'Termux:API' app from the Play Store or F-Droid and granted all permissions (Contacts, SMS, Microphone, Phone)."
echo " "
echo "Run the tool using: python jarvis.py"
