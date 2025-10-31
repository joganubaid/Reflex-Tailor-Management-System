
CREATE TABLE purchase_orders (
	po_id SERIAL NOT NULL, 
	po_number VARCHAR(50) NOT NULL, 
	supplier_id INTEGER, 
	po_date DATE DEFAULT CURRENT_DATE, 
	expected_delivery_date DATE, 
	actual_delivery_date DATE, 
	status VARCHAR(50) DEFAULT 'draft'::character varying, 
	total_amount NUMERIC(10, 2), 
	notes TEXT, 
	created_by VARCHAR(100), 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT purchase_orders_pkey PRIMARY KEY (po_id), 
	CONSTRAINT purchase_orders_po_number_key UNIQUE NULLS DISTINCT (po_number)
)



CREATE TABLE materials (
	material_id SERIAL NOT NULL, 
	material_name VARCHAR(255) NOT NULL, 
	material_type VARCHAR(100), 
	quantity_in_stock NUMERIC(10, 2), 
	unit VARCHAR(50), 
	unit_price NUMERIC(10, 2), 
	reorder_level NUMERIC(10, 2), 
	supplier_name VARCHAR(255), 
	supplier_contact VARCHAR(20), 
	last_purchase_date DATE, 
	batch_number VARCHAR(100), 
	roll_number VARCHAR(100), 
	batch_expiry_date DATE, 
	CONSTRAINT materials_pkey PRIMARY KEY (material_id)
)



CREATE TABLE customers (
	customer_id SERIAL NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	phone_number VARCHAR(20), 
	email VARCHAR(255), 
	address TEXT, 
	registration_date DATE DEFAULT CURRENT_DATE, 
	notes TEXT, 
	total_orders INTEGER DEFAULT 0, 
	opt_in_whatsapp BOOLEAN DEFAULT true, 
	prefer_whatsapp BOOLEAN DEFAULT false, 
	date_of_birth DATE, 
	customer_tier VARCHAR(20) DEFAULT 'new'::character varying, 
	total_points INTEGER DEFAULT 0, 
	referred_by INTEGER, 
	whatsapp_opt_in BOOLEAN DEFAULT true, 
	preferred_notification VARCHAR(20) DEFAULT 'sms'::character varying, 
	CONSTRAINT customers_pkey PRIMARY KEY (customer_id), 
	CONSTRAINT customers_referred_by_fkey FOREIGN KEY(referred_by) REFERENCES customers (customer_id)
)



CREATE TABLE photos (
	photo_id SERIAL NOT NULL, 
	photo_type VARCHAR(50) NOT NULL, 
	reference_id INTEGER NOT NULL, 
	file_name VARCHAR(255) NOT NULL, 
	file_path TEXT NOT NULL, 
	storage_type VARCHAR(20) DEFAULT 'local'::character varying, 
	file_size INTEGER, 
	mime_type VARCHAR(100), 
	upload_date TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	uploaded_by VARCHAR(100), 
	caption TEXT, 
	is_approved BOOLEAN DEFAULT false, 
	approval_date TIMESTAMP WITHOUT TIME ZONE, 
	approved_by VARCHAR(100), 
	CONSTRAINT photos_pkey PRIMARY KEY (photo_id)
)


CREATE INDEX idx_photos_type_ref ON photos (photo_type, reference_id)
CREATE INDEX idx_photos_upload_date ON photos (upload_date DESC)

CREATE TABLE order_templates (
	template_id SERIAL NOT NULL, 
	template_name VARCHAR(255) NOT NULL, 
	cloth_type VARCHAR(100) NOT NULL, 
	measurements JSONB, 
	special_instructions TEXT, 
	default_price NUMERIC(10, 2), 
	created_date DATE DEFAULT CURRENT_DATE, 
	created_by VARCHAR(100), 
	is_active BOOLEAN DEFAULT true, 
	CONSTRAINT order_templates_pkey PRIMARY KEY (template_id)
)



