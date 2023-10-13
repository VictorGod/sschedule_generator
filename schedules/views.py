from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Schedule, Employee, Shift
from .serializers import ScheduleSerializer
from rest_framework.decorators import action

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    @action(methods=['POST'], detail=False, url_path="generate")
    def generate_schedule(self, request):
        month = request.data.get('month')
        year = request.data.get('year')

        # Проверка наличия месяца и года в запросе
        if not month or not year:
            return Response({'error': 'Month and year are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Определение числа дней в месяце
        if month in [4, 6, 9, 11]:
            days_in_month = 30
        elif month == 2:
            if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
                days_in_month = 29
            else:
                days_in_month = 28
        else:
            days_in_month = 31

        # Получение списка сотрудников
        employees = Employee.objects.all()

        # Расчет средней нагрузки на каждого сотрудника в день
        average_load = (days_in_month * 12) / len(employees)

        # Максимальное количество часов в месяц на 1 сотрудника
        max_hours_per_month = 144

        # Создание расписания
        schedule = []
        for day in range(1, days_in_month + 1):
            date = f"{year}-{month:02d}-{day:02d}"  # Форматирование месяца и дня с ведущими нулями

            # Определение количества необходимых сотрудников
            if day % 7 == 1:  # Понедельник
                required_employees = int(average_load) + 1
            elif day % 7 == 0:  # Воскресенье
                required_employees = int(average_load) - 1
            else:
                required_employees = int(average_load)

            # Выбор сотрудников для смены
            selected_employees = employees[:required_employees]

            # Распределение часов для каждого сотрудника
            hours_per_employee = max_hours_per_month / required_employees

            # Выбор времени начала и окончания смены
            if day % 2 == 0:  # Четный день
                shift_start_time = "10:00"
                shift_end_time = "22:00"
            else:  # Нечетный день
                shift_start_time = "08:00"
                shift_end_time = "20:00"

            # Создание записей в расписании
            for employee in selected_employees:
                shift = Shift.objects.create(start_time=shift_start_time, end_time=shift_end_time)

                # Распределение часов для сотрудника
                hours_assigned = 0
                while hours_assigned < hours_per_employee:
                    schedule_entry = {
                        "id": Schedule.objects.latest('id').id + 1,
                        "date": date,
                        "employee": employee.name,
                        "shift": shift.id
                    }
                    schedule.append(schedule_entry)
                    hours_assigned += 12  # Длительность стандартной смены

        return Response(schedule, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        if 'month' in request.data and 'year' in request.data:
            return self.generate_schedule(request)
        else:
            return super().create(request, *args, **kwargs)
