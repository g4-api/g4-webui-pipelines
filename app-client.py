from pipelines.open_ai_proxy_pipeline import Pipeline

pipline = Pipeline()

response = pipline.pipe(
    user_message="User message",
    model_id="gpt-4",
    messages=[{"role": "user", "content": "hi!"}],
    body={"stream": True})

print(response)
