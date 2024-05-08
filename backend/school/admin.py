from django.contrib import admin

from school.models import School, SchoolRequisites, Class, OurSchools, Subject, SubjectSection, SectionAction, \
    SectionHomework, SectionHomeworkAnswer, SectionHomeworkGrade, SectionTests, SectionTestsAnswer, SectionTestsGrade

admin.site.register(School)
admin.site.register(SchoolRequisites)
admin.site.register(Class)
admin.site.register(OurSchools)
admin.site.register(Subject)
admin.site.register(SubjectSection)
admin.site.register(SectionAction)

admin.site.register(SectionHomework)
admin.site.register(SectionHomeworkAnswer)
admin.site.register(SectionHomeworkGrade)

admin.site.register(SectionTests)
admin.site.register(SectionTestsAnswer)
admin.site.register(SectionTestsGrade)
