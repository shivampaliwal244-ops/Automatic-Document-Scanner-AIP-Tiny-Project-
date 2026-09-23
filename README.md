# Automatic Document Scanner Using Image Processing

## Project Overview
Automatic Document Scanner is an image-processing application that detects a document from a photograph, corrects its perspective, and enhances the page to produce a clean scanner-like output.

## Technologies Used
- Python
- OpenCV
- NumPy
- Pillow
- Tkinter

## Image Processing Techniques
- Grayscale Conversion
- Gaussian Blur
- Canny Edge Detection
- Contour Detection
- Perspective Transformation
- Adaptive Thresholding

## Features
- Detects documents automatically
- Detects document boundaries
- Corrects perspective
- Generates scanner-like output
- Provides intermediate processing results
- Simple GUI for selecting images

## Project Structure

```text
source_code/
    document_scanner.py

sample_input/
    real_document_photo.jpg

output/
    01_original.jpg
    02_edges.jpg
    03_detected_document.jpg
    04_scanned_document.jpg
    05_clean_scanned_document.jpg

screenshots/
documentation/
requirements.txt
README.md