CREATE TABLE bank_accounts (
	account_id SERIAL NOT NULL, 
	bank_name VARCHAR(255) NOT NULL, 
	account_number VARCHAR(50) NOT NULL, 
	account_type VARCHAR(50) NOT NULL, 
	balance NUMERIC(12, 2) DEFAULT 0.0, 
	is_active BOOLEAN DEFAULT true, 
	created_date DATE DEFAULT CURRENT_DATE, 
	last_updated TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT bank_accounts_pkey PRIMARY KEY (account_id), 
	CONSTRAINT bank_accounts_account_number_key UNIQUE NULLS DISTINCT (account_number)
)



CREATE TABLE workers (
	worker_id SERIAL NOT NULL, 
	worker_name VARCHAR(255) NOT NULL, 
	phone_number VARCHAR(20), 
	role VARCHAR(100), 
	salary NUMERIC(10, 2), 
	joining_date DATE DEFAULT CURRENT_DATE, 
	active_status BOOLEAN DEFAULT true, 
	incentive_rate NUMERIC(5, 2) DEFAULT 0.0, 
	total_incentives NUMERIC(10, 2) DEFAULT 0.0, 
	CONSTRAINT workers_pkey PRIMARY KEY (worker_id)
)



CREATE TABLE suppliers (
	supplier_id SERIAL NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	contact VARCHAR(20) NOT NULL, 
	email VARCHAR(255), 
	address TEXT, 
	rating NUMERIC(3, 2) DEFAULT 0, 
	notes TEXT, 
	registration_date DATE DEFAULT CURRENT_DATE, 
	CONSTRAINT suppliers_pkey PRIMARY KEY (supplier_id)
)



CREATE TABLE discount_coupons (
	coupon_id SERIAL NOT NULL, 
	coupon_code VARCHAR(50) NOT NULL, 
	discount_type VARCHAR(20) NOT NULL, 
	discount_value NUMERIC(10, 2) NOT NULL, 
	min_order_value NUMERIC(10, 2) DEFAULT 0, 
	valid_from DATE NOT NULL, 
	valid_until DATE NOT NULL, 
	usage_limit INTEGER, 
	used_count INTEGER DEFAULT 0, 
	is_active BOOLEAN DEFAULT true, 
	created_date DATE DEFAULT CURRENT_DATE, 
	description TEXT, 
	CONSTRAINT discount_coupons_pkey PRIMARY KEY (coupon_id), 
	CONSTRAINT discount_coupons_coupon_code_key UNIQUE NULLS DISTINCT (coupon_code)
)



CREATE TABLE expense_categories (
	category_id SERIAL NOT NULL, 
	category_name VARCHAR(100) NOT NULL, 
	description TEXT, 
	is_active BOOLEAN DEFAULT true, 
	created_date DATE DEFAULT CURRENT_DATE, 
	CONSTRAINT expense_categories_pkey PRIMARY KEY (category_id), 
	CONSTRAINT expense_categories_category_name_key UNIQUE NULLS DISTINCT (category_name)
)



CREATE TABLE alert_settings (
	setting_id SERIAL NOT NULL, 
	alert_type VARCHAR(100) NOT NULL, 
	enabled BOOLEAN DEFAULT true, 
	threshold_value NUMERIC(10, 2), 
	notification_method VARCHAR(50) DEFAULT 'sms'::character varying, 
	recipients TEXT, 
	description TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT alert_settings_pkey PRIMARY KEY (setting_id), 
	CONSTRAINT alert_settings_alert_type_key UNIQUE NULLS DISTINCT (alert_type)
)



