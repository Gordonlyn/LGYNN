import requests
import json

COURSE_ID = "spr25"
correct_model = "gpt-3.5-turbo"
url = "https://us-central1-codeinplace-production.cloudfunctions.net/notopenai"

class NotOpenAI:
    def __init__(self, api_key='your_default_api_key'):
        NotOpenAI.api_key = api_key
        

    class chat:
        def __init__(self, parent):
            self.parent = parent
            # self.completions = self.completions(self)  # Correctly initialize completions here

        class completions:

            @staticmethod
            def create(messages, model, response_format={"type": "text"}):
                
                # make sure the model is correct
                if model != correct_model:
                    raise ValueError(f"Model {model} not supported. We only support {correct_model}")
                
                # make sure the messages are formatted correctly. eg:
                """
                messages=[
                    {
                        "role": "user",
                        "content": "What is the capital of Malaysia? Reply in json",
                    }
                ]
                """
                if not isinstance(messages, list):
                    raise ValueError("messages should be a list")
                if len(messages) == 0:
                    raise ValueError("messages should not be empty")
                for message in messages:
                    if not isinstance(message, dict):
                        raise ValueError("Each message should be a dictionary")
                    if "role" not in message:
                        raise ValueError("Each message should have a role")
                    if "content" not in message:
                        raise ValueError("Each message should have content")
            

                # Data payload to send in the POST request
                data = {
                    # "model": model, we only support gpt-3.5-turbo
                    "messages": messages,
                    "response_format":response_format,
                    "api_key": NotOpenAI.api_key,
                    "course_id": COURSE_ID
                }

                # Convert the data payload to a JSON-formatted string
                json_data = json.dumps(data)

                # Headers to indicate the payload is JSON
                headers = {'Content-Type': 'application/json'}

                # Make a POST request to the Firebase Cloud Function
                response = requests.post(url, data=json_data, headers=headers)

                # Check if the request was successful
                if response.status_code == 200:
                    # Function call was successful, print the response
                    return Completion(response.text)
                else:
                    # There was an error
                    raise ValueError({response.text})
                
class Completion:
    def __init__(self, message):
        self.choices = [Message(Content(message))]

    def __str__(self):
        as_str = f"{{ \"choices\": {self.choices}}}"
        return json.dumps(json.loads(as_str), indent=2)

class Message:
    def __init__(self, message):
        self.message = message
      
    def __str__(self):
        as_str = f"{{ \"message\": {self.message}}}"
        return json.dumps(json.loads(as_str), indent=2)
    
    def __repr__(self):
        return self.__str__()

class Content:
    def __init__(self, content):
        self.content = content

    def __str__(self):
        as_str = f"{{ \"content\": {self.content}}}"
        return json.dumps(json.loads(as_str), indent=2)
    
    def __repr__(self):
        return self.__str__()
