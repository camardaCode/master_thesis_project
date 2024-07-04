import requests
import time

endpoint = 'https://api.conceptnet.io/c/en'
relation_needed = ['UsedFor', 'PartOf', 'IsA', 'HasA', 'AtLocation', 'Causes', 'CapableOf',
                   'HasSubevent', 'HasPrerequisite', 'ReceivesAction', 'DefinedAs']


def query_knowledge_base(name, final_results_path):
    all_edges = []
    next_page = f"{endpoint}/{name}"
    exists_next_page = True
    while exists_next_page:
        time.sleep(2)
        try:
            obj = requests.get(next_page).json()
            for edge in obj['edges']:
                if edge['rel']['label'] in relation_needed:
                    edge_relation = edge['rel']['label']
                    edge_start_label = edge['start']['label']
                    edge_start_label = edge_start_label.replace(' ', '_')
                    edge_end_label = edge['end']['label']
                    edge_end_label = edge_end_label.replace(' ', '_')

                    edge_atom = f'{edge_relation}({edge_start_label}, {edge_end_label}).'
                    if edge_atom not in all_edges:
                        all_edges.append(edge_atom)

            if 'view' in obj and 'nextPage' in obj['view'].keys():
                next_page = f"https://api.conceptnet.io{obj['view']['nextPage']}"
            else:
                exists_next_page = False
        except Exception as e:
            print(f"An error occurred: {e}")
    save_edges_to_file(all_edges, f'{final_results_path}/{name}_edges.asp')


def save_edges_to_file(edges, file_path):
    try:
        with open(file_path, 'w') as file:
            for edge in edges:
                file.write(edge + '\n\r')
    except Exception as e:
        print(f"Error occurred while saving edges to '{file_path}': {e}")


def read_entries_from_file(file_path):
    entries = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                entry = line.strip()
                entries.append(entry)
        return entries
    except FileNotFoundError:
        return []


def query_conceptnet(file_path, final_results_path):
    entries_list = read_entries_from_file(file_path)
    for entry in entries_list:
        query_knowledge_base(entry, final_results_path)