CREATE TABLE alert_history (
	alert_id SERIAL NOT NULL, 
	alert_type VARCHAR(100) NOT NULL, 
	message TEXT NOT NULL, 
	severity VARCHAR(20) DEFAULT 'info'::character varying, 
	triggered_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	sent_to TEXT, 
	status VARCHAR(20) DEFAULT 'sent'::character varying, 
	reference_id INTEGER, 
	reference_type VARCHAR(50), 
	resolved_at TIMESTAMP WITHOUT TIME ZONE, 
	notes TEXT, 
	CONSTRAINT alert_history_pkey PRIMARY KEY (alert_id)
)


CREATE INDEX idx_alert_history_type ON alert_history (alert_type)
CREATE INDEX idx_alert_history_triggered ON alert_history (triggered_at)
CREATE INDEX idx_alert_history_date ON alert_history (triggered_at DESC)
CREATE INDEX idx_alert_history_status ON alert_history (status)

CREATE TABLE automation_workflows (
	workflow_id SERIAL NOT NULL, 
	workflow_name VARCHAR(255) NOT NULL, 
	trigger_event VARCHAR(100) NOT NULL, 
	condition_rules JSONB, 
	actions JSONB NOT NULL, 
	is_active BOOLEAN DEFAULT true, 
	created_date DATE DEFAULT CURRENT_DATE, 
	last_triggered TIMESTAMP WITHOUT TIME ZONE, 
	execution_count INTEGER DEFAULT 0, 
	CONSTRAINT automation_workflows_pkey PRIMARY KEY (workflow_id)
)


CREATE INDEX idx_workflows_active ON automation_workflows (is_active)
CREATE INDEX idx_workflows_trigger ON automation_workflows (trigger_event)

CREATE TABLE purchase_order_items (
	po_item_id SERIAL NOT NULL, 
	po_id INTEGER, 
	material_id INTEGER, 
	quantity NUMERIC(10, 2) NOT NULL, 
	unit_price NUMERIC(10, 2) NOT NULL, 
	total_price NUMERIC(10, 2) NOT NULL, 
	received_quantity NUMERIC(10, 2) DEFAULT 0, 
	CONSTRAINT purchase_order_items_pkey PRIMARY KEY (po_item_id), 
	CONSTRAINT purchase_order_items_material_id_fkey FOREIGN KEY(material_id) REFERENCES materials (material_id), 
	CONSTRAINT purchase_order_items_po_id_fkey FOREIGN KEY(po_id) REFERENCES purchase_orders (po_id) ON DELETE CASCADE
)



CREATE TABLE stock_audit (
	audit_id SERIAL NOT NULL, 
	material_id INTEGER, 
	audit_date DATE DEFAULT CURRENT_DATE, 
	system_quantity NUMERIC(10, 2) NOT NULL, 
	physical_quantity NUMERIC(10, 2) NOT NULL, 
	variance NUMERIC(10, 2) NOT NULL, 
	variance_percentage NUMERIC(5, 2), 
	notes TEXT, 
	audited_by VARCHAR(100), 
	adjustment_made BOOLEAN DEFAULT false, 
	CONSTRAINT stock_audit_pkey PRIMARY KEY (audit_id), 
	CONSTRAINT stock_audit_material_id_fkey FOREIGN KEY(material_id) REFERENCES materials (material_id)
)



CREATE TABLE measurements (
	measurement_id SERIAL NOT NULL, 
	customer_id INTEGER, 
	chest NUMERIC(5, 2), 
	waist NUMERIC(5, 2), 
	shoulder_width NUMERIC(5, 2), 
	sleeve_length NUMERIC(5, 2), 
	measurement_date DATE DEFAULT CURRENT_DATE, 
	cloth_type VARCHAR(100), 
	hip NUMERIC(5, 2), 
	shirt_length NUMERIC(5, 2), 
	pant_length NUMERIC(5, 2), 
	inseam NUMERIC(5, 2), 
	neck NUMERIC(5, 2), 
	CONSTRAINT measurements_pkey PRIMARY KEY (measurement_id), 
	CONSTRAINT measurements_customer_id_fkey FOREIGN KEY(customer_id) REFERENCES customers (customer_id)
)



