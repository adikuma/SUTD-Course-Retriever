import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import tempfile

async def scrape_sutd_course(url: str) -> dict:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                html = await response.text()
        except Exception as e:
            print(f"Error fetching course data from {url}: {e}") 
            return {}

        if not html:
            return {}

        course_info = {
            'prerequisites': '',
            'learning_objectives': [],
            'topics_covered': [],
            'instructor': ''
        }

        try:
            soup = BeautifulSoup(html, 'html.parser')
            rich_text = soup.find('span', id='rich-text-generator')

            if rich_text:
                prereq_section = rich_text.find('h5', string='Pre-requisites')
                if prereq_section:
                    next_ul = prereq_section.find_next('ul')
                    if next_ul:
                        course_info['prerequisites'] = ', '.join([li.text.strip() for li in next_ul.find_all('li')])

                objectives_section = rich_text.find('h5', string='Learning Objectives')
                if objectives_section:
                    next_ul = objectives_section.find_next('ul')
                    if next_ul:
                        course_info['learning_objectives'] = [li.text.strip() for li in next_ul.find_all('li')]

                topics_section = rich_text.find('h5', string='Topics Covered')
                if topics_section:
                    next_ul = topics_section.find_next('ul')
                    if next_ul:
                        course_info['topics_covered'] = [li.text.strip() for li in next_ul.find_all('li')]

                instructor_section = rich_text.find('h5', string='Course Instructor(s)')
                if instructor_section:
                    next_p = instructor_section.find_next('p')
                    if next_p:
                        course_info['instructor'] = next_p.text.strip()

        except Exception as e:
            print(f"Error parsing course data from {url}: {e}")

        return course_info

def create_excel_report(courses: list) -> bytes:
    df = pd.DataFrame([{
        'Pillar': c['pillar'],
        'ID': c['id'],
        'Course Name': c['name'],
        'Prerequisites': c['prerequisites'],
        'Learning Objectives': ', '.join(c['learning_objectives']) if c['learning_objectives'] else 'Not specified',
        'Topics Covered': ', '.join(c['topics_covered']) if c['topics_covered'] else 'Not specified',
        'Course Instructor': c['instructor']
    } for c in courses])

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        with pd.ExcelWriter(tmp.name, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        with open(tmp.name, 'rb') as f:
            return f.read()

def get_url(pillar: str, course_id: str, course_name: str) -> str:
    course_id = course_id.strip().replace('.', '-')
    
    if '&' in course_name:
        url_name = course_name.strip().lower().replace(' ', '-').replace('&', 'and')
        return f'https://www.sutd.edu.sg/course/{course_id}-{url_name}/'

    else:
        url_name = course_name.strip().lower().replace(' ', '-')
        return f'https://www.sutd.edu.sg/course/{course_id}-{url_name}'