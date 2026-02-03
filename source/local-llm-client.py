import requests

def analyze_log(file_path):
    # 1. ログファイルを読み込む
    with open(file_path, 'r', encoding='utf-8') as f:
        log_content = f.read()

    # 2. Ollama APIに送信するペイロードを作成
    # ログが巨大な場合は、末尾の数百行に絞るなどの処理を推奨
    payload = {
        "model": "gpt-oss:20b",
        "prompt": f"以下のログファイルを解析し、何が起きたか要約してください:\n\n{log_content}",
        "stream": False
    }

    # 3. Ollama APIにPOSTリクエストを送信
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    
    if response.status_code == 200:
        print("解析結果:", response.json()['response'])

analyze_log("./log/app.log")