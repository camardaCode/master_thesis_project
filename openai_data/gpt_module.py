from openai import OpenAI
import pandas as pd


def chat_with_gpt(client, dataset_column, object_location=False):
    results = []
    messages = []

    if object_location:
        messages.append({"role": "system",
                         "content": "Translate the following sentence in Answer Set Programming facts. "
                                    "When answering, use ONLY predicates 'east(object1, object2)', 'west(object1, "
                                    "object2)','south(object1, object2)', 'north(object1, object2)', "
                                    "'superior(object1, object2)', 'same_level(object1, object2)'. Produce as "
                                    "output just the translation and not the explanation. Example of sentence: "
                                    "'The body was over the ground and, at the right of it, there was a knife'. "
                                    "Example of translation: superior(body, ground). east(body, knife). "
                                    "same_level(body, knife).  Sentence:"
                                    })
    else:
        messages.append({"role": "system",
                         "content": "Translate the following sentence in Answer Set Programming facts. "
                                    "When answering, use predicates 'timestamp(year-month-day_hour:minute:second)', "
                                    "'event(what_happened, year-month-day_hour , where)'. "
                                    "Produce as output just the translation and not the explanation. "
                                    "Example of sentence: '23:00 2024-02-09 The man laying on "
                                    "the sofa called his wife and wishes her a good birthday'."
                                    "Example of translation: timestamp(2024-02-09_23:00). "
                                    "event(the_man_called_his_wife, 2024-02-09_23:00, apartment). Sentence:"
                                    })

    for report in dataset_column:
        messages.append({"role": "user", "content": report})
        results.append(get_output(client, messages))
        messages.pop()
    return results


def get_output(client, messages):
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return completion.choices[0].message.content


def get_translation(folder_path, files_path):
    client = OpenAI()
    columns_names = ['Reports']
    facts_related_to_reports = []

    for file in files_path:
        if 'crime_scene' in file:
            crime_scene_reports = pd.read_csv(f'{folder_path}'+ "/" + f'{file}', sep="\r",
                                              names=columns_names)
            facts_related_to_reports.append(chat_with_gpt(client, crime_scene_reports['Reports'], True))
        else:
            depositions_and_reports = pd.read_csv(f'{folder_path}' + "/" + f'{file}', sep="\r",
                                                  names=columns_names)
            facts_related_to_reports.append(chat_with_gpt(client, depositions_and_reports['Reports']))

    return facts_related_to_reports
