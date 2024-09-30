import PyPDF2
import matplotlib.pyplot as plt

def extract_marks(pdf_file, roll_number):
    # Read the PDF file
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    
    # Extract text from each page
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    # Search for the roll number
    lines = text.split('\n')
    marks = None
    for line in lines:
        if roll_number in line:
            marks = line
            break
    
    # Extract CT marks
    if marks:
        data = marks.split()
        if len(data) >= 3:
            ct1 = data[1]
            ct2 = data[2]
            return ct1, ct2
        else:
            return None, None
    else:
        return None, None

def plot_marks(ct1, ct2, roll_number):
    # Data for plotting
    tests = ['CT1', 'CT2']
    marks = [float(ct1), float(ct2)]
    
    # Plot
    plt.figure(figsize=(5, 5))
    plt.bar(tests, marks, color=['blue', 'green'])
    plt.title(f"Marks for Roll Number: {roll_number}")
    plt.xlabel("Class Tests")
    plt.ylabel("Marks")
    plt.ylim(0, 20)  # Assuming marks are out of 20
    plt.show()

# Ask for the roll number
roll_number = input("What is your roll number? ")

# Specify the path to your PDF
pdf_file = "3107_marks.pdf"  # Update this to the correct file path

# Extract marks
ct1, ct2 = extract_marks(pdf_file, roll_number)

# Plot the marks if available
if ct1 is not None and ct2 is not None:
    plot_marks(ct1, ct2, roll_number)
else:
    print("Could not find marks for the provided roll number.")
