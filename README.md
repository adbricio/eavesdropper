# Quantum Key Distribution (QKD) Eavesdropping Simulator

## Overview
This project provides a simulation framework for analyzing security vulnerabilities in Quantum Key Distribution (QKD) under eavesdropping conditions. The focus is on simulating a single BB84 key exchange while incorporating an intercept-resend attack by an eavesdropper. The tool enables users to evaluate performance across different conditions and collect statistical data.

## Features
- Simulates a complete BB84 key exchange with eavesdropping interference.
- Allows customization of attack parameters such as intensity, Eve's position, and redundancy rate.
- Generates detailed logs and statistical summaries for performance analysis.
- Supports parameterized testing with multiple independent experiments.
- Designed to work on macOS and Linux (requires NetSquid).

## Simulation Parameters
Users can configure the simulation using a YAML configuration file. 

![Figure 1: YAML example](images/YAML.png)


Key parameters include:

### General Configuration
- `qkd-protocol`: Specifies the QKD protocol (currently supports only "BB84").
- `key-length`: Desired key size (integer or array of integers).
- `redundancy-rate`: Specifies the batch size as a fraction of the key length.
- `link-length`: Distance (km) between Alice and Bob.

### Eavesdropper Configuration
- `distance-to-alice`: Distance (km) between Eve and Alice (float or array of floats).
- `percentage-qubits`: Percentage of qubits intercepted and resent by Eve (integer or array of integers).

## Execution
### Prerequisites
- macOS or Linux (NetSquid dependency required)
- Python (ensure required dependencies are installed)

### Running the Simulation
1. Clone the repository

2. Install dependencies

3. Run the simulation:
   ```bash
   python code_eve.py <path_to_yaml_config>
   ```

## Output Data
The simulation results are stored in two CSV files:

1. `<yaml_name>_results.csv`: Logs detailed execution data, including:
   - Protocol, key length, distance to Alice, percentage of intercepted qubits
   - Alice's and Bob’s final keys
   - QBER (before and after error correction)
   - Execution time and number of repetitions

2. `<yaml_name>_means.csv`: Summarizes statistical averages over 100 executions per configuration.

