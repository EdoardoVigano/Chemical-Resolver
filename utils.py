# import library to interrogate database
# from chembl_webresource_client.new_client import new_client
import pubchempy as pcp
import cirpy

# standar library
import requests

# data analysis
from rdkit import Chem
import json

#cst
def SmilesFromCasCST(cas):
    api_url = f"https://cts.fiehnlab.ucdavis.edu/rest/convert/cas/Pubchem CID/{str(cas)}"
    response = requests.get(api_url)
    if response.ok:
        try:
            y = json.loads(response.text)
            b = pcp.get_compounds(y[0]['results'][0], 'cid')
            smile = b[0].isomeric_smiles
        except:
            smile = 'Error'
    else:
        smile = 'Error'
    return smile  

# Cyirpy
def SmileFromCasCirpy(cas):
    try:
        smile = cirpy.resolve(cas,'smiles')
    except:
        smile = 'Error'
    if smile is None: smile = 'Error'
    return smile

def SmileFromNameCirpy(name):
    try:
        smile = cirpy.resolve(name,'smiles')
    except:
        smile = 'Error'
    return smile

def CasFromNameCirpy(name):
    try:
        cas = cirpy.resolve(name,'cas_number')
    except:
        cas = 'Error'
    return cas

# PubChem
def SmilesFromCasPubChem(cas):
    try: 
        cid = pcp.get_cids(str(cas))
        smile = pcp.Compound.from_cid(cid).isomeric_smiles
    except: smile = 'Error'
    return smile

def SmileFromNamePubChem(name):
    try:
        b = pcp.get_compounds(name, 'name')
        smile = b[0].isomeric_smiles
    except: 
        smile = 'Error'   
    return smile

def SmileFromInchikeyPubchem(Inchikey):
    try:
        b = pcp.get_compounds(Inchikey, 'inchikey')
        smile = b[0].isomeric_smiles
    except:
        smile = 'Error'
    return smile 

def CasFromSmilesPubchem(smile): 
    pass

# def CasFromInchikeyPubchem(Inchi): non si può è tra i sinonimi

    
# ChemID 
# ChemID 

def CasFromInchiChemID(Inchi):
    try:
        Syn = 'Error'
        key_in_ChemID = 'ik'
        api_url = f"https://chem.nlm.nih.gov/api/data/{key_in_ChemID}/equals/{Inchi}?data=summary"
        response = requests.get(api_url)
        ChemID = json.loads(response.text)
        Syn = ChemID['results'][0]['summary']['rn']
    except:
        Syn = 'Error'
    return Syn

def NameFromInchiChemID(inchi):
    try:
        Syn = 'Error'
        key_in_ChemID = 'ik'
        api_url = f"https://chem.nlm.nih.gov/api/data/{key_in_ChemID}/equals/{inchi}?data=summary"
        response = requests.get(api_url)
        ChemID = json.loads(response.text)
        Syn = ChemID['results'][0]['summary']['na']
    except:
        Syn = 'Error'
    return Syn

def SmileFromInchiChemID(inchi):
    pass

def InchiKeyFromCasChemID(cas):
    try:
        Syn = 'Error'
        key_in_ChemID = 'rn'
        api_url = f"https://chem.nlm.nih.gov/api/data/{key_in_ChemID}/equals/{cas}?data=summary"
        response = requests.get(api_url)
        ChemID = json.loads(response.text)
        Syn = ChemID['results'][0]['summary']['ik']
    except:
        Syn = 'Error'
    return Syn

def NameFromCasChemID(cas):
    try:
        Syn = 'Error'
        key_in_ChemID = 'rn'
        api_url = f"https://chem.nlm.nih.gov/api/data/{key_in_ChemID}/equals/{cas}?data=summary"
        response = requests.get(api_url)
        ChemID = json.loads(response.text)
        Syn = ChemID['results'][0]['summary']['na']
    except:
        Syn = 'Error'
    return Syn

def CasFromNameChemID(Name):
    try:
        Syn = 'Error'
        key_in_ChemID = 'na'
        api_url = f"https://chem.nlm.nih.gov/api/data/{key_in_ChemID}/equals/{Name}?data=summary"
        response = requests.get(api_url)
        ChemID = json.loads(response.text)
        Syn = ChemID['results'][0]['summary']['rn']
    except:
        Syn = 'Error'
    return Syn

#NCI/CADD (dovrebbe essere cactus)
def InchiFromSmilesNCI(smi):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{smi}/stdinchi"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
    except:
        Syn = 'Error'
    
    return Syn

def CasFromSmilesNCI(smi):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{smi}/cas"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
        else:
            b = Syn.split("\n")
            if len(b)>1:
                Syn = str(b[:])
    except:
        Syn = 'Error'
    
    return Syn    

def NameFromSmilesNCI(smi):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{smi}/iupac_name"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
    except:
        Syn = 'Error'
    
    return Syn

def SmilesFromInchiNCI(inchi):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{inchi}/smiles"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
    except:
        Syn = 'Error'
    return Syn

def InchiFromNameNCI(name):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{name}/stdinchi"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
    except:
        Syn = 'Error'
    return Syn

def InchiFromCasNCI(cas):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{cas}/stdinchi"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
    except:
        Syn = 'Error'
    return Syn
    
def NameFromInchiNCI(inchi):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{inchi}/iupac_name"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
    except:
        Syn = 'Error'
    return Syn

def NameFromCasNCI(cas):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{cas}/iupac_name"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
    except:
        Syn = 'Error'
    return Syn

def SmilesFromNameNCI(name):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{name}/smiles"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
    except:
        Syn = 'Error'
    return Syn

def SmilesFromCasNCI(cas):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{cas}/smiles"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
    except:
        Syn = 'Error'
    return Syn

def CasFromNameNCI(name):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{name}/cas"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
        else:
            b = Syn.split("\n")
            if len(b)>1:
                Syn = str(b[:])
    except:
        Syn = 'Error'
    return Syn

def CasFromInchiNCI(inchi):
    try:
        api_url = f"https://cactus.nci.nih.gov/chemical/structure/{inchi}/stdinchi"
        Syn = requests.get(api_url).text
        if 'Page not found (404)' in Syn: Syn = 'Error'
        elif '<!DOCTYPE html>' in Syn: Syn = 'Error'
    except:
        Syn = 'Error'
    return Syn

def Canonize_list(lst):
    '''list of smiles: input'''
    smile_can = []
    for smi in lst:
        try: 
            can = Chem.CanonSmiles(smi)
            smile_can.append(can)
        except:
            smile_can.append('Error')
    return smile_can

