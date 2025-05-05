import csv
import random

# Load names from CSV file
def load_fake_names(file_path='fake_names.csv'):
    names = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            names.append((row['first_name'], row['last_name']))
    return names

# Get a random fake name
def get_fake_name(names_list):
    return random.choice(names_list)

# Example usage
if __name__ == '__main__':
    fake_names = load_fake_names('fake_names.csv')
    first_name, last_name = get_fake_name(fake_names)
    print(f"Fake name: {first_name} {last_name}")