CREATE TABLE orders (
	order_id SERIAL NOT NULL, 
	customer_id INTEGER, 
	order_date DATE DEFAULT CURRENT_DATE, 
	delivery_date DATE, 
	status VARCHAR(50), 
	total_amount NUMERIC(10, 2), 
	advance_payment NUMERIC(10, 2), 
	balance_payment NUMERIC(10, 2), 
	cloth_type VARCHAR(100), 
	quantity INTEGER DEFAULT 1, 
	special_instructions TEXT, 
	assigned_worker INTEGER, 
	labor_cost NUMERIC(10, 2) DEFAULT 0.0, 
	material_cost NUMERIC(10, 2) DEFAULT 0.0, 
	profit NUMERIC(10, 2) DEFAULT 0.0, 
	coupon_code VARCHAR(50), 
	discount_amount NUMERIC(10, 2) DEFAULT 0, 
	points_earned INTEGER DEFAULT 0, 
	priority VARCHAR(20) DEFAULT 'normal'::character varying, 
	order_template_id INTEGER, 
	is_bulk_order BOOLEAN DEFAULT false, 
	bulk_order_details TEXT, 
	CONSTRAINT orders_pkey PRIMARY KEY (order_id), 
	CONSTRAINT orders_customer_id_fkey FOREIGN KEY(customer_id) REFERENCES customers (customer_id)
)


CREATE INDEX idx_orders_priority ON orders (priority)
CREATE INDEX idx_orders_template ON orders (order_template_id)

CREATE TABLE material_suppliers (
	id SERIAL NOT NULL, 
	material_id INTEGER, 
	supplier_id INTEGER, 
	price NUMERIC(10, 2), 
	is_preferred BOOLEAN DEFAULT false, 
	CONSTRAINT material_suppliers_pkey PRIMARY KEY (id), 
	CONSTRAINT material_suppliers_material_id_fkey FOREIGN KEY(material_id) REFERENCES materials (material_id) ON DELETE CASCADE, 
	CONSTRAINT material_suppliers_supplier_id_fkey FOREIGN KEY(supplier_id) REFERENCES suppliers (supplier_id) ON DELETE CASCADE, 
	CONSTRAINT material_suppliers_material_id_supplier_id_key UNIQUE NULLS DISTINCT (material_id, supplier_id)
)



CREATE TABLE customer_referrals (
	referral_id SERIAL NOT NULL, 
	referrer_customer_id INTEGER, 
	referred_customer_id INTEGER, 
	referral_date DATE DEFAULT CURRENT_DATE, 
	referral_status VARCHAR(20) DEFAULT 'pending'::character varying, 
	reward_points INTEGER DEFAULT 0, 
	order_completed BOOLEAN DEFAULT false, 
	completed_date DATE, 
	CONSTRAINT customer_referrals_pkey PRIMARY KEY (referral_id), 
	CONSTRAINT customer_referrals_referred_customer_id_fkey FOREIGN KEY(referred_customer_id) REFERENCES customers (customer_id), 
	CONSTRAINT customer_referrals_referrer_customer_id_fkey FOREIGN KEY(referrer_customer_id) REFERENCES customers (customer_id)
)



CREATE TABLE worker_attendance (
	attendance_id SERIAL NOT NULL, 
	worker_id INTEGER NOT NULL, 
	date DATE DEFAULT CURRENT_DATE NOT NULL, 
	check_in_time TIME WITHOUT TIME ZONE, 
	check_out_time TIME WITHOUT TIME ZONE, 
	total_hours NUMERIC(5, 2), 
	status VARCHAR(20) DEFAULT 'present'::character varying, 
	notes TEXT, 
	CONSTRAINT worker_attendance_pkey PRIMARY KEY (attendance_id), 
	CONSTRAINT worker_attendance_worker_id_fkey FOREIGN KEY(worker_id) REFERENCES workers (worker_id) ON DELETE CASCADE, 
	CONSTRAINT unique_worker_date UNIQUE NULLS DISTINCT (worker_id, date)
)


