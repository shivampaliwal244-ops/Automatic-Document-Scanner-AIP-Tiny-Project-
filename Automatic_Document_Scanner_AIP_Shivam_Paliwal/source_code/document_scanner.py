"""
Automatic Document Scanner
Advanced Image Processing - Tiny Project

Student: Shivam Paliwal
Enrollment No.: 2305101270430
Program: BCA (Hons.) | Semester 7 | Division A

GUI run:
    python source_code/document_scanner.py

Quick test / demo run:
    python source_code/document_scanner.py --input sample_input/sample_document.jpg
"""

import argparse
import os
import cv2
import numpy as np
from tkinter import Tk, filedialog, messagebox

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def order_points(points):
    """Return four corners in top-left, top-right, bottom-right, bottom-left order."""
    pts = np.array(points, dtype="float32")
    ordered = np.zeros((4, 2), dtype="float32")

    sums = pts.sum(axis=1)
    differences = np.diff(pts, axis=1).reshape(-1)

    ordered[0] = pts[np.argmin(sums)]
    ordered[2] = pts[np.argmax(sums)]
    ordered[1] = pts[np.argmin(differences)]
    ordered[3] = pts[np.argmax(differences)]
    return ordered


def four_point_transform(image, points):
    """Flatten the detected page into a rectangular view."""
    rect = order_points(points)
    top_left, top_right, bottom_right, bottom_left = rect

    width_a = np.linalg.norm(bottom_right - bottom_left)
    width_b = np.linalg.norm(top_right - top_left)
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(top_right - bottom_right)
    height_b = np.linalg.norm(top_left - bottom_left)
    max_height = max(int(height_a), int(height_b))

    destination = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(rect, destination)
    return cv2.warpPerspective(image, matrix, (max_width, max_height))


def find_document_contour(edges, image_area):
    """Find a large, convex, four-sided contour."""
    contours, _ = cv2.findContours(
        edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours[:30]:
        area = cv2.contourArea(contour)
        if area < image_area * 0.15:
            continue

        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(approx) == 4 and cv2.isContourConvex(approx):
            return approx.reshape(4, 2)

    return None


def clean_scanned_page(page):
    """Create a readable black-and-white scan."""
    gray = cv2.cvtColor(page, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    return cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        21, 12
    )


def scan_document(image_path):
    """Run the complete document-scanning pipeline."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("The selected image could not be opened.")

    original = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contour = find_document_contour(
        edges, image.shape[0] * image.shape[1]
    )

    if contour is None:
        raise ValueError(
            "No clear document boundary was detected. "
            "Keep the complete page and all four edges visible."
        )

    marked = original.copy()
    cv2.polylines(
        marked, [contour.reshape(-1, 1, 2)],
        True, (0, 180, 0), 5
    )

    scanned = four_point_transform(original, contour)
    cleaned = clean_scanned_page(scanned)

    cv2.imwrite(os.path.join(OUTPUT_DIR, "01_original.jpg"), original)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "02_edges.jpg"), edges)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "03_detected_document.jpg"), marked)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "04_scanned_document.jpg"), scanned)
    cv2.imwrite(os.path.join(OUTPUT_DIR, "05_clean_scanned_document.jpg"), cleaned)

    return cleaned


def choose_image():
    """Open a simple file picker for normal GUI use."""
    root = Tk()
    root.withdraw()

    image_path = filedialog.askopenfilename(
        title="Select a document photo",
        filetypes=[
            ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ("All files", "*.*")
        ]
    )
    root.destroy()

    if not image_path:
        return

    try:
        scan_document(image_path)
        messagebox.showinfo(
            "Scan Complete",
            "Document scanned successfully.\n"
            "Open the output folder to view the results."
        )
    except Exception as error:
        messagebox.showerror("Scanning Error", str(error))


def main():
    parser = argparse.ArgumentParser(
        description="Automatic Document Scanner using OpenCV"
    )
    parser.add_argument(
        "--input",
        help="Path to an image. If omitted, a file picker opens."
    )
    args = parser.parse_args()

    if args.input:
        scan_document(os.path.abspath(args.input))
        print("Scan complete.")
        print("Results saved in:", OUTPUT_DIR)
    else:
        choose_image()


if __name__ == "__main__":
    main()
