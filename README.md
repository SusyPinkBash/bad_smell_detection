# Susanna Ardigò
## Knowledge Analysis and Management
### Project 1: Bad Smell Detection
#### Run the project with scripts
To run the project use the command:
    `sh run.sh`
    
To test  the project use the command:
    `sh test.sh`
    
 #### Run single files
Ontology Creator:
* `python3 src/onto_creator/onto_creator.py path_of_tree.py`
* `python3 src/onto_creator/onto_creator.py tree.py`


Individ Creator:
* `python3 src/individ_creator/individ_creator.py path_of_folder_with_javafiles`
* `python3 src/individ_creator/individ_creator.py res/android-chess/app/src/main/java/jwtc/chess/`


Bad Smells:
* `python3 src/bad_smells/bad_smells.py path_of_tree2.owl > path_to_save_output.txt`
* `python3 src/bad_smells/bad_smells.py res/tree2.owl > res/bad_smells.txt`
