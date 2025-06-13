from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import pytesseract
from PIL import Image
import io
import re
from datetime import datetime
import pandas as pd
import os
from pathlib import Path
import fitz  # PyMuPDF for PDF handling
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload and processed directories if they don't exist
UPLOAD_DIR = Path("../uploads")
PROCESSED_DIR = Path("../processed")
UPLOAD_DIR.mkdir(exist_ok=True)
PROCESSED_DIR.mkdir(exist_ok=True)

class InvoiceData(BaseModel):
    invoice_number: str
    invoice_date: str
    vendor_name: str
    total_amount: str
    due_date: Optional[str] = None

class BulkInvoiceData(BaseModel):
    invoices: List[InvoiceData]

def extract_date(text):
    # Common date patterns
    patterns = [
        r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            return matches[0]
    return None

def extract_amount(text):
    # Look for currency amounts
    pattern = r'(?:USD|EUR|GBP|[$€£])?\s*\d+(?:,\d{3})*(?:\.\d{2})?'
    matches = re.findall(pattern, text)
    if matches:
        return matches[0]
    return None

def extract_invoice_number(text):
    # Look for invoice numbers (common patterns)
    patterns = [
        r'INV[-\s]?\d+',
        r'Invoice\s+#?\s*\d+',
        r'Bill\s+#?\s*\d+'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return matches[0]
    return None

def extract_vendor_name(text):
    # Look for common vendor name patterns
    patterns = [
        r'(?:From|Vendor|Company|Seller):\s*([A-Za-z0-9\s&.,]+)',
        r'(?:Bill To|Sold To):\s*([A-Za-z0-9\s&.,]+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            return matches[0].strip()
    return None

def process_pdf(file_content):
    try:
        # Open PDF file
        pdf_document = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        
        # Extract text from each page
        for page in pdf_document:
            text += page.get_text()
        
        return text
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

def process_image(file_content):
    try:
        # Open image file
        image = Image.open(io.BytesIO(file_content))
        # Convert to text using OCR
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/upload/")
async def upload_invoice(file: UploadFile = File(...)):
    try:
        # Read file content
        contents = await file.read()
        
        # Save file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Process file based on content type
        content_type = file.content_type
        if content_type == "application/pdf":
            text = process_pdf(contents)
        elif content_type.startswith("image/"):
            text = process_image(contents)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Extract information
        invoice_data = {
            "invoice_number": extract_invoice_number(text) or "",
            "invoice_date": extract_date(text) or "",
            "vendor_name": extract_vendor_name(text) or "",
            "total_amount": extract_amount(text) or "",
            "due_date": extract_date(text) or "",
            "filename": file.filename  # Add filename to response
        }
        
        return invoice_data
    
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/bulk/")
async def upload_multiple_invoices(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        try:
            result = await upload_invoice(file)
            results.append(result)
        except Exception as e:
            results.append({
                "error": str(e),
                "filename": file.filename
            })
    return results

@app.post("/save/")
async def save_invoice(data: InvoiceData):
    try:
        # Convert to DataFrame and save as CSV
        df = pd.DataFrame([data.dict()])
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = PROCESSED_DIR / f"invoice_{timestamp}.csv"
        df.to_csv(output_file, index=False)
        return {"message": "Invoice data saved successfully"}
    
    except Exception as e:
        logger.error(f"Error saving invoice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/save/bulk/")
async def save_bulk_invoices(data: BulkInvoiceData):
    try:
        # Convert to DataFrame and save as CSV
        df = pd.DataFrame([invoice.dict() for invoice in data.invoices])
        
        # Rename columns for better readability
        df = df.rename(columns={
            'invoice_number': 'Invoice Number',
            'invoice_date': 'Invoice Date',
            'vendor_name': 'Vendor Name',
            'total_amount': 'Total Amount',
            'due_date': 'Due Date'
        })
        
        # Reorder columns
        df = df[['Invoice Number', 'Invoice Date', 'Vendor Name', 'Total Amount', 'Due Date']]
        
        # Format the data
        df['Total Amount'] = df['Total Amount'].apply(lambda x: f"${x}" if x and not x.startswith('$') else x)
        
        # Add timestamp to filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = PROCESSED_DIR / f"invoices_bulk_{timestamp}.csv"
        
        # Save with proper formatting
        df.to_csv(
            output_file,
            index=False,
            encoding='utf-8',
            date_format='%Y-%m-%d',
            float_format='%.2f'
        )
        
        return {
            "message": f"{len(data.invoices)} invoices saved successfully",
            "filename": output_file.name
        }
    
    except Exception as e:
        logger.error(f"Error saving bulk invoices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/latest/")
async def download_latest_csv(background_tasks: BackgroundTasks):
    try:
        # Get the most recent CSV file from the processed directory
        csv_files = list(PROCESSED_DIR.glob("invoices_bulk_*.csv"))
        if not csv_files:
            raise HTTPException(status_code=404, detail="No processed invoices found")
        
        latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)
        
        # Read the CSV file
        df = pd.read_csv(latest_file)
        
        # Format the data before sending
        df['Total Amount'] = df['Total Amount'].apply(lambda x: f"${x}" if x and not str(x).startswith('$') else x)
        
        # Create a temporary file with formatted data
        temp_file = PROCESSED_DIR / f"temp_{latest_file.name}"
        df.to_csv(
            temp_file,
            index=False,
            encoding='utf-8',
            date_format='%Y-%m-%d',
            float_format='%.2f'
        )
        
        # Schedule deletion of the temp file after response
        background_tasks.add_task(temp_file.unlink)
        
        return FileResponse(
            path=temp_file,
            filename=latest_file.name,
            media_type="text/csv"
        )
    except Exception as e:
        logger.error(f"Error downloading CSV: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 