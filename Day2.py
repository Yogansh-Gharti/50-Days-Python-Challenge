from pypdf import PdfReader, PdfWriter
import pdfplumber

def merge_pdfs(files, output):
    writer = PdfWriter()

    for file in files:
        reader = PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)

    with open(output, "wb") as f:
        writer.write(f)

    print("✅ PDFs Merged Successfully!")


def split_pdf(file):
    reader = PdfReader(file)

    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)

        with open(f"page_{i+1}.pdf", "wb") as f:
            writer.write(f)

    print("✅ PDF Split Successfully!")


def rotate_pdf(file, output):
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(90)
        writer.add_page(page)

    with open(output, "wb") as f:
        writer.write(f)

    print("✅ PDF Rotated!")


def extract_text(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"

    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("✅ Text Extracted!")


def protect_pdf(file, password):
    reader = PdfReader(file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    writer.encrypt(password)

    with open("protected.pdf", "wb") as f:
        writer.write(f)

    print("✅ Password Protected PDF Created!")


while True:

    print("\n===== SMART PDF TOOLKIT =====")
    print("1.Merge PDFs")
    print("2.Split PDF")
    print("3.Rotate PDF")
    print("4.Extract Text")
    print("5.Protect PDF")
    print("6.Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        files = input("Enter PDF names separated by comma: ").split(",")
        merge_pdfs([f.strip() for f in files], "merged.pdf")

    elif choice == "2":
        split_pdf(input("Enter PDF: "))

    elif choice == "3":
        rotate_pdf(input("Enter PDF: "), "rotated.pdf")

    elif choice == "4":
        extract_text(input("Enter PDF: "))

    elif choice == "5":
        pdf = input("Enter PDF: ")
        pwd = input("Password: ")
        protect_pdf(pdf, pwd)

    elif choice == "6":
        break

    else:
        print("Invalid Choice")
