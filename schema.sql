
CREATE TABLE customers (
	customer_id SERIAL NOT NULL, 
	name VARCHAR(255) NOT NULL, 
	phone_number VARCHAR(20), 
	email VARCHAR(255), 
	address TEXT, 
	registration_date DATE DEFAULT CURRENT_DATE, 
	CONSTRAINT customers_pkey PRIMARY KEY (customer_id)
)



CREATE TABLE materials (
	material_id SERIAL NOT NULL, 
	material_name VARCHAR(255) NOT NULL, 
	material_type VARCHAR(100), 
	quantity_in_stock NUMERIC(10, 2), 
	unit VARCHAR(50), 
	unit_price NUMERIC(10, 2), 
	reorder_level NUMERIC(10, 2), 
	CONSTRAINT materials_pkey PRIMARY KEY (material_id)
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
	CONSTRAINT orders_pkey PRIMARY KEY (order_id), 
	CONSTRAINT orders_customer_id_fkey FOREIGN KEY(customer_id) REFERENCES customers (customer_id)
)



CREATE TABLE measurements (
	measurement_id SERIAL NOT NULL, 
	customer_id INTEGER, 
	chest NUMERIC(5, 2), 
	waist NUMERIC(5, 2), 
	shoulder_width NUMERIC(5, 2), 
	sleeve_length NUMERIC(5, 2), 
	measurement_date DATE DEFAULT CURRENT_DATE, 
	CONSTRAINT measurements_pkey PRIMARY KEY (measurement_id), 
	CONSTRAINT measurements_customer_id_fkey FOREIGN KEY(customer_id) REFERENCES customers (customer_id)
)

