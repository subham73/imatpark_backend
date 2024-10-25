#TODO, few exercises are not getting the details,
# need to fix it cz of the different div names,
#  like some has comment and some has commentary as div id

import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

# Load exercise_link file to get the links
with open('exercises_link_data.json', 'r') as f:
    datas = json.load(f)

exercisesDetails = []
for data in tqdm(datas, desc="Processing exercises"):
    url = data['url']
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    title = url.split('/')[-2]
    exercise_data = soup.find('div', class_='inside-article')

    primary_muscles_element = exercise_data.find('h3', id='h-primary-muscles-worked')
    if primary_muscles_element:
        primary_muscles = [li.text.strip() for li in primary_muscles_element.find_next('ul').find_all('li')]
    else:
        primary_muscles = ""

    secondary_muscles_element = exercise_data.find('h3', id='h-secondary-muscles-worked')
    if secondary_muscles_element:
        secondary_muscles = [li.text.strip() for li in secondary_muscles_element.find_next('ul').find_all('li')]
    else:
        secondary_muscles = ""

    instructions_element = exercise_data.find('div', class_='wp-block-column is-layout-flow wp-block-column-is-layout-flow')
    if instructions_element:
        instructions = [li.text.strip() for li in instructions_element.find_next('ol').find_all('li')]
    else:
        instructions = ""

    comments_element = exercise_data.find('h2', id='h-commentary')
    if comments_element:
        comments = comments_element.find_next('p').text.strip()
    else:
        comments = ""

    exerciseDetails = {
        "title": title,
        "primary_muscles": primary_muscles,
        "secondary_muscles": secondary_muscles,
        "instructions": instructions,
        "comments": comments
    }
    exercisesDetails.append(exerciseDetails)

# Save the data to a JSON file
with open('exercise_details.json', 'w') as f:
    json.dump(exercisesDetails, f, indent=4)

# Print the extracted details
print(json.dumps(exercisesDetails, indent=4))