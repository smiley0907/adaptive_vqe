# ============================================================
# CELL 2: GHZ, QFT and Grover Circuit Generation
# ============================================================

from qiskit.circuit.library import QFT


def create_ghz(n):
    qc = QuantumCircuit(n)

    qc.h(0)

    for q in range(1, n):
        qc.cx(0, q)

    return qc


def create_qft(n):
    qc = QuantumCircuit(n)

    qft = QFT(n, do_swaps=False)

    qc.compose(
        qft,
        inplace=True
    )

    return qc


def create_grover(n):
    qc = QuantumCircuit(n)

    # Initial superposition
    qc.h(range(n))

    # Oracle
    qc.x(range(n))

    qc.h(n - 1)

    if n == 1:
        qc.z(n - 1)
    else:
        qc.mcx(
            list(range(n - 1)),
            n - 1
        )

    qc.h(n - 1)

    qc.x(range(n))

    # Diffusion operator
    qc.h(range(n))
    qc.x(range(n))

    qc.h(n - 1)

    if n == 1:
        qc.z(n - 1)
    else:
        qc.mcx(
            list(range(n - 1)),
            n - 1
        )

    qc.h(n - 1)

    qc.x(range(n))
    qc.h(range(n))

    return qc


# ------------------------------------------------------------
# Generate all circuits
# ------------------------------------------------------------

logical_circuits = {}

for family in CIRCUIT_FAMILIES:

    logical_circuits[family] = {}

    for n in QUBIT_CONFIGS:

        if family == "GHZ":
            circuit = create_ghz(n)

        elif family == "QFT":
            circuit = create_qft(n)

        elif family == "Grover":
            circuit = create_grover(n)

        logical_circuits[family][n] = circuit


# ------------------------------------------------------------
# Verification
# ------------------------------------------------------------

print("===== LOGICAL CIRCUITS GENERATED =====\n")

for family in CIRCUIT_FAMILIES:

    print(
        f"{family}: "
        f"{len(logical_circuits[family])} circuits"
    )

print(
    "\nTotal circuits:",
    sum(
        len(logical_circuits[family])
        for family in CIRCUIT_FAMILIES
    )
)

print("\nCell 2 completed successfully.")
