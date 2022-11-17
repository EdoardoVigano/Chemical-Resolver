from rdkit import Chem
from rdkit.Chem import Descriptors
import pandas as pd

'''if self.propertyAll.isChecked(): self.propertyCheck_list.append('All')'''

def propertyCalculator(input_, Id_in, propertyCheck_list):
        
        ''' some specific descriptors'''
        dic = {}
        if Id_in == 'SMILES': 
            m = Chem.MolFromSmiles(input_)
            dic['SMILES'] = input_
        elif Id_in == 'INCHI': 
            m = Chem.MolFromInchi(input_)
            dic['INCHI'] = input_ 
            
        if 'LogP' in propertyCheck_list: dic['LogP'] = Descriptors.MolLogP(m)
        if 'MW' in propertyCheck_list: dic['MW'] = Descriptors.ExactMolWt(m)
        if 'NumAromaticRing' in propertyCheck_list: dic['NumAromaticRings'] = Descriptors.NumAromaticRings(m)       
        if 'MaxPartialCharge' in propertyCheck_list: dic['MaxPartialCharge'] = Descriptors.MaxPartialCharge(m)       
        if 'MinPartialCharge' in propertyCheck_list: dic['MinPartialCharge'] = Descriptors.MinPartialCharge(m)     
        if 'NumHAcceptors' in propertyCheck_list: dic['NumHAcceptors '] = Descriptors.NumHAcceptors(m)    
        if 'NumHDonors' in propertyCheck_list: dic['NumHDonors'] = Descriptors.NumHDonors(m)
        if 'All' in propertyCheck_list:
            dic['LogP'] = Descriptors.MolLogP(m)
            dic['MW'] = Descriptors.ExactMolWt(m)
            dic['NumAromaticRings'] = Descriptors.NumAromaticRings(m)
            dic['MaxPartialCharge'] = Descriptors.MaxPartialCharge(m)
            dic['MinPartialCharge'] = Descriptors.MinPartialCharge(m)
            dic['NumHAcceptors '] = Descriptors.NumHAcceptors(m)
            dic['NumHDonors'] = Descriptors.NumHDonors(m)
        Descriptors_result = pd.DataFrame([dic])
        return Descriptors_result