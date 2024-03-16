import streamlit as st
import numpy as np
from scipy.stats import norm

def hypothesis_test(cgv, cgc, tgv, tgc, ci):
    # Calculate conversion rates for control and treatment groups
    control_cr = cgc / cgv
    treatment_cr = tgc / tgv
    
    # Calculate pooled standard error
    pooled_se = np.sqrt((control_cr * (1 - control_cr) / cgv) + (treatment_cr * (1 - treatment_cr) / tgv))
    
    # Calculate z-score
    z_score = (treatment_cr - control_cr) / pooled_se
    
    # Determine critical z-value based on confidence level
    if ci == 90:
        critical_z = norm.ppf(0.95)
    elif ci == 95:
        critical_z = norm.ppf(0.975)
    elif ci == 99:
        critical_z = norm.ppf(0.995)
    else:
        raise ValueError("Confidence level must be 90, 95, or 99")
    
    # Determine interpretation
    if z_score > critical_z:
        interpretation = "Experiment Group is Better"
    elif z_score < -critical_z:
        interpretation = "Control Group is Better"
    else:
        interpretation = "Indeterminate"
    
    return interpretation

def main():
    st.title('AB Test Hypothesis Testing App')
    st.write('Enter the following inputs to perform the hypothesis test:')

    # User inputs
    control_visitors = st.number_input('Control Group Visitors', min_value=0, step=1)
    control_conversions = st.number_input('Control Group Conversions', min_value=0, step=1)
    treatment_visitors = st.number_input('Experiment Group Visitors', min_value=0, step=1)
    treatment_conversions = st.number_input('Experiment Group Conversions', min_value=0, step=1)
    confidence_level = st.slider('Confidence Level (%)', min_value=90, max_value=99, value=95, step=1)

    # Perform hypothesis test when user clicks the button
    if st.button('Perform Hypothesis Test'):
        result = hypothesis_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level)
        st.write('Hypothesis Test Result:', result)

if __name__ == "__main__":
    main()
