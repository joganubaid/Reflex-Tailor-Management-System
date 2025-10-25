
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
	CONSTRAINT customers_pkey PRIMARY KEY (customer_id), 
	CONSTRAINT customers_referred_by_fkey FOREIGN KEY(referred_by) REFERENCES customers (customer_id)
)



CREATE TABLE workers (
	worker_id SERIAL NOT NULL, 
	worker_name VARCHAR(255) NOT NULL, 
	phone_number VARCHAR(20), 
	role VARCHAR(100), 
	salary NUMERIC(10, 2), 
	joining_date DATE DEFAULT CURRENT_DATE, 
	active_status BOOLEAN DEFAULT true, 
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
	CONSTRAINT orders_pkey PRIMARY KEY (order_id), 
	CONSTRAINT orders_customer_id_fkey FOREIGN KEY(customer_id) REFERENCES customers (customer_id)
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
	CONSTRAINT transactions_pkey PRIMARY KEY (transaction_id), 
	CONSTRAINT transactions_material_id_fkey FOREIGN KEY(material_id) REFERENCES materials (material_id), 
	CONSTRAINT transactions_order_id_fkey FOREIGN KEY(order_id) REFERENCES orders (order_id)
)



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
	CONSTRAINT payment_installments_pkey PRIMARY KEY (installment_id), 
	CONSTRAINT payment_installments_order_id_fkey FOREIGN KEY(order_id) REFERENCES orders (order_id) ON DELETE CASCADE, 
	CONSTRAINT payment_installments_order_id_installment_number_key UNIQUE NULLS DISTINCT (order_id, installment_number)
)



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

