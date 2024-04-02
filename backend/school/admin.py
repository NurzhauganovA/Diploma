from django.contrib import admin

from school.models import School, SchoolRequisites, Class, OurSchools, Subject, SubjectSection, SectionAction


admin.site.register(School)
admin.site.register(SchoolRequisites)
admin.site.register(Class)
admin.site.register(OurSchools)
admin.site.register(Subject)
admin.site.register(SubjectSection)
admin.site.register(SectionAction)
