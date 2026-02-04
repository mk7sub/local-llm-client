import requests

class LocalLLMClient:
  def __init__(self, model, api_url, prompt):
    self.model = model
    self.api_url = api_url
    self.prompt = prompt
    self.log_content = ""

  def main(self):    
    # Ollama APIに送信するペイロードを作成
    # ログが巨大な場合は、末尾の数百行に絞るなどの処理を推奨
    payload = {
      "model": self.model,
      "prompt": self.prompt,
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

  log_content = ""
  with open("./log/app.log", 'r', encoding='utf-8') as f:
    log_content = f.read()
  
  prompt = "以下のログファイルを解析し、何が起きたか要約してください" + "\n\n" + log_content

  client = LocalLLMClient(
      "gpt-oss:20b",
      "http://localhost:11434/api/generate",
      prompt
    )
  response = client.main()
  print("解析結果:", response)