import streamlit as st
from utils import scrape_sutd_course, create_excel_report, get_url
import pandas as pd
from datetime import datetime
import asyncio

st.set_page_config(
    page_title="Course List",
    layout="wide",
)

def main():
    st.title("Course Retriever")

    if 'courses' not in st.session_state:
        st.session_state.courses = []

    pillar = st.text_input("Enter Pillar (e.g., ISTD, ESD, ASD, EPD, HASS):")
    course_id = st.text_input("Enter Course ID (e.g., 50.004):")
    course_name = st.text_input("Enter Course Name (e.g., Introduction to Algorithms):")

    if st.button("Add Course"):
        if pillar and course_id and course_name:
            new_course = {"pillar": pillar, "id": course_id, "name": course_name}
            if new_course not in st.session_state.courses:
                st.session_state.courses.append(new_course)
                st.success("Course added successfully!")
            else:
                st.error("Course already exists in the list.")
        else:
            st.error("Please fill in all the fields.")

    st.subheader("Added Courses:")
    if st.session_state.courses:
        for i, course in enumerate(st.session_state.courses):
            st.write(f"**{i+1}. {course['pillar']} {course['id']} - {course['name']}**")

        if st.button("Get Course Information"):
            progress = st.progress(0)
            analyzed_courses = []

            async def analyze_courses():  
                for idx, course in enumerate(st.session_state.courses):
                    try:
                        url = get_url(course["pillar"], course["id"], course["name"])
                        scraped_info = await scrape_sutd_course(url) 

                        course_info = {
                            'pillar': course['pillar'],
                            'id': course['id'],
                            'name': course['name'],
                            'prerequisites': scraped_info.get('prerequisites', ''),
                            'learning_objectives': scraped_info.get('learning_objectives', []),
                            'topics_covered': scraped_info.get('topics_covered', []),
                            'instructor': scraped_info.get('instructor', '')
                        }

                        analyzed_courses.append(course_info)
                        progress.progress((idx + 1) / len(st.session_state.courses))

                    except Exception as e:
                        st.error(f"Error analyzing {course['id']}: {e}")
                return analyzed_courses

            if 'analyzed_courses' not in st.session_state or st.session_state.analyze_pressed:
                try:
                    analyzed_courses = asyncio.run(analyze_courses())
                    st.session_state.analyzed_courses = analyzed_courses
                    st.session_state.analyze_pressed = False
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")

            if 'analyzed_courses' in st.session_state:
                df = pd.DataFrame([{
                    'Pillar': c['pillar'],
                    'ID': c['id'],
                    'Course': c['name'],
                    'Prerequisites': c['prerequisites'],
                    'Learning Objectives': ', '.join(c['learning_objectives']) if c['learning_objectives'] else 'Not specified',
                    'Topics Covered': ', '.join(c['topics_covered']) if c['topics_covered'] else 'Not specified',
                    'Course Instructor': c['instructor']
                } for c in st.session_state.analyzed_courses])

                st.dataframe(df)

                excel_data = create_excel_report(st.session_state.analyzed_courses)
                st.download_button(
                    "Download Report",
                    excel_data,
                    f"sutd_courses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        st.write("No courses added yet.")

if __name__ == "__main__":
    main()
