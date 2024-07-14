import json
from django_classified.models import Item
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'load item'

    def handle(self, *args, **kwargs):


# Load data from JSON file
        with open('data.json') as f:
            data_json = json.load(f)

# Iterate over each item in the JSON data
        for item_data in data_json:
        # Create a new Item instance and save it to the database
            item = Item.objects.create(
            title=item_data['title'],
            description=item_data['description'],
            user_id=item_data['user_id'],
            area_id=item_data['area_id'],
            group_id=item_data['group_id'],
            is_active=item_data['is_active']
            )


    # Print a message indicating that the item has been saved
            print(f"Item '{item.title}' saved successfully.")