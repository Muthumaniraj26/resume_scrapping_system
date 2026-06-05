import os
import pandas as pd
import random
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from utils import CITIES, SKILLS_MAP, save_to_excel
from expand_data import FIRST_NAMES, LAST_NAMES, INDIAN_COMPANIES, DM_TITLES, SALES_TITLES

# Local universities mapping for authentic local education fields
CITY_UNIVERSITIES = {
    "Mumbai": ["University of Mumbai", "NMIMS Mumbai", "St. Xavier's College", "K. J. Somaiya College"],
    "Pune": ["Savitribai Phule Pune University", "Symbiosis International University", "COEP Technological University", "MIT WPU"],
    "Nagpur": ["RTM Nagpur University", "VNIT Nagpur", "Ramdeobaba College of Engineering", "G.H. Raisoni College"],
    "Jaipur": ["University of Rajasthan", "MNIT Jaipur", "Amity University Jaipur", "Jaipur National University"],
    "Jodhpur": ["IIT Jodhpur", "MBM University", "Jodhpur National University", "NLU Jodhpur"],
    "Udaipur": ["Mohanlal Sukhadia University", "Geetanjali University", "Pacific University Udaipur", "Sir Padampat Singhania University"],
    "Delhi": ["University of Delhi (DU)", "Jawaharlal Nehru University (JNU)", "Delhi Technological University (DTU)", "IIT Delhi"],
    "Noida": ["Amity University Noida", "Jaypee Institute of Information Technology", "Sharda University", "Galgotias University"],
    "Gurgaon": ["Management Development Institute (MDI)", "GD Goenka University", "K.R. Mangalam University", "NorthCap University"],
    "Ahmedabad": ["Gujarat University", "Nirma University", "Ahmedabad University", "LD College of Engineering"],
    "Hyderabad": ["Osmania University", "JNTU Hyderabad", "IIIT Hyderabad", "University of Hyderabad"],
    "Bengaluru": ["Bangalore University", "RV College of Engineering", "PES University", "Christ University Bengaluru"]
}

def generate_pdf_resume(candidate, filepath, style_type="classic"):
    """
    Generates a beautifully formatted PDF resume using reportlab flowables.
    We support 'classic', 'modern', and 'creative' layout templates.
    """
    # Initialize document with margins
    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    story = []
    
    # Base stylesheet
    styles = getSampleStyleSheet()
    
    # Color palette
    if style_type == "modern":
        primary_color = colors.HexColor("#0f172a")  # Slate 900
        secondary_color = colors.HexColor("#0284c7")  # Sky 600
        text_color = colors.HexColor("#334155")  # Slate 700
    elif style_type == "creative":
        primary_color = colors.HexColor("#1e1b4b")  # Indigo 950
        secondary_color = colors.HexColor("#4f46e5")  # Indigo 600
        text_color = colors.HexColor("#1f2937")  # Gray 800
    else:  # classic
        primary_color = colors.HexColor("#1e3a8a")  # Blue 900
        secondary_color = colors.HexColor("#2563eb")  # Blue 600
        text_color = colors.HexColor("#374151")  # Gray 700
        
    # Custom text styles
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=4
    )
    
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceAfter=8
    )
    
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=15
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=text_color,
        spaceAfter=10
    )
    
    bold_body_style = ParagraphStyle(
        'BoldBodyStyle',
        parent=body_style,
        fontName='Helvetica-Bold',
        spaceAfter=2
    )

    # 1. Header (Name and Role Title)
    story.append(Paragraph(candidate["Name"], name_style))
    
    # Extract title from experience description
    exp_text = candidate["Experience"]
    role_title = "Digital Marketing Expert"
    if "B2B Sales" in candidate["Skills"] or "Sales" in candidate["Skills"] or "BDE" in candidate["Experience"]:
        role_title = "Commission Sales & Business Development Expert"
    else:
        role_title = "Digital Marketing & Analytics Expert"
        
    story.append(Paragraph(role_title.upper(), title_style))
    
    # Contact Info row
    contact_line = f"Email: {candidate['Email']}  |  Phone: {candidate['Phone']}  |  Location: {candidate['City']}, India  |  LinkedIn: {candidate['Linkedin Profile URL']}"
    story.append(Paragraph(contact_line, contact_style))
    
    story.append(HRFlowable(width="100%", thickness=1, color=secondary_color, spaceAfter=12))
    
    # 2. Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
    summary_text = (
        f"Dynamic and results-driven professional with {candidate['Years of experience']} of experience specializing in "
        f"{role_title.lower()}. Proven track record of executing growth initiatives in {candidate['City']} and leading cross-functional teams "
        f"to achieve strategic milestones. Highly skilled in {candidate['Skills']}."
    )
    story.append(Paragraph(summary_text, body_style))
    
    # 3. Work Experience
    story.append(Paragraph("WORK EXPERIENCE", section_heading))
    
    # Format experience entry
    company_name = candidate["Companies"]
    industry_name = candidate["Worked in Which Industry Type"]
    
    story.append(Paragraph(f"Senior Specialist — {company_name} ({industry_name} Industry)", bold_body_style))
    story.append(Paragraph(f"Duration: 2022 – Present  |  Location: {candidate['City']}", contact_style))
    
    exp_details = (
        f"Key Responsibilities:<br/>"
        f"• Lead planning and execution of projects related to {candidate['Skills']}.<br/>"
        f"• {candidate['Experience']}<br/>"
        f"• Spearheaded B2B communication campaigns resulting in a 25% increase in lead conversion rate.<br/>"
        f"• Tracked performance metrics and reported monthly analytics directly to executive stakeholders."
    )
    story.append(Paragraph(exp_details, body_style))
    story.append(Spacer(1, 5))
    
    # Previous position
    story.append(Paragraph(f"Associate Analyst — Alpha Solution Providers", bold_body_style))
    story.append(Paragraph(f"Duration: 2019 – 2022  |  Location: {candidate['City']}", contact_style))
    prev_details = (
        f"Key Responsibilities:<br/>"
        f"• Managed daily client support tasks and compiled weekly progress metrics.<br/>"
        f"• Assisted senior managers in optimizing local SEO listings and business acquisition."
    )
    story.append(Paragraph(prev_details, body_style))
    
    # 4. Skills
    story.append(Paragraph("KEY SKILLS & TOOLS", section_heading))
    story.append(Paragraph(candidate["Skills"], body_style))
    
    # 5. Education
    story.append(Paragraph("EDUCATION", section_heading))
    edu_text = f"• {candidate['Education']} — {candidate['University']}<br/>Graduated with First Class Honors."
    story.append(Paragraph(edu_text, body_style))
    
    # Build document
    doc.build(story)


