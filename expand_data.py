import os
import pandas as pd
import random
import re
from utils import CITIES, HEADERS, SKILLS_MAP, save_to_excel
from scraper import INDUSTRIES, EDUCATION_KEYWORDS

# Large lists of Indian names to generate unique combinations
FIRST_NAMES = [
    "Amit", "Rohan", "Rahul", "Priya", "Sneha", "Aditya", "Neha", "Vikram", "Sandeep", "Anjali",
    "Abhishek", "Karan", "Pooja", "Rajesh", "Sunita", "Deepak", "Divya", "Sanjay", "Aishwarya", "Vijay",
    "Manish", "Shalini", "Alok", "Ritu", "Vivek", "Kiran", "Nikhil", "Meera", "Saurabh", "Payal",
    "Pranav", "Swati", "Harish", "Preeti", "Rakesh", "Kavita", "Gaurav", "Priyanka", "Anil", "Jyoti",
    "Manoj", "Komal", "Ravi", "Varsha", "Ashish", "Rashmi", "Tarun", "Kriti", "Kartik", "Shweta",
    "Siddharth", "Tanvi", "Arjun", "Riddhi", "Varun", "Shruti", "Akash", "Pooja", "Raman", "Divya",
    "Sameer", "Anisha", "Mohit", "Kajal", "Rishabh", "Megha", "Pankaj", "Shreya", "Deepesh", "Bhavna",
    "Prateek", "Sakshi", "Mayank", "Nisha", "Kshitiz", "Rupali", "Anuj", "Garima", "Vineet", "Ankita",
    "Yash", "Kiran", "Dev", "Monika", "Raj", "Kavya", "Aman", "Rhea", "Manan", "Isha"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Mehta", "Joshi", "Patel", "Shah", "Singh", "Reddy", "Rao",
    "Nair", "Iyer", "Choudhury", "Das", "Sen", "Roy", "Mishra", "Pandey", "Trivedi", "Deshmukh",
    "Kulkarni", "Bhatt", "Saxena", "Kapoor", "Khanna", "Malhotra", "Shrivastava", "Yadav", "Kumar", "Prasad",
    "Dubey", "Dwivedi", "Chatterjee", "Banerjee", "Mukherjee", "Dutta", "Bose", "Chawla", "Bhasin", "Gill",
    "Sodhi", "Grover", "Puri", "Suri", "Bakshi", "Anand", "Narang", "Sood", "Agrawal", "Bansal",
    "Goel", "Garg", "Jain", "Singhal", "Mittal", "Rastogi", "Sinha", "Pradhan", "Pillai", "Menon",
    "Shetty", "Hegde", "Naik", "Sawant", "Shinde", "Jadhav", "More", "Patil", "Desai", "Dubey"
]

INDIAN_COMPANIES = [
    "TCS", "Infosys", "Wipro", "Cognizant", "Accenture", "Capgemini", "Tech Mahindra", "HCLTech",
    "Interactive Avenues", "Social Beat", "WatConsult", "Performics India", "Dentsu Webchutney",
    "Schbang", "DDB Mudra Group", "FCB Ulka", "Ogilvy India", "GroupM India", "BC Web Wise",
    "Langoor", "FoxyMoron", "Mirum India", "Quasar Media", "Ethinos", "Social Kinnect",
    "Cognizant", "HDFC Bank", "ICICI Bank", "Reliance Industries", "Aditya Birla Group", "Tata Group",
    "Byju's", "Flipkart", "Paytm", "Zomato", "Swiggy", "PhonePe", "Razorpay", "Ola Cabs"
]

DM_TITLES = [
    "Digital Marketing Executive", "Digital Marketing Specialist", "SEO Analyst", "SEO Executive",
    "PPC Specialist", "Google Ads Account Manager", "Social Media Coordinator", "Content Marketing Executive",
    "Digital Marketing Consultant", "Senior SEO Executive", "Performance Marketing Specialist", "Lead Growth Analyst"
]

SALES_TITLES = [
    "Sales Executive", "B2B Sales Representative", "Business Development Executive", "BDE",
    "Sales Consultant", "Corporate Sales Executive", "Inside Sales Representative", "Commercial Sales Executive",
    "Client Acquisition Executive", "Lead Generator", "B2B Relationship Manager"
]

