"""
Execution workflow

Input: declaration(s), URL(s), file(s)
Output: list of ingredients in our DB (eventually ingredients too) + maybe accuracy scores if passed declaration object + usage info

The steps:
0. (maybe will add in) use classification to determine if the image has ingredients and quantities
1. extract the ingredients lists by langauge
2. clean up the french list
3. match to our db

NB: configuration options to be modifyable eventually by interface
NB: the input and output of this pipeline to be API'd
NB: maybe want to be able to return outputs for intermediary steps for debugging purposes
"""

import json
from .mistral_pipeline import extract_lists, get_french_list, clean_ingredient_list, match_ingredients


# for now won't subclass this, since I am not sure. In the future a refacto could make it abstract and move
# the current implementation to a new class, without having to change usages
# input : documents/urls for one declaration
# output : declaration object with data filled in but not as a saved object in the database
# probs actually a representation bc want to be able to address the multi choice ingredient
class ProductLabelOCRPipeline:
    # a wrapper around whatever model we are using so we could switch it out easier
    # model = ...  # perhaps an enum
    # prompt = ...  # perhaps there are multiple
    debugger = []

    # def __init__(self, model, prompt):
    #     self.model = model
    #     self.prompt = prompt
    #     # etc

    def extract_french_list(self, urls):
        # TODO: handle the logic of having multiple documents to scan for ingredients
        # and choosing only one french list
        # TODO: what happens when there is no french list? Bubble up error and stop pipeline?
        url = urls[0]
        self.__log("extract_french_list 1", f"Using first URL only {url}")
        result = extract_lists(url)
        self.__log("extract_french_list 2", f"Lists: {json.dumps(result)}")
        french_list = get_french_list(result["ingredients_lists"])
        self.__log("extract_french_list 3", f"French list: {json.dumps(french_list)}")
        return french_list

    def clean_list(self, urls):
        french_list = self.extract_french_list(urls)
        cleaned_list = clean_ingredient_list(french_list)
        self.__log("clean_list", f"Clean list: {json.dumps(cleaned_list)}")
        return cleaned_list

    def match_to_db(self, urls):
        cleaned_list = self.clean_list(urls)
        # TODO: attempt match to db directly before resorting to AI tools?
        matched_list = match_ingredients(cleaned_list)
        self.__log("match_to_db", f"Matched: {json.dumps(matched_list)}")
        # TODO output: a dict of ingredient names as written in label with suggestions of ing objects
        """
        ingredient_options = {}
        for names, label_text in matched_list:
            ingredient_options[label_text] = []
            for ing_name in names:
                ing = db_search(ing_name)
                if ing:
                    ingredient_options[label_text].append(ing)
                else:
                    print(f"Proposed ingredient '{ing_name}' doesn't exist in db")
                # if multiple matches also print/throw error
        return ingredient_options
        """
        return matched_list

    def __reset_debugger(self):
        self.debugger = []

    def __log(self, step, message):
        # format of logs: {step: 'description of step', message: 'misc message'}
        self.debugger.append({"step": step, "message": message})

    def print_debugger(self):
        for log in self.debugger:
            print(f"{log['step']}: {log['message']}")

    # perhaps prefill_declaration or something is better
    # more generic, more expandable, still aligned with current work
    def extract_ingredients(self, urls):
        self.__reset_debugger()
        return self.__match_to_db(self.clean_list(self.extract_french_list(urls)))

    def __str__(self):
        return "Model A using prompts XYZ"


# Then there is the testing workflow

# Fetch X declaration objects randomly
# Run the pipeline
# Aggregate scores
# Compare against another report?
