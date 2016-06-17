import os
import CleanUpDocument


myPathRoot = 'C:/Users/E083318N/Documents/ADExCHM/TH-OC-50-journaliers/'


for dossier, sous_dossiers, fichiers in os.walk(myPathRoot):
    print(dossier)
    cl = CleanUpDocument.CleanUpDocument(dossier)
    cl.main()

