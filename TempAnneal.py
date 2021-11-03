#Import Modules
import tkinter as tk
from tkinter import filedialog
import math
root = tk.Tk()
root.withdraw()

#Import primer sequences and the product sequence
F_primer = input("Input forward primer sequence: ")
R_primer = input("Input reverse primer sequence: ")
print("Choose .txt file from python pop-up that contains the PCR product sequence.")
product_seq = filedialog.askopenfilename() 

with open(product_seq, "r") as product_intro:
    product = product_intro.read()

#define variables:
dH = float #kcal - enthalpy of annealing 
dS = float #cal/K - entropy of annealing 
R = 1.987E-3 #kcal/(C*mol) - molar gas constant
c = 250 #M (picoMolar) - total molar concentration of the annealing oligonucleotides (when oligonucleotides are not self-complementary) - empirically determined value
K = 50 #M (milliMolar) - standard K+ concentration in PCR buffer (working concentration)
l = len(product) #Length of product in bp

#Table - Nearest-neighbor thermodynamics [dH (kcal), dS (cal/K), dG (kcal)]
AAorTT = [9.1, 24E-3, 1.9] 
AT = [8.6, 23.9E-3, 1.5] 
ACorGT = [6.5, 17.3E-3, 1.3] 
AGorCT = [7.8, 20.8E-3, 1.6] 
TA = [6.0, 16.9E-3, 0.9] 
TCorGA = [5.6, 13.5E-3, 1.6] 
TGorCA = [5.8, 12.9E-3, 1.9] 
CCorGG = [11.0, 26.6E-3, 3.1]
CG = [11.9, 27.8E-3, 3.6]
GC = [11.1, 26.7E-3, 3.1]

#Define Functions 
#Make complementary strand 
def complementer(sequence):
    comp_index = 0
    sort_lst = []
    complement = []
    for base in sequence:
        sort_lst.append([comp_index, base])
        comp_index += 1
    sorted_comp_lst = sorted(sort_lst, reverse=True)
    index = 0 
    while index < (len(sorted_comp_lst)):
        if sorted_comp_lst[index][1] == "A":
            complement.append("T")
            index += 1
        elif sorted_comp_lst[index][1] == "T":
            complement.append("A")
            index += 1
        elif sorted_comp_lst[index][1] == "C":
            complement.append("G")
            index += 1
        elif sorted_comp_lst[index][1] == "G":
            complement.append("C")
            index += 1        
    return str(''.join(complement))

#Calculate dH and dS - pick sequences from table and sum dH/dS values from the table for the primer sequence
def dH_dS_finder(primer_seq):
    dH = 0
    dS = 0
    enum_iter = enumerate(primer_seq)
    for i, _ in enum_iter:
        if primer_seq[i:(i+2)] == "AT":
            i = next(enum_iter)                
            dH += AT[0]
            dS += AT[1]
        elif primer_seq[i:(i+2)] == "AA" or primer_seq[i:(i+2)] == "TT":
            i = next(enum_iter)
            dH += AAorTT[0]
            dS += AAorTT[1]
        elif primer_seq[i:(i+2)] == "AC" or primer_seq[i:(i+2)] == "GT":
            i = next(enum_iter)
            dH += ACorGT[0]
            dS += ACorGT[1]
        elif primer_seq[i:(i+2)] == "AG" or primer_seq[i:(i+2)] == "CT":
            i = next(enum_iter)
            dH += AGorCT[0]
            dS += AGorCT[1]
        elif primer_seq[i:(i+2)] == "TA":
            i = next(enum_iter)
            dH += TA[0]
            dS += TA[1]
        elif primer_seq[i:(i+2)] == "TC" or primer_seq[i:(i+2)] == "GA":
            i = next(enum_iter)
            dH += TCorGA[0]
            dS += TCorGA[1]
        elif primer_seq[i:(i+2)] == "TG" or primer_seq[i:(i+2)] == "CA":
            i = next(enum_iter)
            dH += TGorCA[0]
            dS += TGorCA[1]
        elif primer_seq[i:(i+2)] == "CG":
            i = next(enum_iter)
            dH += CG[0]
            dS += CG[1]
        elif primer_seq[i:(i+2)] == "CC" or primer_seq[i:(i+2)] == "GG":
            i = next(enum_iter)
            dH += CCorGG[0]
            dS += CCorGG[1]
        elif primer_seq[i:(i+2)] == "GC":
            i = next(enum_iter)
            dH += GC[0]
            dS += GC[1]
    return dH, dS 

#Calculate the GC percentage of PCR product
def GC_Content(product_seq):
    GC_content = 0
    for base in product_seq:
        if base == "G" or base == "C":
            GC_content += 1
    return GC_content/len(product_seq)*100

#Run calculations for each strand | dHF1 = dH of F_primer sequence, dHFC1 = dH of F_primer complementary sequence (annealing target)
F_comp = complementer(F_primer)
R_comp = complementer(R_primer)  
dHF1, dSF1 = dH_dS_finder(F_primer)
dHR1, dSR1 = dH_dS_finder(R_primer)
if len(R_primer) % 2 == 0:
    dHFC1, dSFC1 = dH_dS_finder(F_comp[1:])
    dHRC1, dSRC1 = dH_dS_finder(R_comp[1:])
else:
    dHFC1, dSFC1 = dH_dS_finder(F_comp)
    dHRC1, dSRC1 = dH_dS_finder(R_comp)

dHF = dHF1 + dHFC1
dSF = dSF1 + dSFC1 
dHR = dHR1 + dHRC1 
dSR = dSR1 + dSRC1 

Tm_product = 0.41*(GC_Content(product))+16.6*math.log(K,10)-675/l

#Calculate Tm of primers 
def Tm_calculator(dH, dS): 
    Tm_primer = dH/(dS+R*math.log(c/4))-273.15+16.6*math.log(K,10)
    return Tm_primer

Tm_primer_F = Tm_calculator(dHF, dSF)
Tm_primer_R = Tm_calculator(dHR, dSR)

#Calculate Optimal Annealing Temperature
def Ta_Calculator(primer):
    Opt_Ta = 0.3*primer+0.7*Tm_product-14.9
    return Opt_Ta
#Use least stable primer melting temperature
if Tm_primer_F >= Tm_primer_R:
    Opt_Ta = Ta_Calculator(Tm_primer_R)
else: 
    Opt_Ta = Ta_Calculator(Tm_primer_F)

#Output
print("The optimal annealing temperature for this primer set is " + str(Opt_Ta) + " degrees celsius.")
print("Analysis complete.")
