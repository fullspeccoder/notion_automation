from datetime import datetime
import pdfplumber
import pandas as pd


class ContentParser:
    def __init__(self, page=None, start=None, end=None):
        self.page = page
        self.start = start
        self.end = end
        self.content = ''
        self.tables = TableList()

    def set_page(self, page):
        self.page = page

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end

    def parse_content(self):
        if self.page == None:
            return IndexError()
        # Read through page
        page_text = self.page.extract_text()
        # Find starting point
        starting_point = page_text.find(self.start)
        # Find ending point
        ending_point = page_text.find(self.end)
        if ending_point == -1:
            self.content += page_text[starting_point + len(self.start):]
        elif starting_point == -1:
            self.content += page_text[0:ending_point]
        else:
            # Add content to original value
            self.content = page_text[starting_point +
                                     len(self.start):ending_point]

    def recieve_partial_content(self, start_line, end_line):
        if self.content is None:
            print("No content")

        return '\n'.join(self.content.split('\n')[start_line:end_line])

    def create_table_contents(self, start_line, end_line, table_name):
        partial_content = self.recieve_partial_content(
            start_line, end_line).split('\n')[0:-1]
        categories = list()
        values = list()
        for line in partial_content:
            curr_val_list = list()
            # Total points
            total_points = line.split(' ')[-1]
            curr_val_list.append(total_points)
            # Number Value
            item_value = line.split(' ')[-2]
            curr_val_list.append(item_value)
            # Number of Graded Items
            num_items = line.split(' ')[-3]
            curr_val_list.append(num_items)
            # Categories
            category = ''.join(line.split(' ')[0:-3])
            categories.append(category)
            values.append(curr_val_list)
        self.tables.append(Table(table_name, categories, values))

    def print_partial_content(self, start_line, end_line):
        if self.content is None:
            print("No content")

        print('\n'.join(self.content.split('\n')[start_line:end_line]))

    def grab_table(self, name):
        table = self.tables.translate_table(name)

        items_list = [x[::-1] for x in table[name][1]]
        num_items = []
        points = []
        total_points = []
        for ls in items_list:
            num_items.append(ls[0])
            points.append(ls[1])
            total_points.append(ls[2])
        return pd.DataFrame({'Categories': table[name][0], 'Number of Graded Items': num_items, 'Points per Item': points, 'Total Points': total_points})

    def save_table(self, name):
        df = self.grab_table(name)
        df.to_csv(f'{name}-{self.start}-{datetime.today()}.csv')

    def __str__(self):
        return self.content


class TableList:
    def __init__(self):
        self.table_list = dict()

    def append(self, table):
        self.table_list.update({table.name: table.contents})

    def remove(self, table):
        self.table_list.pop(table)

    def translate_table(self, name):
        return {name: self.table_list.get(name)}


class Table:
    def __init__(self, name, categories, values):
        # takes in a list of categories, with values in order and translates them to TableContents
        self.name = name
        self.contents = (categories, values)

    def grab_table_name(self):
        return self.name

    def grab_table_contents(self):
        return self.contents

# College Syllabus Parser


class CollegeParser:
    def __init__(self, file):
        self.parser = ContentParser()
        self.file = file
        self.name = ""
        self.instructor = ""
        self.instructor_email = ""
        self.course_code = ""
        self.start_date = ""
        self.end_date = ""
        self.goals_list = ""
        self.desc = str()
        self.grade_distro = pd.DataFrame()
        self.assignments = list()

    def parse_course_name(self):
        with pdfplumber.open(self.file) as pdf:
            self.parser.set_start("Syllabus")
            self.parser.set_end("Course Prerequisites")
            self.parser.set_page(pdf.pages[0])
            self.parser.parse_content()
        self.name = self._stringify_content(self.parser.content)

    def parse_course_desc(self):
        with pdfplumber.open(self.file) as pdf:
            self.parser.set_start('Course Description')
            self.parser.set_end('Course Competencies')
            self.parser.set_page(pdf.pages[0])
            self.parser.parse_content()

        self.desc = self._stringify_content(self.parser.content)

    def parse_grade_distro(self):
        with pdfplumber.open(self.file) as pdf:
            self.parser.set_start('Grade Distribution')
            self.parser.set_end('University Grading System: Undergraduate')
            self.parser.set_page(pdf.pages[2])
            self.parser.parse_content()
        self.parser.create_table_contents(4, 9, 'Graded Items')
        # self.parser.save_table('Graded Items')
        self.grade_distro = self.parser.grab_table('Graded Items')

    def parse_assignments(self):
        with pdfplumber.open(self.file) as pdf:
            self.parser.set_start('Weekly Assignment Schedule')
            self.parser.set_end('Course Participation')
            self.parser.set_page(pdf.pages[3])
            self.parser.parse_content()
            self.parser.set_page(pdf.pages[4])
            self.parser.parse_content()

        self.assignments = [x for x in self.parser.content.split(
            '\n') if x.find('-') != -1][1:]

    def _stringify_content(self, string):
        return ''.join(string.split('\n')[1:-1])

    def to_dict(self):
        return {"name": self.name, 'description': self.desc, 'grad_distro': self.grade_distro, 'assignments': self.assignments}

    def __str__(self):
        return f'\nCourse Name: {self.name}\n' + f'\nCourse Description: {self.desc}\n' + '\nCourse Grade Distribution:\n\n' + str(self.grade_distro) + "\n\nAssignments:\n\n" + "\n".join(self.assignments)