CREATE INDEX idx_attendance_worker ON worker_attendance (worker_id)
CREATE INDEX idx_attendance_date ON worker_attendance (date)

CREATE TABLE worker_skills (
	skill_id SERIAL NOT NULL, 
	worker_id INTEGER NOT NULL, 
	skill_name VARCHAR(100) NOT NULL, 
	proficiency_level VARCHAR(20) DEFAULT 'beginner'::character varying, 
	years_experience INTEGER DEFAULT 0, 
	notes TEXT, 
	CONSTRAINT worker_skills_pkey PRIMARY KEY (skill_id), 
	CONSTRAINT worker_skills_worker_id_fkey FOREIGN KEY(worker_id) REFERENCES workers (worker_id) ON DELETE CASCADE, 
	CONSTRAINT unique_worker_skill UNIQUE NULLS DISTINCT (worker_id, skill_name)
)


CREATE INDEX idx_skills_worker ON worker_skills (worker_id)

CREATE TABLE worker_leaves (
	leave_id SERIAL NOT NULL, 
	worker_id INTEGER NOT NULL, 
	leave_type VARCHAR(50) NOT NULL, 
	start_date DATE NOT NULL, 
	end_date DATE NOT NULL, 
	total_days INTEGER NOT NULL, 
	reason TEXT, 
	status VARCHAR(20) DEFAULT 'pending'::character varying, 
	applied_date DATE DEFAULT CURRENT_DATE, 
	approved_by VARCHAR(100), 
	approval_date DATE, 
	CONSTRAINT worker_leaves_pkey PRIMARY KEY (leave_id), 
	CONSTRAINT worker_leaves_worker_id_fkey FOREIGN KEY(worker_id) REFERENCES workers (worker_id) ON DELETE CASCADE
)


CREATE INDEX idx_leaves_status ON worker_leaves (status)
CREATE INDEX idx_leaves_worker ON worker_leaves (worker_id)

CREATE TABLE expenses (
	expense_id SERIAL NOT NULL, 
	category_id INTEGER NOT NULL, 
	amount NUMERIC(10, 2) NOT NULL, 
	expense_date DATE DEFAULT CURRENT_DATE, 
	payment_method VARCHAR(50), 
	description TEXT, 
	receipt_path TEXT, 
	vendor_name VARCHAR(255), 
	is_recurring BOOLEAN DEFAULT false, 
	recurrence_frequency VARCHAR(20), 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT expenses_pkey PRIMARY KEY (expense_id), 
	CONSTRAINT expenses_category_id_fkey FOREIGN KEY(category_id) REFERENCES expense_categories (category_id)
)


CREATE INDEX idx_expenses_date ON expenses (expense_date)
CREATE INDEX idx_expenses_recurring ON expenses (is_recurring)
CREATE INDEX idx_expenses_category ON expenses (category_id)

CREATE TABLE workflow_execution_log (
	log_id SERIAL NOT NULL, 
	workflow_id INTEGER NOT NULL, 
	execution_time TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	status VARCHAR(20) DEFAULT 'success'::character varying, 
	trigger_data JSONB, 
	result_data JSONB, 
	error_message TEXT, 
	CONSTRAINT workflow_execution_log_pkey PRIMARY KEY (log_id), 
	CONSTRAINT workflow_execution_log_workflow_id_fkey FOREIGN KEY(workflow_id) REFERENCES automation_workflows (workflow_id) ON DELETE CASCADE
)


CREATE INDEX idx_workflow_log_workflow ON workflow_execution_log (workflow_id)

