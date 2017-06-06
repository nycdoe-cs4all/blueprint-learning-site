import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "activityshare.settings")
django.setup()

from activities.models import School

data = open('schools.txt', 'r').readlines()

out = []
for d in data:
    d = d.strip()
    num, school = d.split('    ')
    out.append([num.strip(), school.strip()])

out = sorted(out, key=lambda k: k[1])

for o in out:
    dbn, school = o
    School.objects.get_or_create(
        name=school,
        dbn=dbn
    )

# with open('schools.csv', 'w') as outfile:
#     writer = csv.writer(outfile)
#     for o in out:
#         writer.writerow(o)
