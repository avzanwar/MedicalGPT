from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai
import pandas as pd
import os
from dotenv import load_dotenv
from generate_medical_data import generate_medical_records

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Configure Google Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash')

# Generate medical records if they don't exist
if not os.path.exists('medical_records.csv'):
    print("Generating medical records...")
    df = generate_medical_records()
    df.to_csv('medical_records.csv', index=False)
    print("Medical records generated successfully!")

# Load medical records
medical_records = pd.read_csv('medical_records.csv')

# Store conversation history
conversation_history = {}

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_symptoms():
    try:
        data = request.json
        user_input = data.get('symptoms', '')
        session_id = data.get('session_id', '')
        is_followup = data.get('is_followup', False)
        
        # Get or create conversation history
        if session_id not in conversation_history:
            conversation_history[session_id] = []
        
        # Find similar cases
        similar_cases = medical_records[
            medical_records['symptoms'].str.contains(user_input, case=False, na=False)
        ].head(3)
        
        # Prepare context
        context = "You are a medical doctor providing a professional consultation. Respond in this format:\n\n"
        context += "CLINICAL ASSESSMENT:\n"
        context += "- Primary Symptoms:\n"
        context += "- Duration and Progression:\n"
        context += "- Associated Symptoms:\n\n"
        
        context += "DIFFERENTIAL DIAGNOSIS:\n"
        context += "- Most Likely:\n"
        context += "- Other Possibilities:\n\n"
        
        context += "RECOMMENDATIONS:\n"
        context += "- Immediate Actions:\n"
        context += "- Follow-up Steps:\n\n"
        
        context += "CLINICAL URGENCY: [EMERGENT/URGENT/ROUTINE]\n\n"
        
        if is_followup and conversation_history[session_id]:
            context += "Previous Consultation Summary:\n"
            for msg in conversation_history[session_id][-2:]:
                if msg['role'] == 'user':
                    context += f"Patient: {msg['content']}\n"
                else:
                    context += f"Doctor: {msg['content']}\n"
            context += "\n"
        
        context += f"Current Patient Report: {user_input}\n\n"
        context += "Relevant Clinical Cases:\n"
        
        for _, case in similar_cases.iterrows():
            context += f"- Case Presentation: {case['symptoms']}\n"
            context += f"  Final Diagnosis: {case['conditions']}\n"
            context += f"  Treatment Plan: {case['medications']}\n\n"
        
        # Generate response
        response = model.generate_content(
            f"{context}\nProvide a professional medical consultation. "
            "Use medical terminology appropriately. "
            "Be clear and concise while maintaining a professional tone. "
            "Remember to emphasize that this is not a substitute for in-person medical evaluation."
        )
        
        # Update conversation history
        conversation_history[session_id].append({
            'role': 'user',
            'content': user_input
        })
        conversation_history[session_id].append({
            'role': 'assistant',
            'content': response.text
        })
        
        # Keep only last 6 messages
        conversation_history[session_id] = conversation_history[session_id][-6:]
        
        return jsonify({
            'advice': response.text,
            'similar_cases': similar_cases.to_dict('records'),
            'session_id': session_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 