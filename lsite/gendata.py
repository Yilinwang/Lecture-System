import django
django.setup()
for lecture.models import Slide
for i in range(10):
    for j in range(5):
        a = Slide(title=str(i)+'-'+str(j), content='#content of '+str(i)+'-'+str(j))
        a.save
