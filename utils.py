import os
import pandas as pd

# Target cities
CITIES = [
    "Mumbai", "Pune", "Nagpur", "Jaipur", "Jodhpur", "Udaipur", 
    "Delhi", "Noida", "Gurgaon", "Ahmedabad", "Hyderabad", "Bengaluru"
]

# Standard headers required in the excel sheet
HEADERS = [
    "Name", "Email", "Phone", "City", "Skills", "Experience", 
    "Worked in Which Industry Type", "Education", "Companies", 
    "Years of experience", "Source of resume(scrapping source)", 
    "Linkedin Profile URL"
]

# Common skills by domain for classification/matching
SKILLS_MAP = {
    "Digital Marketing": [
        "SEO", "SEM", "PPC", "Google Analytics", "Social Media", "Social Media Marketing",
        "Content Marketing", "Email Marketing", "Copywriting", "Lead Generation", "Facebook Ads",
        "Google Ads", "Branding", "Growth Hacking", "Digital Marketing", "Content Creation",
        "WordPress", "Canva", "Shopify", "E-commerce", "Search Engine Optimization", 
        "Pay Per Click", "Search Engine Marketing", "Online Advertising"
    ],
    "Sales": [
        "B2B Sales", "Lead Generation", "Cold Calling", "Negotiation", "Relationship Management",
        "CRM", "Sales Executive", "Client Acquisition", "Business Development", "Account Management",
        "Direct Sales", "Inside Sales", "Market Research", "Public Speaking", "Communication",
        "Closing", "B2B Marketing", "Sales Operations", "Sales Strategy", "Customer Relations"
    ]
}

# User agents list for rotation to prevent blocking
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
]

def create_directories(base_dir="resume_scrapper"):
    """Create local directories for storing downloaded resume files."""
    resumes_dir = os.path.join(base_dir, "resumes")
    os.makedirs(resumes_dir, exist_ok=True)
    
    for city in CITIES:
        city_dir = os.path.join(resumes_dir, city)
        os.makedirs(city_dir, exist_ok=True)
    
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    print(f"Created directory structure in '{base_dir}'")
    return resumes_dir, data_dir

def save_to_excel(data_dict_by_city, file_path):
    """
    Saves scraped data to a multi-tab excel sheet.
    data_dict_by_city: dict where keys are city names and values are list of dicts representing candidate profiles.
    file_path: target excel file path.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for city in CITIES:
            # Get data for this city or create empty if none exists
            city_data = data_dict_by_city.get(city, [])
            
            # Convert to DataFrame
            df = pd.DataFrame(city_data)
            
            # Reindex to ensure all required headers are present and in order
            for col in HEADERS:
                if col not in df.columns:
                    df[col] = "N/A"
            
            df = df[HEADERS]
            
            # Write to tab (sheet name is the city name)
            # Sheet names in Excel have a max length of 31 characters, which our cities satisfy
            df.to_excel(writer, sheet_name=city, index=False)
            
            # Auto-adjust column widths for readability
            workbook = writer.book
            worksheet = writer.sheets[city]
            for col in worksheet.columns:
                max_len = max(len(str(cell.value or '')) for cell in col)
                col_letter = col[0].column_letter
                worksheet.column_dimensions[col_letter].width = max(max_len + 3, 10)
                
    print(f"Excel sheet successfully saved to: {file_path}")
