# Invoice Processing Tool

A simple tool for processing invoices using OCR to extract key information and save it to CSV format.

## Features

- Upload invoice files (PDF, JPG, PNG)
- Extract essential fields using OCR:
  * Invoice number
  * Invoice date
  * Vendor name
  * Total amount
  * Due date
- Edit extracted data before saving
- Export to CSV format
- Simple drag-and-drop interface

## Prerequisites

- Python 3.8+
- Node.js 14+
- Tesseract OCR

### Installing Tesseract OCR

#### Windows
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH

#### Linux
```bash
sudo apt-get install tesseract-ocr
```

#### macOS
```bash
brew install tesseract
```

## Setup

1. Clone the repository
2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
cd backend
python main.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Open http://localhost:3000 in your browser

## Usage

1. Drag and drop an invoice file (PDF, JPG, or PNG) onto the upload area
2. Review the extracted data
3. Make any necessary corrections
4. Click "Save" to export the data to CSV format

## Project Structure

```
invoice-processor/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── App.js
│   └── package.json
├── uploads/
├── processed/
└── README.md
```

## Notes

- The OCR accuracy depends on the quality of the input images
- Supported file formats: PDF, JPG, PNG
- Processed files are saved in the `processed` directory
- Original files are stored in the `uploads` directory 