import yaml
import subprocess
import argparse
import os
import csv

from bb84_eve_percentage import bb84_key_perc



def load_yaml(file_path):
    """
    Load the YAML file and return the content.
    """
    print(f"Loading YAML file from: {file_path}")
    with open(file_path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(f"Error in YAML file: {exc}")
            return None
        

def run_tests(file_path, parameter_name, yaml_parameters, qkd_protocol, key_lengths, link_length, distance_to_alice, attenuation, redundancy_rate):

    
    if not isinstance(key_lengths, list):
        key_lengths = [key_lengths]

    if not isinstance(distance_to_alice, list):
        distance_to_alice = [distance_to_alice]
    
    
    yaml_name = file_path[:-5] # drop the .yaml extension from the name
    results_filename = f'{yaml_name}_results.csv'
    means_filename = f'{yaml_name}_means.csv'
    
    with open(results_filename, mode='w', newline='') as file_results, \
            open(means_filename, mode='w', newline='') as file_means:
        writer_results = csv.writer(file_results)
        writer_means = csv.writer(file_means)
        # Write the CSVs headers
        writer_results.writerow(["protocol", "key_length", "distance_to_alice",parameter_name, "alice_key", "bob_key", "qber", "qber_after_correction", "simulated_time", "repetitions"])
        writer_means.writerow(["protocol", "key_length","distance_to_alice", parameter_name, "mean_qber", "mean_qber_after_correction", "mean_simulated_time", "mean_repetitions"])

    
        for key_length in key_lengths:
            print(f"\n\n\n---------KEY LENGTH: {key_length}---------")

            for each_distance in distance_to_alice:
                print(f"\n\n---Eve is at {each_distance} km from Alice---\n")

                for each_parameter in yaml_parameters:
                    mean_qber = 0
                    mean_qber_after_correction = 0
                    corrected = 0
                    mean_time = 0
                    mean_repetitions = 0
                    should_break = False

                    print(f"\nRunning tests for {parameter_name}: {each_parameter}")

                    for i in range(100): # repeat experiment 100 times

                        if qkd_protocol == 'BB84':
                            if parameter_name == 'percentage':
                                alice_key, bob_key, qber, qber_after_correction, simulated_time, repetitions = bb84_key_perc(key_length, link_length, each_distance, each_parameter, attenuation, redundancy_rate)
                        
                        else: 
                            print('Error: protocol not yet implemented')
                            should_break = True
                            break

                        mean_qber += qber

                        if mean_qber_after_correction:
                            mean_qber_after_correction += qber_after_correction
                            corrected +=1
                        
                        mean_time += simulated_time
                        mean_repetitions += repetitions
                        writer_results.writerow([qkd_protocol, key_length, each_distance, each_parameter, alice_key, bob_key, qber, qber_after_correction, simulated_time, repetitions])
                        
                        
                    if should_break:
                        break

                    mean_time /= 100
                    mean_qber /= 100
                    if corrected!=0:
                        mean_qber_after_correction /=corrected
                    else:
                        mean_qber_after_correction = None
                    mean_repetitions /= 100
                    writer_means.writerow([qkd_protocol, key_length, each_distance, each_parameter, mean_qber, mean_qber_after_correction, mean_time, mean_repetitions])

                    print(f"Tests completed for {parameter_name}: {each_parameter}")



def execute_on_data(data, file_path):

    qkd_protocol = data['qkd-protocol']
    key_lengths = data['key-length']
    redundancy_rate = data['redundancy-rate']
    link_length = data['link-length']
    attenuation = data['fibre-attenuation']
    #attenuation = 0

    distance_to_alice = data['eavesdropper']['distance-to-alice']
    
    percentage_qubits = data['eavesdropper']['percentage-qubits']

    if not isinstance(percentage_qubits, list):
        percentage_qubits = [percentage_qubits]


    if percentage_qubits:
        run_tests(file_path, 'percentage', percentage_qubits, qkd_protocol, key_lengths, link_length, distance_to_alice, attenuation, redundancy_rate)


def main():

    parser = argparse.ArgumentParser(description="Process a YAML file and execute tasks based on its content.")
    parser.add_argument('yaml_file', help="Path to the YAML file")
    
    args = parser.parse_args()
    
    # Check if file exists
    if not os.path.exists(args.yaml_file):
        print(f"Error: File '{args.yaml_file}' not found.")
        return

    # Load and process the YAML file
    data = load_yaml(args.yaml_file)

    execute_on_data(data, args.yaml_file)

if __name__ == "__main__":
    main()