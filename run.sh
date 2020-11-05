#!/bin/bash

python3 src/onto_creator/onto_creator.py res/tree.py

python3 src/individ_creator/individ_creator.py res/android-chess/app/src/main/java/jwtc/chess/

python3 src/bad_smells/bad_smells.py res/tree2.owl > res/bad_smells.txt