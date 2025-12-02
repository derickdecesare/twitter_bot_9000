import requests
import PyPDF2
import io

def download_and_extract_text(arxiv_id: str, output_file: str = None) -> str:
    """
    Downloads the PDF for a given arXiv ID, extracts its text content, and optionally saves it to a file.
    
    Args:
    arxiv_id (str): The arXiv ID of the paper.
    output_file (str, optional): The filename to save the extracted text. If None, text is not saved to a file.
    
    Returns:
    str: The extracted text content.
    """
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    # url = "https://storage.googleapis.com/deepmind-media/AlphaCode2/AlphaCode2_Tech_Report.pdf"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to download PDF. Status code: {response.status_code}"
    
    text = ""
    with io.BytesIO(response.content) as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    # Limit to first 1,000,000 characters to avoid potential token limits
    text = text[:1000000]
    
    # Save to file if output_file is provided
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Text saved to {output_file}")
    
    return text


# https://arxiv.org/pdf/2203.11171
# Usage
arxiv_id = "2203.11171"
output_file = "self-consistency.txt"
extracted_text = download_and_extract_text(arxiv_id, output_file)
print("First 500 characters of extracted text:")
print(extracted_text[:500])