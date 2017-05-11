import string
import sys

# split the input file into words and the dependencies
def evens(ls):
	newls = []
	for i in range(len(ls)):
		if i % 2 == 0:
			newls.append(ls[i])
	return newls

# read the input file and get to correct format
def read_from_file(f):
	ls = f.readlines()	

	words = evens(ls)
	words_clean = [x[2:-3] for x in words]
	info = [x.split() for x in ls if x not in words]
	
	return words_clean, info

# add code for the \deptext (the actual sentence) in the graph
# adds POS tag information if showpos is set to 1
def write_sentence(words,info,close,showpos):
	deptext = ""
	deptext = deptext + "\t" + r"\begin{deptext}[column sep=.2cm, row sep = .2ex]" + "\n"
	
	# combine consecutive words that have dependencies to adjust spacing
	newwords = []
	tags = []
	skip = 0
	for w in range(len(words)):
		if (skip != 0):
			skip = skip - 1
			continue
		if w in close:
			s = "%s" %(words[w])
			toadd = []
			for i in range(w+1,len(words)):
				if i in close:
					toadd.append(i)
				else:
					toadd.append(i)
					break
			for k in toadd:
				s = s + " \&[.5cm] %s" %(words[k])
			newwords.append(s)
			skip = len(toadd)
		else:
			newwords.append(words[w])
	
	sent = " \& ".join(x for x in newwords if (x not in string.punctuation))
	sent = sent + r" \& ROOT \\ "

	deptext = deptext + "\t\t" + sent + "\n"

	if showpos:
		tags = []
		for i in info:
			tags.append(i[1])

		tagsent = " \& ".join(x.upper() for x in tags if x != 'sent')
		tagsent = tagsent + r" \& - \\ "
		deptext = deptext + "\t\t" + tagsent + "\n"

	deptext = deptext + "\t" + r"\end{deptext}"
	
	return deptext

# add code for all the \depedges in the graph
# if include != [], only displays dependencies with a type listed in include
def write_edges(words,info,include):
	#print(info)
	edges = []
	close = []
	for i in info:
		dep = None
		name = None
		for elt in i:
			if (dep != None) and (name != None):
				break
			if elt.startswith("#"):
				dep = elt
			if elt.startswith("@"):
				name = elt
		
		if (dep == None) or (name == None):
			continue
		dep = dep[1:]
		edge = dep.split("->")
		edge = [int(x) for x in edge]
		if edge[1] == 0:
			edge = [edge[0],len(info)]
		name = name[1:]

		if (include != []) and (name not in include):
			continue

		if abs(edge[1] - edge[0]) == 1:
			close.append((min(edge[1],edge[0])) - 1)

		edges.append("\t" + r"\depedge" + "{%d}{%d}{%s}" %(edge[1],edge[0],name)) 

	#print(edges)
	return edges,close

# initialize the tikz-dependency framework, call helper functions to fill in body
def create_latex(words,info,include,showpos):
	latex = []	

	latex.append(r"\begin{dependency}")
	edges,close = write_edges(words,info,include)
	sent = write_sentence(words,info,close,showpos)
	latex.append(sent)
	for k in edges:
		latex.append(k)
	latex.append(r"\end{dependency}")

	return latex
	
# write new .txt file in Latex code that is readable by tikz-dependency package
def write_latex(latex,fl):
	f = open('%s_output.txt'%(fl),'w')
	for line in latex:
		f.write("%s\n" % line)
	print("Written to %s_output.txt" %(fl))

# main program
# parses arguments, determines whether to only look at one sentence or several
def main():
	if len(sys.argv) < 4:
		print("ERROR: not enough arguments")
		print("format: python [filename] [input file] [1 or 0 (show POS tags or not)] <dependencies to include - OPTIONAL>")
		sys.exit(0)

	# parse arguments
	fl = sys.argv[1]

	if sys.argv[3] == '1':
		showpos = True
	else:
		showpos = False		
	
	include = []
	if len(sys.argv) > 4:
		include = sys.argv[4:]

	# either run program on multiple files or just one
	if sys.argv[2] == 'm':
		flist = open(fl)
		for sent in flist.readlines():
			sent = sent.strip()
			f = open('%s_input.txt'%(sent))
			words,info = read_from_file(f)
			latex = create_latex(words,info,include,showpos)
			write_latex(latex,sent)
	elif sys.argv[2] == 's':
		f = open('%s_input.txt'%(fl))
		words, info = read_from_file(f)
		latex = create_latex(words,info,include,showpos)
		write_latex(latex,fl)
	else:
		print("argument 2 must be 'm' (multiple) or 's' (single)")
		sys.exit(0)

main()
