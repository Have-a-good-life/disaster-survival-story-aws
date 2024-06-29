import json

import boto3


bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")


def done(err, res):
    if err:
        return f"Error: {err}"
    return res;

def create_prompt(data):
    situation = data["situation"]
    best_react = "\n".join([f'{item}' for item in data["best_reactions"]])
    user_react = data["user_reaction"]
    
    prompt = (
        "#상황은 사용자가 대응해야 하는 상황이다.\n"
        "#모범대응은 사용자의 모범적인 대응 항목이다.\n"
        "#사용자대응은 사용자가 직접 작성한 대응이다.\n"
        "모범대응의 내용을 기준으로 사용자의 대응을 평가하라. 별도의 형식 없이 반드시 200자 이내로 내용 작성하라.\n\n"
        f"#상황: {situation}\n"
        f"#모범대응:\n{best_react}\n"
        f"#사용자대응: {user_react}\n"
    )

    return prompt


def lambda_handler(event, context):
    try:
        print(event)
        situation = event["situation"]
        best_reactions = event["bestReactions"]
        user_reaction = event["userReaction"]
        
        data = {
            "situation": situation,
            "best_reactions": best_reactions,
            "user_reaction": user_reaction
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

        eval = response_body["content"][0]["text"]
        
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": eval + "를 보고 살았다면 '생존', 그렇지 않다면 '사망'이라고 답하라. 반드시 '생존' 또는 '사망'으로만 답하라."}],
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

        return done(None, eval + "/" + result)
    except Exception as e:
        print(f"Error!!!: {e}")
        return done(e, "Error occured!")