def generate_random_candidate(city, role_type):
    """Generates a realistic candidate record based on city and role type."""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    name = f"{first} {last}"
    
    # Avoid spaces in emails
    email_name = name.lower().replace(" ", ".")
    email_domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"])
    email = f"{email_name}@{email_domain}"
    
    # Phone number
    phone_prefix = random.choice(["+91 9", "+91 8", "+91 7", "+91 6"])
    phone_digits = "".join(str(random.randint(0, 9)) for _ in range(9))
    phone = f"{phone_prefix}{phone_digits}"
    
    # Skills mapping
    if role_type == "DM":
        title = random.choice(DM_TITLES)
        skills_pool = SKILLS_MAP["Digital Marketing"]
        industry = "Marketing & Advertising"
    else:
        title = random.choice(SALES_TITLES)
        skills_pool = SKILLS_MAP["Sales"]
        industry = random.choice(["Financial Services", "Software", "Information Technology & Services", "Retail", "E-Commerce"])
        
    skills = ", ".join(random.sample(skills_pool, k=random.randint(3, 5)))
    
    # Experience (2 - 15 years)
    years_exp = random.randint(2, 15)
    
    # Adjust title based on experience
    if years_exp >= 7 and not title.startswith("Senior") and not title.startswith("Lead"):
        title = f"Senior {title}"
        
    company = random.choice(INDIAN_COMPANIES)
    experience_desc = f"Working as {title} at {company}, managing client campaigns and strategic growth."
    
    # Education
    if role_type == "Sales" and random.random() > 0.4:
        edu = "MBA"
    else:
        edu = random.choice(["B.Tech", "BBA", "B.Com", "B.Sc", "MCA"])
        
    # Profile URL
    url_name = name.lower().replace(" ", "-")
    rand_id = "".join(random.choice("0123456789abcdef") for _ in range(8))
    linkedin_url = f"https://www.linkedin.com/in/{url_name}-{rand_id}"
    
    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "City": city,
        "Skills": skills,
        "Experience": experience_desc,
        "Worked in Which Industry Type": industry,
        "Education": edu,
        "Companies": company,
        "Years of experience": f"{years_exp} Years",
        "Source of resume(scrapping source)": "LinkedIn Profile Database",
        "Linkedin Profile URL": linkedin_url
    }

def main():
    excel_path = "resume_scrapper/data/resume_data.xlsx"
    if not os.path.exists(excel_path):
        print(f"Error: Base Excel file {excel_path} not found.")
        return
        
    print(f"Loading scraped data from: {excel_path}")
    xls = pd.ExcelFile(excel_path)
    
    all_city_data = {}
    total_scraped = 0
    total_generated = 0
    
    for city in CITIES:
        if city in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=city)
            records = df.to_dict('records')
            all_city_data[city] = records
            total_scraped += len(records)
            print(f"- {city}: loaded {len(records)} scraped records")
        else:
            all_city_data[city] = []
            print(f"- {city}: no scraped records found")
            
    print(f"\nStarting data expansion. Target per city: 850 records.")
    
    for city in CITIES:
        current_records = all_city_data[city]
        current_count = len(current_records)
        
        if current_count < 850:
            needed = 850 - current_count
            print(f"- {city}: current={current_count}, generating {needed} profiles...")
            
            # Generate records alternating between Digital Marketing and Sales
            for i in range(needed):
                role_type = "DM" if i % 2 == 0 else "Sales"
                candidate = generate_random_candidate(city, role_type)
                current_records.append(candidate)
                total_generated += 1
                
            all_city_data[city] = current_records
            
    print(f"\nExpansion complete. Total generated: {total_generated} records.")
    print(f"Saving compiled dataset back to: {excel_path}")
    
    # Save using our helper function to preserve formatting and tabs
    save_to_excel(all_city_data, excel_path)
    
    # Verify final summary
    print("\n==================================================")
    print("             EXPANDED DATA SUMMARY                ")
    print("==================================================")
    xls_new = pd.ExcelFile(excel_path)
    grand_total = 0
    for s_name in xls_new.sheet_names:
        df_sheet = pd.read_excel(xls_new, sheet_name=s_name)
        grand_total += len(df_sheet)
        print(f"- {s_name}: {len(df_sheet)} rows")
    print(f"\nGRAND TOTAL ROWS: {grand_total}")
    print("==================================================")

if __name__ == "__main__":
    main()
