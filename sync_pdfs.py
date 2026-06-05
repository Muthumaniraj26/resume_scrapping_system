import os
import pandas as pd
from generate_resumes import generate_pdf_resume
from utils import CITIES

def main():
    excel_path = "data/resume_data.xlsx"
    if not os.path.exists(excel_path):
        print(f"Error: Excel file {excel_path} not found.")
        return
        
    print(f"Loading Excel file to sync PDFs: {excel_path}")
    xls = pd.ExcelFile(excel_path)
    
    total_synced = 0
    
    for city in CITIES:
        if city not in xls.sheet_names:
            print(f"Warning: Sheet {city} not found in Excel!")
            continue
            
        df = pd.read_excel(xls, sheet_name=city)
        records = df.head(10).to_dict('records')
        
        city_dir = f"resumes/{city}"
        os.makedirs(city_dir, exist_ok=True)
        
        print(f"Syncing {len(records)} resume PDFs for {city}...")
        
        for i, r in enumerate(records):
            # Parse university from the enriched education string (e.g. "B.Tech from MNIT Jaipur")
            edu_str = r.get("Education", "Graduate")
            univ = "Local University"
            edu = edu_str
            if " from " in edu_str:
                parts = edu_str.split(" from ")
                edu = parts[0]
                univ = parts[1]
                
            # Create a dictionary compatible with the generate_pdf_resume function
            candidate = {
                "Name": r.get("Name"),
                "Email": r.get("Email"),
                "Phone": r.get("Phone"),
                "City": r.get("City"),
                "Skills": r.get("Skills"),
                "Experience": r.get("Experience"),
                "Worked in Which Industry Type": r.get("Worked in Which Industry Type"),
                "Education": edu,
                "Companies": r.get("Companies"),
                "Years of experience": r.get("Years of experience"),
                "Linkedin Profile URL": r.get("Linkedin Profile URL"),
                "University": univ
            }
            
            filepath = os.path.join(city_dir, f"resume_{i+1}.pdf")
            
            # Select style based on index
            style = "classic"
            if i % 3 == 1:
                style = "modern"
            elif i % 3 == 2:
                style = "creative"
                
            # Regenerate the PDF using the exact same format
            try:
                generate_pdf_resume(candidate, filepath, style_type=style)
                total_synced += 1
            except Exception as e:
                print(f"Error generating PDF for {candidate['Name']} in {city}: {e}")
                
    print(f"\nPDF rebuild complete! Total synced: {total_synced} resumes.")

if __name__ == "__main__":
    main()
