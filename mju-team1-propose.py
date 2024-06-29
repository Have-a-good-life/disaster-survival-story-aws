import json

import boto3


bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")


def done(err, res):
    if err:
        return f"Error: {err}"
    return res;

def create_prompt(data):
    best_react = "\n".join([f'{item}' for item in data["best_reactions"]])
    
    prompt = (
       "아래 모범 대응 항목을 기반으로 모범 대응 요령을 작성하라. 리스트로 작성하지말고 줄글의 형태로 200자 이내로 작성하라\n\n"
       f"{best_react}"
    )

    return prompt


def lambda_handler(event, context):
    try:
        best_reactions = event["bestReactions"]
        
        data = {
            "best_reactions": best_reactions,
        }

        prompt = create_prompt(data)


        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    }
                ],
            }
        )

        response = bedrock_runtime.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=body,
        )
        response_body = json.loads(response.get("body").read())

        result = response_body["content"][0]["text"]

        return done(None, result)
    except Exception as e:
        print(f"Error!!!: {e}")
        return done(e, "Error occured!")