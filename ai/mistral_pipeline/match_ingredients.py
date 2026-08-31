from .client import client
import json


def get_plain_text_names(ing_model):
    return "\n".join(ing_model.objects.values_list("name", flat=True).order_by("name"))


# input: list of ingredient names as strings
# output: dict of ingredient name to db ingredient objects
def match_ingredients(ing_list):
    from api.utils.search import search_elements

    print(f"matching {len(ing_list)} ingredients")
    list_for_ai = []
    matches = {}

    # match against our db first before trying with AI
    for ingredient in ing_list:
        search_results = search_elements({"term": ingredient})
        if not search_results:
            list_for_ai.append(ingredient)
        else:
            matches[ingredient] = search_results

    if len(list_for_ai):
        # TODO: send these messages to the debugger logs
        print(f"matching {len(list_for_ai)} ingredients with ai")
        print(list_for_ai)
        foo = match_ingredients_with_ai(list_for_ai)

        for ing, suggestions in foo.items():
            matches[ing] = []
            for ingredient in suggestions:
                search_results = search_elements({"term": ingredient})
                if search_results:
                    matches[ing] += search_results
                else:
                    print("no match for suggestion: ", ingredient)

    return matches


def match_ingredients_with_ai(ing_list):
    instructions = """You are given a predefined list of ingredient names from a database at the end of these instructions. The user will send a list of ingredients.
    Your role is to search for ingredients from our list that could correspond to the ingredients the user sends.
    Return a json object where the original ingredient name is the key and the value is a list of possible matches. Order the matches by relevance. If there are no close matches, return an empty list.
    The predefined ingredient names are as followed, grouped by ingredient type with a markdown title heading.

    # Database ingredients
    """

    # have to import from here when running this method as a command
    from data.models import Plant, Microorganism, Substance, Ingredient

    instructions += "\n\n## Ingredients\n"
    instructions += get_plain_text_names(Ingredient)
    instructions += "\n\n## Substances\n"
    instructions += get_plain_text_names(Substance)
    instructions += "\n\n## Plants\n"
    instructions += get_plain_text_names(Plant)
    instructions += "\n\n## Microorganisms\n"
    instructions += get_plain_text_names(Microorganism)

    response = client.beta.conversations.start(
        inputs=[
            {
                "role": "user",
                "content": json.dumps(ing_list, ensure_ascii=False),  # ', '.join(ing_list)
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
    print("Total tokens, match_ingredients", response.usage.total_tokens)
    return json.loads(response.outputs[0].content)
