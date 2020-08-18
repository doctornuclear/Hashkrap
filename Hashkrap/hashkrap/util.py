import requests

def send_telegram_msg(username, keyword, sort_by):
    text = "Username: " + username + "\n" + "Keyword: " + keyword + "\nSort by: " + sort_by
    params = {"chat_id": 476539155, "text": text}
    requests.get("https://api.telegram.org/bot1261577950:AAFMyHHafrmeVt5453JXucktQ4hPtP3uAWU/sendMessage",
                 params=params)