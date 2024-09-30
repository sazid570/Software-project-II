import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import matplotlib.pyplot as plt
import numpy as np

def extract_marks(pdf_file, roll_number):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    lines = text.split('\n')
    marks = None
    all_marks = []

    for line in lines:
        data = line.split()
        
        # Ensure the line has enough data and starts with a digit (indicating a roll number)
        if len(data) >= 2 and data[0].isdigit():
            try:
                all_marks.append([
                    float(data[1]) if data[1] != "A" else 0,  # CT1
                    float(data[2]) if len(data) > 2 and data[2] != "A" else 0,  # CT2
                    float(data[3]) if len(data) > 3 and data[3] != "A" else 0,  # CT3
                    float(data[4]) if len(data) > 4 and data[4] != "A" else 0   # CT4
                ])
            except ValueError:
                continue  # Skip lines that cannot be processed as marks
        
        # Extract the specific roll number's marks
        if roll_number in line:
            marks = line

    if marks:
        data = marks.split()
        ct1 = data[1] if data[1] != "A" else "0"
        ct2 = data[2] if len(data) > 2 and data[2] != "A" else "0"
        ct3 = data[3] if len(data) > 3 and data[3] != "A" else "0"
        ct4 = data[4] if len(data) > 4 and data[4] != "A" else "0"
        return ct1, ct2, ct3, ct4, all_marks
    else:
        return None, None, None, None, all_marks

def calculate_averages(all_marks):
    if not all_marks:
        return 0, 0, 0, 0
    avg_ct1 = np.mean([marks[0] for marks in all_marks])
    avg_ct2 = np.mean([marks[1] for marks in all_marks])
    avg_ct3 = np.mean([marks[2] for marks in all_marks])
    avg_ct4 = np.mean([marks[3] for marks in all_marks])
    return avg_ct1, avg_ct2, avg_ct3, avg_ct4

def plot_marks(ct1, ct2, ct3, ct4, avg_ct1, avg_ct2, avg_ct3, avg_ct4, roll_number):
    tests = ['CT1', 'CT2', 'CT3', 'CT4']
    marks = [float(ct1), float(ct2), float(ct3), float(ct4)]
    averages = [avg_ct1, avg_ct2, avg_ct3, avg_ct4]
    
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
    plt.show()

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, file_path)

def find_marks():
    roll_number = roll_entry.get().strip()
    pdf_file = pdf_entry.get().strip()
    
    if not roll_number:
        messagebox.showwarning("Input Error", "Please enter your roll number.")
        return
    
    if not pdf_file:
        messagebox.showwarning("Input Error", "Please select a PDF file.")
        return
    
    ct1, ct2, ct3, ct4, all_marks = extract_marks(pdf_file, roll_number)
    avg_ct1, avg_ct2, avg_ct3, avg_ct4 = calculate_averages(all_marks)
    
    if ct1 is not None and ct2 is not None:
        result_label.config(text=f"CT1: {ct1}, CT2: {ct2}, CT3: {ct3}, CT4: {ct4}")
        plot_marks(ct1, ct2, ct3, ct4, avg_ct1, avg_ct2, avg_ct3, avg_ct4, roll_number)
    else:
        result_label.config(text="Marks not found for the given roll number.")

# Create the main window
root = tk.Tk()
root.title("CT Marks Finder")

# Roll Number Input
tk.Label(root, text="Enter Roll Number:").grid(row=0, column=0, padx=10, pady=10)
roll_entry = tk.Entry(root)
roll_entry.grid(row=0, column=1, padx=10, pady=10)

# PDF File Input
tk.Label(root, text="Select PDF File:").grid(row=1, column=0, padx=10, pady=10)
pdf_entry = tk.Entry(root)
pdf_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_file).grid(row=1, column=2, padx=10, pady=10)

# Submit Button
tk.Button(root, text="Find Marks", command=find_marks).grid(row=2, column=1, padx=10, pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

# Start the application
root.mainloop()
