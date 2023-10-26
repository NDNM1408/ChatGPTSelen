import time
import argparse
import os
import logging

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from dotenv import load_dotenv


def redirect_mainscreen(driver, args):
    driver.get('https://chat.openai.com/')
    time.sleep(0.5)
    curent_url = driver.current_url
    load_dotenv()
    if "login" in curent_url:
        openai_login(driver,
                     os.getenv("GPT_ACCOUNT"),
                     os.getenv("GPT_PASSWORD"))


def openai_login(driver, email, password):

    curent_url = driver.current_url
    if "login" not in curent_url:
        driver.get('https://chat.openai.com/auth/login')

    inputElement = driver.find_element(
        By.XPATH, "//button[@data-testid='login-button']")
    inputElement.click()
    time.sleep(3)
    mail = driver.find_element(By.XPATH, "//input[@inputmode='email']")
    mail.send_keys(u'\ue009' + u'\ue003')
    mail.send_keys(email)
    btn = driver.find_elements(By.TAG_NAME, "button")[0]
    btn.click()
    time.sleep(0.75)
    password_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@id='password']"))
    )
    password_element.send_keys(password)
    btn = driver.find_element(
        By.XPATH, "//button[starts-with(text(),'Continue') and @data-action-button-primary]")
    btn.click()
    logging.info(f"Logging as {email} ...")


def skip_popups(driver):
    time.sleep(3)
    try:
        skip = driver.find_element(
            By.XPATH, "//div[starts-with(text(),'Okay, let')]")
        skip.click()
    except NoSuchElementException:
        logging.info("* Skipping skip_popups")


def get_response(driver, prompt, waittime=90):
    inputElement = driver.find_element(
        By.XPATH, "//textarea[@id='prompt-textarea']")
    inputElement.send_keys(prompt)

    inputElement = WebDriverWait(driver, 1).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//button[@data-testid='send-button']"))
    )
    # time.sleep(0.25)
    # inputElement = driver.find_element(By.XPATH, "//button[@data-testid='send-button']")
    inputElement.click()

    element = WebDriverWait(driver, waittime).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[starts-with(@data-testid, 'conv')][last()]/descendant::div[starts-with(@class, 'markdown')]"))
    )
    response = element.text
    return response


if __name__ == "__main__":

    args = argparse.ArgumentParser()
    args.add_argument("--prompt",
                      default="This is an example prompt",
                      type=str)

    load_dotenv()
    arg_parse = args.parse_args()

    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    op = uc.ChromeOptions()
    op.add_argument("--headless")
    op.add_argument('--no-sandbox')
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument(f"--user-agent={UserAgent.random}")
    op.add_argument("--user-data-dir=selenium-data/")

    driver = uc.Chrome(options=op,
                       use_subprocess=False)

    redirect_mainscreen(driver, args=arg_parse)
    skip_popups(driver)
    question = "Việc trích lập dự phòng nghiệp vụ của doanh nghiệp kinh doanh bảo hiểm phải bảo đảm những yêu cầu nào?"
    passage = "Khoản 2 Điều 97 Luật Kinh doanh bảo hiểm 2022 quy định về các yêu cầu với việc trích lập dự phòng nghiệp vụ như sau: Dự phòng nghiệp vụ 1. Dự phòng nghiệp vụ là khoản tiền mà doanh nghiệp bảo hiểm, doanh nghiệp tái bảo hiểm, chi nhánh nước ngoài tại Việt Nam phải trích lập nhằm mục đích thanh toán cho những trách nhiệm bảo hiểm có thể phát sinh từ các hợp đồng bảo hiểm đã giao kết. 2. Việc trích lập dự phòng nghiệp vụ phải bảo đảm các yêu cầu sau đây: a) Trích lập riêng cho từng nghiệp vụ bảo hiểm; b) Tương ứng với phần trách nhiệm đã cam kết theo thỏa thuận trong hợp đồng bảo hiểm; c) Tách biệt giữa các hợp đồng bảo hiểm của đối tượng bảo hiểm trong và ngoài phạm vi lãnh thổ Việt Nam, kể cả trong cùng một nghiệp vụ bảo hiểm, sản phẩm bảo hiểm, trừ trường hợp pháp luật có quy định khác; d) Luôn có tài sản tương ứng với dự phòng nghiệp vụ đã trích lập, đồng thời tách biệt tài sản tương ứng với dự phòng quy định tại điểm c khoản này; đ) Sử dụng Chuyên gia tính toán để tính toán, trích lập dự phòng nghiệp vụ; e) Thường xuyên rà soát, đánh giá việc trích lập dự phòng nghiệp vụ; kịp thời có các biện pháp nhằm bảo đảm trích lập đầy đủ dự phòng để chi trả cho các trách nhiệm của doanh nghiệp bảo hiểm, doanh nghiệp tái bảo hiểm, chi nhánh nước ngoài tại Việt Nam. ... "
    prompt = f"Trả lời bằng Tiếng Việt, Ngữ cảnh được cung cấp ở phần ** có thể dùng để trả lời Câu hỏi ở phần ** không? Nếu có thì trả lời là True nếu không thì trả lời False.     Ngữ cảnh:   * {passage} *      Câu hỏi: * {question} *"
    prompt_preprocess = prompt.replace("\n", " "*4)
    print(prompt_preprocess)

    logging.info(f"Your prompt is: {arg_parse.prompt}")
    response = get_response(driver, prompt_preprocess)
    logging.info(f'ChatGPT answer: {response}')
    driver.close()
