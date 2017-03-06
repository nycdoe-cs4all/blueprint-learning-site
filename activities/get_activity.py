from apiclient.discovery import build
from bs4 import BeautifulSoup
import json
import re
import os 
from .models import Grade, Subject, Software

with open(os.path.dirname(os.path.realpath(__file__)) + '/credentials.json') as data:
    keys = json.load(data)

KEY = keys['google_key']


class Activity:

    def __init__(self, file_id):
        # change this to oauth later? ask for developer key at init
        self.drive_service = build('drive', 'v3', developerKey=KEY)

        # if file_id is a url, then parse out the fileId
        if '/' in file_id:
            file_id = file_id.split('/')[-2]

        html = self.get_html(file_id)
        self.soup = BeautifulSoup(html, 'html.parser')

        self.set_by_selector('subtitle', 'p.subtitle')
        self.set_by_selector('title', 'p.title')
        self.set_by_sibling(fieldname='grade_name', selector='h1,h2,h3', search='Grade')
        self.set_by_sibling(fieldname='subject_name', selector='h1,h2,h3', search='Subject')
        self.set_by_sibling(fieldname='pacing', selector='h1,h2,h3', search='Pacing')
        self.set_by_sibling(fieldname='software_name', selector='h1,h2,h3', search='Software')

        self.subject = None
        self.grade = None
        self.software = None
        try:
            self.grade = Grade.objects.get(name=self.grade_name).id
        except:
            print("Can't find grade")
        try:
            self.subject = Subject.objects.get(name=self.subject_name).id
        except:
            print("Can't find subject")
        try:
            self.software = Software.objects.get(name=self.software_name).id
        except:
            print("Can't find software")

        self.set_devices()
        self.set_concepts()
        self.set_body()
        self.set_plain_body()


    def get_html(self, file_id):
        files = self.drive_service.files()
        response = files.export(fileId=file_id, mimeType='text/html')
        html = response.execute()
        return html

    def set_by_selector(self, fieldname, selector, index=0):
        try:
            value = self.soup.select(selector)[index].text.strip()
        except:
            value = None
        setattr(self, fieldname, value)
        return value

    def set_by_sibling(self, fieldname, selector, search):
        print(fieldname, search)
        try:
            for e in self.soup.select(selector):
                print(e.text)
            el = [e for e in self.soup.select(selector) if search in e.text][0]
            value = el.next_sibling.text
        except Exception as e:
            value = None
        setattr(self, fieldname, value)
        print('------')
        return value

    def set_concepts(self):
        try:
            el = [e for e in self.soup.select('h1, h2, h3') if 'Concepts' in e.text][0]
            concepts = [e.text.strip() for e in el.next_sibling.children]
        except Exception as e:
            concepts = [] 
        self.concepts = concepts

    def set_devices(self):
        try:
            el = [e for e in self.soup.select('h1, h2, h3') if 'Devices' in e.text][0]
            devices = [e.text.strip() for e in el.next_sibling.children]
        except Exception as e:
            devices = [] 
        self.devices = devices

    def set_body(self):
        self.body = str(self.soup.find('body'))
        self.body = re.sub(r"\s*style='(.*?)'\s*", '', self.body, flags=re.MULTILINE)
        self.body = re.sub(r'\s*(style|class|id)="(.*?)"\s*', '', self.body, flags=re.MULTILINE)
        return self.body

    def set_plain_body(self):
        self.plain_body = self.soup.find('body').getText(separator=' ')

    def to_dict(self):
        return {
            'title': self.title,
            'grade': self.grade,
            'subject': self.subject,
            'body': self.body,
            'plain_body': self.plain_body,
            'devices': self.devices,
            'concepts': self.concepts,
            'software': self.software,
            'pacing': self.pacing
        }


if __name__ == '__main__':
    import sys
    from pprint import pprint
    activity = Activity(sys.argv[1])
    print(activity.to_dict())
    # print(activity.title, activity.subtitle)
    # print(activity.grade)
    # print(activity.body)
    # print(activity.soup.prettify())
