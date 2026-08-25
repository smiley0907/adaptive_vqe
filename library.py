# ============================================================
# CELL 1: Libraries, Parameters and Controlled Noise Model
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

# ------------------------------------------------------------
# Experimental configuration
# ------------------------------------------------------------

QUBIT_CONFIGS = [3, 5, 7, 9, 11]

CIRCUIT_FAMILIES = [
    "GHZ",
    "QFT",
    "Grover"
]

# Low level gate basis
BASIS_GATES = ["u", "cx"]

# No compiler optimization during structural analysis
OPTIMIZATION_LEVEL = 0

# Number of measurement shots
SHOTS = 1024

# Controlled depolarizing noise probability
NOISE_PROBABILITY = 0.01

# Reproducible simulator seed
SIMULATOR_SEED = 12345

# ------------------------------------------------------------
# Create controlled depolarizing noise model
# ------------------------------------------------------------

noise_model = NoiseModel()

# Single qubit depolarizing error
single_qubit_error = depolarizing_error(
    NOISE_PROBABILITY,
    1
)

# Two qubit depolarizing error
two_qubit_error = depolarizing_error(
    NOISE_PROBABILITY,
    2
)

noise_model.add_all_qubit_quantum_error(
    single_qubit_error,
    ["u"]
)

noise_model.add_all_qubit_quantum_error(
    two_qubit_error,
    ["cx"]
)

# ------------------------------------------------------------
# Simulator
# ------------------------------------------------------------

simulator = AerSimulator(
    noise_model=noise_model,
    seed_simulator=SIMULATOR_SEED
)

# ------------------------------------------------------------
# Configuration summary
# ------------------------------------------------------------

print("===== EXPERIMENTAL CONFIGURATION =====")
print("Circuit families       :", CIRCUIT_FAMILIES)
print("Qubit configurations   :", QUBIT_CONFIGS)
print("Basis gates            :", BASIS_GATES)
print("Optimization level     :", OPTIMIZATION_LEVEL)
print("Shots                  :", SHOTS)
print("Noise probability      :", NOISE_PROBABILITY)
print("Simulator seed         :", SIMULATOR_SEED)
print("Noise model            : Depolarizing")
print("\nCell 1 completed successfully.")
