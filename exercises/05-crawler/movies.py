# %%
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# %%
def get_element(xpath, browser):
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

        return element
    except:
        return False

# %%
browser = webdriver.Chrome()

# %%
browser.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')

# %%
table_xpath = '//*[@id="mw-content-text"]/div[1]/table[2]'

# %%
tb_movies = get_element(table_xpath, browser)

# %%
if tb_movies:
    df_movies = pd.read_html(tb_movies.get_attribute('outerHTML'))[0]
    df_movies.to_csv('movies.csv', sep = ';', index = False)

    with open('screenshot.png', 'wb') as f:
        f.write(browser.find_element_by_xpath(
            '//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr[2]/td/div/div/div/a/img').screenshot_as_png)

    browser.quit()
else:
    print('Table not found.')

# %%
# Save virtualenv pip dependencies with:
# pip freeze > requirements.txt