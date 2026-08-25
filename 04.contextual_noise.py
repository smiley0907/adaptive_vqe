# ============================================================
# CELL 4: Contextual Noise Exposure Score
# ============================================================

contextual_exposure_profiles = {}
contextual_exposure_summary = []

for family in CIRCUIT_FAMILIES:

    contextual_exposure_profiles[family] = {}

    for n in QUBIT_CONFIGS:

        circuit = analysis_circuits[family][n]

        # ----------------------------------------------------
        # Track accumulated exposure for every qubit
        # ----------------------------------------------------

        qubit_exposure = {
            q: 0.0 for q in range(n)
        }

        gate_records = []

        # ----------------------------------------------------
        # Process gates sequentially
        # ----------------------------------------------------

        for gate_index, instruction in enumerate(
            circuit.data
        ):

            gate = instruction.operation

            qubit_indices = [
                circuit.find_bit(q).index
                for q in instruction.qubits
            ]

            qubit_count = len(
                qubit_indices
            )

            # ------------------------------------------------
            # Exposure already present on participating qubits
            # ------------------------------------------------

            contextual_exposure = np.mean([
                qubit_exposure[q]
                for q in qubit_indices
            ])

            # ------------------------------------------------
            # Contextual exposure score
            #
            # CES_g =
            # CE_g * [1 - (1-p)^N_g]
            # ------------------------------------------------

            gate_noise_factor = (
                1.0
                -
                (
                    1.0
                    -
                    NOISE_PROBABILITY
                )
                ** qubit_count
            )

            contextual_score = (
                contextual_exposure
                *
                gate_noise_factor
            )

            # ------------------------------------------------
            # Update qubit exposure after the gate
            # ------------------------------------------------

            for q in qubit_indices:

                qubit_exposure[q] = (
                    1.0
                    -
                    (
                        (1.0 - qubit_exposure[q])
                        *
                        (1.0 - NOISE_PROBABILITY)
                    )
                )

            # ------------------------------------------------
            # Store gate-level record
            # ------------------------------------------------

            gate_records.append({

                "Gate_Index":
                    gate_index,

                "Gate":
                    gate.name,

                "Qubits":
                    tuple(qubit_indices),

                "Qubit_Count":
                    qubit_count,

                "Contextual_Exposure":
                    contextual_exposure,

                "Gate_Noise_Factor":
                    gate_noise_factor,

                "Contextual_Exposure_Score":
                    contextual_score
            })


        # ----------------------------------------------------
        # Gate-level dataframe
        # ----------------------------------------------------

        gate_df = pd.DataFrame(
            gate_records
        )

        contextual_exposure_profiles[
            family
        ][n] = gate_df


        # ----------------------------------------------------
        # Circuit-level summary
        # ----------------------------------------------------

        contextual_exposure_summary.append({

            "Circuit":
                family,

            "Qubits":
                n,

            "Total_Gates":
                len(gate_df),

            "Maximum_Contextual_Score":
                gate_df[
                    "Contextual_Exposure_Score"
                ].max(),

            "Mean_Contextual_Score":
                gate_df[
                    "Contextual_Exposure_Score"
                ].mean(),

            "Total_Contextual_Score":
                gate_df[
                    "Contextual_Exposure_Score"
                ].sum()
        })


# ------------------------------------------------------------
# Create summary dataframe
# ------------------------------------------------------------

contextual_exposure_summary_df = pd.DataFrame(
    contextual_exposure_summary
)


# ------------------------------------------------------------
# Round numerical values
# ------------------------------------------------------------

numeric_columns = [
    "Maximum_Contextual_Score",
    "Mean_Contextual_Score",
    "Total_Contextual_Score"
]

contextual_exposure_summary_df[
    numeric_columns
] = contextual_exposure_summary_df[
    numeric_columns
].round(8)


# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print(
    "============================================================"
)

print(
    "CONTEXTUAL NOISE EXPOSURE SCORE"
)

print(
    "============================================================\n"
)

print(
    contextual_exposure_summary_df.to_string(
        index=False
    )
)

print(
    "\nCell 4 completed successfully."
)
