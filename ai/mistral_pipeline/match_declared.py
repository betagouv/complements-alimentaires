# pairing names read from a label with names taken from the declaration, when
# only a pairing beyond doubt is of any use to the caller
from .client import client, add_format_boilerplate
from .throttle import throttled
import json

DEFAULT_INSTRUCTIONS = """You are given two lists of ingredient names of the same food supplement, 'candidates' read from its label and 'declared' taken from the declaration filed by its producer.
Return an object with a key 'matches' holding an array of objects with the keys 'candidate' and 'declared', pairing a candidate with the declared name that designates the same ingredient.
Only return a pair you are certain of, leave out every candidate you cannot pair with certainty, and never return a name that is absent from the list it is given for."""


# returns the pairs as read from the model, so that the caller can check them
# against the lists it sent
@throttled
def match_declared_names(
    candidates,
    declared,
    model="mistral-medium-latest",
    instructions=DEFAULT_INSTRUCTIONS,
    # pairing names is a deterministic task, and a creative model pairs names
    # that merely look alike
    temperature=0.1,
):
    schema = {
        "properties": {
            "matches": {
                "items": {
                    "properties": {
                        "candidate": {
                            "description": "the name, copied exactly, from the 'candidates' list sent by the user",
                            "type": "string",
                        },
                        "declared": {
                            "description": "the name, copied exactly, from the 'declared' list sent by the user",
                            "type": "string",
                        },
                    },
                    "required": ["candidate", "declared"],
                    "type": "object",
                },
                "type": "array",
            }
        },
        "required": ["matches"],
        "type": "object",
    }
    response = client.beta.conversations.start(
        inputs=[
            {
                "role": "user",
                "content": json.dumps({"candidates": candidates, "declared": declared}, ensure_ascii=False),
            }
        ],
        model=model,
        instructions=instructions,
        completion_args={
            "temperature": temperature,
            "max_tokens": 2048,
            "top_p": 1,
            "response_format": add_format_boilerplate(schema),
        },
        tools=[],
    )
    return json.loads(response.outputs[0].content)["matches"]
