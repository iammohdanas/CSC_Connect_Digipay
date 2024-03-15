import os
import requests
import tabula

output_directory = "mainapp/api_err_pdf_json"
os.makedirs(output_directory, exist_ok=True)

pdf_url = "https://nulm.gov.in/PDF/UIDAI-APIerrorcode.pdf"

# Download the PDF file
def pdf_csv(pdf_url):
    response = requests.get(pdf_url)
    with open(os.path.join(output_directory, "uidai_error_codes.pdf"), "wb") as f:
        f.write(response.content)   
    # Specify the path to the downloaded PDF file
    pdf_file = os.path.join(output_directory, "uidai_error_codes.pdf")
    # Specify the output CSV file path
    output_csv = os.path.join(output_directory, "output.csv")
    tabula.convert_into(pdf_file, output_csv, output_format="csv", pages='all')


def pdf_json(pdf_url):
    response = requests.get(pdf_url)
    with open(os.path.join(output_directory, "uidai_error_codes.pdf"), "wb") as f:
        f.write(response.content)
    # Specify the path to the downloaded PDF file
    pdf_file = os.path.join(output_directory, "uidai_error_codes.pdf")
    # Specify the output json file path
    output_json = os.path.join(output_directory, "output.json")
    tabula.convert_into(pdf_file, output_json, output_format="json", pages='all')

# Call the function