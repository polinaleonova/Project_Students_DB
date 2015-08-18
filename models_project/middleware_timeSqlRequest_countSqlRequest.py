import time

from django.db import connection


class SqlRequestParametersMiddleware(object):

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        content_type = response.get('content-type')
        if 'text/html' in content_type and response.status_code == 200:
            count_request = len(connection.queries)
            where_body = response.content.index('</body')
            first_part = response.content[:where_body]
            second_part = response.content[where_body:]
            time_spend = '{0:.4f}ms'.format(
                (time.time()-request.start_time)*1000
            )
            insert = '<span>Counts of SQL calls = {}. Processing of HTML ' \
                     'request taken {}.</span>'.format(count_request,
                                                       time_spend)
            response.content = first_part + insert + second_part
        return response