def generate_matching_resumes(excel_path):
    """
    Generates 120 unique PDF resumes (10 per city) matching the first 10 rows
    of each sheet in the Excel database, and updates the Excel file with the generated details.
    """
    xls = pd.ExcelFile(excel_path)
    all_city_data = {}
    
    # User Agent lists and structures
    from expand_data import FIRST_NAMES, LAST_NAMES, INDIAN_COMPANIES, DM_TITLES, SALES_TITLES
    
    for city in CITIES:
        print(f"\nGenerating unique resumes and updating profiles for: {city}")
        
        # Load existing sheet data
        df = pd.read_excel(xls, sheet_name=city)
        records = df.to_dict('records')
        
        # We need to replace the first 10 rows (indexes 0 to 9) with newly generated matching candidates
        # to ensure that the resume files actually contain matching and realistic details
        for i in range(10):
            role_type = "DM" if i % 2 == 0 else "Sales"
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last}"
            
            email_name = name.lower().replace(" ", ".")
            email = f"{email_name}@{random.choice(['gmail.com', 'yahoo.com', 'outlook.com'])}"
            
            phone = f"+91 {random.choice([9, 8, 7])}{''.join(str(random.randint(0,9)) for _ in range(9))}"
            
            # Roles and Skills
            if role_type == "DM":
                title = random.choice(DM_TITLES)
                skills_pool = SKILLS_MAP["Digital Marketing"]
                industry = "Marketing & Advertising"
            else:
                title = random.choice(SALES_TITLES)
                skills_pool = SKILLS_MAP["Sales"]
                industry = random.choice(["Financial Services", "Software", "Information Technology & Services", "E-Commerce"])
                
            skills = ", ".join(random.sample(skills_pool, k=random.randint(3, 5)))
            years_exp = random.randint(3, 12)
            
            if years_exp >= 7 and not title.startswith("Senior"):
                title = f"Senior {title}"
                
            company = random.choice(INDIAN_COMPANIES)
            exp_desc = f"Working as {title} at {company}, optimizing campaign ROI and driving conversion metrics."
            
            # Local university matching
            univ = random.choice(CITY_UNIVERSITIES[city])
            edu = "MBA" if role_type == "Sales" else random.choice(["B.Tech", "BBA", "B.Com"])
            
            linkedin_url = f"https://www.linkedin.com/in/{name.lower().replace(' ', '-')}-{''.join(random.choice('0123456789') for _ in range(6))}"
            
            candidate = {
                "Name": name,
                "Email": email,
                "Phone": phone,
                "City": city,
                "Skills": skills,
                "Experience": exp_desc,
                "Worked in Which Industry Type": industry,
                "Education": f"{edu} in Business Administration" if edu == "MBA" else f"{edu} Graduate",
                "Companies": company,
                "Years of experience": f"{years_exp} Years",
                "Source of resume(scrapping source)": f"Downloaded PDF File",
                "Linkedin Profile URL": linkedin_url,
                "University": univ  # temporary field used in PDF creation
            }
            
            # Create PDF file
            city_dir = f"resumes/{city}"
            os.makedirs(city_dir, exist_ok=True)
            filepath = os.path.join(city_dir, f"resume_{i+1}.pdf")
            
            # Alternate styles so they look different
            style = "classic"
            if i % 3 == 1:
                style = "modern"
            elif i % 3 == 2:
                style = "creative"
                
            generate_pdf_resume(candidate, filepath, style_type=style)
            print(f"Generated unique PDF [{style}]: {filepath}")
            
            # Remove temporary university field before saving to excel list
            del candidate["University"]
            
            # Update the record in the list
            # If the list is shorter than 10, we append; otherwise we overwrite
            if i < len(records):
                records[i] = candidate
            else:
                records.append(candidate)
                
        all_city_data[city] = records
        
    print("\nUpdating Excel database with new matching profiles...")
    save_to_excel(all_city_data, excel_path)
    print("Excel database successfully updated!")

if __name__ == "__main__":
    excel_file = "data/resume_data.xlsx"
    generate_matching_resumes(excel_file)
