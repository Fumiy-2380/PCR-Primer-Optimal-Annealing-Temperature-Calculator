#Import Modules
import tkinter as tk
from tkinter import filedialog
import xlsxwriter as xls
import math
workbook = xls.Workbook("Primer-Anneal_Results.xlsx")
worksheet = workbook.add_worksheet()

root = tk.Tk()
root.withdraw()

#Import primer sequences and the product sequence
#primer_seq = filedialog.askopenfilename()
F_primer = input("Input forward primer sequence: ")
R_primer = input("Input reverse primer sequence: ")
product_seq = filedialog.askopenfilename() 

"""
with open(primer_seq, "r") as primer_intro:
    primers = [line.strip("\n") for line in primer_intro]
"""
with open(product_seq, "r") as product_intro:
    product = product_intro.read()

#define variables:
dH = float #kcal 
dS = float #cal/K
R = 1.987E-3 #kcal/(C*mol)
c = 250 #M (picoMolar)
K = 50 #M (milliMolar)
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

#Calculate dH and dS 
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
        

#Run calculations for each strand   
Tm_product = 0.41*(GC_Content(product))+16.6*math.log(K,10)-675/l
#primer_number = 1
#or seq in primers:
def Ta_Calculator(primer):
    primer_number = 1
    dH, dS = dH_dS_finder(primer)
    Tm_primer = dH/(dS+R*math.log(c/4))-273.15+16.6*math.log(K,10)
    Opt_Ta = 0.3*Tm_primer+0.7*Tm_product-14.9
    primer_number += 1
    return Opt_Ta
 
#Input results into excel sheet
worksheet.write(1,0,"F. Primer")
worksheet.write(2,0,"R. Primer")
worksheet.write(0,1,"Opt Ta")
worksheet.write(0,2,"Primer Sequence")
worksheet.write(1,1,Ta_Calculator(F_primer))
worksheet.write(2,1,Ta_Calculator(R_primer))
worksheet.write(1,2,F_primer)
worksheet.write(2,2,R_primer)
workbook.close()
print("Analysis complete.")
