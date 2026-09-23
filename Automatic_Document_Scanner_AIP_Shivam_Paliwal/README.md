# Automatic Document Scanner Using Image Processing

**Subject:** Advanced Image Processing  
**Student:** Shivam Paliwal  
**Enrollment No.:** 2305101270430  
**Program:** BCA (Hons.)  
**Semester:** 7th Semester  
**Division:** A

## Project Overview
This tiny project converts a photograph of a paper document into a clean, scanner-like page. It uses classical image-processing operations rather than a pre-trained AI model.

## Processing Pipeline
Input → Grayscale → Gaussian Blur → Canny Edge Detection → Contour Detection → Corner Ordering → Perspective Transform → Adaptive Thresholding

## Requirements
- Python 3.9+
- OpenCV
- NumPy
- Pillow
- Tkinter (normally included with Python)

## Installation
```bash
pip install -r requirements.txt
```

## Run with the sample
From the project root:
```bash
python source_code/document_scanner.py --input sample_input/real_document_photo.jpg
```

## Normal GUI run
```bash
python source_code/document_scanner.py
```
A file picker opens so you can select any suitable document photograph.

## Output
Results are saved in the `output/` folder:
- `01_original.jpg`
- `02_edges.jpg`
- `03_detected_document.jpg`
- `04_scanned_document.jpg`
- `05_clean_scanned_document.jpg`

## Tips
Keep the whole document inside the photo and make all four edges visible. A reasonably contrasting background gives better contour detection.

## Academic Note
The project is based on explainable image-processing methods and does not require an external AI model or cloud service.
