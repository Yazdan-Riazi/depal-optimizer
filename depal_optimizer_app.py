
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# Pallet dimensions (mm)
PALLET_WIDTH = 1219
PALLET_LENGTH = 1016
MAX_LAYER_WEIGHT_LBS = 450

# Title
st.title("Depal Layer Optimizer")

# User input
st.header("Enter Case Details")
case_length = st.number_input("Case Length (mm)", min_value=1, value=299)
case_width = st.number_input("Case Width (mm)", min_value=1, value=204)
case_weight_g = st.number_input("Case Weight (grams)", min_value=1, value=1596)

# Convert to lbs
case_weight_lbs = case_weight_g / 453.592

if st.button("Optimize Layout"):
    orientations = [(case_width, case_length), (case_length, case_width)]
    best_layout = None
    max_cases = 0

    for (cw, cl) in orientations:
        if cw >= 110 and cl >= 92:
            cols = PALLET_WIDTH // cw
            rows = PALLET_LENGTH // cl
            total_cases = int(cols * rows)
            total_weight = total_cases * case_weight_lbs

            if total_weight <= MAX_LAYER_WEIGHT_LBS and total_cases > max_cases:
                max_cases = total_cases
                best_layout = (cw, cl, cols, rows, total_cases, total_weight)

    if best_layout:
        cw, cl, cols, rows, total_cases, total_weight = best_layout

        # Centering the layout
        used_w = cols * cw
        used_l = rows * cl
        offset_x = (PALLET_WIDTH - used_w) / 2
        offset_y = (PALLET_LENGTH - used_l) / 2

        # Plot
        fig, ax = plt.subplots()
        ax.set_xlim(0, PALLET_WIDTH)
        ax.set_ylim(0, PALLET_LENGTH)
        ax.set_title(f"Optimized Layout: {total_cases} Cases ({total_weight:.1f} lbs)")

        count = 1
        for i in range(int(cols)):
            for j in range(int(rows)):
                x = offset_x + i * cw
                y = offset_y + j * cl
                rect = patches.Rectangle((x, y), cw, cl, linewidth=1, edgecolor='blue', facecolor='lightblue')
                ax.add_patch(rect)
                ax.text(x + cw / 2, y + cl / 2, f"{count}", ha='center', va='center', fontsize=6)
                count += 1

        ax.set_xlabel("Pallet Width (mm)")
        ax.set_ylabel("Pallet Length (mm)")
        ax.set_aspect('equal')
        st.pyplot(fig)
    else:
        st.warning("No valid layout found within weight and size constraints.")
