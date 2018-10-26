#!/bin/bash

#Fetches any changes that have been made to upstream repository
git pull upstream master

# Prompts for user input when done 
# (this is so that the console stays open so that user can read any error messages)
read -p "Press Return to Close..."