CREATE TABLE transactions (
	transaction_id SERIAL NOT NULL, 
	transaction_date DATE DEFAULT CURRENT_DATE, 
	transaction_type VARCHAR(50), 
	amount NUMERIC(10, 2), 
	payment_method VARCHAR(50), 
	description TEXT, 
	order_id INTEGER, 
	material_id INTEGER, 
	invoice_number VARCHAR(100), 
	bank_account_id INTEGER, 
	CONSTRAINT transactions_pkey PRIMARY KEY (transaction_id), 
	CONSTRAINT transactions_bank_account_id_fkey FOREIGN KEY(bank_account_id) REFERENCES bank_accounts (account_id), 
	CONSTRAINT transactions_material_id_fkey FOREIGN KEY(material_id) REFERENCES materials (material_id), 
	CONSTRAINT transactions_order_id_fkey FOREIGN KEY(order_id) REFERENCES orders (order_id)
)


CREATE INDEX idx_transactions_bank ON transactions (bank_account_id)

CREATE TABLE order_materials (
	id SERIAL NOT NULL, 
	order_id INTEGER, 
	material_id INTEGER, 
	quantity_used NUMERIC(10, 2), 
	wastage NUMERIC(10, 2), 
	cost NUMERIC(10, 2), 
	CONSTRAINT order_materials_pkey PRIMARY KEY (id), 
	CONSTRAINT order_materials_material_id_fkey FOREIGN KEY(material_id) REFERENCES materials (material_id), 
	CONSTRAINT order_materials_order_id_fkey FOREIGN KEY(order_id) REFERENCES orders (order_id)
)



CREATE TABLE invoices (
	invoice_id SERIAL NOT NULL, 
	order_id INTEGER, 
	invoice_number VARCHAR(100), 
	invoice_date DATE DEFAULT CURRENT_DATE, 
	subtotal NUMERIC(10, 2), 
	gst_amount NUMERIC(10, 2), 
	total_amount NUMERIC(10, 2), 
	payment_status VARCHAR(50), 
	pdf_path TEXT, 
	CONSTRAINT invoices_pkey PRIMARY KEY (invoice_id), 
	CONSTRAINT invoices_order_id_fkey FOREIGN KEY(order_id) REFERENCES orders (order_id), 
	CONSTRAINT invoices_invoice_number_key UNIQUE NULLS DISTINCT (invoice_number)
)



CREATE TABLE qc_checklist (
	checklist_id SERIAL NOT NULL, 
	order_id INTEGER NOT NULL, 
	checkpoint_name VARCHAR(255) NOT NULL, 
	status VARCHAR(20) DEFAULT 'pending'::character varying, 
	checked_by VARCHAR(100), 
	checked_date TIMESTAMP WITHOUT TIME ZONE, 
	notes TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT qc_checklist_pkey PRIMARY KEY (checklist_id), 
	CONSTRAINT qc_checklist_order_id_fkey FOREIGN KEY(order_id) REFERENCES orders (order_id) ON DELETE CASCADE
)


CREATE INDEX idx_qc_order ON qc_checklist (order_id)
CREATE INDEX idx_qc_status ON qc_checklist (status)

CREATE TABLE alteration_orders (
	alteration_id SERIAL NOT NULL, 
	customer_id INTEGER NOT NULL, 
	original_order_id INTEGER, 
	alteration_type VARCHAR(100) NOT NULL, 
	description TEXT NOT NULL, 
	price NUMERIC(10, 2) NOT NULL, 
	status VARCHAR(50) DEFAULT 'pending'::character varying, 
	created_date DATE DEFAULT CURRENT_DATE, 
	completion_date DATE, 
	assigned_worker INTEGER, 
	notes TEXT, 
	CONSTRAINT alteration_orders_pkey PRIMARY KEY (alteration_id), 
	CONSTRAINT alteration_orders_assigned_worker_fkey FOREIGN KEY(assigned_worker) REFERENCES workers (worker_id), 
	CONSTRAINT alteration_orders_customer_id_fkey FOREIGN KEY(customer_id) REFERENCES customers (customer_id), 
	CONSTRAINT alteration_orders_original_order_id_fkey FOREIGN KEY(original_order_id) REFERENCES orders (order_id)
)


