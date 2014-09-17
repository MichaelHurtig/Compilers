0	JMP	0	37	#  Main program Jump
1	JMP	0	2	# func/proc Jump
2	INT	0	4	#  Inc TOS for func/proc variables
3	LOD	0	3	# Load variable num
4	JMP	0	5	# Cal & Andy's NO-OP instruction :-)
5	LIT	0	0	# Push literal num 0
6	OPR	0	8	# ==
7	JPC	0	11	# backpatched over IF
8	LIT	0	0	# Push literal num 0
9	STO	1	4	# Store in variable fib
10	JMP	0	36	#  backpatched over else
11	LOD	0	3	# Load variable num
12	JMP	0	13	# Cal & Andy's NO-OP instruction :-)
13	LIT	0	1	# Push literal num 1
14	OPR	0	8	# ==
15	JPC	0	19	# backpatched over IF
16	LIT	0	1	# Push literal num 1
17	STO	1	4	# Store in variable fib
18	JMP	0	36	#  backpatched over else
19	LOD	0	3	# Load variable num
20	JMP	0	21	# Cal & Andy's NO-OP instruction :-)
21	LIT	0	1	# Push literal num 1
22	OPR	0	3	# Subtract
23	PAS	0	1	# Pass parameters to function fib
24	CAL	1	1	# Call function fib
25	LOD	1	4	# Function Load fib
26	JMP	0	27	# Cal & Andy's NO-OP instruction :-)
27	LOD	0	3	# Load variable num
28	JMP	0	29	# Cal & Andy's NO-OP instruction :-)
29	LIT	0	2	# Push literal num 2
30	OPR	0	3	# Subtract
31	PAS	0	1	# Pass parameters to function fib
32	CAL	1	1	# Call function fib
33	LOD	1	4	# Function Load fib
34	OPR	0	2	# Add
35	STO	1	4	# Store in variable fib
36	OPR	0	0	# Exit Function
37	INT	0	5	#  Inc TOS for main/global variables
38	LIT	0	9	# Push literal num 9
39	PAS	0	1	# Pass parameters to function fib
40	CAL	0	1	# Call function fib
41	LOD	0	4	# Function Load fib
42	OPR	0	20	# Coerse INT to REAL
43	STO	0	3	# Store in variable ans
44	LOD	0	3	# Load variable ans
45	OPR	0	47	# Write 
46	OPR	0	0	#  Exit main
