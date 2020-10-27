#!/bin/bash
# Susanna Ardigò
# Knowledge Analysis and Management
# Project 1: Bad Smell Detection

python3 src/onto_creator/onto_creator.py res/tree.py

python3 src/individ_creator/individ_creator.py res/android-chess/app/src/main/java/jwtc/chess/

python3 src/bad_smell/bad_smell.py res/tree2.py