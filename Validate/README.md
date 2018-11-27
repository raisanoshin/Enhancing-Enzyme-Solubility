# Example Run of the Enhancing Enzyme Solubility Python Script

#####Generate minimum Calpha distance to active site and contact number-


Input files:

-3ich.pdb

-3ich_activesite.csv


Command line:

python enhance_enzyme_solubility.py CalculateDistAndCN -p 3ich.pdb -c Linux -r 
	~/path/to/Rosetta/ -a 3ich_activesite.csv


The output should match the given '3ich_dist_cn.csv' file.




#####Generate Favorable Mutations-


Input files:

-3ich_PSSM.csv

-3ich_dist_cn.csv (or a file you generated on your own in the same format)


Command line:

python enhance_enzyme_solubility.py GenerateMutations -m 
	3ich_PSSM.csv -n 3ich_dist_cn.csv 


The output should match the given '3ich_dist_cn_favorable_mutations.csv' file.