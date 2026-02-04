import requests

MODEL = "gpt-oss:20b"
API_URL = "http://localhost:11434/api/generate"
LOG_FILE = "./log/app.log"
PROMPT = "以下のログファイルを解析し、何が起きたか要約してください"

class LocalLLMClient:
  def __init__(self, model, api_url, log_file, prompt):
    self.model = model
    self.api_url = api_url
    self.log_file = log_file
    self.prompt = prompt
    self.log_content = ""

  def import_log(self):
    # ログファイルを読み込む
    with open(self.log_file, 'r', encoding='utf-8') as f:
      self.log_content = f.read()

  def main(self):
    # ログファイルをインポート
    self.import_log()
    
    # Ollama APIに送信するペイロードを作成
    # ログが巨大な場合は、末尾の数百行に絞るなどの処理を推奨
    payload = {
      "model": self.model,
      "prompt": f"{self.prompt}:\n\n{self.log_content}",
      "stream": False
    }

    try:
      # Ollama APIにPOSTリクエストを送信
      response = requests.post(self.api_url, json=payload)
    
      if response.status_code == 200:
        return response.json()['response']
      else:
        print(f"APIリクエストに失敗しました。ステータスコード: {response.status_code}")
        return None
    except Exception as e:
      print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
  client = LocalLLMClient(MODEL, API_URL, LOG_FILE, PROMPT)
  response = client.main()
  print("解析結果:", response)