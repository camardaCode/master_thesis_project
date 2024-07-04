import re

file_path = 'llm_output.txt'
save_file_path = 'instance_knowledge.asp'


def save_facts_to_file(facts, final_results_path):
    final_path = f'{final_results_path}/{save_file_path}'
    try:
        with open(final_path, 'a') as file:
            for fact in facts:
                file.write(fact + '\n\r')
                file.flush()
    except Exception as e:
        print(f"Error occurred while saving facts to '{final_path}': {e}")


def extract_correct_asp_facts(text, correct_pattern):
    text = text.replace("'", '"')
    matches = re.findall(correct_pattern, text)
    facts = []
    if len(matches) != 0:
        for match in matches:
            facts.append(match[0])
        return facts
    else:
        return []


def correct_asp_facts(text, incorrect_patterns, corrections_switch):
    incorrect_facts = set()
    corrections = []

    for pattern in incorrect_patterns:
        matches = re.fullmatch(pattern, text)
        if matches:
            incorrect_facts.add(matches[0][0])

    for fact in incorrect_facts:
        for pattern in incorrect_patterns:
            if re.fullmatch(pattern, fact):
                fact = corrections_switch[pattern](fact)
                corrections.append(fact)
                break

    return corrections


def start_scanner(final_results_path, correct_pattern, incorrect_patterns, corrections_switch):
    with open(file_path, 'r') as file:
        log_entries = file.read().split("\n")

    for entry in log_entries:
        already_corrected_facts = extract_correct_asp_facts(entry, correct_pattern)
        save_facts_to_file(already_corrected_facts, final_results_path)
        corrected_facts = correct_asp_facts(entry, incorrect_patterns, corrections_switch)
        save_facts_to_file(corrected_facts, final_results_path)

