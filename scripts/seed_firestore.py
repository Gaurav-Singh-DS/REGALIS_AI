import os
import json
import pandas as pd
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

def seed_firestore():
    print("🚀 Seeding NovaBank Data into Firestore...")
    
    # In a real scenario, we would use a service account JSON
    # For the local prototype, we assume the environment is configured
    # or we use the emulator.
    try:
        if not firebase_admin._app.exists:
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"⚠️ Firebase Init Error: {e}")
        print("Note: This script requires GOOGLE_APPLICATION_CREDENTIALS or Firebase Emulator.")
        return

    db = firestore.client()

    # --- 1. Seed Reports ---
    report_id = "rep_credit_risk_2026_09"
    report_ref = db.collection('reports').document(report_id)
    report_ref.set({
        'name': 'Credit Risk Exposure Report',
        'period': 'September 2026',
        'status': 'Anomaly Detected',
        'createdAt': datetime.utcnow(),
        'updatedAt': datetime.utcnow()
    })
    print(f"✅ Seeded report: {report_id}")

    # --- 2. Seed Metrics ---
    # We load from the CSV we generated in Phase 2
    report_csv_path = "regreport-ai/data/synthetic/regulatory_report.csv"
    df = pd.read_csv(report_csv_path)
    
    metrics_coll = db.collection('report_metrics')
    for _, row in df.iterrows():
        metric_id = row['metric'].lower().replace(" ", "_")
        metrics_coll.document(metric_id).set({
            'reportId': report_id,
            'metric_name': row['metric'],
            'previous_value': row['aug_2026'],
            'current_value': row['sep_2026'],
            'delta_pct': ((row['sep_2026'] - row['aug_2026']) / row['aug_2026']) * 100 if row['aug_2026'] != 0 else 0,
            'is_anomaly': False # Will be calculated by the Anomaly Engine in Phase 7
        })
    print("✅ Seeded report metrics")

    # --- 3. Seed Knowledge Base (Policy) ---
    policy_path = "regreport-ai/data/synthetic/risk_classification_policy.md"
    with open(policy_path, "r") as f:
        content = f.read()
    
    db.collection('knowledge_base').document('policy_risk_001').set({
        'title': 'Risk Classification Policy',
        'content': content,
        'category': 'Credit Risk',
        'version': '2026.1'
    })
    print("✅ Seeded knowledge base")

    # --- 4. Seed Data Lineage ---
    lineage_path = "regreport-ai/data/synthetic/lineage.json"
    with open(lineage_path, "r") as f:
        lineage_data = json.load(f)
    
    for node in lineage_data:
        db.collection('data_lineage').document(node['id']).set(node)
    print("✅ Seeded data lineage")

    print("\n✨ Firestore seeding completed successfully!")

if __name__ == "__main__":
    seed_firestore()
