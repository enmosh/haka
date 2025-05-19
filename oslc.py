import urllib.parse

class OSLCQueryBuilder:
    def __init__(self, base_url):
        self.base_url = base_url
        self.select_fields = []
        self.where_clauses = []
        self.prefixes = {}
        self.order_by = []
        self.page_size = None
        self.paging = None

    def select(self, *fields):
        self.select_fields.extend(fields)
        return self

    def where(self, clause):
        self.where_clauses.append(clause)
        return self

    def add_prefix(self, prefix, uri):
        self.prefixes[prefix] = uri
        return self

    def order(self, *fields):
        self.order_by.extend(fields)
        return self

    def set_page_size(self, size):
        self.page_size = size
        return self

    def enable_paging(self, enable=True):
        self.paging = enable
        return self

    def build(self):
        params = {}

        if self.select_fields:
            params['oslc.select'] = ','.join(self.select_fields)

        if self.where_clauses:
            params['oslc.where'] = ' and '.join(self.where_clauses)

        if self.prefixes:
            prefix_list = [f"{k}=<{v}>" for k, v in self.prefixes.items()]
            params['oslc.prefix'] = ','.join(prefix_list)

        if self.order_by:
            params['oslc.orderBy'] = ','.join(self.order_by)

        if self.page_size is not None:
            params['oslc.pageSize'] = str(self.page_size)

        if self.paging is not None:
            params['oslc.paging'] = 'true' if self.paging else 'false'

        query_string = urllib.parse.urlencode(params, safe=':<>,{}')
        return f"{self.base_url}?{query_string}"
        
        
        
        builder = OSLCQueryBuilder("https://example.com/oslc/query")

query_url = (
    builder
    .add_prefix("dcterms", "http://purl.org/dc/terms/")
    .select("dcterms:title", "dcterms:identifier")
    .where('dcterms:identifier="1234"')
    .order("+dcterms:title")
    .set_page_size(50)
    .enable_paging(True)
    .build()
)

print(query_url)
        
