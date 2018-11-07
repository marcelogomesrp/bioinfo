from django.core.urlresolvers import reverse
from django.views.generic.list_detail import object_list, object_detail
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from util.views import create_object
from forms import AddDepartmentForm, AddInstitutionForm
from models import Institution


def list_institutions(request):
    ''' List all institutions '''
    return object_list(request,
            template_name='institutions/list_institutions.html',
            queryset=Institution.objects.all()) 


def add_institution(request):
    ''' Form to add a new institution '''
    return create_object(request, 
            form_class=AddInstitutionForm, 
            template_name='institutions/add_institution.html',
            post_save_redirect=reverse('list_institutions'),
            message=_('Institution added'),
            login_required=True)


def view_institution(request, object_id):
    ''' View detailed info of the intitution '''
    return render_to_response('institutions/view_institution.html',
            {'object': get_object_or_404(Institution, pk=object_id)},
            context_instance=RequestContext(request))


def add_department(request):
    ''' Form to add a new department '''
    return create_object(request, 
            form_class=AddDepartmentForm, 
            template_name='institutions/add_department.html',
            post_save_redirect=reverse('list_institutions'),
            message=_('Department added'),
            login_required=True)