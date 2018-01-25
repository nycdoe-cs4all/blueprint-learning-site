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
            print(self.grade_name)
            self.grade = Grade.objects.get(name=self.grade_name).id
        except:
            print("Can't find grade")
        try:
            self.subject = Subject.objects.get(name=self.subject_name).id
        except:
            print("Can't find subject")
        # try:
        #     self.software = Software.objects.get(name=self.software_name).id
        # except:
        #     print("Can't find software")

        self.set_devices()
        self.set_concepts()
        self.set_software()
        self.set_tags()
        print("I got here!")
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
        # print(fieldname, search)
        try:
            # for e in self.soup.select(selector):
            #     print(e.text)
            el = [e for e in self.soup.select(selector) if search in e.text][0]
            value = el.next_sibling.text
        except Exception as e:
            value = None
        setattr(self, fieldname, value)
        # print('------')
        return value

    def set_concepts(self):
        try:
            el = [e for e in self.soup.select('h1, h2, h3') if 'Concepts' in e.text][0]
            concepts = [e.text.strip() for e in el.next_sibling.children]
        except Exception as e:
            concepts = []
        self.concepts = concepts

    def set_tags(self):
        try:
            el = [e for e in self.soup.select('h1, h2, h3') if 'Tags' in e.text or 'Topics' in e.text][0]
            tags = [e.text.strip() for e in el.next_sibling.children]
        except Exception as e:
            tags = []
        self.tags = tags

    def set_devices(self):
        try:
            el = [e for e in self.soup.select('h1, h2, h3') if 'Devices' in e.text][0]
            devices = [e.text.strip() for e in el.next_sibling.children]
        except Exception as e:
            devices = []
        self.devices = devices

    def set_software(self):
        try:
            el = [e for e in self.soup.select('h1, h2, h3') if 'Software' in e.text][0]
            software = [e.text.strip() for e in el.next_sibling.children]
        except Exception as e:
            software = []
        self.software = software

    def set_body(self):
        self.body = str(self.soup.find('body'))
        # self.para = str(self.body.find('p'))
        self.bodyTags = self.soup.find('body')

        # print "\n".join(set(span['style'] for span in spans))
        #     else:
        #         newPar= par
        #         newPar2=str(newPar)
        #         newPar3= re.sub(r'\s*(style)="(.*?)"\s*', '', newPar2, flags=re.MULTILINE)
        #         # newPar3= re.sub(r'\s*(style)="(.*?)"\s*', '', newPar2, flags=re.MULTILINE)
        #         self.body = self.body.replace(newPar2, newPar3)
                #
        for child in self.bodyTags.children:
            if child.find('img'):
                print('has image')
            else:
                    # print(child)
                newTag=child
                tag1= str(newTag)
                tag2= re.sub(r'\s*(style)="(.*?)"\s*', '',tag1, flags=re.MULTILINE)
                self.body = self.body.replace(tag1, tag2)


        h3Tag = self.bodyTags.findAll('h3')
        # h2Tag = self.soup.new_tag("h2")
        for tag in h3Tag:
            tagVar=tag
            tag1=str(tagVar)
            change= str(tag.string.wrap(self.soup.new_tag("h4")))
            self.body = self.body.replace(tag1, change)
            # print change


        title = self.bodyTags.find('p', class_="title")
        # print title
        titleTag=str(title)
        changeTitle= str(title.string.wrap(self.soup.new_tag("h2")))
        self.body = self.body.replace(titleTag, changeTitle)

        # pars= self.soup.findAll('p')
        # for par in pars:
        #     if par.text == '':
        #         empty=par
        #         # del empty
        #         print empty


        # self.soup.title.wrap(self.soup.new_tag("h2"))
        # for content in reversed(title.contents):
        #     new_h2.insert(0, content.extract())
        #






        # tds= self.soup.find_all('td')

        # for td in tds:
                # del tag['style']

                # newTable=td
                # table1= str(newTable)
                # table2= re.sub(r'\s*(style)="(.*?)"\s*', '',table1, flags=re.MULTILINE)
                # self.body = self.body.replace(table1, table2)

        # trs= self.soup.find_all('table')
        #
        # for tr in trs:
        #         newTr=tr
        #         tr1= str(newTr)
        #         tr2= re.sub(r'\s*(style)="(.*?)"\s*', '',tr1, flags=re.MULTILINE)
        #         self.body = self.body.replace(tr1, tr2)
        #

        # self.body = re.sub(r"\s*style='(.*?)'\s*", '',  self.body, flags=re.MULTILINE)
        # self.body = re.sub(r'\s*(style)="(.*?)"\s*', '',  self.body, flags=re.MULTILINE)
        self.body = re.sub(r"\s*style='(.*?)'\s*", '', self.body, flags=re.MULTILINE)
        # self.body = re.sub(r'\s*(style)="(.*?)"\s*', '', self.body, flags=re.MULTILINE)

        # Checks for google annoying redirects and sends them back from whence they came
        self.body = re.sub(r'(&amp;sa=D&amp;ust=).{59}', '', self.body, flags=re.MULTILINE) #after
        self.body = self.body.replace('https://www.google.com/url?q=http', 'http') #before
        self.body = self.body.replace('%3D', '=') #for videos
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
            'tags': self.tags,
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
