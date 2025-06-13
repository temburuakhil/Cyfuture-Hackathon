# Fintech Solution - Cyfuture Hackathon

A comprehensive financial management platform built for the Cyfuture Hackathon, integrating multiple AI-powered modules for efficient business operations and GST compliance.

## 🌟 Features

### 1. Mobile Scanner & Multilingual OCR
- High-accuracy (99%) invoice scanning
- Multilingual text extraction
- Support for multiple document formats

### 2. Auto-HSN/SAC Lookup & GSTIN Validation
- Automatic HSN/SAC code detection
- Real-time GSTIN validation
- Accurate tax classification

### 3. Automated Bank Reconciliation
- Intelligent transaction matching
- Automated reconciliation reports
- Real-time sync with bank statements

### 4. GST Reconciliation Assistant
- AI-driven GST categorization
- Automated match reports
- Compliance verification

### 5. One-Click GST Return Filing
- Automated return preparation
- Built-in compliance checks
- Streamlined filing process

### 6. Cash Flow Forecasting & Alerts
- Predictive analytics
- Intelligent alerts
- Financial insights dashboard

### 7. Offline Mode & Seamless Sync
- PWA capabilities
- Automatic data synchronization
- Offline-first architecture

### 8. Role-Based Access & Collaboration
- Secure multi-user access
- Customizable permissions
- Team collaboration tools

### 9. E-Way Bill Auto-Generation
- Automated bill creation
- Management dashboard
- Logistics integration

### 10. Multilingual Finance Chatbot
- AI-powered assistance
- Compliance guidance
- Operational support

## 🚀 Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS, Vite
- **Backend**: Python (FastAPI), Node.js
- **AI/ML**: Google Gemini, OpenAI GPT
- **Database**: SQLite
- **OCR Engine**: Tesseract
- **Authentication**: JWT

## 📦 Project Structure

```
├── src/                  # Main React application
├── finbot-linguist-ai/  # AI Chatbot module
├── GST Assistant/       # GST reconciliation module
├── invoice-processor/   # Invoice processing module
└── public/             # Static assets
```

## 🛠️ Setup & Installation

1. Clone the repository:
```bash
git clone https://github.com/temburuakhil/Cyfuture-Hackathon.git
cd Cyfuture-Hackathon
```

2. Install dependencies for the main app:
```bash
npm install
```

3. Setup the Finbot module:
```bash
cd finbot-linguist-ai
npm install
```

4. Setup the GST Assistant:
```bash
cd ../GST\ Assistant
pip install -r requirements.txt
```

5. Setup the Invoice Processor:
```bash
cd ../invoice-processor/backend
pip install -r requirements.txt
cd ../frontend
npm install
```

## 🏃‍♂️ Running the Application

1. Start the main application:
```bash
npm run dev
```

2. Start the Finbot module:
```bash
cd finbot-linguist-ai
npm run dev
```

3. Start the GST Assistant:
```bash
cd GST\ Assistant
streamlit run app.py
```

4. Start the Invoice Processor:
```bash
cd invoice-processor
# Terminal 1 - Backend
cd backend
python main.py
# Terminal 2 - Frontend
cd frontend
npm start
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is [MIT](LICENSE) licensed.


## 🙏 Acknowledgments

- Cyfuture for organizing the hackathon
- All the open-source libraries and tools used in this project
