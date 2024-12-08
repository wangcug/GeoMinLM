import json
import os
import codecs
import random

def get_entity(folder):
    entityfiles = [file for file in os.listdir(folder) if file.endswith(".json")]  # Get all files ending with .json in the folder

    entity_dict = {}
    for entityfile in entityfiles:
        with codecs.open(os.path.join(folder, entityfile), "r", encoding="utf-8-sig") as f:
            data = json.load(f)  # Load JSON data
            entityfile_name = os.path.splitext(entityfile)[0]  # Get the file name without extension
            entity_dict[entityfile_name] = []  # Initialize a list for storing entities
            for item in data:
                properties = item["n"]["properties"]  # Get properties of the entity
                name = properties["name"]  # Extract the entity name
                entity_dict[entityfile_name].append(name)  # Add the entity name to the list

    return entity_dict  # Return the dictionary containing entities


def get_triple(folder):
    triplefiles = [file for file in os.listdir(folder) if file.endswith(".json")]  # Get all triple files

    triple_dict = {}
    for triplefile in triplefiles:
        with codecs.open(os.path.join(folder, triplefile), "r", encoding="utf-8-sig") as f:
            datas = json.load(f)  # Load JSON data
            for data in datas:
                segment = data['p']['segments'][0]  # Extract segment information of the triple
                head = segment['start']['properties'].get('name', '')  # Get the name of the head entity
                relation = segment['relationship'].get('type', '')  # Get the relationship type
                tail = segment['end']['properties'].get('name', '')  # Get the name of the tail entity
                tail_label = segment['end'].get('labels', '')  # Get the labels of the tail entity

                if len(tail_label) > 0:
                    label = tail_label[0]  # Use the first label if available

                if head and relation and tail:  # Proceed only if head, relation, and tail exist
                    if head not in triple_dict:
                        triple_dict[head] = {}  # Initialize the dictionary for the head entity
                    if relation not in triple_dict[head]:
                        triple_dict[head][relation] = {}  # Initialize the dictionary for the relation
                    if label not in triple_dict[head][relation]:
                        triple_dict[head][relation][label] = []  # Initialize the list for the tail entity
                    if tail not in triple_dict[head][relation][label]:
                        triple_dict[head][relation][label].append(tail)  # Add the tail entity to the list

    return triple_dict  # Return the dictionary of triples


def load_question(questionfile):
    with open(questionfile, 'r', encoding='utf-8') as file:
        questiondict = json.load(file)  # Load the question templates in JSON format
    return questiondict  # Return the question dictionary


def make_dataset(entityfolder, triplefolder, questionfile, datasetflie):
    """
    Generate a dataset based on entities, triples, and question templates.
    """
    try:
        if not os.path.exists(entityfolder) or not os.path.exists(triplefolder) or not os.path.exists(questionfile):
            raise ValueError("folder or file not exists!")  # Raise an error if paths do not exist

        entitydict = get_entity(entityfolder)  # Load entity data
        tripledict = get_triple(triplefolder)  # Load triple data
        questiondict = load_question(questionfile)  # Load question templates

        qadatas = []  # Initialize the list for storing question-answer pairs

        for head, rlist in tripledict.items():
            for relation, elist in rlist.items():
                for entitylabel, entitylist in elist.items():
                    entitylabeltemplates = questiondict.get(relation, '')  # Get templates for the relation
                    if isinstance(entitylabeltemplates, dict) and len(entitylabeltemplates) > 0:
                        templates = entitylabeltemplates.get(entitylabel, '')  # Get templates for the specific label
                        if isinstance(templates, list) and len(templates) > 0:
                            for template in templates:
                                question = template.replace('#', head)  # Replace the placeholder in the template with the head entity
                                qadatas.append([question, entitylist])  # Add the question-answer pair

        random.shuffle(qadatas)  # Shuffle the order of question-answer pairs

        with open(datasetflie, 'w', encoding="utf-8") as f:
            count = 0
            for qadata in qadatas:
                f.write('\n{')  # Write the start of a QA pair 
                f.write('\n  "id":"{}",'.format(count))  # Write the QA pair ID
                f.write('\n  "conversations": [')  # Write the start of the conversation section
                f.write('\n    {')
                f.write('\n      "from":"human",')  # Write the user's question
                f.write('\n      "value":"{}"'.format(qadata[0]))
                f.write('\n    },')
                f.write('\n    {')
                f.write('\n      "from":"gpt",')  # Write the model's answer
                f.write('\n      "value":"{}"'.format(",".join(qadata[1])))
                f.write('\n    }')
                f.write('\n  ]')
                f.write('\n},')  # End the QA pair 
                count = count + 1
            f.write("\n]")  # End the dataset in JSON format

    except Exception as e:
        print(f"{e}")  # Print the error message if an exception occurs


if __name__ == '__main__':
    absolute_path_prefix = "E:/TransE/"  # Define the path prefix
    entityfolder = absolute_path_prefix + "entityjson"  # Path to the entity folder
    triplefolder = absolute_path_prefix + "triplejson"  # Path to the triple folder
    questionfile = absolute_path_prefix + "questiondict.json"  # Path to the question template file
    datasetflie = absolute_path_prefix + "dataset.txt"  # Path to the output dataset file
    make_dataset(entityfolder, triplefolder, questionfile, datasetflie)  # Call the function to generate the dataset
