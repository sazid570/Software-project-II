import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
from matplotlib.backends.backend_pdf import PdfPages

# Function to extract marks from a single PDF
def extract_marks_from_pdf(pdf_file, roll_number):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    lines = text.split('\n')
    marks = None
    ct_marks = []  # Store CT marks from this PDF

    for line in lines:
        data = line.split()
        
        # Ensure the line has enough data and starts with a digit (indicating a roll number)
        if len(data) >= 2 and data[0].isdigit():
            if roll_number in line:
                marks = line
                break
    
    if marks:
        data = marks.split()
        # Extract CT marks from this line (after the roll number)
        for i in range(1, len(data)):  # Skip the roll number (first element)
            if i <= 4:  # Only handle up to 4 CTs
                ct_marks.append(float(data[i]) if data[i] != "A" else 0)

    return ct_marks

# Function to accumulate CT marks from multiple PDFs
def accumulate_ct_marks(pdf_files, roll_number):
    accumulated_marks = []  # This will store all CT marks sequentially

    for pdf_file in pdf_files:
        ct_marks = extract_marks_from_pdf(pdf_file, roll_number)
        accumulated_marks.extend(ct_marks)  # Add marks to the array
        print(f"Extracted marks from {pdf_file}: {ct_marks}")  # Debugging output

    # Ensure that the array has 4 entries, padding with zeros if necessary
    while len(accumulated_marks) < 4:
        accumulated_marks.append(0)

    return accumulated_marks

# Function to calculate averages
def calculate_averages(all_marks):
    if not all_marks:
        return 0, 0, 0, 0
    avg_ct1 = np.mean([marks[0] for marks in all_marks if len(marks) > 0])
    avg_ct2 = np.mean([marks[1] for marks in all_marks if len(marks) > 1])
    avg_ct3 = np.mean([marks[2] for marks in all_marks if len(marks) > 2])
    avg_ct4 = np.mean([marks[3] for marks in all_marks if len(marks) > 3])
    return avg_ct1, avg_ct2, avg_ct3, avg_ct4

# Function to plot CT marks and averages
def plot_marks(ct_marks, avg_ct_marks, roll_number):
    tests = ['CT1', 'CT2', 'CT3', 'CT4']
    marks = ct_marks
    averages = avg_ct_marks
    
    plt.figure(figsize=(7, 5))
    plt.bar(tests, marks, color=['blue', 'green', 'red', 'purple'], label="Student's Marks")
    
    # Plot average lines
    for i, avg in enumerate(averages):
        plt.axhline(y=avg, color=['blue', 'green', 'red', 'purple'][i], linestyle='--', label=f'Avg {tests[i]}: {avg:.2f}')
    
    plt.title(f"Marks for Roll Number: {roll_number}")
    plt.xlabel("Class Tests")
    plt.ylabel("Marks")
    plt.ylim(0, 20)  # Assuming marks are out of 20
    plt.legend()

    # Save the plot to a PDF page
    pdf_filename = f"Marks_for_{roll_number}.pdf"
    with PdfPages(pdf_filename) as pdf:
        pdf.savefig()  # Save the current figure
    plt.close()  # Close the plot

    return pdf_filename

# Function to merge PDFs into one
def merge_pdfs(pdf_files, output_path):
    pdf_merger = PyPDF2.PdfMerger()

    for pdf in pdf_files:
        pdf_merger.append(pdf)

    with open(output_path, 'wb') as output_pdf:
        pdf_merger.write(output_pdf)

# File browser for multiple PDFs
def browse_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
    if file_paths:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, ', '.join(file_paths))
    else:
        messagebox.showwarning("File Selection Error", "No file was selected.")

# Process all PDFs and calculate the results
def find_marks():
    roll_number = roll_entry.get().strip()
    pdf_files = pdf_entry.get().strip().split(', ')
    
    if not roll_number:
        messagebox.showwarning("Input Error", "Please enter your roll number.")
        return
    
    if not pdf_files or pdf_files == ['']:
        messagebox.showwarning("Input Error", "Please select at least one PDF file.")
        return
    
    # Accumulate CT marks from multiple PDFs
    ct_marks = accumulate_ct_marks(pdf_files, roll_number)

    # Simulate class marks for average calculation (this should be collected from all students in real case)
    all_marks = [ct_marks]  # Simulating marks from other students for now
    avg_ct1, avg_ct2, avg_ct3, avg_ct4 = calculate_averages(all_marks)

    # Update the result label
    result_label.config(text=f"CT1: {ct_marks[0]}, CT2: {ct_marks[1]}, CT3: {ct_marks[2]}, CT4: {ct_marks[3]}")

    # Plot and save the results to PDF
    plot_pdf = plot_marks(ct_marks, [avg_ct1, avg_ct2, avg_ct3, avg_ct4], roll_number)

    # Merge the student results and plot into a single PDF
    final_output = f"Combined_Marks_for_{roll_number}.pdf"
    merge_pdfs([plot_pdf] + list(pdf_files), final_output)

    messagebox.showinfo("Success", f"Results saved to {final_output}")

# GUI Setup
root = tk.Tk()
root.title("CT Marks Finder")

# Roll Number Input
tk.Label(root, text="Enter Roll Number:").grid(row=0, column=0, padx=10, pady=10)
roll_entry = tk.Entry(root)
roll_entry.grid(row=0, column=1, padx=10, pady=10)

# PDF File Input
tk.Label(root, text="Select PDF Files:").grid(row=1, column=0, padx=10, pady=10)
pdf_entry = tk.Entry(root, width=50)
pdf_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_files).grid(row=1, column=2, padx=10, pady=10)

# Submit Button
tk.Button(root, text="Find Marks", command=find_marks).grid(row=2, column=1, padx=10, pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Start the application
root.mainloop()
