from django.contrib.admin.filters import AllValuesFieldListFilter


# https://stackoverflow.com/questions/5429276/how-to-change-the-django-admin-filter-to-use-a-dropdown-instead-of-list/20900314#20900314
class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'
