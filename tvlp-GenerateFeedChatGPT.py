import time
import argparse
import os
import json
import logging

import undetected_chromedriver as uc
from fake_useragent import UserAgent
from selenium.common.exceptions import TimeoutException

from SeleniumChatGPT import redirect_mainscreen, skip_popups, get_response, openai_login

def tvlp_generate_feeds(driver, args):

    # Read normal jsonl data
    with open(args.input_tvlp_path) as json_file:
        qa_data = json.load(json_file)
        len_qa_data = len(qa_data)

    if os.path.exists(args.output_tvlp_path):
        with open(args.output_tvlp_path) as json_file:
            qa_data_generated = json.load(json_file)

    else:
        qa_data_generated = {} #id -> answer 
    
    count = 0
    time_exception_count = 0
    idx_qa = 0
    while idx_qa < len(qa_data):
        qa =  qa_data[idx_qa]
        idx = qa["id"]
        if str(idx) in qa_data_generated:
            idx_qa += 1
            continue
        else:
            start_time = time.time()
            passage = qa["passage"]
            question = qa["question"]
            prompt = f"Trả lời bằng Tiếng Việt.     Ngữ cảnh:    {passage}       Câu hỏi: {question}"
            # https://stackoverflow.com/questions/33783394/selenium-webdriver-enter-multiline-text-in-form-without-submitting-it
            # prompt_preprocess = prompt.replace("\n", Keys.chord(Keys.SHIFT, Keys.ENTER));
            prompt_preprocess = prompt.replace("\n", " "*4);
            try:
                response = get_response(driver, prompt=prompt_preprocess)
                count += 1
                time_exception_count = 0


            except TimeoutException as e:
                logging.info("Bug ..... " + str(e))
                logging.info(e.stacktrace)
                with open(args.output_tvlp_path, "w") as json_file:
                    json.dump(qa_data_generated, json_file)
                    logging.info(f"Save results at {args.output_tvlp_path}")

                time_exception_count +=1 
                if time_exception_count == 4:
                    logging.info(f"Time out. Sleep {args.break_time}s ...")
                    time.sleep(args.break_time)

                driver.delete_all_cookies()
                time.sleep(10)


                account = accounts.pop()
                accounts.insert(0, account)

                openai_login(driver, email=account[0], password=account[1])
                skip_popups(driver)
                continue

            except Exception as e:
                with open(args.output_tvlp_path, "w") as json_file:
                    json.dump(qa_data_generated, json_file)
                    logging.info(f"Save results at {args.output_tvlp_path}")

                raise(f"Bug at question {idx}: " + str(e))

            qa_data_generated[idx] = response.strip()
            logging.info(f"Question {idx}/{len_qa_data-1} - {time.time() - start_time:.3f}s - {response[:30]} ... {response[-30:]}")

            if not count % args.save_rate:
                with open(args.output_tvlp_path, "w") as json_file:
                    json.dump(qa_data_generated, json_file)
                    logging.info(f"Save results at {args.output_tvlp_path}")

            time.sleep(3)
            idx_qa += 1


    with open(args.output_tvlp_path, "w") as json_file:
        json.dump(qa_data_generated, json_file)    
        logging.info(f"Save results at {args.output_tvlp_path}")


    logging.info("Finish.")

if __name__ == "__main__":

    DATA_FOLDER = "tvpl_data"
    args = argparse.ArgumentParser()

    args.add_argument("--account_path", 
                    default="account.txt", 
                    type=str)

    args.add_argument("--input_tvlp_path", 
                    default=os.path.join(DATA_FOLDER, "QA_Law_ID.json"), 
                    type=str)

    args.add_argument("--output_tvlp_path",
                    default=os.path.join(DATA_FOLDER, "QA_Law_Generated.json"), 
                    type=str)
    
    args.add_argument("--save_rate",
                      default=10,
                      type=int)
    
    args.add_argument("--break_time",
                      default=1000,
                      type=int)

    arg_parse = args.parse_args()

    accounts = []
    with open(arg_parse.account_path) as f:
        for line in f:
            accounts.append(line.strip().split(","))

    logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
    
    op = uc.ChromeOptions()
    # op.add_argument("--headless")
    op.add_argument('--no-sandbox') 
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument(f"--user-agent={UserAgent.random}")
    op.add_argument("--user-data-dir=selenium-data/")

    driver = uc.Chrome(options=op, use_subprocess=True)

    redirect_mainscreen(driver, args=arg_parse)
    skip_popups(driver)
    tvlp_generate_feeds(driver, args=arg_parse)
    driver.close()