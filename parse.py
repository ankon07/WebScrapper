import requests

# Use a smaller, faster Hugging Face model (e.g., GPT-2)
HF_API_URL = "https://api-inference.huggingface.co/models/01-ai/Yi-1.5-34B-Chat"  # Updated model URL
HF_API_KEY = "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"  # Replace with your Hugging Face API key

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}.\n"
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}.\n"
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response.\n"
    "3. **Empty Response:** If no information matches the description, return an empty string ('').\n"
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def query_huggingface(payload):
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    return response.json()

def parse_with_huggingface(dom_chunks, parse_description):
    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        # Create the prompt using the template and chunk
        prompt = template.format(dom_content=chunk, parse_description=parse_description)
        
        # Sending the prompt to Hugging Face Inference API
        payload = {
            "inputs": prompt,
            "parameters": {"max_length": 1500}  # Adjust token limit as needed
        }
        
        response = query_huggingface(payload)
        
        # Extracting the text response
        parsed_response = response[0].get('generated_text', "")
        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(parsed_response)

    return "\n".join(parsed_results)
