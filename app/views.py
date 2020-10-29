from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from .forms import EmployeeForm
from .models import Employee


class UsersIndex(TemplateView):
    template_name = 'app/index.html'

    def get(self, request, *args, **kwargs):
        """
        Return the list of all the active users data.
        """
        return render(request, self.template_name)


"""
    Purpose : List view for employees.
"""


class EmployeeList(ListView):
    template_name = 'app/list_view.html'

    def get(self, request, *args, **kwargs):
        """
        Return the list of all the active employee data.
        """
        search_filter = self.request.GET.get('filter')
        click = self.request.GET.get('click')
        sort_value = '-created_at'
        if click == '1':
            sort_value = self.request.GET.get('sortfn')
        if click == '2':
            sort_value = self.request.GET.get('sortln')
        if self.request.GET.get('click') == '3':
            sort_value = self.request.GET.get('sortemail')
        if self.request.GET.get('click') == '4':
            sort_value = self.request.GET.get('sortage')

        print(search_filter)
        if not search_filter:
            queryset = Employee.objects.filter(is_active=True).all().order_by(sort_value)
        else:
            queryset = Employee.objects.filter(Q(is_active=True) & (Q(firstName__icontains=search_filter) |
                                               Q(lastName__icontains=search_filter) |
                                               Q(email__icontains=search_filter) |
                                               Q(age__icontains=search_filter))).all().order_by(sort_value)

        paginator = Paginator(queryset, 5)
        try:
            page = int(request.GET.get('page', '1'))
        except:
            page = 1

        try:
            record_list = paginator.page(page)
        except PageNotAnInteger:
            record_list = paginator.page(1)
        except EmptyPage:
            record_list = paginator.page(paginator.num_pages)

            # Get the index of the current page
        index = record_list.number - 1

        # This value is maximum index of pages, so the last page - 1
        max_index = len(paginator.page_range)

        # range of 7, calculate where to slice the list
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 4 if index <= max_index - 4 else max_index

        # new page range
        page_range = paginator.page_range[start_index:end_index]

        # showing first and last links in pagination
        if index >= 4:
            start_index = 1
        if end_index - index >= 4 and end_index != max_index:
            end_index = max_index
        else:

            end_index = None

        return render(request, self.template_name,
                      {'record_list': record_list, 'page_range': page_range, 'start_index': start_index,
                       'end_index': end_index, 'max_index': max_index})


class EmployeeAdd(View):
    """
        This class will covers the create and list view of employee.
    """
    form_class = EmployeeForm
    template_name = 'app/add_view.html'

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        """
        Create new employee instance.
        :param request:
        :param args:
        :param kwargs:
        :return: Return status as 200 if form is valid else it will return status as 400 if data is invalid.
        """

        form = self.form_class(request.POST)
        queryset = Employee.objects.filter(is_active=True).all()

        if form.is_valid():
            data = form.save(commit=False)
            data.save()

            messages.add_message(request, messages.SUCCESS, 'Data Added Successfully')
            return redirect('/')
        print(form.errors)
        return render(request, self.template_name,
                      {'form': form, 'record_list': queryset, 'ValidationError': form}, status=400)


class EmployeeUpdate(View):
    """
        This class will covers the update view of employee.
    """
    form_class = EmployeeForm
    template_name = 'app/edit_view.html'

    def get(self, request, pk):
        """
        Get employee data by pk.
        :param request:
        :param pk:
        :return: Return status as 200 if form is valid else it will return status as 400 if data is invalid.
        """

        emp_data = Employee.objects.filter(id=pk, is_active=True).first()
        if emp_data:
            return render(request, self.template_name, {'form': emp_data}, status=200)
        return render(request, self.template_name, status=400)

    def post(self, request, pk):
        """
        Update new employee instance.
        :param request:
        :param pk:
        :return: Return status as 200 if form is valid else it will return status as 400 if data is invalid.
        """
        form = self.form_class(request.POST)
        print(request.POST)
        first_name = form.data.get('firstName')
        last_name = form.data.get('lastName')
        email = form.data.get('email')
        age = form.data.get('age')
        queryset = Employee.objects.filter(is_active=True).all()

        if form.is_valid():
            Employee.objects.filter(id=pk).update(firstName=first_name, lastName=last_name, email=email, age=age)

            messages.add_message(request, messages.SUCCESS, 'Employee details Updated Successfully')
            return redirect('/')
        return render(request, self.template_name,
                      {'form': form.data, 'record_list': queryset, 'ValidationError': form}, status=400)


class EmployeeDelete(View):
    """
        This class will covers the delete view of users.
    """

    def get(self, request, pk):
        """
        This method will deactivate the passed user_id.
        :param request:
        :param pk: Instance pk
        :return: Return status as 200 if is_activate gets update successfully as False else it will
                return status as 400 if there is any
        """

        data = {}
        inactive_user = Employee.objects.filter(id=pk).update(is_active=False)
        if inactive_user:
            data['message'] = 1
        else:
            data['message'] = 0

        return JsonResponse(data)
