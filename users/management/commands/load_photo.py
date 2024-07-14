import json
from django.core.management.base import BaseCommand
from django_classified.models import Image

class Command(BaseCommand):
    help = 'Load image data from a JSON file and save it to the database'

    def handle(self, *args, **kwargs):
        # Load data from JSON file
        with open('data.json') as f:
            data_json = json.load(f)

        # Iterate over each item in the JSON data
        for image_data in data_json:
            # Create a new Image instance and save it to the database
            image = Image.objects.create(
                file=image_data['file'],
                item_id=image_data['item_id'],
            )
            print(f"Image '{image.file}' saved successfully.")