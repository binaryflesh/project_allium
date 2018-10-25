#!/bin/bash
git add -p

echo "Type the summary you want for your commit and press enter"

read summary

git commit -m "$summary"

git push origin master
read -p "Press Return to Close..."
