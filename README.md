# SUTD Course Retriever

This project provides a simple Streamlit application to manage a list of SUTD courses and extract information from the official SUTD course website.

## Features

- Add courses to a list by providing the Pillar, Course ID, and Course Name.
- Remove courses from the list.
- Scrape course information (prerequisites, learning objectives, topics covered, instructor) from the SUTD website.
- Display the scraped information in a table.
- Download the course information as an Excel report.

## Requirements

- Python 3.7+
- Install the required packages using pip:

  ```bash
  pip install -r requirements.txt
  ```

## Usage

1. Clone the repository:

   ```bash
   git clone [invalid URL removed]
   cd sutd-course-scraper
   ```
2. Run the Streamlit application:

   ```bash
   streamlit run main.py
   ```
3. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).
4. Enter the course details (Pillar, Course ID, Course Name) and click "Add Course".
5. Repeat step 4 to add more courses.
6. Click "Remove" next to a course to remove it from the list.
7. Click "Analyze Courses" to scrape course information from the SUTD website. The information will be displayed in a table below.
8. Click "Download Report" to download the course information as an Excel file.

## Notes

- The web scraping functionality relies on the structure of the SUTD course website. If the website structure changes, the scraping code may need to be updated.
- The error handling is basic. More robust error handling can be added as needed.
