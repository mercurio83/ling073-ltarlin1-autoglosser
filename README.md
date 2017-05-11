# ling073-ltarlin1-autoglosser

Wiki page with more documentation:
https://wikis.swarthmore.edu/ling073/Ltarlin1/Final_Project

Usage instructions:

The autoglosser.py file can be run with the following format:
python autoglosser.py [input file] [type] [POS tags] <dependencies to include - OPTIONAL>

Each of these arguments is explained in more detail below:

   -input file:
	This argument specifies the CG file to be diagrammed. The code expects the name of the 
	file to follow the form "<label>_input.txt", but this parameter only requires the label. 
	For example, if the desired input file were "fox_input.txt", this argument would simply be "fox". 
	The exception to this rule is if the user wants to do batch processing, in which case this 
	argument is simply the name of the file containing the other filenames.
    
   -type:
	This argument specifies whether the input file is a single sentence or a list of filenames. 
	The options are m (for multiple, or batch processing) or s (for a single sentence).
    
   -POS tags:
	This argument specifies whether the part-of-speech tags should be displayed below the text of 
	the sentence. The options are 1 (for yes) or 0 (for no).
    
   -[OPTIONAL] Dependencies:
	This optional argument (or arguments) are the specific dependency types that should be displayed 
	in the graph. If more than one is desired, simply list them here separated by spaces. For example, 
	if you wanted to only see dependencies of type "det" and "amod", you would add "det amod" after 
	the POS tag argument.
