import argparse
import os
import logging
import random
import time

from newTvlpOneAccount import get_driver_with_account, one_account_tvlp_generate_feeds

from selenium.common.exceptions import TimeoutException

if __name__ == "__main__":

    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    DATA_FOLDER = "data/generated"
    args = argparse.ArgumentParser()

    args.add_argument("--path",
                      # default=os.path.join(DATA_FOLDER, "QA_Law_ID.json"),
                      default=os.path.join(DATA_FOLDER, "dev.json"),
                      type=str)

    # args.add_argument("--output_tvlp_path",
    #                   # default=os.path.join(DATA_FOLDER, "QA_Law_Generated.json"),
    #                   default=os.path.join(DATA_FOLDER, "dev.json"),
    #                   type=str)

    args.add_argument("--save_rate",
                      default=10,
                      type=int)

    args.add_argument("--break_time",
                      default=1000,
                      type=int)

    args.add_argument("--account_path",
                      default="accounts.txt",
                      type=str)

    arg_parse = args.parse_args()

    accounts = []
    with open(arg_parse.account_path) as f:
        for line in f:
            accounts.append(line.strip().split("\t"))

    random.shuffle(accounts)
    print(accounts[0])
    idx = 0
    count_timeout = 0
    while True:
        account = accounts[idx % len(accounts)]
        logging.info([account[0]])
        mail = account[0]
        username, gmail = mail.split("@")
        password = account[1]
        folder_path = username.replace(
            ".", "-") + "-" + gmail.replace(".", "-")
        driver = get_driver_with_account(
            mail, password, folder_path)
        try:
            one_account_tvlp_generate_feeds(driver, arg_parse)
            # If there is no bug, bug is expected to move to another account
            break
        except TimeoutException as e:
            logging.info("Bug ..... " + str(e))
            logging.info(e.stacktrace)
            driver.close()
            idx += 1
            count_timeout += 1
            if count_timeout % len(accounts) == 0:
                logging.info(f"Time out. Sleep {600}s ...")
                time.sleep(600)
            continue
        except Exception as e:
            logging.info("Bug ..... " + str(e))
            logging.info(e.stacktrace)
            time.sleep(100)
            driver.close()
            logging.info(f"Time out. Sleep {100}s ...")
            continue
