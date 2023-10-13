from rest_framework.routers import DefaultRouter
from schedules.views import ScheduleViewSet
from employees.views import EmployeeViewSet
from shifts.views import ShiftViewSet
import sqlite3

router=DefaultRouter()


router.register('shed', ScheduleViewSet)
router.register('employee', EmployeeViewSet)
router.register('shift', ShiftViewSet)