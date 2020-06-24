import re

company_dictionary = []

def dict_check(line):
    
    for name in company_dictionary:
        #print(name)
        #print(line)
        if name in line:
            return True
    #print(line+" not found; dict size ="+ str(len(company_dictionary)))
    return False




with open("top-1m.txt", "r") as a_file:
  counter = 1
  for line in a_file:
    line = line.strip()
    if '.co.' in line:
        continue
    if dict_check(line):
      continue
    p = re.compile('.+,')
    url = p.sub('', line, count=1)
    p2 = re.compile('\.[^.]+$')
    name_server = p2.sub('', url)
    p3 = re.compile('.*\.')
    company = p3.sub('',name_server)
    if len(company) >= 4:
        company_dictionary.append(company)
    #print("Dict size =" + str(len(company_dictionary)))
    print(str(counter)+","+url)
    counter +=1


