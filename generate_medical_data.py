import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Define lists for generating realistic medical data
conditions = [
    "Hypertension", "Type 2 Diabetes", "Asthma", "Arthritis", "Migraine",
    "Anxiety", "Depression", "GERD", "Hypothyroidism", "High Cholesterol",
    "Osteoporosis", "Sleep Apnea", "Fibromyalgia", "Chronic Pain", "Allergies"
]

symptoms = [
    "Headache", "Fever", "Cough", "Fatigue", "Nausea",
    "Dizziness", "Chest Pain", "Shortness of Breath", "Joint Pain",
    "Abdominal Pain", "Rash", "Insomnia", "Anxiety", "Depression",
    "Muscle Weakness", "Vision Problems", "Hearing Loss", "Memory Issues"
]

medications = [
    "Lisinopril", "Metformin", "Albuterol", "Ibuprofen", "Sumatriptan",
    "Sertraline", "Omeprazole", "Levothyroxine", "Atorvastatin",
    "Alendronate", "CPAP", "Gabapentin", "Loratadine", "Aspirin",
    "Metoprolol", "Warfarin", "Insulin", "Prednisone"
]

def generate_medical_records(num_records=50000):
    records = []
    
    for _ in range(num_records):
        # Generate random patient age between 18 and 90
        age = random.randint(18, 90)
        
        # Generate random conditions (1-3 per patient)
        num_conditions = random.randint(1, 3)
        patient_conditions = random.sample(conditions, num_conditions)
        
        # Generate random symptoms (2-5 per patient)
        num_symptoms = random.randint(2, 5)
        patient_symptoms = random.sample(symptoms, num_symptoms)
        
        # Generate random medications (1-4 per patient)
        num_medications = random.randint(1, 4)
        patient_medications = random.sample(medications, num_medications)
        
        # Generate random vital signs
        blood_pressure = f"{random.randint(90, 140)}/{random.randint(60, 90)}"
        heart_rate = random.randint(60, 100)
        temperature = round(random.uniform(36.1, 37.2), 1)
        
        # Generate random visit date within last 2 years
        visit_date = datetime.now() - timedelta(days=random.randint(0, 730))
        
        record = {
            'patient_id': f"P{random.randint(10000, 99999)}",
            'age': age,
            'gender': random.choice(['M', 'F']),
            'conditions': ', '.join(patient_conditions),
            'symptoms': ', '.join(patient_symptoms),
            'medications': ', '.join(patient_medications),
            'blood_pressure': blood_pressure,
            'heart_rate': heart_rate,
            'temperature': temperature,
            'visit_date': visit_date.strftime('%Y-%m-%d'),
            'notes': f"Patient reported {random.choice(patient_symptoms)}. "
                    f"Currently taking {random.choice(patient_medications)}. "
                    f"Follow-up recommended in {random.randint(1, 6)} months."
        }
        records.append(record)
    
    return pd.DataFrame(records)

if __name__ == "__main__":
    # Generate the medical records
    df = generate_medical_records()
    
    # Save to CSV
    df.to_csv('medical_records.csv', index=False)
    print(f"Generated {len(df)} medical records and saved to medical_records.csv") 