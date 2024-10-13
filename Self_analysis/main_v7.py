import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Function to extract marks of all students from a PDF
def extract_all_marks_from_pdf(pdf_file): ### Changed this function
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text()+"\n"

    lines = text.split('\n')
    
    all_marks = []  # To store the marks of all students in this PDF
    i = 0
    for line in lines:
        data = line.split()
        # Ensure the line has enough data and starts with a digit (indicating a roll number)
        if len(data) >= 2 and data[0].isdigit():
            all_marks.append([])
            for element in range(1,len(data)):        
                try :
                    all_marks[i].append(
                        float(data[element]) if data[element] != "A" else 0
                    )
                except ValueError:      
                    break  # Skip lines that cannot be processed as marks
            i += 1
    return all_marks

# Function to extract a specific student's marks
def extract_student_marks_from_pdf(pdf_file, roll_number):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    for page in pdf_reader.pages:
        text += page.extract_text()+"\n"
    
    lines = text.split('\n')
    student_marks = None

    for line in lines:
        data = line.split()
        if roll_number in line:
            student_marks = line
            break

    ct_marks = []
    if student_marks:
        data = student_marks.split()
        for i in range(1, len(data)):
            if i <= 4:  # Only handle up to 4 CTs
                ct_marks.append(float(data[i]) if data[i] != "A" else 0)

    return ct_marks

# Accumulate CT marks for the target student from multiple PDFs
def accumulate_student_ct_marks(pdf_files, roll_number):
    accumulated_marks = []

    for pdf_file in pdf_files:
        ct_marks = extract_student_marks_from_pdf(pdf_file, roll_number)
        accumulated_marks.extend(ct_marks)
        
    ######## Removed the part that appends 0 if the accumulated_marks is not of length 4
    return accumulated_marks

# Function to calculate averages from all students' marks
def calculate_averages(all_students_marks): ## Changed this function

    marks_array = np.array(all_students_marks, dtype=float)
    avg_marks = np.mean(marks_array,axis = 0)

    return list(avg_marks)

# Plot the marks and averages, and save to a PDF
def plot_marks(marks, avg_marks, roll_number):
    n = len(marks)
    stock_col = ['blue', 'green', 'red', 'black', 'yellow', 'violet']
    col = stock_col[:n]
    tests = [f"CT{i+1}" for i in range(n)]
    averages = avg_marks

    plt.figure(figsize=(7, 5))
    
    # Plot student marks as a line plot
    plt.plot(tests, marks, color='blue', marker='o', label="Student's Marks", linewidth=2)
    
    # Plot average marks as a line plot with matching colors
    plt.plot(tests, averages, color='green', marker='x', linestyle='--', label="Average Marks", linewidth=2)

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
    
    # Accumulate CT marks from multiple PDFs for the target student
    ct_marks = accumulate_student_ct_marks(pdf_files, roll_number)

    # Collect marks for all students across all PDFs
    # Calculate averages based on all students' marks
    average_marks = []
    for pdf_file in pdf_files:
        average_marks.extend(calculate_averages(extract_all_marks_from_pdf(pdf_file)))
    # Update the result label
    text = ""  ## Changed the Update so that it only updates the given ct data.
    for i in range(len(ct_marks)):
        text += "  "+f"CT{i+1}: {ct_marks[i]}"
    result_label.config(text=text)
    
    # Plot and save the results to PDF
    plot_pdf = plot_marks(ct_marks, average_marks, roll_number)

    # Merge the student results and plot into a single PDF
    final_output = f"Combined_Marks_for_{roll_number}.pdf"
    try :
        merge_pdfs([plot_pdf] + list(pdf_files), final_output)
    
        messagebox.showinfo("Success", f"Results saved to {final_output}")
    except:
        messagebox.showinfo("Error saving", f"Results saved to {final_output}")
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
