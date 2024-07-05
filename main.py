from fastapi import FastAPI
import os
import re
app = FastAPI()

output = {
}
invalidSuffix = 0

if 'MANUAL_ADD' in os.environ:
    manual_add = os.environ['MANUAL_ADD'].split()
else:
    manual_add = []

def import_psl_to_list(file_path):
    suffixes = []
    current_description = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                #if line and not line.startswith("//"):
                #if line.startswith("//"):
                #    current_description.append(line)
                #elif line:
                    #suffixes[line] = current_description
                suffixes.append(line)
                    #suffixes.append({ 'domain' :line,'description' : current_description} ) - move to dictionary
                    #current_description = []
    except UnicodeDecodeError as e:
        print(f"Error decoding file: {e}")
    return suffixes



#print(detect_encoding('public_suffix_list.dat'))
pslData = import_psl_to_list('./public_suffix_list.dat')
pslData.append ("")
pslData.append ("// Manually added")
pslData = pslData + manual_add


def parse_data(data):
    domain_dict = {}
    current_metadata = []
    inBlock = 0
    for line in data:
        line = line.strip()
        if line.startswith('//') and inBlock == 0:
        #if re.match('(\/\/ [a-z]{0,10}) : .*',line) and inBlock == 0:
        #if re.match('(\/\/ [a-z]{0,10}) : .*',line): # check if the line is TLD description/note
            current_metadata.append(line.replace("// ",""))
        elif len(line) > 0:
            domain_dict[line] = current_metadata.copy()
            inBlock =+ 1
        else:
            inBlock = 0
            current_metadata = []




    return domain_dict


domain_dict = parse_data(pslData)
#for k, v in domain_dict.items():
    #if (".au" in k):
#    print(f"{k}: {v}")

#parse_data(pslData)

def remove_first_part(domain):
    # Split the domain by dots
    parts = domain.split('.')
    
    # Check if there are enough parts to remove the first one
    if len(parts) > 1:
        # Join the parts excluding the first one
        return '.'.join(parts[1:])
    else:
        # If the domain doesn't have a dot, return it as is
        return domain


def returnPSL(domain):
        count = 0
        while ("." in domain and domain not in pslData and count < 50):
            domain = remove_first_part(domain)
            count+=1
        if count == 50:
            return invalidSuffix
        else:
            return domain

def returnOrgLevelDomain(domain):
        count = 0
        countLimit = 50
        while (domain != returnPSL(domain) and remove_first_part(domain) not in pslData and count < countLimit):
            count+=1
            domain = remove_first_part(domain)
        if count == countLimit:
            domain = invalidSuffix
        else:
            return domain


def checkDomain(domain):
    # Split the domain by dots
    parts = domain.split('.')
    
    # Check if there are enough parts to remove the first one
    if len(parts) > 0 and invalidSuffix == 0:
        # Join the parts excluding the first one
        output["sourceDomain"] = domain
        output["parentDomain"] = remove_first_part(domain)
        output["isTld"] =  domain in pslData
        output["tldDomain"] =  returnPSL(domain)
        output["manuallyAdded"] = returnPSL(domain) in manual_add
        if output["isTld"] == False:
            output["orgLevelDomain"] =  returnOrgLevelDomain(domain)
            output["isOrgLevel"] = remove_first_part(domain) in pslData and domain != returnPSL(domain)
        else:
            output["isOrgLevel"] = False

        try:
            output["comment"] = domain_dict[returnPSL(domain)]
        except:
            output["comment"] = "unknown"
        return output
        #return '.'.join(parts[1:])
    else:
        # If the domain doesn't have a dot, return it as is
        return "invalidSuffix"


#print(returnOrgLevelDomain("com.au"))




@app.get("/getPsl")
def generate(domain):
    return checkDomain(domain)


