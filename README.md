# PCR-Primer-Optimal-Annealing-Temperature-Calculator
Based on the papers "_Optimization of the annealing temperature for DNA amplification in vitro_" by W.Rychlik, W.J.Spencer and R.E.Rhoads (1990) and "_Predicting DNA duplex stability from the base sequence_" by K.J. Breslauer, R. Frank, H. Blöcker, L.A. Marky (1986).

# Input file - Primer Sequences and Format

Copy & paste the primer sequences in a .txt file, and the predicted product sequence in a separate .txt file. When running the file, it will first ask to input the primer .txt file, then the product .txt file. Using equations and values from the papers listed above, the optimal annealing temperature for the primers will be calculated. 

Calculations can be done for one set of forward & reverse primers at a time. 
**Format** <br>
**Primers.txt** <br>
TAGACGTAGCTAGTC #Sample forward primer in .txt file <br>
AGCGTAGGGAGCTGA #Sample reverse primer in .txt file <br>
** There should be no other text in the .txt file 

**Product.txt** <br>
TAGACGTAGCTAGTCATGCATGTGACTGATCGGGATCACACTCAGCTCCCTACGCT <br>
** There should be no other text in the .txt file

# Output file
Outputs an excel sheet with the primer ID, sequence and the optimal annealing temperature in <sup>o</sup>Celsius. 

# Dependencies 
1. tkinter
2. xlsxwriter
