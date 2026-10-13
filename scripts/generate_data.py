import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_novabank_data():
    print("🚀 Generating NovaBank Synthetic Data...")
    output_dir = "regreport-ai/data/synthetic"
    os.makedirs(output_dir, exist_ok=True)

    # --- 1. Customers Dataset ---
    # 1.2M customers
    num_customers = 1_200_000
    customer_ids = [f"CUST_{i:07d}" for i in range(num_customers)]
    segments = ['Retail', 'Corporate', 'SME', 'HNI']
    
    customers_df = pd.DataFrame({
        'customer_id': customer_ids,
        'segment': np.random.choice(segments, num_customers),
        'country': np.random.choice(['USA', 'UK', 'Canada', 'Singapore'], num_customers),
        'onboarding_date': [datetime(2020, 1, 1) + timedelta(days=np.random.randint(0, 2000)) for _ in range(num_customers)]
    })
    customers_df.to_csv(f"{output_dir}/customers.csv", index=False)
    print("✅ Created customers.csv")

    # --- 2. Exposure Datasets (Previous vs Current) ---
    # Scenario: Exposure 100M -> 117.8M
    # High Risk: 80k -> 125k
    
    def create_exposure_df(month, total_exposure, high_risk_count):
        # Sample 10k rows for the prototype to keep it manageable but realistic
        num_rows = 10000 
        ids = [f"CUST_{np.random.randint(0, num_customers):07d}" for _ in range(num_rows)]
        
        # Distribute risk: 0=Low, 1=Medium, 2=High
        # We adjust the probability of 'High' based on high_risk_count
        risk_prob = [0.6, 0.3, (high_risk_count / num_customers)] 
        # For the prototype, we'll force a specific number of 'High' in the sample
        risks = np.random.choice(['Low', 'Medium', 'High'], num_rows, p=[0.6, 0.3, 0.1])
        
        # Scale exposure values to hit the total_exposure target
        avg_exposure = total_exposure / num_customers
        exposure_vals = np.random.lognormal(mean=np.log(avg_exposure), sigma=1.0, size=num_rows)
        
        df = pd.DataFrame({
            'customer_id': ids,
            'risk_category': risks,
            'exposure_amount': exposure_vals,
            'reporting_date': month
        })
        return df

    prev_exp = create_exposure_df('2026-08-31', 100_000_000, 80_000)
    curr_exp = create_exposure_df('2026-09-30', 117_800_000, 125_000)
    
    prev_exp.to_csv(f"{output_dir}/exposure_previous.csv", index=False)
    curr_exp.to_csv(f"{output_dir}/exposure_current.csv", index=False)
    print("✅ Created exposure_previous.csv and exposure_current.csv")

    # --- 3. Regulatory Report (Aggregated) ---
    # This is what the user sees on the dashboard
    report_data = {
        'metric': ['Total Exposure', 'High Risk Count', 'Total Customers', 'Avg Exposure per Customer'],
        'aug_2026': [100_000_000, 80_000, 1_200_000, 83.33],
        'sep_2026': [117_800_000, 125_000, 1_210_000, 97.35]
    }
    report_df = pd.DataFrame(report_data)
    report_df.to_csv(f"{output_dir}/regulatory_report.csv", index=False)
    print("✅ Created regulatory_report.csv")

    # --- 4. Legacy SAS Code ---
    sas_code = """
    /* NovaBank Risk Classification Logic - v2.1 */
    DATA customer_risk_final;
        SET customer_raw_data;
        
        /* RISK CLASSIFICATION RULE */
        IF credit_score < 600 AND loan_to_value > 0.8 THEN risk_category = 'High';
        ELSE IF credit_score < 700 THEN risk_category = 'Medium';
        ELSE risk_category = 'Low';
        
        /* NEW UPDATE SEPT 2026: Adjusted threshold for Credit Card portfolio */
        IF portfolio_type = 'CreditCard' AND credit_score < 650 THEN risk_category = 'High';
        
        LABEL risk_category = 'Regulatory Risk Category';
    RUN;
    """
    with open(f"{output_dir}/customer_risk.sas", "w") as f:
        f.write(sas_code)
    print("✅ Created customer_risk.sas")

    # --- 5. Regulatory Policy (RAG) ---
    policy_md = """
# NovaBank Synthetic Regulatory Policy - Risk Classification
**Version:** 2026.1
**Effective Date:** January 1, 2026

## Section 4.2: Credit Risk Exposure
All customers with a credit score below 600 must be classified as 'High Risk' for the purpose of Basel III regulatory reporting.

## Section 4.2.1: Portfolio Specifics
For Credit Card portfolios, the risk threshold is more sensitive. Any customer with a score below 650 is automatically flagged as 'High Risk' to maintain conservative capital buffers.

## Section 5.1: Reporting Frequency
Reports must be submitted by the 10th of the following month.
    """
    with open(f"{output_dir}/risk_classification_policy.md", "w") as f:
        f.write(policy_md)
    print("✅ Created risk_classification_policy.md")

    # --- 6. Data Lineage (JSON) ---
    import json
    lineage = [
        {"id": "L1", "name": "Raw Transactions", "type": "Source", "downstream": ["L2"]},
        {"id": "L2", "name": "Customer Risk Job", "type": "Transformation", "upstream": ["L1"], "downstream": ["L3"], "code_ref": "customer_risk.sas"},
        {"id": "L3", "name": "Exposure Calculation", "type": "Transformation", "upstream": ["L2"], "downstream": ["L4"], "code_ref": "exposure_calculation.sql"},
        {"id": "L4", "name": "Regulatory Report", "type": "Final Report", "upstream": ["L3"]}
    ]
    with open(f"{output_dir}/lineage.json", "w") as f:
        json.dump(lineage, f, indent=2)
    print("✅ Created lineage.json")

if __name__ == "__main__":
    generate_novabank_data()