CREATE INDEX idx_alteration_status ON alteration_orders (status)
CREATE INDEX idx_alteration_customer ON alteration_orders (customer_id)

CREATE TABLE payment_installments (
	installment_id SERIAL NOT NULL, 
	order_id INTEGER NOT NULL, 
	installment_number INTEGER NOT NULL, 
	amount NUMERIC(10, 2) NOT NULL, 
	due_date DATE NOT NULL, 
	paid_date DATE, 
	status VARCHAR(20) DEFAULT 'pending'::character varying, 
	payment_method VARCHAR(50), 
	notes TEXT, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	bank_account_id INTEGER, 
	CONSTRAINT payment_installments_pkey PRIMARY KEY (installment_id), 
	CONSTRAINT payment_installments_bank_account_id_fkey FOREIGN KEY(bank_account_id) REFERENCES bank_accounts (account_id), 
	CONSTRAINT payment_installments_order_id_fkey FOREIGN KEY(order_id) REFERENCES orders (order_id) ON DELETE CASCADE, 
	CONSTRAINT payment_installments_order_id_installment_number_key UNIQUE NULLS DISTINCT (order_id, installment_number)
)


CREATE INDEX idx_installments_bank ON payment_installments (bank_account_id)

CREATE TABLE loyalty_points (
	loyalty_id SERIAL NOT NULL, 
	customer_id INTEGER, 
	points_change INTEGER NOT NULL, 
	new_balance INTEGER NOT NULL, 
	transaction_type VARCHAR(50) NOT NULL, 
	transaction_date TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
	order_id INTEGER, 
	description TEXT, 
	CONSTRAINT loyalty_points_pkey PRIMARY KEY (loyalty_id), 
	CONSTRAINT loyalty_points_customer_id_fkey FOREIGN KEY(customer_id) REFERENCES customers (customer_id), 
	CONSTRAINT loyalty_points_order_id_fkey FOREIGN KEY(order_id) REFERENCES orders (order_id)
)



CREATE TABLE worker_tasks (
	task_id SERIAL NOT NULL, 
	order_id INTEGER NOT NULL, 
	worker_id INTEGER NOT NULL, 
	task_type VARCHAR(50) NOT NULL, 
	assigned_date DATE DEFAULT CURRENT_DATE, 
	completed_date DATE, 
	status VARCHAR(20) DEFAULT 'assigned'::character varying, 
	notes TEXT, 
	estimated_hours NUMERIC(5, 2), 
	actual_hours NUMERIC(5, 2), 
	CONSTRAINT worker_tasks_pkey PRIMARY KEY (task_id), 
	CONSTRAINT worker_tasks_order_id_fkey FOREIGN KEY(order_id) REFERENCES orders (order_id) ON DELETE CASCADE, 
	CONSTRAINT worker_tasks_worker_id_fkey FOREIGN KEY(worker_id) REFERENCES workers (worker_id)
)


CREATE INDEX idx_tasks_worker ON worker_tasks (worker_id)
CREATE INDEX idx_tasks_order ON worker_tasks (order_id)
CREATE INDEX idx_tasks_status ON worker_tasks (status)

CREATE TABLE payment_reminders (
	reminder_id SERIAL NOT NULL, 
	installment_id INTEGER NOT NULL, 
	reminder_date DATE NOT NULL, 
	sent_date TIMESTAMP WITHOUT TIME ZONE, 
	status VARCHAR(20) DEFAULT 'scheduled'::character varying, 
	created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP, 
	CONSTRAINT payment_reminders_pkey PRIMARY KEY (reminder_id), 
	CONSTRAINT payment_reminders_installment_id_fkey FOREIGN KEY(installment_id) REFERENCES payment_installments (installment_id) ON DELETE CASCADE
)

