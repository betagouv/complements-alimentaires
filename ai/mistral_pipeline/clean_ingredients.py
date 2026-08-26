from .client import client
import json


def clean_ingredient_list(ing_list):
    response = client.beta.conversations.start(
        inputs=[{"role": "user", "content": json.dumps(ing_list)}],
        model="mistral-medium-latest",
        instructions="Given a series of strings by the user, return an object with a key 'ingredients' with an array of the ingredient names.\nWhere a scientific name is given, return only the scientific name.",
        completion_args={
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 1,
            "response_format": {"type": "json_object"},
        },
        tools=[],
    )
    # also interested in response.usage.total_tokens
    return json.loads(response.outputs[0].content)["ingredients"]
