from selenium import webdriver
import sys
import time

# Run with:
# python location.py 80420130
cep = sys.argv[1]

if cep:
    browser = webdriver.Chrome()
    
    time.sleep(10)
    browser.get('https://buscacepinter.correios.com.br/app/endereco/index.php?t')
    input = browser.find_element_by_name('endereco')
    input.clear()
    input.send_keys('80420130')
    select = browser.find_element_by_xpath('//*[@id="formulario"]/div[2]/div/div[2]/select/option[6]').click()
    browser.find_element_by_id('btn_pesquisar').click()
    
    time.sleep(10)
    address = browser.find_element_by_xpath('/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr/td[1]').text
    district = browser.find_element_by_xpath("//*[@id='resultado-DNEC']/tbody/tr/td[2]").text
    location = browser.find_element_by_xpath('/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr/td[3]').text
    
    browser.close()

    print(f"""
        CEP: {cep}
        Endereço: {address}
        Bairro: {district}
        Cidade: {location.split('/')[0]}
        Estado: {location.split('/')[1]}
    """)
