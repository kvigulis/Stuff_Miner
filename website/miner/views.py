from django.views import generic
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView  # UpdateView for editing object.
from django.core.urlresolvers import reverse_lazy
from .models import Filter, Condition, Keyword, Result
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .script import API
import json

def send_filter(request):
    if request.is_ajax() and request.method == 'POST':
        data = request.POST.dict()
        filter_data = json.loads(data['filter_data_object'])
        keyword_data = json.loads(data['key_data_object'])

        for key, value in filter_data.items():
            print('key:',key)
            print('value:', value)

        for key, value in keyword_data.items():
            print('key:',key)
            print('value:', value)

        new_filter = Filter()
        new_filter.title = filter_data['title']
        new_filter.logo_url = filter_data['logo_url']
        new_filter.description = filter_data['description']
        new_filter.site = filter_data['site']
        new_filter.search_text = filter_data['search_text']
        new_filter.category = filter_data['category']
        if filter_data['min_p']:
            new_filter.min_price = float(filter_data['min_p'])
        if filter_data['max_p']:
            new_filter.max_price = float(filter_data['max_p'])

        new_filter.save()
        # Filter associated DataBase objects: conditions and keywords
        # Conditions
        cond_choice = {'cond_new': 'New', 'cond_new_other': 'New other',
                       'cond_manufacturer_refurbished': 'Manufacturer refurbished',
                       'cond_seller_refurbished': 'Seller refurbished',
                       'cond_used': 'Seller refurbished',
                       'cond_for_parts': 'For parts or not working',
                       'cond_not_specified': 'Not specified'}

        for cond_key, cond_value in cond_choice.items():  # Check if the condition was selected in the form, if true add to DB.
            if filter_data[cond_key]:
                condition = Condition()
                condition.filter = new_filter
                condition.true_condition = cond_value
                condition.save()

        for key, value in keyword_data.items():
            keyword = Keyword()
            keyword.filter = new_filter
            keyword.word = value[0]

            if value[1]=='Include':
                keyword.logic = True
            else:
                keyword.logic = False
            keyword.save()

        return render(request, 'miner/index.html', {'filter_list': Filter.objects.all()})
    else:
        raise Http404


def index(request):
    filter_list = Filter.objects.all()
    conditions_list = Condition.objects.all()
    template = loader.get_template('miner/index.html')
    context = {
        'filter_list': filter_list,
        'conditions_list': conditions_list
    }
    return HttpResponse(template.render(context, request))

class DetailView(generic.DetailView):
    """DetailView expects a primary key of a Filter object"""
    model = Filter
    template_name = 'miner/detail.html'

def create_filter(request):
    return render(request, 'miner/filter_form.html')

class FilterUpdate(UpdateView):
    model = Filter
    fields = ['title', 'logo_url', 'description', 'search_text', 'category',
              'condition', 'min_price', 'max_price', 'date_created']


class FilterDelete(DeleteView):
    model = Filter
    success_url = reverse_lazy('miner:index')



# TODO: finish result deletion feature in detail view
class ResultDelete(DeleteView):
    model = Result
    success_url = reverse_lazy('miner:detail')

def favorite_filter(request, filter_id):
    filter = get_object_or_404(Filter, pk=filter_id)
    try:
        if filter.is_favorite:
            filter.is_favorite = False
        else:
            filter.is_favorite = True
            filter.save()
    except (KeyError, Filter.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def run_script(request):
    if request.is_ajax() and request.method == 'POST':
        data = request.POST
        print(data['message'])
        API.run_search()


