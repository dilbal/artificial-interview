import requests 
from config import CANDIDATE_API_KEY, BASE_URL, MODEL_NAME

class LLMClient:
    def __init__(self, api_key=CANDIDATE_API_KEY, base_url=BASE_URL, model=MODEL_NAME):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
    
    def get_response(self, prompt):
        #send prompt to LLM and return response text. 
        try:
            # Build and send request
            response = requests.post(
                self.base_url,
                headers={
                    "Content-Type": "application/json",
                    "x-api-key": self.api_key
                },
                json={
                    "model": self.model,
                    "input": [
                        {
                            "role": "user",
                            "content": prompt  
                        }
                    ]
                },
                timeout=30  
            )
            
            # check if request was successful
            response.raise_for_status()
            
            # parse response
            data = response.json()
            
            # extract text from response
            if 'output' in data:
                for output_item in data['output']:
                    if output_item.get('type') == 'message':
                        content = output_item.get('content', [])
                        if content and len(content) > 0:
                            return content[0].get('text', '')
            
            # Fallback if structure is unexpected
            raise ValueError(f"Unexpected response structure: {data}")
                
        except requests.exceptions.RequestException as e:
            print(f"Error calling LLM API: {e}")
            raise
        except (KeyError, ValueError) as e:
            print(f"Error parsing LLM response: {e}")
            raise