from local_llm_client import LocalLLMClient

class CheckAppLog(LocalLLMClient):
  def __init__(self, model, api_url, spec_file, log_file):
    super().__init__(model, api_url, "")
    self.spec_file = spec_file
    self.log_file = log_file

  def load_specification(self):
    with open(self.spec_file, 'r', encoding='utf-8') as f:
      return f.read()

  def load_log(self):
    with open(self.log_file, 'r', encoding='utf-8') as f:
      return f.read()
    
  def main(self):
    specification = self.load_specification()
    log_data = self.load_log()
    self.prompt = f"""
あなたはQAエンジニアです。以下の各テストケースとログを照合し、仕様通りであれば'PASS'、
異なる点があれば'FAIL'とその理由を簡潔に回答してください。
また、テストケースに存在しない仕様がログに記録されている場合、その内容を説明してください。

【テストケース】:
{specification}

【ログ】:
{log_data}
"""
    return super().main()

if __name__ == "__main__":
  model = 'gpt-oss:20b'
  api_url = 'http://localhost:11434/api/generate'
  spec_file = './testcase/test_cases.csv'
  log_file = './log/app_sample.log'
  check_app_log = CheckAppLog(model, api_url, spec_file, log_file)

  response = check_app_log.main()
  print("解析結果:", response)