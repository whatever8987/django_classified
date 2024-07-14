# Sample list of dictionaries
images = [
    {'item_id': '457', 'file': 'download_image_98_13_xkdlolqd.jpg'},
    {'item_id': '457', 'file': 'download_image_99_1_AfgmhaUK.jpg'},
    ]

# Function to set item_id in chunks of 4 starting from a specified number
def set_item_ids(images, chunk_size=4, start_number=458):
    item_id = start_number
    for i in range(0, len(images), chunk_size):
        for j in range(i, min(i + chunk_size, len(images))):
            images[j]['item_id'] = str(item_id)
        item_id += 1

# Set the starting number
start_number = 458

# Call the function with the starting number
set_item_ids(images, chunk_size=4, start_number=start_number)

# Print the modified list to check the result
for image in images:
    print(image)
