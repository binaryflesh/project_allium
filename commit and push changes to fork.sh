#!/bin/bash
echo "Type the summary you want for your commit and press enter"

read summary

git add -A && git commit -m $summary

git push origin master
read -p "Press Return to Close..."
