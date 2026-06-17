from openai import OpenAI


def analyze_code(
    prompt,
    api_key,
    model_name,
    temperature
):

    client = OpenAI(
        api_key=api_key
    )

    response = client.chat.completions.create(
        model=model_name,
        temperature=temperature,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content