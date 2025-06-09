# MedicalGPT - AI Medical Assistant

MedicalGPT is an AI-powered medical consultation assistant that uses Google's Gemini AI model to analyze patient symptoms and provide medical advice based on a database of medical records.

## Features

- AI-powered medical consultation using Google Gemini
- Analysis based on 5000 sample medical records
- Modern, responsive web interface
- Real-time symptom analysis
- Similar case matching
- Professional medical response format

## Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd MedicalGPT
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file and add your Google Gemini API key:
```
GOOGLE_API_KEY=your_api_key_here
```

5. Generate sample medical records:
```bash
python generate_medical_data.py
```

6. Run the application:
```bash
python app.py
```

7. Open your browser and navigate to `http://localhost:5000`

## Deployment to Render

1. Create a free account on [Render](https://render.com)

2. Fork this repository to your GitHub account

3. In Render:
   - Click "New +"
   - Select "Web Service"
   - Connect your GitHub repository
   - Configure the service:
     - Name: medicalgpt
     - Environment: Python
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Add environment variable:
     - Key: GOOGLE_API_KEY
     - Value: Your Google Gemini API key

4. Click "Create Web Service"

Your application will be deployed and available at `https://medicalgpt.onrender.com` (or similar URL)

## Important Notes

- This application is for educational purposes only
- Not a substitute for professional medical advice
- Always consult healthcare professionals for medical decisions
- Keep your API key secure and never commit it to version control

## License

MIT License 