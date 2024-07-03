import ollama

stream = ollama.chat(
    model='qwen2:1.5b-instruct-q8_0',
    messages=[{'role': 'system', 'content': 'you are an expert task analyst and a senior programmer. Your job is the to divide the given task into as amny subtask tasks as possible and provide them as json object with each subtask nested inside parent task and also provide he parameters associated with each subtask. Try to split the task as much as possible. Don''t output anything apart from json.'},
     {'role': 'user', 'content': 'Give me the steps to create an angular web application with a login page, a landing page and side menu and header and report option. Be as creative as possible'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)
