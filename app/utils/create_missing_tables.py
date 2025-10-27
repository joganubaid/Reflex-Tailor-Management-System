import os
import asyncio
import logging
from sqlalchemy import text
import reflex as rx


async def create_missing_tables():
    """Create missing database tables for expenses and alerts"""
    create_tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS expense_categories (
            category_id SERIAL PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id SERIAL PRIMARY KEY,
            category_id INTEGER REFERENCES expense_categories(category_id),
            amount NUMERIC(10,2) NOT NULL,
            expense_date DATE NOT NULL,
            description TEXT,
            vendor_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS bank_accounts (
            account_id SERIAL PRIMARY KEY,
            bank_name VARCHAR(255) NOT NULL,
            account_number VARCHAR(50) NOT NULL,
            account_type VARCHAR(50),
            balance NUMERIC(15,2) DEFAULT 0,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS alert_settings (
            setting_id SERIAL PRIMARY KEY,
            alert_type VARCHAR(50) NOT NULL UNIQUE,
            enabled BOOLEAN DEFAULT TRUE,
            threshold_value NUMERIC(10,2),
            notification_method VARCHAR(20) DEFAULT 'sms',
            recipients TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS alert_history (
            alert_id SERIAL PRIMARY KEY,
            alert_type VARCHAR(50) NOT NULL,
            message TEXT NOT NULL,
            severity VARCHAR(20) DEFAULT 'info',
            triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) DEFAULT 'sent'
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS automation_workflows (
            workflow_id SERIAL PRIMARY KEY,
            workflow_name VARCHAR(255) NOT NULL,
            trigger_event VARCHAR(100) NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            execution_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ]
    seed_categories_sql = """
    INSERT INTO expense_categories (category_name, description) VALUES
    ('Rent', 'Monthly shop rent and utilities'),
    ('Utilities', 'Electricity, water, internet bills'),
    ('Salaries', 'Worker and staff salaries'),
    ('Raw Materials', 'Fabric, thread, buttons, zippers'),
    ('Marketing', 'Advertising and promotional expenses'),
    ('Maintenance', 'Equipment and shop maintenance'),
    ('Transport', 'Delivery and transportation costs'),
    ('Miscellaneous', 'Other business expenses')
    ON CONFLICT (category_name) DO NOTHING;
    """
    seed_alerts_sql = """
    INSERT INTO alert_settings (alert_type, enabled, threshold_value, notification_method, recipients) VALUES
    ('low_stock', TRUE, 10.0, 'sms', '+919876543210'),
    ('payment_due', TRUE, 3.0, 'both', '+919876543210,admin@tailorflow.com'),
    ('overdue_order', TRUE, NULL, 'sms', '+919876543210'),
    ('delivery_reminder', TRUE, 2.0, 'both', '+919876543210,admin@tailorflow.com'),
    ('qc_pending', TRUE, NULL, 'email', 'admin@tailorflow.com'),
    ('task_deadline', TRUE, 1.0, 'sms', '+919876543210')
    ON CONFLICT (alert_type) DO UPDATE SET
    enabled = EXCLUDED.enabled,
    threshold_value = EXCLUDED.threshold_value,
    notification_method = EXCLUDED.notification_method,
    recipients = EXCLUDED.recipients;
    """
    seed_expenses_sql = """
    INSERT INTO expenses (category_id, amount, expense_date, description, vendor_name) VALUES
    ((SELECT category_id FROM expense_categories WHERE category_name = 'Rent'), 25000.00, '2025-10-22', 'Monthly shop rent', 'ABC Properties'),
    ((SELECT category_id FROM expense_categories WHERE category_name = 'Salaries'), 45000.00, '2025-10-24', 'Worker salaries for October', 'Workers'),
    ((SELECT category_id FROM expense_categories WHERE category_name = 'Utilities'), 5500.00, '2025-10-27', 'Monthly electricity bill for shop', 'City Power Company'),
    ((SELECT category_id FROM expense_categories WHERE category_name = 'Marketing'), 3500.00, '2025-10-17', 'Facebook ads campaign', 'Meta Ads'),
    ((SELECT category_id FROM expense_categories WHERE category_name = 'Maintenance'), 2800.00, '2025-10-15', 'Sewing machine repair', 'Tech Services')
    ON CONFLICT DO NOTHING;
    """
    try:
        async with rx.asession() as session:
            for sql in create_tables_sql:
                await session.execute(text(sql))
                print(f"✅ Executed table creation")
            await session.execute(text(seed_categories_sql))
            print("✅ Inserted expense categories")
            await session.execute(text(seed_alerts_sql))
            print("✅ Inserted alert settings")
            await session.execute(text(seed_expenses_sql))
            print("✅ Inserted sample expenses")
            await session.commit()
            print("🎉 All tables and seed data created successfully!")
    except Exception as e:
        logging.exception(f"Error creating tables: {e}")
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(create_missing_tables())