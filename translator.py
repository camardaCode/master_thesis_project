import kaggle_data.llama_module
import openai_data.gpt_module
import new_scanner
import json

GPT = 'GPT'
LLAMA = 'LLAMA'
output_file = "llm_output.txt"

correct_pattern = r'(\w+\(([\w:_-]+)(,\s*([\w:_-]+))*\)\.)\n*'
incorrect_patterns = [
    r'(\w+-([\w:_-]+)(,\s*([\w:_-]+))*\)\.)\n*',  # Dash instead of opening parenthesis
    r'(\w+\(([\w:_-]+)(,\s*([\w:_-]+))*\)[^\.])\n*',  # Wrong character at the end
    r'(\w+\(([\w:_-]+)(,\s*([\w:_-]+))*-\.)\n*',  # Dash instead of closing parenthesis
    r'(\w+-([\w:_-]+)(,\s*([\w:_-]+))*-\.)\n*'  # Dash instead of opening and closing parenthesis
]
corrections_switch = {
    incorrect_patterns[0]: lambda match: match.replace('-', '(', 1),
    incorrect_patterns[1]: lambda match: match[:-1] + '.',
    incorrect_patterns[2]: lambda match: match.replace('-', ')', 1),
    incorrect_patterns[3]: lambda match: double_replace(match)
}


def double_replace(match):
    first_replacement_index = match.find('-')
    if first_replacement_index != -1:
        match = match[:first_replacement_index] + '(' + match[first_replacement_index + 1:]

    last_replacement_index = match.rfind('-')
    if last_replacement_index != -1:
        match = match[:last_replacement_index] + ')' + match[last_replacement_index + 1:]

    return match


class Translator:
    def __init__(self, llm_chosen):
        self.llm_translator = llm_chosen

    def make_translation(self, folder_path, files_path):
        if self.llm_translator == 'GPT':
            chat_messages = openai_data.gpt_module.get_translation(folder_path, files_path)
            with open(output_file, 'w') as file:
                for messages_list in chat_messages:
                    for message in messages_list:
                        file.write(message)

        elif self.llm_translator == 'LLAMA':
            kaggle_data.llama_module.get_translation(folder_path, files_path)
            with open("kaggle_data/mynotebook/notebooka7c9c2c15d.log", 'r') as file:
                log_data = file.read()
            log_entries = json.loads(log_data)
            with open(output_file, 'w') as file:
                for entry in log_entries:
                    if entry.get('stream_name') == 'stdout':
                        file.write(entry.get('data'))

    def write_translation_outputs(self, final_results_path):
        new_scanner.start_scanner(final_results_path, correct_pattern,
                                  incorrect_patterns, corrections_switch)
