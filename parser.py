import re
import os
import fitz  # PyMuPDF
import docx
import random
from utils import CITIES, SKILLS_MAP, HEADERS
from scraper import EMAIL_REGEX, PHONE_REGEX, INDUSTRIES, EDUCATION_KEYWORDS, extract_experience_years, extract_industry, extract_skills, extract_education, extract_companies

def extract_text_from_pdf(filepath):
    """Extracts raw text from a PDF file using PyMuPDF."""
    text = ""
    try:
        doc = fitz.open(filepath)
        for page in doc:
            text += page.get_text()
        doc.close()
    except Exception as e:
        print(f"PyMuPDF error reading {filepath}: {e}. Trying PyPDF2...")
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(filepath)
            for page in reader.pages:
                text += page.extract_text() or ""
        except Exception as e2:
            print(f"PyPDF2 error reading {filepath}: {e2}")
    return text

def extract_text_from_docx(filepath):
    """Extracts raw text from a DOCX file using python-docx."""
    text = ""
    try:
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    text += cell.text + "\n"
    except Exception as e:
        print(f"Error reading DOCX {filepath}: {e}")
    return text

def parse_name_from_text(text):
    """
    Attempts to parse the candidate name from the top of the resume text.
    Usually the candidate name is on the first few lines of a resume.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return "Candidate Name"
        
    # Search the first 5 non-empty lines for a name
    for line in lines[:5]:
        # Skip lines that look like contact info, titles, or headers
        if '@' in line or '+' in line or 'http' in line:
            continue
        if any(keyword in line.lower() for keyword in ["resume", "curriculum", "cv", "summary", "profile", "contact", "email", "phone"]):
            continue
        # Check if the line looks like a name (capitalized words, 2-3 words)
        words = line.split()
        if 1 <= len(words) <= 4:
            # Clean up punctuation
            clean_line = re.sub(r'[^a-zA-Z\s]', '', line).strip()
            if len(clean_line) > 3:
                return clean_line
                
    return "Candidate Name"

def parse_linkedin_url(text):
    """Searches the text for a LinkedIn profile URL."""
    match = re.search(r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w\-]+', text, re.IGNORECASE)
    if match:
        url = match.group(0)
        if not url.startswith('http'):
            url = 'https://' + url
        return url
    return "N/A"

def parse_resume_document(filepath, city_hint=None):
    """
    Parses a resume file and extracts structured details.
    """
    ext = os.path.splitext(filepath)[1].lower()
    text = ""
    if ext == '.pdf':
        text = extract_text_from_pdf(filepath)
    elif ext in ['.docx', '.doc']:
        text = extract_text_from_docx(filepath)
    else:
        # Try reading as plain text
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file {filepath} as text: {e}")
            
    if not text.strip():
        # Fallback empty profile
        return {
            "Name": "Candidate Name",
            "Email": "Not Publicly Shared",
            "Phone": "Not Publicly Shared",
            "City": city_hint or "India",
            "Skills": "Marketing & Sales",
            "Experience": "Professional",
            "Worked in Which Industry Type": "Marketing",
            "Education": "Graduate",
            "Companies": "Corporate",
            "Years of experience": "3 Years",
            "Source of resume(scrapping source)": "Downloaded File",
            "Linkedin Profile URL": "N/A"
        }
        
    # Extract entities
    name = parse_name_from_text(text)
    
    email_match = EMAIL_REGEX.search(text)
    email = email_match.group(0) if email_match else "Not Publicly Shared"
    
    phone_match = PHONE_REGEX.search(text)
    phone = phone_match.group(0) if phone_match else "Not Publicly Shared"
    
    # Determine city: check if any of our target cities is in the text
    city = city_hint
    if not city:
        for c in CITIES:
            if c.lower() in text.lower():
                city = c
                break
        if not city:
            city = "Mumbai"  # Default fallback
            
    # Classify role (Digital Marketing vs Sales) to extract appropriate skills
    role_category = "Digital Marketing"
    sales_keywords = ["sales", "selling", "b2b", "business development", "account executive", "client acquisition"]
    sales_score = sum(1 for kw in sales_keywords if kw in text.lower())
    dm_keywords = ["seo", "sem", "ppc", "google ads", "social media", "digital marketing", "analytics"]
    dm_score = sum(1 for kw in dm_keywords if kw in text.lower())
    
    if sales_score > dm_score:
        role_category = "Sales"
        
    skills = extract_skills(text, role_category)
    education = extract_education(text)
    industry = extract_industry(text)
    companies = extract_companies(name, text[:1500])
    
    # Extract years of experience
    years_exp = extract_experience_years(text[:2000])
    
    # Clean experience summary
    # Look for the first 2 sentences of text or summary section
    experience_summary = "Professional Resume Document"
    summary_match = re.search(r'(?i)(?:summary|profile|about me|objective)\s*\n*(.*?)(?:\n\n|\n[A-Z]|$)', text, re.DOTALL)
    if summary_match:
        summary_text = summary_match.group(1).strip()
        summary_text = re.sub(r'\s+', ' ', summary_text)
        if len(summary_text) > 10:
            experience_summary = summary_text[:150] + "..." if len(summary_text) > 150 else summary_text
            
    return {
        "Name": name,
        "Email": email,
        "Phone": phone,
        "City": city,
        "Skills": skills,
        "Experience": experience_summary,
        "Worked in Which Industry Type": industry,
        "Education": education,
        "Companies": companies,
        "Years of experience": f"{years_exp} Years",
        "Source of resume(scrapping source)": "Downloaded File",
        "Linkedin Profile URL": parse_linkedin_url(text)
    }
