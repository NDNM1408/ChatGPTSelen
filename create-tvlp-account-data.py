import time

import undetected_chromedriver as uc
from fake_useragent import UserAgent

username = "dvietsang".replace(".", "-")
mail = "mail.ru".replace(".", "-")

folder_path = username + "-" + mail

op = uc.ChromeOptions()
# op.add_argument("--headless")
op.add_argument('--no-sandbox') 
op.add_argument('--disable-dev-shm-usage')
op.add_argument(f"--user-agent={UserAgent.random}")
op.add_argument(f"--user-data-dir=selenium-data/{folder_path}/")

driver = uc.Chrome(options=op, use_subprocess=True)
driver.get("https://chat.openai.com/")
time.sleep(120)
driver.close()