import time
import os
import json
import logging
import shutil
import copy

import undetected_chromedriver as uc
from fake_useragent import UserAgent

from SeleniumChatGPT import get_response, openai_login, skip_popups
from selenium.common.exceptions import WebDriverException


def get_driver_with_account(account, password, data_user_folder):

    op = uc.ChromeOptions()
    # op.add_argument("--headless")
    op.add_argument('--no-sandbox')
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument(f"--user-agent={UserAgent.random}")
    op.add_argument(f"--user-data-dir=selenium-data/{data_user_folder}/")
    op_copy = copy.deepcopy(op)

    try:
        driver = uc.Chrome(options=op, use_subprocess=True)
    except WebDriverException as e:
        logging.info("Unknown Bug " + str(e))
        logging.info(e.stacktrace)
        logging.info("Attempting to debug the exception")
        selenium_data_path = f"selenium-data/{data_user_folder}/"
        if os.path.exists(selenium_data_path):
            shutil.rmtree(selenium_data_path)
            logging.info(f"Delete folder {selenium_data_path}")
            driver = uc.Chrome(options=op_copy, use_subprocess=True)

        else:
            logging.info(
                f"There is not exist {selenium_data_path} to delete and debug.")
            raise (e)

    driver.get("https://chat.openai.com/")
    time.sleep(5)
    curent_url = driver.current_url
    if "login" in curent_url:
        try:
            openai_login(driver, account, password)
            time.sleep(10)
        except Exception as e:
            logging.info("--------------------------------")
            logging.info(f"Something wrong when logging as {account}.")
            logging.info("--------------------------------")
            raise (e)

    skip_popups(driver)
    return driver


def one_account_tvlp_generate_feeds(driver, args):

    # Read normal jsonl data
    with open(args.path, encoding="utf8") as json_file:
        qa_data = json.load(json_file)
        len_qa_data = len(qa_data)

    # if os.path.exists(args.output_tvlp_path):
    #     with open(args.output_tvlp_path) as json_file:
    #         qa_data_generated = json.load(json_file)

    # else:
    #     qa_data_generated = {}  # id -> answer

    count = 0
    idx_qa = 0
    for idx, qa in enumerate(qa_data):
        if "oke" in qa.keys():
            if "'True'" in qa["oke"] or "'False'" in qa["oke"] or "True" in qa["oke"] or "False" in qa["oke"]:
                continue

        start_time = time.time()
        passage = qa["context"]
        question = qa["question"]
        prompt = f"""
You are a Vietnamese , you can understand anything in Vietnamese. You are also a good researcher and you have ability to read a passage, think step by step and decide whether the information in the passage can be use to find the answer for any questions.


Cho ngữ cảnh sau

'{passage}'

Liệu ngữ cảnh trên có thể dùng để trả lời câu hỏi '{question}' không? Hãy giải thích chi tiết và trả lời ở CUỐI CÂU là True nếu có và False nếu không, lưu ý True và False phải được đặt ở cuối câu.

OUTPUT:
"""
        # https://stackoverflow.com/questions/33783394/selenium-webdriver-enter-multiline-text-in-form-without-submitting-it
        # prompt_preprocess = prompt.replace("\n", Keys.chord(Keys.SHIFT, Keys.ENTER));
        prompt_preprocess = prompt
        try:
            response = get_response(
                driver, prompt=prompt_preprocess, waittime=100)
            count += 1
            qa["oke"] = response.strip()
            logging.info(
                f"Question ID {idx+1}/{len_qa_data}  - {time.time() - start_time:.3f}s - {response[:30]} ... {response[-30:]}")

            if not count % args.save_rate:
                with open(args.path, "w", encoding="utf8") as json_file:
                    json.dump(qa_data, json_file)
                    logging.info(
                        f"Save results at {args.path}")

            time.sleep(3)

        except Exception as e:
            with open(args.path, "w", encoding='utf8') as json_file:
                json.dump(qa_data, json_file)
                logging.info(f"Save results at {args.path}")

            raise (e)

    with open(args.output_tvlp_path, "w", encoding="utf8") as json_file:
        json.dump(qa_data, json_file)
        logging.info(f"Save results at {args.output_tvlp_path}")

    logging.info("Finish.")
    logging.info(count)
