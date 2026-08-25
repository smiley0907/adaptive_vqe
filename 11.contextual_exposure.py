# ============================================================
# CELL 11: CONTEXTUAL EXPOSURE SUMMARY
# ============================================================

comparison_df = contextual_noise_results_df[
    [
        "Circuit",
        "Qubits",
        "Total_Gates",
        "Maximum_Contextual_Score",
        "Mean_Contextual_Score",
        "Total_Contextual_Score"
    ]
].copy()

print("============================================================")
print("BASELINE CIRCUIT / NOISE EXPOSURE PROFILE")
print("============================================================\n")

print(
    comparison_df.to_string(index=False)
)

print("\nCell 11 completed successfully.")
