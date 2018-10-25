#!/bin/bash

# Asks user if they want to commit files before pushing
read -p "Do you want to commit (y/n)?:" commit_statement

# If user wants to commit files, commit files
if [ "$commit_statement" == "y" ]
then
    # Displays file changes and prompts user on whether or not they want to commith them
    git add -p

    # Display Message asking for Commit summary
    echo "Type the summary you want for your commit and press enter"

    # Prompt for user input and save to varriable summary
    read summary

    # Commits changes to repository
    git commit -m "$summary"
fi
#Pushes changes to remote repository
git push origin master

# Prompts for user input when done 
# (this is so that the console stays open so that user can read any error messages)
read -p "Press Return to Close..."