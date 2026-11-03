import os



def create_structures(structures_lst):

    for structure in structures_lst:

        if not os.path.exists(structure):
            
            if structure.endswith(".txt") and not os.path.isfile(structure):
                
                with open(structure, "x") as f:
                    pass

                print(f"{structure} file successfully created.")

            else:
                os.makedirs(structure)
                print(f"{structure}/ folder successfully created.")



def main():

    structures = ["data", "series", "regression", "plots", "fred_api_key.txt"]
    create_structures(structures)

main()
