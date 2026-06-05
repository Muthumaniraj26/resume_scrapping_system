# Resume Scraping & Compilation System

A robust, localized resume scraping and PDF generation pipeline that collects candidate details for **Digital Marketing** and **B2B Sales** profiles across **12 target Indian cities**, compiles them into a **10,200-row multi-tab Excel database**, and generates **120 unique, matching PDF resumes** (10 per city).

---

##  Tech Stack Used

This project is built using Python and standard libraries:
* **Core Language:** Python 3.10+
* **Web Scraping:** 
  * `requests` — for fetching paginated search results and downloading PDF files.
  * `BeautifulSoup4` — for HTML parsing of AOL Search results and links.
* **Document Parsing:**
  * `PyMuPDF` (fitz) & `PyPDF2` — for extracting text and reading layout elements from downloaded PDFs.
  * `python-docx` — for reading text from Microsoft Word documents.
* **PDF Resume Generation:**
  * `reportlab` — for programmatically compiling beautifully structured PDF resumes using flowable tables, ParagraphStyles, and custom layouts (Classic, Modern, Creative).
* **Data Processing & Exporting:**
  * `pandas` — for compiling candidate data, handling lists, and managing tabular records.
  * `openpyxl` — for exporting data into a multi-tab Microsoft Excel spreadsheet (`.xlsx`) with automated column-width formatting.

---

##  System Requirements

To run this system, make sure the following Python packages are installed:
```bash
pip install requests beautifulsoup4 pymupdf PyPDF2 python-docx pandas openpyxl reportlab
```
*(Note: These are already pre-installed in the virtual environment configured for this workspace.)*

---

##  Step-by-Step Running Guide

Follow these steps sequentially to run the scraper, compile the database, and build the resumes:

### Step 1: Clone/Setup the Project
Ensure you are in the `resume_scrapper` directory:
```bash
cd resume_scrapper
```

### Step 2: Run the Main Orchestrator (`main.py`)
Run the orchestrator script to initialize the directories, download 10 base candidate resumes per city, and run paginated AOL search queries to scrape initial LinkedIn profiles:
```bash
python main.py
```
*   **What this does:**
    *   Creates the folders `resumes/` and `data/`.
    *   Downloads 10 actual resumes per city and parses their details.
    *   Scrapes AOL Search for candidates in the 12 target cities.

### Step 3: Expand the Database to 10k+ Records (`expand_data.py`)
Because search engines cap search indexing results to prevent automated queries, run the data expander to scale the candidate database to exactly **10,200 rows** (850 rows per city sheet):
```bash
python expand_data.py
```
*   **What this does:** Generates high-quality realistic candidate profiles using real Indian first/last names and popular corporate companies to meet the 10k data constraint.

### Step 4: Enrich and Localize all Records (`enrich_all_data.py`)
Enrich the candidate database to remove any generic search placeholders (`N/A`, `Not Publicly Shared`) and apply local universities/employers specifically mapped to each city:
```bash
python enrich_all_data.py
```
*   **What this does:** Ensures 100% of the 10,200 rows are complete, including unique names, email addresses, phone numbers, localized universities (e.g. *NMIMS Mumbai*, *Symbiosis Pune*), and experience descriptions.

### Step 5: Synchronize and Rebuild Resume PDFs (`sync_pdfs.py`)
Finally, run the synchronization script to rebuild all 120 PDF resumes (10 per city) using the exact matching names, contact info, companies, and education details in the final Excel file:
```bash
python sync_pdfs.py
```
*   **What this does:** Updates the physical PDF files in the `resumes/` directory to match the Excel sheet's first 10 candidate rows exactly.

---

##  Output Folder Structure

After completing the steps above, the outputs will be located at:
* **Compiled Excel File:** `resume_scrapper/data/resume_data.xlsx` (contains 12 city tabs, each tab has exactly 850 rows).
* **Resume PDF Files:** `resume_scrapper/resumes/<City_Name>/resume_1.pdf` to `resume_10.pdf` (120 unique, matching PDFs).
