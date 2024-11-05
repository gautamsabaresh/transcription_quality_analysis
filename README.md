# Audio Transcription Quality Measure
This project is a Streamlit application designed to assess the quality of audio transcriptions by calculating a variety of transcription quality metrics. These metrics help analyze the accuracy of transcription systems, providing insights on areas for improvement.

## Key Features
Transcription Quality Metrics: Calculates multiple transcription metrics including:
- Word Error Rate (WER)
- Match Error Rate (MER)
- Word Information Lost (WIL)
- Word Information Preserved (WIP)
- Character Error Rate (CER)

File Upload: Supports CSV and Excel file uploads containing transcript comparisons.

Data Visualization: Visualizes metrics using bar and histogram plots to analyze performance and distribution trends.

Downloadable Metrics: Allows users to download calculated metrics in CSV format for further analysis.

## Future To Dos
- Proper noun evaluation
- Meaning preservation beyond just WER
- Considering other data points in dataset such as Accent of the speaker to compare it with other ASR models in future to decide what works the best for us.