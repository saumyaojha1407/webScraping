import requests


class Requests:
    def __init__(self):
        self.request_method_mapping = {'GET': 'get',
                                       }
        self.force_timeout = None

    def make_request(self, method, base_url, url_slug, headers=None, data=None, body=None, query_parameter=None,
                     timeout=5, retries=1, proxies=None):
        if self.force_timeout:
            timeout = self.force_timeout
        response = getattr(self, self.request_method_mapping[method] + '_request')(base_url, url_slug, headers, data,
                                                                                   body, query_parameter, timeout,
                                                                                   retries, proxies)
        return response

    def get_request(self, base_url, url_slug, headers=None, data=None, body=None, query_parameter=None, timeout=None,
                    retries=1, proxies=None):
        url = base_url + url_slug
        requests_kwargs = {'url': url}
        if headers:
            requests_kwargs['headers'] = headers
        if query_parameter:
            requests_kwargs['params'] = query_parameter
        if body:
            requests_kwargs['json'] = body
        if timeout:
            requests_kwargs['timeout'] = timeout
        if proxies:
            requests_kwargs['proxies'] = proxies
        for _ in range(retries):
            try:
                response = requests.get(**requests_kwargs)
            except requests.exceptions.ConnectionError:
                pass
        return response
