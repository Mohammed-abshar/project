import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_dataset(num_rows=1200):
    np.random.seed(42)
    random.seed(42)

    hospitals = ['Apollo Hospitals', 'Fortis Healthcare', 'Max Healthcare', 'Manipal Hospitals', 'Medanta', 'Narayana Health', 'AIIMS', 'Christian Medical College', 'Tata Memorial']
    departments = ['Cardiology', 'Neurology', 'Oncology', 'Orthopedics', 'Pediatrics', 'Radiology', 'Emergency', 'IT Dept', 'Research', 'Pharmacy']
    services = ['Storage', 'Compute', 'Database', 'AI Services', 'Backup', 'Security', 'Networking', 'Analytics', 'IoT Hub']
    regions = ['us-east-1', 'us-west-2', 'ap-south-1', 'eu-central-1', 'ap-southeast-1', 'eu-west-1']
    vendors = ['AWS', 'Azure', 'Google Cloud']
    statuses = ['Paid', 'Pending', 'Overdue']

    data = []
    start_date = datetime(2023, 1, 1)

    for i in range(num_rows):
        billing_id = f"INV-{10000 + i}"
        hospital = random.choice(hospitals)
        department = random.choice(departments)
        service = random.choice(services)
        region = random.choice(regions)
        vendor = random.choice(vendors)
        
        # Date generation within the last year
        random_days = random.randint(0, 365)
        date = start_date + timedelta(days=random_days)
        
        usage_hours = round(random.uniform(10, 720), 2)
        storage_used = round(random.uniform(50, 5000), 2) if service == 'Storage' else round(random.uniform(0, 500), 2)
        
        cpu_usage = round(random.uniform(10, 99), 2) if service in ['Compute', 'AI Services', 'Analytics'] else round(random.uniform(1, 20), 2)
        memory_usage = round(random.uniform(10, 95), 2)
        
        # Cost calculation logic
        base_cost = usage_hours * 0.15 + storage_used * 0.02
        if service == 'AI Services':
            base_cost *= 2.5
        elif service == 'Database':
            base_cost *= 1.5
        elif service == 'Compute':
            base_cost *= 1.2
            
        # Add some random noise and anomaly
        if random.random() < 0.05: # 5% chance of anomalous high cost
            base_cost *= random.uniform(3, 5)
            
        monthly_cost = round(base_cost, 2)
        
        forecast_demand = round(monthly_cost * random.uniform(0.9, 1.2), 2)
        status = random.choices(statuses, weights=[0.7, 0.2, 0.1])[0]
        cost_center = f"CC-{random.randint(100, 999)}"
        resource_id = f"RES-{random.randint(1000, 9999)}"

        data.append([
            billing_id, hospital, department, service, region, usage_hours, 
            storage_used, monthly_cost, date.strftime('%Y-%m-%d'), status, 
            vendor, resource_id, cpu_usage, memory_usage, forecast_demand, cost_center
        ])

    df = pd.DataFrame(data, columns=[
        'Billing ID', 'Hospital Name', 'Department Name', 'Service Type', 'Region', 
        'Usage Hours', 'Storage Used (GB)', 'Monthly Cost', 'Date', 'Payment Status', 
        'Vendor Name', 'Resource ID', 'CPU Usage %', 'Memory Usage %', 'Forecast Demand', 'Cost Center'
    ])
    
    # Ensure Date column is actually datetime object so it sorts well before writing if we wanted, but strings are fine for CSV
    df = df.sort_values(by='Date').reset_index(drop=True)
    
    df.to_csv('healthcare_cloud_billing.csv', index=False)
    print(f"Dataset generated successfully with {num_rows} rows!")

if __name__ == "__main__":
    generate_dataset()
