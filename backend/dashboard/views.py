from django.shortcuts import render

from authorization.models import User, Student
from dashboard.services import GetSchoolRegionsService, GetLastRegisteredUsersService, GetCountNewUsersThisMonthService, \
    GetOverallGoalUsersService, DailyUsersService, GetCurrentWeekDays, SchoolScheduleService, \
    SchoolSectionAttendanceService
from notification.views import get_notifications, send_notification
from school.models import School, SubjectSection, SectionAction, SectionHomework, SectionHomeworkAnswer, SectionTests, \
    SectionTestsAnswer, SectionHomeworkGrade
from django.http import JsonResponse


def home(request):
    if request.user.role == 'Student':
        return student_dashboard(request)

    regions = GetSchoolRegionsService().get_school_regions()  # work
    last_registered_users = GetLastRegisteredUsersService().get_last_registered_users()  # work
    count_last_registered_users = GetCountNewUsersThisMonthService().get_count_new_users_current_month()  # work
    overall_users_analytics = GetOverallGoalUsersService().get_overall_users_analytics()  # work
    daily_users_analytics = DailyUsersService().get_daily_users()  # work

    context = {
        'regions': regions,
        'last_registered_users': last_registered_users,
        'count_last_registered_users': count_last_registered_users,
        'overall_users_analytics': overall_users_analytics,
        'daily_users_analytics': daily_users_analytics,
    }

    return render(request, 'dashboard/home.html', context)


def student_dashboard(request):
    notifications = get_notifications(request)
    school_schedule_context = SchoolScheduleService(request.user).get_school_schedule()
    attendance_context = SchoolSectionAttendanceService(request.user).get_section_attendance()

    total_homeworks = SectionHomework.objects.filter(section__subject__classroom=Student.objects.get(user=request.user).stud_class).count()
    done_total_homeworks = SectionHomeworkAnswer.objects.filter(student=Student.objects.get(user=request.user)).count()

    homeworks = {
        'total_homeworks': total_homeworks,
        'completed': done_total_homeworks,
        'not_completed': total_homeworks - done_total_homeworks,
        'percent': int(done_total_homeworks / total_homeworks * 100) if total_homeworks != 0 else 0,
    }

    total_tests = SectionTests.objects.filter(section__subject__classroom=Student.objects.get(user=request.user).stud_class).count()
    done_total_tests = SectionTestsAnswer.objects.filter(student=Student.objects.get(user=request.user)).count()

    tests = {
        'total_tests': total_tests,
        'completed': done_total_tests,
        'not_completed': total_tests - done_total_tests,
        'percent': int(done_total_tests / total_tests * 100) if total_tests != 0 else 0
    }

    instance = SectionHomeworkGrade.objects.create(
        homework=SectionHomework.objects.first(),
        student=Student.objects.get(user=request.user),
        grade=5
    )

    teacher = instance.homework.section.subject.teacher
    student = instance.student.user
    subject = instance.homework.section.subject.name
    grade = instance.grade

    body = f"Вам выставлена оценка по предмету {subject}"
    text = f"""
            Оценка: {grade}.
            Ответственный учитель: {teacher.mobile_phone}.
            """
    # send_notification(teacher, student, body, text)

    context = {
        'school_schedule': school_schedule_context,
        'attendance': attendance_context,
        'homeworks': homeworks,
        'tests': tests,
        'total_subjects': SubjectSection.objects.filter(subject__classroom=Student.objects.get(user=request.user).stud_class).count(),
        'notifications': notifications,
    }

    return render(request, 'dashboard/student_dashboard.html', context)
