Susanna Ardigò
Knowledge Analysis and Management
Project 1: Bad Smell Detection

To run the project use the command:
    `sh run.sh`
    
To test  the project use the command:
    `sh test.sh`
    
To run seperately:
Ontology Creator: `python3 src/onto_creator/onto_creator.py res/tree.py`

Individ Creator: `python3 src/individ_creator/individ_creator.py res/android-chess/app/src/main/java/jwtc/chess/`

Bad Smells: `python3 src/bad_smells/bad_smells.py res/tree2.owl > res/bad_smells.txt`