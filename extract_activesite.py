#!/usr/bin/env python
#
# (c) Copyright Rosetta Commons Member Institutions.
# (c) This file is part of the Rosetta software suite and is made available under license.
# (c) The Rosetta software is developed by the contributing members of the Rosetta Commons.
# (c) For more information, see http://www.rosettacommons.org. Questions about this can be
# (c) addressed to University of Washington CoMotion, email: license@uw.edu.

## @file   ~/generate_favorable_mutations.py
## @brief  calculating the distance to the active site and contact number for each residue in an enzyme 
## @author Raisa Noshin

import os, math, subprocess, csv

import argparse

parser = argparse.ArgumentParser(prog='Extract Active Site',description='Extract the Active Site from a pdb given the atoms intended to be used to define it')
parser.add_argument('-p','--pdb',required=True,action='store',dest='input',help="Enter the name of the file whose active site coordinates you want to extract in the form 'filename.pdb'")
parser.add_argument('-i','--identifiers',required=True,action='store',dest='identifiers',help='Enter the name of the file containing the coordinate identifiers. The file must be formatted such that each line contains the following information for 1 atom: Positiion, WT_Name, Atom ID. The first line should be an integer representing the starting position of the original file.')
parser.add_argument('-o','--manual_offset',action='store',default='',dest='man_offset',help="Enter the position at which there is an offset in the numbering in the original pdb file, which typically happens when there's a HETATM in the middle of the structure. ")
parser.add_argument('-l''--manual_offset_length',action='store',default=1,dest='man_offset_length',help="Enter the number of residues an offset HETATM takes up. Paired with the --manual_offset flag, and default length is 1.")
options = parser.parse_args()

amino_acids = {'A':'ALA','R':'ARG','N':'ASN','D':'ASP','C':'CYS','Q':'GLN','E':'GLU','G':'GLY','H':'HIS','I':'ILE','L':'LEU','K':'LYS','M':'MET','F':'PHE','P':'PRO','S':'SER','T':'THR','W':'TRP','Y':'TYR','V':'VAL','U':'SEL','O':'PYL'}

def extract_activesite():
	rpath = '../Rosetta/'
	identifiers = []
	activesite = []
	with open(options.identifiers) as readfile:
		for line in readfile:
			temp = line.splitlines()
			identifiers.extend(temp)
	try:
		starting_position_original = int(identifiers[0].split()[0])
		starting_residue_original = identifiers[0].split()[1]
		identifiers = identifiers[1:]
	except (ValueError, IndexError) as e:
		print e, "Invalid input file given with atom identifiers. The first line must be the starting position and residue of the file these identifiers come from."
	with open(options.input) as readfile:
		lines = readfile.readlines()
		done = False
		first_atom = 0
		for line in lines:
			first_atom += 1
			if done:
				break
			items = line.split()
			for key, value in amino_acids.iteritems():
				if ("ATOM" in items) & (value in items):
					done = True
		chain = lines[first_atom-2].split()[4]
		starting_residue_input = lines[first_atom-2].split()[3]

	call_clean = rpath+'tools/protein_tools/scripts/clean_pdb.py '+options.input+' '+chain
	try:
		print "Cleaning and renumbering input pdb file..."
		status = os.system(call_clean)
		subprocess.call(call_clean,shell=True)
		print "Pdb successfully renumbered!"
	except (OSError, ValueError) as e:
		print e, ": Unable to renumber and clean the pdb file. Please check if your path to Rosetta is correct, or that your pdb file is in the current directory."
		return
	except subprocess.CalledProcessError as f:
		print f.output

	cleaned_pdb = options.input[:len(options.input)-4]+'_'+chain+'.pdb'
	with open(cleaned_pdb) as readfile:
		first_line = readfile.readline().split()
		starting_position_input = int(first_line[5])
	offset = abs(starting_position_input-starting_position_original)
	if starting_position_input > starting_position_original:
		offset = -1*offset
	if offset == 0:
		if starting_residue_input != starting_residue_original:
			offset += 1
	if options.man_offset != '':
		man_offset_position = int(options.man_offset.strip())
		if offset < 0:
			man_offset_length = int(options.man_offset_length.strip())*-1
		else:
			man_offset_length = int(options.man_offset_length.strip())

	with open(cleaned_pdb) as readfile:
		lines = readfile.readlines()
		for line in lines:
			items = line.split()
			if 'ATOM' in items:
				position = items[5]
				if position < abs(offset):
					pass
				else:
					position = int(position)+offset
					if options.man_offset == '':
						pass
					else:
						if int(position) == int(man_offset_position):
							position+=man_offset_length
							offset+=man_offset_length
							options.man_offset = ''
					position = str(position)
				for id in identifiers:
					ids = id.split()
					if offset == 0:
						if (position == ids[0]) & (items[3] == ids[1]) & (items[2] == ids[2]):
							activesite.append(items[6:9])
					else:
						if (position == ids[0]) & (items[3] == ids[1]) & (items[2] == ids[2]):
							activesite.append(items[6:9])
	outfilename = options.input[:options.input.find('_')]+options.input[options.input.rfind('_'):len(options.input)-4]+"_activesite.csv"
	
	with open(outfilename, 'w') as newfile:
			write = csv.writer(newfile,quoting=csv.QUOTE_ALL)
			write.writerows(activesite)
	if len(activesite) == len(identifiers):
		print "Active site file '"+outfilename+"' generated and placed in current directory!"
	else:
		print "Some residues were missed when extracting :( Please check if you have any HETATMs in the middle of structure, and if you do, see the -o option to manually add in those offsets I couldn't predict!"

	try:
		os.remove(cleaned_pdb)
		os.remove(cleaned_pdb[:cleaned_pdb.find('.')]+".fasta")
	except OSError as e:
		print e, "Can't locate cleaned file that was just generated. Aborting..."
		return
extract_activesite()


