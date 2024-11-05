import streamlit as st
import pandas as pd
import jiwer
from io import BytesIO
import plotly.express as px

# Function to calculate transcription quality metrics
def calculate_metrics(df):
    metrics = []

    for index, row in df.iterrows():
        actual_transcript = row['Actual Transcript']
        asr_transcript = row['ASR Transcript']
        
        # Calculate various metrics using jiwer
        wer_asr = jiwer.wer(actual_transcript, asr_transcript)
        mer_asr = jiwer.mer(actual_transcript, asr_transcript)
        wil_asr = jiwer.wil(actual_transcript, asr_transcript)
        wip_asr = jiwer.wip(actual_transcript, asr_transcript)
        cer_asr = jiwer.cer(actual_transcript, asr_transcript)
        
        # Store results in a list of dicts
        metrics.append({
            'Audio File': row['Audio File'],
            'WER': wer_asr,
            'MER': mer_asr,
            'WIL': wil_asr,
            'WIP': wip_asr,
            'CER': cer_asr,
        })
    
    # Convert the list of dicts to a DataFrame
    return pd.DataFrame(metrics)

# Function to convert DataFrame to CSV
def to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue().decode('utf-8')

# Streamlit App
st.title("Audio Transcription Quality Measure")

st.write("""
The following metrics will be calculated:
- **Word Error Rate (WER)**: Measures the percentage of words incorrectly predicted compared to the reference transcript.
  - **Worst**: 1.0 (100% error), **Best**: 0.0 (perfect match).
  - Common Range: In real-world applications, WER of 0.2–0.4 (20–40%) is typical for automatic speech recognition (ASR) systems. 
- **Match Error Rate (MER)**: The fraction of incorrect word matches.
  - **Worst**: 1.0 (all matches incorrect), **Best**: 0.0 (all matches correct).
  - Common Range: Like WER, MER tends to range from 0.2 to 0.4 for many real-world ASR systems.
- **Word Information Lost (WIL)**: Indicates how much important word information was lost.
  - **Worst**: 1.0 (everything lost), **Best**: 0.0 (nothing lost).
  - Common Range: WIL is typically between 0.2 and 0.5 for automatic transcription systems.
- **Word Information Preserved (WIP)**: Measures how much word information was preserved correctly.
  - **Worst**: 0.0 (nothing preserved), **Best**: 1.0 (everything preserved).
  - Common Range: WIP values closer to 1.0 are better and indicate more accurate transcriptions. WIP values in practice can range from 0.5 to 0.8.
- **Character Error Rate (CER)**: Measures the percentage of characters incorrectly predicted compared to the reference transcript.
  - **Worst**: 1.0 (100% character error), **Best**: 0.0 (perfect character match).
  - Common Range: CER for many modern ASR systems tends to fall between 0.1 and 0.3, depending on the language and system quality.

### Ideal Values
- **WER, MER, WIL, CER**: Closer to **0** is better.
- **WIP**: Closer to **1** is better.

These metrics provide insights into the accuracy of your audio transcripts, helping you assess their quality effectively.
""")

# File uploader for CSV or Excel
uploaded_file = st.file_uploader("Upload an Excel or CSV file with audio transcripts to compare ASR and the actual transcripts.", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Read the file depending on its type
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    
    st.write("File Uploaded Successfully!")
    
    # Ensure columns for comparison exist
    if {'Actual Transcript', 'ASR Transcript', 'Audio File'}.issubset(df.columns):
        # Display the uploaded file as a preview
        st.write("Uploaded Data Preview:")
        st.dataframe(df.head())

        # Calculate quality metrics
        st.write("Calculating transcription quality metrics...")
        metrics_df = calculate_metrics(df)
        
        # Display the metrics as a table
        st.header("Transcription Quality Metrics:")
        st.dataframe(metrics_df)
        # Provide an option to download the results as CSV
        st.download_button(
            label="Download Metrics as CSV",
            data=to_csv(metrics_df),
            file_name='transcription_metrics.csv',
            mime='text/csv'
        )

        # Plot the metrics
        st.header("Visualizing Transcription Quality Metrics:")

        # Overall Performance Analysis: Average metrics
        avg_metrics = metrics_df[['WER', 'MER', 'WIL', 'WIP', 'CER']].mean()
        avg_metrics_df = avg_metrics.reset_index()
        avg_metrics_df.columns = ['Metric', 'Average Value']

        # Plotting Average Metrics
        fig = px.bar(avg_metrics_df, x='Metric', y='Average Value', title='Average Transcription Quality Metrics')
        st.plotly_chart(fig)

        # Error Analysis: Histogram of WER
        fig2 = px.histogram(metrics_df, x='WER', nbins=10, title='Distribution of Word Error Rate (WER)')
        st.plotly_chart(fig2)
        
    else:
        st.error("The uploaded file must contain 'Actual Transcript', 'ASR Transcript' and 'Audio File' columns.")
