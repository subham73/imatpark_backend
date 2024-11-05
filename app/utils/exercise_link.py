import requests
from bs4 import BeautifulSoup
import json

######################################################################
# Task: Extract all the exercises and their links from the website
baseUrl = "https://www.strengthlog.com/exercise-directory/"

response = requests.get(baseUrl)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')
categories = soup.find_all('ol', class_='wp-block-list')

AllExerciseList = [] # List to store all exercises [{category, {exercise, url}}]
for category in categories:
    exercises_data = category.find_all('li')
    for exercise_data in exercises_data:
        exercise_name = exercise_data.text
        exercise_link = exercise_data.a['href']
        exercise = {
            "name": exercise_name,
            "url": exercise_link
        }
        AllExerciseList.append(exercise)

for exercise_data in AllExerciseList:
    print(exercise_data)

print(len(AllExerciseList))

#write the data to a file
import json
with open('exercises_link_data.json', 'w') as f:
    json.dump(AllExerciseList, f, indent=4)




