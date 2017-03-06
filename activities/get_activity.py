from apiclient.discovery import build
from bs4 import BeautifulSoup
import json
import re
import os 
from .models import Grade, Subject

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
        self.set_by_sibling(fieldname='grade_name', selector='h3', search='Grade Band')
        self.set_by_sibling(fieldname='subject_name', selector='h3', search='Subject')

        self.subject = None
        self.grade = None
        try:
            self.grade = Grade.objects.get(name=self.grade_name).id
        except:
            print("Can't find grade")
        try:
            self.subject = Subject.objects.get(name=self.subject_name).id
        except:
            print("Can't find subject")

        self.set_devices()
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
        try:
            el = [e for e in self.soup.select(selector) if search in e.text][0]
            value = el.next_sibling.text
        except Exception as e:
            value = None
        setattr(self, fieldname, value)
        return value

    def set_devices(self):
        try:
            el = [e for e in self.soup.select('h2') if 'Devices' in e.text][0]
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
            'devices': self.devices
        }


if __name__ == '__main__':
    import sys
    from pprint import pprint
    activity = Activity(sys.argv[1])
    print(activity.to_dict()['body'])
    # print(activity.title, activity.subtitle)
    # print(activity.grade)
    # print(activity.body)
    # print(activity.soup.prettify())
