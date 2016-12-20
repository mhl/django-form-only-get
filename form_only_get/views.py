from django.views.generic import FormView


class FormViewOnlyGET(FormView):

    '''Like FormView, but for when form submission can be with HTTP GET'''

    http_method_names = ['get']
    required_form_field = None

    def get_required_form_field(self):
        '''Get the field we'll use to tell if this is a form submission'''
        if self.required_form_field is not None:
            return self.required_form_field
        # If the developer hasn't picked a field, arbitrarily pick the
        # first field in the form.
        form_class = self.get_form_class()
        return list(form_class.base_fields)[0]

    def get_form_kwargs(self):
        kwargs = {
            'initial': self.get_initial(),
            'prefix': self.get_prefix(),
        }
        if self.get_required_form_field() in self.request.GET:
            kwargs['data'] = self.request.GET
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() not in self.http_method_names:
            return self.http_method_not_allowed(request, *args, **kwargs)
        if self.get_required_form_field() in request.GET:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.get(request, *args, **kwargs)
