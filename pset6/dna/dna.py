from sys import argv, exit
import csv


def main():
    database_path, sequence_path = get_file_args()
    people, dna_strs = read_people_from_database(database_path)
    sequence = read_sequence_from_file(sequence_path)
    dna = calculate_dna(dna_strs, sequence)
    person = lookup_people(people, dna_strs, dna)
    if person:
        print(person["name"])
    else:
        print("No Match")
        
        
def get_file_args():
    if len(argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        exit(1)
        
    return argv[1], argv[2]
    
    
def read_people_from_database(database_path):
    people = []
    dna_strs = []
    
    with open(database_path) as csv_file:
        reader = csv.DictReader(csv_file)
        
        dna_strs = reader.fieldnames[1:]
        
        for row in reader:
            person = {}
            for key in row:
                person[key] = int(row[key]) if key != "name" else row[key]
            
            people.append(person)
            
    return people, dna_strs
    
    
def read_sequence_from_file(sequence_path):
     with open(sequence_path) as sequence_file:
         return sequence_file.read()
         
         
def calculate_dna(dna_strs, sequence):
    result = {}
    
    for dna_str in dna_strs:
        result[dna_str] = calculate_dna_str(sequence, dna_str)
        
    return result
    
    
def calculate_dna_str(sequence, dna_str):
    max_group_sequence = 0
    
    while True:
        index = sequence.find(dna_str)
        if index >= 0:
            next_sequence = sequence[index:]
            dna_groups, group_length = calculate_dna_groups(
                next_sequence, dna_str)
            max_group_sequence = max(max_group_sequence, dna_groups)
            sequence = next_sequence[group_length:]
        else:
            break
        
    return max_group_sequence
    
    
def calculate_dna_groups(sequence, dna_str):
    dna_groups = 0
    dna_len = len(dna_str)
    
    while sequence.find(dna_str) == 0:
        dna_groups += 1
        sequence = sequence[dna_len:]
        
    return dna_groups, dna_groups * dna_len
        
        
def lookup_people(people, dna_strs, dna):
    required_matches = len(dna_strs)
        
    for person in people:
        matches = compare_dna_strs(dna_strs, person, dna)
        if matches == required_matches:
            return person        
        
        
def compare_dna_strs(dna_strs, person, dna):
    matches = 0
    
    for dna_str in dna_strs:
        if person[dna_str] == dna[dna_str]:
            matches += 1
        else:
            return 0
            
    return matches
    
    
main()
