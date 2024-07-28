# Creating cities table if not exists
city_create_query = f'''CREATE TABLE IF NOT EXISTS cities_status (
                    id INTEGER AUTO_INCREMENT PRIMARY KEY,
                    city_name VARCHAR(255) UNIQUE,
                    city_json JSON,
                    city_status VARCHAR(255) DEFAULT 'Pending',
                    city_filename VARCHAR(255));'''

store_create_query = f'''CREATE TABLE IF NOT EXISTS store_data(
                    id INTEGER AUTO_INCREMENT PRIMARY KEY,
                    store_name VARCHAR(255) DEFAULT 'VIJAY SALES',
                    store_address VARCHAR(255) UNIQUE,
                    store_contact_no BIGINT,
                    area_name VARCHAR(255),
                    city_name VARCHAR(255));'''
