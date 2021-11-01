# PCR-Primer-Optimal-Annealing-Temperature-Calculator
Based on the papers "_Optimization of the annealing temperature for DNA amplification in vitro_" by W.Rychlik, W.J.Spencer and R.E.Rhoads (1990) and "_Predicting DNA duplex stability from the base sequence_" by K.J. Breslauer, R. Frank, H. Blöcker, L.A. Marky (1986).

# Input file - Primer Sequences and Format

Using equations and values from the papers listed above, the optimal annealing temperature for the primers will be calculated. 
Calculations can be done for one set of PCR primers and product. 

**Format** <br>
**Product.txt** <br>
TAGACGTAGCTAGTCATGCATGTGACTGATCGGGATCACACTCAGCTCCCTACGCT <br>
** There should be no other text in the .txt file. Simply copy and paste the expected PCR product sequence into a .txt file.

# Output file
Outputs an excel sheet with the primer ID, sequence and the optimal annealing temperature in <sup>o</sup>Celsius. 

# Dependencies 
1. tkinter
2. xlsxwriter
