from ebaysdk.finding import Connection as finding
from ..models import Filter, Condition, Keyword, Result
import datetime


def run_search():
    # TODO: [BUG] - ebay.com is not working...
    filters = list(Filter.objects.all())
    print('Filters: ', filters)
    site_choices = {'ebay.co.uk':'EBAY-GB','ebay.com':'EBAY-US'}
    for filter in filters:
        api = finding(siteid=site_choices[filter.site], appid='KarlisVi-Miner-PRD-15d80d3bd-1be698e3', config_file=None)

        condition_list = []
        cond_choices = {'New': '1000', 'New other': '1500',
                        'Manufacturer refurbished': '2000',
                        'Seller refurbished': '2500', 'Used': '3000',
                        'For parts or not working': '7000',
                        'Not specified': 'Not specified'}
        for condition in filter.condition_set.all():
            condition_list.append(cond_choices[condition.true_condition])

        for condition in condition_list:

            api.execute('findItemsAdvanced', {
                'keywords': filter.search_text,
                'categoryId': filter.category,
                'itemFilter': [
                    {'name': 'Condition', 'value': condition},
                    {'name': 'MinPrice', 'value': filter.min_price, 'paramName': 'Currency', 'paramValue': 'GBP'},
                    {'name': 'MaxPrice', 'value': filter.max_price, 'paramName': 'Currency', 'paramValue': 'GBP'}
                ],
                'paginationInput': {
                    'entriesPerPage': '100',
                    'pageNumber': 1
                },
                'sortOrder': 'CurrentPriceHighest'
            })

            dictstr = api.response.dict()
            pass
            if 'errorMessage' in dictstr.keys():
                print(dictstr['errorMessage'])
            else:
                total_pages = dictstr['paginationOutput']['totalPages']

                for page in range(int(total_pages)):
                    api.execute('findItemsAdvanced', {
                        'keywords': filter.search_text,
                        'categoryId': filter.category,
                        'itemFilter': [
                            {'name': 'Condition', 'value': condition},
                            {'name': 'MinPrice', 'value': filter.min_price, 'paramName': 'Currency',
                             'paramValue': 'GBP'},
                            {'name': 'MaxPrice', 'value': filter.max_price, 'paramName': 'Currency',
                             'paramValue': 'GBP'}
                        ],
                        'paginationInput': {
                            'entriesPerPage': '100',
                            'pageNumber': page + 1
                        },
                        'sortOrder': 'CurrentPriceHighest'
                    })

                    dictstr = api.response.dict()

                    print("======================")
                    print("======================")
                    print('Search for: ', filter.title)
                    if dictstr['searchResult']['item'][0]:
                        print('Condition: ', dictstr['searchResult']['item'][0]['condition']['conditionDisplayName'])
                    print(dictstr['paginationOutput'])

                    keyword_list = filter.keyword_set.all()
                    for item in dictstr['searchResult']['item']:

                        include_found = False
                        exclude_found = False
                        for keyword in keyword_list:
                            if not keyword.logic and item['title'].lower().count(keyword.word.lower()):
                                # exclusion word found break out of the loop
                                exclude_found = True
                                break

                            if keyword.logic and item['title'].lower().count(' '+keyword.word.lower()+' '):
                                include_found = True

                        # add result
                        if include_found and (not exclude_found):
                            # print('Item found! Titel: ', item['title'])
                            # print(item['sellingStatus']['currentPrice']['value'])
                            result = Result()
                            result.filter = filter
                            result.title = item['title']
                            result.url = item['viewItemURL']
                            result.image_url = item['galleryURL']
                            result.date_found = datetime.datetime.now()
                            result.price = item['sellingStatus']['currentPrice']['value']
                            result.is_favorite = False
                            result.save()



