# Enhancing-Enzyme-Solubility

This is the readme file explaining how to use the script entitled "enhance_enzyme_solubility.py." It is designed to be used with singular inputs rather than in batches, and it is designed with the assumption that the user possesses basic command line knowledge.

Package Contents: 
enhance_enzyme_solubility.py - Can be used to (1) calculate the distance to active site and contact number and (2) to generate favorable mutations based upon PSSM score (generated from script written by GitHub user JKlesmith) and distance to active site and contact number file

contact_num.xml - Used in Parser 1 (defined below) to calculate the contact number of each residue by using the AverageDegree filter in Rosetta



Overall Script Help: 

Use a residue's distance to active site, contact number, and PSSM score to
isolate solubility-enhancing mutations that preserve catalytic activity.

positional arguments:
  {GenerateMutations,CalculateDistAndCN}
                        Usage: python enhance_enzyme_solubility.py {RunMode}
                        -flags
    GenerateMutations   Uses PSSM score, distance to active site, and contact
                        number information to calculate solubilty-enhancing
                        mutations that maintain catalytic activity.
    CalculateDistAndCN  Runs the script written to calculate the distance to
                        the active site and the contact number of each residue
                        in a protein.

optional arguments:
  -h, --help            show this help message and exit
___________________________________________________________________________________

Parser 1 - CalculateDistAndCN

Minimum Files/Information Needed: 

	The protein pdb file path

	Whether or not there is a ligand present in the provided pdb (T/F)

	The ligand ID (record type) OR a file with all the ligand information (x y z coordinates)

	The type of compiler (Mac or Linux)

	Rosetta and PyRosetta must be properly set up and installed

	The path to Rosetta

	The file entitled 'contact_num.xml'

Options Help:

usage: Enhance Enzyme Solubility CalculateDistAndCN [-h] [-o OUTFILENAME] -p
                                                    PDB -c OSCOMPILER [-l]
                                                    [-t RECORD_TYPE] -r RPATH
                                                    [-a ASITE]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILENAME, --outfile OUTFILENAME
                        Specify the desired name for the output file
                        containing the distance to the active site and contact
                        number (Default: 'results.csv'):
  -p PDB, --pdb PDB     Enter the path to the pdb file, noting that the last
                        thing should have the form of 'filename.pdb'
                        (REQUIRED)
  -c OSCOMPILER, --compiler OSCOMPILER
                        Enter your operating system (i.e. Mac or Linux)
                        (REQUIRED)
  -l, --lig             Use this flag to indicate that a ligand is present
                        within the pdb structure.
  -t RECORD_TYPE, --recordtype RECORD_TYPE
                        Enter the Atom ID of the ligand. If there are
                        multiple, separate them by a space. Note: Must be
                        specified if -l flag is used
  -r RPATH, --rosetta RPATH
                        Enter the path to Rosetta. (REQUIRED)
  -a ASITE, --asite ASITE
                        Enter the path to the file containing the active site
                        coordinates for the pdb structure in question. Note:
                        This is required if the -l flag is not used.


Sample Command Lines: 

python enhance_enzyme_solubility.py CalculateDistAndCN -p ~/Desktop/2dfb.pdb -c 	Linux -l -t SEL -r ~/Modeling/Rosetta/ 

python enhance_enzyme_solubility.py CalculateDistAndCN -p ~/Desktop/3ich.pdb -c 	Linux -r ~/		Modeling/Rosetta/ -a ~/Desktop/3ich/3ich_asite.csv

___________________________________________________________________________________

Parser 2 - GenerateMutations

Minimum Files/Information Needed:

	The path to the file containing PSSM values (generated from pipeline created by GitHub user JKlesmith or formatted according to said pipeline output)

	The path to the file containing the distance to active site and contact number information (as formatted through the CalculateDistAndCN parser if created manually)

Options Help: 

usage: Enhance Enzyme Solubility GenerateMutations [-h] [-s PSSM_THRESHOLD]
                                                   [-d DIST_THRESHOLD]
                                                   [-c CONTACT_THRESHOLD]
                                                   [-o OUTFILENAME] -m
                                                   PSSM_FILENAME -n
                                                   DIST_AND_CONTACT_FILENAME
                                                   [-p]

optional arguments:
  -h, --help            show this help message and exit
  -s PSSM_THRESHOLD, --score_threshold PSSM_THRESHOLD
                        Indicate the threshold above which PSSM scores will be
                        favorable. Default: 0
  -d DIST_THRESHOLD, --distance_threshold DIST_THRESHOLD
                        Indicate the Calpha distance to the active site
                        threshold above which will enhance favorablility.
                        Default: 15.0
  -c CONTACT_THRESHOLD, --contact_threshold CONTACT_THRESHOLD
                        Indicate the contact number below which enhance
                        favoribility. Default: 16
  -o OUTFILENAME, --outfile OUTFILENAME
                        Specify the desired name for the project. Default:
                        'enzyme_0001'
  -m PSSM_FILENAME, --pssm PSSM_FILENAME
                        Provide the file name for the csv file containing the
                        PSSM scores formatted similar to the output of the
                        script written to calculate PSSM score by J. Klesmith.
  -n DIST_AND_CONTACT_FILENAME, --distance_and_contact DIST_AND_CONTACT_FILENAME
                        Provide the file name for the csv file containing the
                        distance to the active site and contact number for
                        each residue formatted into four columns with the
                        following information [Position, WT_Residue, Distance
                        to Active Stie, Contact Number]
  -p, --possibilities   Use this flag to indicate that you would like a file
                        generated with all possible mutations and their
                        respective information.


Sample Command Lines: 

python enhance_enzyme_solubility.py GenerateMutations -m 
	~/Desktop/3ich/3ich_PSSM.csv -n ~/Desktop/3ich/3ich_dist_cn.csv 

python enhance_enzyme_solubility.py GenerateMutations -m 
	~/Desktop/2dfb/2dfb_PSSM.csv -n ~/Desktop/2dfb/2dfb_dist_cn.csv 
	-s 1 -d 14.7 -c 12 -p -o 2dfb_favorable_mutations

