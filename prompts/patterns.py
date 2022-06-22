import random

from django.db.models import Max
from django.apps import apps

from .models import Activity, Adjective, Creature, Location


# random selection function is based on this method for efficiently selecting
# random objects from a django model:
# https://books.agiliq.com/projects/django-orm-cookbook/en/latest/random.html

def get_word(model_name):
    """
    Retrieves a randomly selected prompt word from the requested model
    """
    # find the requested model
    word_model = apps.get_model("prompts", model_name)
    # set max_id as the highest assigned id in the model
    max_id = word_model.objects.all().aggregate(max_id=Max("id"))["max_id"]

    # in case there are deletions (i.e. empty ids) in the database, use a while
    # loop to attempt 10 times to retrieve a random entry
    attempts = 0
    while attempts < 10:
        # set primary key equal to a random integer between 1 and the max id
        pk = random.randint(1, max_id)
        # find the corresponding database entry
        word = word_model.objects.filter(pk=pk).first()

        if word:
            # if an entry is found, return the entry
            return word
        else:
            # if an entry is not found, iterate the attempts counter
            attempts += 1

    # if no entry was found in 10 attempts, return false
    return False


def adjective_creature_activity_location():
    """
    Generates and returns a drawing prompt in the format of the function name
    """
    # use get_word function to get values for all required words
    adjective = get_word("Adjective")
    creature = get_word("Creature")
    activity = get_word("Activity")
    location = get_word("Location")
    # if all values are found
    if adjective and creature and activity and location:
        # generate prompt and return
        result = (
            f"{adjective.determiner} {adjective.adjective} {creature.creature}"
            f" {activity.activity} {location.location}"
        )
        return result
    else:
        # if a get_word failed, return false
        return False


def adjective_creature_activity():
    """
    Generates and returns a drawing prompt in the format of the function name
    """
    adjective = get_word("Adjective")
    creature = get_word("Creature")
    activity = get_word("Activity")
    # if all values are found
    if adjective and creature and activity:
        # generate prompt and return
        result = (
            f"{adjective.determiner} {adjective.adjective} {creature.creature}"
            f" {activity}"
        )
        return result
    else:
        # if a get_word failed, return false
        return False


def adjective_creature():
    """
    Generates and returns a drawing prompt in the format of the function name
    """
    adjective = get_word("Adjective")
    creature = get_word("Creature")
    # if all values are found
    if adjective and creature:
        # generate prompt and return
        result = (
            f"{adjective.determiner} {adjective.adjective} {creature.creature}"
        )
        return result
    else:
        # if a get_word failed, return false
        return False


def creature_activity_location():
    """
    Generates and returns a drawing prompt in the format of the function name
    """
    creature = get_word("Creature")
    activity = get_word("Activity")
    location = get_word("Location")
    # if all values are found
    if creature and activity and location:
        # generate prompt and return
        result = (
            f"{creature.determiner} {creature.creature} {activity} "
            f"{location.location}"
        )
        return result
    else:
        # if a get_word failed, return false
        return False


def creature_activity():
    """
    Generates and returns a drawing prompt in the format of the function name
    """
    creature = get_word("Creature")
    activity = get_word("Activity")
    # if all values are found
    if creature and activity:
        # generate prompt and return
        result = f"{creature.determiner} {creature.creature} {activity}"
        return result
    else:
        # if a get_word failed, return false
        return False


def adjective_creature_location():
    """
    Generates and returns a drawing prompt in the format of the function name
    """
    adjective = get_word("Adjective")
    creature = get_word("Creature")
    location = get_word("Location")
    # if all values are found
    if adjective and creature and location:
        # generate prompt and return
        result = (
            f"{adjective.determiner} {adjective.adjective} {creature.creature}"
            f" {location.location}"
        )
        return result
    else:
        # if a get_word failed, return false
        return False


def creature_location():
    """
    Generates and returns a drawing prompt in the format of the function name
    """
    creature = get_word("Creature")
    location = get_word("Location")
    # if all values are found
    if creature and location:
        # generate prompt and return
        result = (
            f"{creature.determiner} {creature.creature} {location.location}"
        )
        return result
    else:
        # if a get_word failed, return false
        return False
