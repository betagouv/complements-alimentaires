from .client import client
import json


def get_plain_text_names(ing_model):
    return "\n".join(ing_model.objects.values_list("name", flat=True).order_by("name"))


def match_ingredients(ing_list):
    instructions = """You are given a predefined list of ingredient names from a database at the end of these instructions. The user will send a list of ingredients.
    Your role is to search for ingredients from our list that could correspond to the ingredients the user sends.
    Return a json object where the original ingredient name is the key and the value is a list of possible matches. Order the matches by relevance. If there are no close matches, return an empty list.
    The predefined ingredient names are as followed, grouped by ingredient type with a markdown title heading.

    # Database ingredients
    """

    # have to import from here when running this method as a command
    from data.models import Plant, Microorganism, Substance, Ingredient

    instructions += "\n\n## Plants\n"
    instructions += get_plain_text_names(Plant)
    instructions += "\n\n## Microorganisms\n"
    instructions += get_plain_text_names(Microorganism)
    instructions += "\n\n## Ingredients\n"
    instructions += get_plain_text_names(Ingredient)
    instructions += "\n\n## Substances\n"
    instructions += get_plain_text_names(Substance)

    # print(instructions)

    response = client.beta.conversations.start(
        inputs=[
            {
                "role": "user",
                "content": json.dumps(ing_list),  # ', '.join(ing_list)
            }
        ],
        model="mistral-medium-latest",
        instructions=instructions,
        completion_args={
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 1,
            "response_format": {"type": "json_object"},
        },
        tools=[],
    )

    # also interested in response.usage.total_tokens
    return json.loads(response.outputs[0].content)
