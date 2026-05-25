from django.forms import widgets


class ClearableFileInput(widgets.ClearableFileInput):
    template_name = 'blog/forms/widgets/clearable_file_input.html'
