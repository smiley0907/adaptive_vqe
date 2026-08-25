# ============================================================
# CELL 3: Baseline Circuit and Low Level Analysis Profile
# ============================================================

baseline_circuits = {}
analysis_circuits = {}
baseline_profiles = []

for family in CIRCUIT_FAMILIES:

    baseline_circuits[family] = {}
    analysis_circuits[family] = {}

    for n in QUBIT_CONFIGS:

        # ----------------------------------------------------
        # Original logical circuit
        # ----------------------------------------------------

        logical = logical_circuits[family][n]

        baseline_circuits[family][n] = logical.copy()

        # ----------------------------------------------------
        # Low level analysis representation
        # ----------------------------------------------------

        analysis = transpile(
            logical,
            basis_gates=BASIS_GATES,
            optimization_level=OPTIMIZATION_LEVEL
        )

        analysis_circuits[family][n] = analysis

        # ----------------------------------------------------
        # Gate classification
        # ----------------------------------------------------

        total_gates = len(analysis.data)

        single_qubit_gates = 0
        two_qubit_gates = 0
        multi_qubit_gates = 0

        for instruction in analysis.data:

            qcount = len(instruction.qubits)

            if qcount == 1:
                single_qubit_gates += 1

            elif qcount == 2:
                two_qubit_gates += 1

            else:
                multi_qubit_gates += 1

        # ----------------------------------------------------
        # Logical depth of low level representation
        # ----------------------------------------------------

        logical_depth = analysis.depth()

        # ----------------------------------------------------
        # Dependency edges
        # ----------------------------------------------------

        dependency_edges = 0

        for i in range(total_gates):

            qubits_i = {
                analysis.find_bit(q).index
                for q in analysis.data[i].qubits
            }

            for j in range(i + 1, total_gates):

                qubits_j = {
                    analysis.find_bit(q).index
                    for q in analysis.data[j].qubits
                }

                if qubits_i.intersection(qubits_j):
                    dependency_edges += 1

        # ----------------------------------------------------
        # Store structural profile
        # ----------------------------------------------------

        baseline_profiles.append({

            "Circuit": family,

            "Qubits": n,

            "Total_Gates": total_gates,

            "Single_Qubit_Gates":
                single_qubit_gates,

            "Two_Qubit_Gates":
                two_qubit_gates,

            "Multi_Qubit_Gates":
                multi_qubit_gates,

            "Logical_Depth":
                logical_depth,

            "Dependency_Edges":
                dependency_edges
        })


baseline_profile_df = pd.DataFrame(
    baseline_profiles
)

# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print(
    "===== BASELINE / LOW LEVEL STRUCTURAL PROFILE =====\n"
)

print(
    baseline_profile_df.to_string(
        index=False
    )
)

print(
    "\nLow level basis:",
    BASIS_GATES
)

print(
    "\nCell 3 completed successfully."
)
