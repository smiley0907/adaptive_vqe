# ============================================================
# CELL 7: Contextual Exposure and Noisy Fidelity
# ============================================================

from qiskit.quantum_info import Statevector


FIDELITY_SHOTS = 4096

contextual_noise_results = []


# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def counts_to_probabilities(counts, shots):

    return {
        state: count / shots
        for state, count in counts.items()
    }


def classical_fidelity(p, q):

    states = set(p.keys()) | set(q.keys())

    return (
        sum(
            np.sqrt(
                p.get(state, 0.0)
                *
                q.get(state, 0.0)
            )
            for state in states
        )
        ** 2
    )


# ------------------------------------------------------------
# Execute every circuit
# ------------------------------------------------------------

for family in CIRCUIT_FAMILIES:

    for n in QUBIT_CONFIGS:

        circuit = analysis_circuits[
            family
        ][n]

        # ----------------------------------------------------
        # Exact ideal probability distribution
        # ----------------------------------------------------

        ideal_state = Statevector.from_instruction(
            circuit
        )

        ideal_prob = (
            ideal_state
            .probabilities_dict()
        )

        # ----------------------------------------------------
        # Noisy execution
        # ----------------------------------------------------

        noisy_circuit = circuit.copy()

        noisy_circuit.measure_all()

        noisy_simulator = AerSimulator(
            noise_model=noise_model,
            seed_simulator=SIMULATOR_SEED
        )

        noisy_job = noisy_simulator.run(
            noisy_circuit,
            shots=FIDELITY_SHOTS
        )

        noisy_counts = (
            noisy_job
            .result()
            .get_counts()
        )

        noisy_prob = counts_to_probabilities(
            noisy_counts,
            FIDELITY_SHOTS
        )

        # ----------------------------------------------------
        # Fidelity
        # ----------------------------------------------------

        noisy_fidelity = classical_fidelity(
            ideal_prob,
            noisy_prob
        )

        fidelity_loss = (
            1.0 - noisy_fidelity
        )

        # ----------------------------------------------------
        # Contextual exposure data
        # ----------------------------------------------------

        exposure_data = (
            contextual_exposure_summary_df[
                (
                    contextual_exposure_summary_df[
                        "Circuit"
                    ]
                    == family
                )
                &
                (
                    contextual_exposure_summary_df[
                        "Qubits"
                    ]
                    == n
                )
            ]
            .iloc[0]
        )

        # ----------------------------------------------------
        # High exposure gate information
        # ----------------------------------------------------

        region_data = (
            contextual_region_summary_df[
                (
                    contextual_region_summary_df[
                        "Circuit"
                    ]
                    == family
                )
                &
                (
                    contextual_region_summary_df[
                        "Qubits"
                    ]
                    == n
                )
            ]
            .iloc[0]
        )

        # ----------------------------------------------------
        # Concentration information
        # ----------------------------------------------------

        ranking_data = (
            contextual_ranking_df[
                (
                    contextual_ranking_df[
                        "Circuit"
                    ]
                    == family
                )
                &
                (
                    contextual_ranking_df[
                        "Qubits"
                    ]
                    == n
                )
            ]
            .iloc[0]
        )

        # ----------------------------------------------------
        # Store results
        # ----------------------------------------------------

        contextual_noise_results.append({

            "Circuit":
                family,

            "Qubits":
                n,

            "Total_Gates":
                int(
                    exposure_data[
                        "Total_Gates"
                    ]
                ),

            "Maximum_Contextual_Score":
                exposure_data[
                    "Maximum_Contextual_Score"
                ],

            "Mean_Contextual_Score":
                exposure_data[
                    "Mean_Contextual_Score"
                ],

            "Total_Contextual_Score":
                exposure_data[
                    "Total_Contextual_Score"
                ],

            "High_Exposure_Gates":
                int(
                    region_data[
                        "High_Exposure_Gates"
                    ]
                ),

            "High_Exposure_Regions":
                int(
                    region_data[
                        "High_Exposure_Regions"
                    ]
                ),

            "Exposure_Concentration_%":
                ranking_data[
                    "Top_10_Exposure_Concentration_%"
                ],

            "Relative_Top_Exposure":
                ranking_data[
                    "Relative_Top_Exposure"
                ],

            "Noisy_Fidelity":
                noisy_fidelity,

            "Fidelity_Loss":
                fidelity_loss
        })


# ------------------------------------------------------------
# Create dataframe
# ------------------------------------------------------------

contextual_noise_results_df = pd.DataFrame(
    contextual_noise_results
)


# ------------------------------------------------------------
# Round values
# ------------------------------------------------------------

numeric_columns = [
    "Maximum_Contextual_Score",
    "Mean_Contextual_Score",
    "Total_Contextual_Score",
    "Exposure_Concentration_%",
    "Relative_Top_Exposure",
    "Noisy_Fidelity",
    "Fidelity_Loss"
]

contextual_noise_results_df[
    numeric_columns
] = contextual_noise_results_df[
    numeric_columns
].round(6)


# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print(
    "============================================================"
)

print(
    "CONTEXTUAL EXPOSURE AND NOISY FIDELITY RESULTS"
)

print(
    "============================================================\n"
)

print(
    contextual_noise_results_df.to_string(
        index=False
    )
)

print(
    "\nFidelity shots:",
    FIDELITY_SHOTS
)

print(
    "\nCell 7 completed successfully."
)
