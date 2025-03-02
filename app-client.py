from pipelines.python_code_pipeline import Pipeline

pipline = Pipeline()
pipline.pipe("User message", "gpt-4", [{"message_1": "value_1"}], {"body_field": "value"})

