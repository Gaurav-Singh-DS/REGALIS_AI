
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
    