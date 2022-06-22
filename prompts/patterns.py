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
    word_model = apps.get_model('prompts', model_name)
    # set max_id as the highest assigned id
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


def get_adjective():
    """
    Retrieves a randomly selected adjective from the Adjective database
    """
    # set max_id as the highest assigned id
    max_id = Adjective.objects.all().aggregate(max_id=Max("id"))["max_id"]

    # in case there are deletions (i.e. empty ids) in the database, use a while
    # loop to attempt 10 times to retrieve a random entry
    attempts = 0
    while attempts < 10:
        # set primary key equal to a random integer between 1 and the max id
        pk = random.randint(1, max_id)
        # find the corresponding database entry
        adjective = Adjective.objects.filter(pk=pk).first()

        if adjective:
            # if an entry is found, return the entry
            return adjective
        else:
            # if an entry is not found, iterate the attempts counter
            attempts += 1

    # if no entry was found in 10 attempts, return false
    return False


def get_creature():
    """
    Retrieves a randomly selected creature from the Creature database
    """
    # set max_id as the highest assigned id
    max_id = Creature.objects.all().aggregate(max_id=Max("id"))["max_id"]

    # in case there are deletions (i.e. empty ids) in the database, use a while
    # loop to attempt 10 times to retrieve a random entry
    attempts = 0
    while attempts < 10:
        # set primary key equal to a random integer between 1 and the max id
        pk = random.randint(1, max_id)
        # find the corresponding database entry
        creature = Adjective.objects.filter(pk=pk).first()

        if adjective:
            # if an entry is found, return the entry
            return adjective
        else:
            # if an entry is not found, iterate the attempts counter
            attempts += 1

    # if no entry was found in 10 attempts, return false
    return False




def adjective_creature_activity_location():
    adjective = random.choice(list(adjectives))
    creature = random.choice(list(creatures))
    activity = random.choice(activities)
    location = random.choice(locations)
    result = (
        f"{adjective[0]} {adjective[1]} {creature[1]} {activity} {location}"
    )
    return result
