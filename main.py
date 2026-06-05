import os
import time
from utils import CITIES, create_directories, save_to_excel, HEADERS
from downloader import download_city_resumes
from parser import parse_resume_document
from scraper import scrape_city_candidates

def main():
    print("==================================================")
    print("    STARTING RESUME SCRAPING & COMPILING SYSTEM   ")
    print("==================================================")
    
    # 1. Initialize folders
    base_dir = "resume_scrapper"
    resumes_dir, data_dir = create_directories(base_dir)
    excel_path = os.path.join(data_dir, "resume_data.xlsx")
    
    # Store all candidate records grouped by city
    all_city_data = {city: [] for city in CITIES}
    
    # 2. Main Processing Loop for each City
    for city in CITIES:
        print(f"\n>>> PROCESSING CITY: {city.upper()} <<<")
        
        # Step 2a: Download at least 10 actual resumes
        print(f"\n--- Downloading actual resumes for {city} ---")
        downloaded_info = download_city_resumes(city, target_count=10, base_dir=base_dir)
        
        # Step 2b: Parse downloaded resumes
        print(f"\n--- Parsing downloaded resumes for {city} ---")
        parsed_resumes_count = 0
        for filepath, source_url in downloaded_info:
            try:
                candidate = parse_resume_document(filepath, city_hint=city)
                # Set source and LinkedIn profile if available
                candidate["Source of resume(scrapping source)"] = f"Downloaded PDF File ({source_url[:35]}...)"
                all_city_data[city].append(candidate)
                parsed_resumes_count += 1
            except Exception as e:
                print(f"Error parsing resume {filepath}: {e}")
                
        print(f"Successfully parsed {parsed_resumes_count} resume documents for {city}.")
        
        # Step 2c: Scrape LinkedIn profiles from AOL search to meet the count requirement
        # Target is at least 850 total records per city (10 downloaded + 840 scraped)
        # 850 * 12 = 10,200 total records (> 10,000 threshold)
        target_scraped_count = 840
        print(f"\n--- Scraping LinkedIn profiles via AOL for {city} (Target: {target_scraped_count}) ---")
        
        scraped_candidates = scrape_city_candidates(city, target_count=target_scraped_count)
        all_city_data[city].extend(scraped_candidates)
        
        total_city_count = len(all_city_data[city])
        print(f"\nCity {city} processing complete. Total records collected: {total_city_count}")
        print("--------------------------------------------------")
        
        # Cool down period between cities to prevent rate limits
        time.sleep(random_sleep := time.time() % 3 + 2)
        
    # 3. Save all results to a multi-tab excel sheet
    print("\n>>> COMPILING DATA & SAVING TO EXCEL <<<")
    save_to_excel(all_city_data, excel_path)
    
    # Print summary statistics
    print("\n==================================================")
    print("                SCRAPING SUMMARY                  ")
    print("==================================================")
    total_records = 0
    for city in CITIES:
        count = len(all_city_data[city])
        total_records += count
        print(f"- {city}: {count} records")
    print(f"\nTOTAL RECORDS COLLECTED: {total_records}")
    print(f"Resumes downloaded: {sum(len(os.listdir(os.path.join(resumes_dir, c))) for c in CITIES)} files")
    print(f"Output Excel sheet: {excel_path}")
    print("==================================================")

if __name__ == "__main__":
    main()
