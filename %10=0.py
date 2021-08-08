from selenium import webdriver
import csv
import time 
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
    
    
driver = webdriver.Chrome(r'C:\webdrivers\chromedriver.exe')

driver.get('http://www.pj.ma/pages-blanches-maroc.html')


driver.maximize_window()
time.sleep(1)

df = pd.read_excel(r'F:/project/PageJaunes/prenom.xlsx')
liste= df['prenom'].tolist()
ou="rabat"


for j in liste:
    driver.find_element_by_id('part_ou').send_keys(ou)
    time.sleep(1)
    driver.find_element_by_id('part_qui').send_keys(j)
    time.sleep(1)
    driver.find_element_by_xpath('//input[@tabindex="3"]').click()
    time.sleep(2)
    
    
    page_num=driver.find_element_by_class_name('sersh-resultatxt').text
    pat='sur+\s\d{0,5}\s'
    pj=re.findall(pat,page_num)
    page_num_sur=' '.join(pj)
    pat1='\d{0,5}'
    pj1=re.findall(pat1,page_num_sur)
    pj1=''.join(pj1)
    
        
    if int(pj1)>=10 and int(pj1)%10==0:
        
        file_name = j + '-' + ou
        with open(f'{file_name}.csv','w') as file:
            file.write("Nom & Prenom;Adress;Ville;Telephone \n")
        print(j+"==="+pj1)
        
        pj_num=(int((int)(pj1)/10))
        for k in range(pj_num):
            noms=driver.find_elements_by_xpath('//h2[@class="annoncesd-ttre"]/a')
            adresses=driver.find_elements_by_xpath('//li[@class="annoncesd-adressec"]/table/tbody/tr/td[2]/div/div')
            villes=driver.find_elements_by_xpath('//li[@class="annoncesd-adressec"]/table/tbody/tr/td[2]/div/div/strong')
            tels=driver.find_elements_by_xpath('//li[@class="annoncesd-adressec"]/table/tbody/tr/td[3]/strong')
        
            with open(f'{file_name}.csv','a') as file:
                for i in range(len(noms)):
                    file.write(noms[i].text + ";" + adresses[i].text + ";" + villes[i].text +";" + tels[i].text +"\n")
                next=driver.find_element_by_xpath('//*[@id="formresultats"]/div/div[1]/div[4]/ul/li/a[4]')
                next.click()
            file.close()
    driver.get('http://www.pj.ma/pages-blanches-maroc.html')
driver.close()
