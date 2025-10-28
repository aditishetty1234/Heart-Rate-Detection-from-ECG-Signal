import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

st.set_page_config(page_title="Heart Rate Detection App", page_icon="🩺")

st.title("🩺 Heart Rate Detection from ECG Signal")
st.write("Upload your ECG signal file (CSV or TXT) to detect R-peaks and calculate heart rate.")

uploaded_file = st.file_uploader("Upload ECG File", type=["csv", "txt"])

if uploaded_file is not None:
    try:
        ecg_data = pd.read_csv(uploaded_file, header=None)
        ecg_signal = ecg_data.iloc[:, 0].values
        
        st.subheader("Raw ECG Signal")
        st.line_chart(ecg_signal)

        fs = st.number_input("Enter Sampling Frequency (Hz):", value=360)

        peaks, _ = find_peaks(ecg_signal, distance=fs/2.5, height=np.mean(ecg_signal)+0.2*np.std(ecg_signal))

        rr_intervals = np.diff(peaks) / fs
        heart_rate = 60 / np.mean(rr_intervals) if len(rr_intervals) > 0 else 0

        st.subheader("Detected Peaks and Heart Rate")
        st.write(f"❤️ Estimated Heart Rate: **{heart_rate:.2f} BPM**")

        fig, ax = plt.subplots()
        ax.plot(ecg_signal, label="ECG Signal")
        ax.plot(peaks, ecg_signal[peaks], "ro", label="R-peaks")
        ax.set_xlabel("Samples")
        ax.set_ylabel("Amplitude")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error processing file: {e}")

else:
    st.info("Please upload an ECG signal file to start.")
