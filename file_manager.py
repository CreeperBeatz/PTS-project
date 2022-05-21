import pandas as pd
import os
import json

'''
For now, the files are hard coded for simplicity
'''


def make_grade_to_visited_courses():
    '''
    Creation of a data structure for easier math analysis
    '''
    grade_visited_courses = []

    # Map grade to user id's
    user_grades_df = pd.read_excel(os.path.join(
        "public", "Grades.xlsx"))
    user_grades_df.reset_index()  # prepare for iteration
    for _, row in user_grades_df.iterrows():
        # check if that user id has been registered
        if any(grade_visited_courses_row.get('id') == int(row[0]) for grade_visited_courses_row in grade_visited_courses):
            index = next((i for i, item in enumerate(
                grade_visited_courses) if item["id"] == int(row[0])), None)
            grade_visited_courses[index]['grade'] = float(row[1])
        else:
            grade_visited_courses.append({'id': int(row[0]),
                                          'times_visited_courses': 0,
                                          'grade': float(row[1])})

    # Get all activities where user viewed a course
    activities_list = get_activity_per_user(None)
    filtered_activities = [
        lecture_viewed for lecture_viewed in activities_list if "viewed the 'resource' activity with course module id" in lecture_viewed[1]]

    # Map times visiting a course to user id
    for row in filtered_activities:
        # check if that user id has been registered
        if any(grade_visited_courses_row.get('id') == row[0] for grade_visited_courses_row in grade_visited_courses):
            index = next((i for i, item in enumerate(
                grade_visited_courses) if item["id"] == row[0]), None)
            grade_visited_courses[index]['times_visited_courses'] += 1
        else:
            pass  # User doesn't have a grade

    return grade_visited_courses

#### Loading from JSON files ####


def load_grade_to_visited_courses():
    with open("grade_to_visited_courses.json", "r") as openfile:
        return json.load(openfile)


def load_all_activities():
    with open("all_activities.json", "r") as openfile:
        return json.load(openfile)


def get_activity_per_user(user_id):
    """
    user_id: int or None(for all records)

    method uses already generated JSON file
    """
    all_activities = load_all_activities()

    if user_id is not None:
        return [activity for activity in all_activities if activity[0] == user_id]
    else:
        return all_activities


#### JSON Creation ####

def create_json_files():
    """
    This method:

    1. Loads Logs and parses them to be 
    only user id + activity, then saves them to a JSON


    2. Uses the make_grade_to_visited_courses() to make a data structure
    and saves it to a JSON file
    """

    # make file for all activities
    activities = []
    df = pd.read_excel(os.path.join(
        "public", "Logs.xlsx"))
    # get last column from dataframe
    description: pd.DataFrame = df.iloc[:, -1]
    for row in description:
        # append tuple of user_id + activity(minus coma)
        activities.append((int(row[18:22]), row[24:-1]))

    # Write file for all activities
    json_activities = json.dumps(activities, indent=4)
    with open("all_activities.json", "w") as outfile:
        outfile.write(json_activities)

    # Write file for grade to visited courses corellation
    json_grade_to_courses = json.dumps(
        make_grade_to_visited_courses(), indent=4)
    with open("grade_to_visited_courses.json", "w") as outfile:
        outfile.write(json_grade_to_courses)
