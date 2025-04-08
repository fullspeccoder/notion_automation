from datetime import datetime, timedelta
from college.parser import CollegeParser
import os
from notion_client import Client
from schemas.course_schema import NotionCourse

client = Client(auth=os.getenv("NOTION_API_KEY"))

# Content Object
col_parser = CollegeParser('assets/syllabus.pdf')

col_parser.parse_course_name()
col_parser.parse_course_desc()
col_parser.parse_grade_distro()
col_parser.parse_assignments()
print(col_parser.to_dict())
# print(col_parser)

start_d = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
formatted_start_d = start_d.strftime("%Y-%m-%d")
end_d = start_d + timedelta(weeks=8)
formatted_end_d = end_d.strftime("%Y-%m-%d")

print(start_d, end_d)

course = NotionCourse(db_id=os.getenv("NOTION_COURSE_DATABASE_ID"), name=col_parser.name, cover_url='https://images.unsplash.com/photo-1501504905252-473c47e087f8?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y291cnNlfGVufDB8fDB8fHww', instructor="someinstructor",
                      instructor_email="someinstructoremail", course_code=col_parser.name[0:7], syllabus_url="someurl", start_date=formatted_start_d, end_date=formatted_end_d, goals_list="competencies")

client.pages.create(page_id=course.retrieve_id(), **course.to_dict())
