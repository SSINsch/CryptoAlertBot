from typing import Dict, List
import yaml
import requests
import time
import telegram
import json


def load_config(config_file: str) -> Dict:
    """
    loads the config file
    :param config_file: path
    :return: config dictionary
    """
    with open(config_file, "r", encoding="utf-8") as f:
        _config = yaml.safe_load(f)

    return _config


def load_address(file: str) -> List[str]:
    """
    loads the address from file
    :param file: path of the file
    :return: list of address
    """
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    target_address = set()

    # dict item contains only one date key-value
    dict_token_address = list(data.values())[0]

    # update address
    for k in dict_token_address:
        target_address.update(dict_token_address[k])

    return list(target_address)


def load_last_tx_hashes(tx_file: str) -> Dict[str, str]:
    """
    loads the last tx hashes from file
    :param tx_file: tx hashes file
    :return: address-tx hashes dictionary
    """
    try:
        with open(tx_file, "r") as f:
            return json.load(f)

    except FileNotFoundError as fe:
        print(f'file not found: {tx_file}')
        return {}


def get_latest_transaction(address: str,
                           arkham_api_key: str,
                           sleep_time: int=3):
    """
    get the latest transaction from the arkham api
    :param address: wallet address
    :param arkham_api_key: ARKHAM api key
    :param sleep_time: sleep time
    :return: transaction information
    """
    url = f"https://api.arkhamintelligence.com/v1/addresses/{address}/transactions"
    headers = {"Authorization": f"Bearer {arkham_api_key}"}
    response = requests.get(url, headers=headers)
    time.sleep(sleep_time)

    if response.status_code == 200:
        data = response.json()
        transactions = data.get("transactions", [])
        if transactions:
            return transactions[0]

    return None


def send_telegram_alert(transaction: Dict[str, str],
                        address: str,
                        chat_id: str="AlertBot") -> None:
    """
    send telegram alert
    :param transaction: transaction information from arkham api
    :param address: wallet address
    :param chat_id: ID of telegram chatbot
    :return:
    """
    message = (f"New Transaction in {address}\n"
               f"\t[Info] {transaction['from']} -> {transaction['to']}\n"
               f"\t[Hash] {transaction['hash']}"
               f"\t[Current] {transaction['asset']}: {transaction['value']}\n")
    bot.send_message(chat_id=chat_id, text=message)


def save_last_tx_hashes(tx_file: str):
    """
    save the last tx hashes from file
    :param tx_file: path of the tx hashes file
    :return:
    """
    with open(tx_file, "w") as f:
        json.dump(last_tx_hashes, f)


def main(target_addresses: List[str],
         tx_hashes: Dict[str, str],
         arkham_api_key: str,
         tx_file: str,
         chat_id: str="AlertBot") -> None:
    """
    main function
    :param target_addresses: target wallet addresses from json file given by Sponsor
    :param tx_hashes: address-tx hashes
    :param arkham_api_key: ARKHAM api key
    :param tx_file: file for saving (address - last tx hashes)
    :param chat_id: ID of telegram chatbot
    :return:
    """
    while True:
        for address in target_addresses:
            transaction = get_latest_transaction(address, arkham_api_key=arkham_api_key)
            if transaction and transaction['hash'] != tx_hashes.get(address):
                send_telegram_alert(transaction, address, chat_id=chat_id)
                tx_hashes[address] = transaction['hash']
                save_last_tx_hashes(tx_file)

        time.sleep(60 * 5)


if __name__ == "__main__":
    # 설정값
    config = load_config("my-setting.yml")
    ARKHAM_API_KEY = config['ARKHAM_API_KEY']
    TELEGRAM_BOT_TOKEN = config['TELEGRAM_BOT_TOKEN']
    CHAT_ID = config['CHAT_ID']
    last_tx_file = config['LAST_TX_FILE']
    path_hacker_address = config['PATH_HACKER_ADDRESS']

    # load target address from hacker-address.json
    new_address = load_address(path_hacker_address)

    # load last transaction file
    last_tx_hashes = load_last_tx_hashes(last_tx_file)

    # Telegram 봇 초기화
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

    main(target_addresses=new_address,
         tx_hashes=last_tx_hashes,
         arkham_api_key=ARKHAM_API_KEY,
         tx_file=last_tx_file,
         chat_id=CHAT_ID)
