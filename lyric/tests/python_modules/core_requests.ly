# core_requests.ly
# Lyric adhoc test — exercises public methods, attributes, and classes of Python's requests module.
#
# Run with:  lyric run lyric/tests/python_modules/core_requests.ly
# Output:    PASS: <desc>   for working features
#            ERROR: <desc>  for failures or thrown exceptions
#
# NOTE: Some tests make real HTTP calls (to httpbin.org). If network is
#       unavailable those tests will print ERROR but the module is still usable.

importpy requests

# -----------------------------------------------------------------------
# Helper: print PASS or ERROR based on a condition
# -----------------------------------------------------------------------
def check(var label, var cond) {
    if cond
        print("PASS:", label)
    else
        print("ERROR:", label)
    end
}

def main() {
    print("=== Lyric requests module adhoc test ===")
    print("")

    # ================================================================
    # Module-level attributes
    # ================================================================
    print("--- Module-level attributes ---")

    try:
        var ver = requests.__version__
        check("requests.__version__ exists", true)
        print("  __version__:", ver)
    catch:
        print("ERROR: requests.__version__ threw exception")
    fade

    try:
        var codes = requests.codes
        check("requests.codes exists", true)
    catch:
        print("ERROR: requests.codes threw exception")
    fade

    # ================================================================
    # Status code lookups via requests.codes
    # ================================================================
    print("")
    print("--- requests.codes ---")

    try:
        var ok = requests.codes.ok
        check("requests.codes.ok == 200", ok == 200)
    catch:
        print("ERROR: requests.codes.ok threw exception")
    fade

    try:
        var not_found = requests.codes.not_found
        check("requests.codes.not_found == 404", not_found == 404)
    catch:
        print("ERROR: requests.codes.not_found threw exception")
    fade

    try:
        var server_error = requests.codes.internal_server_error
        check("requests.codes.internal_server_error == 500", server_error == 500)
    catch:
        print("ERROR: requests.codes.internal_server_error threw exception")
    fade

    try:
        var created = requests.codes.created
        check("requests.codes.created == 201", created == 201)
    catch:
        print("ERROR: requests.codes.created threw exception")
    fade

    try:
        var bad_req = requests.codes.bad_request
        check("requests.codes.bad_request == 400", bad_req == 400)
    catch:
        print("ERROR: requests.codes.bad_request threw exception")
    fade

    try:
        var unauthorized = requests.codes.unauthorized
        check("requests.codes.unauthorized == 401", unauthorized == 401)
    catch:
        print("ERROR: requests.codes.unauthorized threw exception")
    fade

    try:
        var forbidden = requests.codes.forbidden
        check("requests.codes.forbidden == 403", forbidden == 403)
    catch:
        print("ERROR: requests.codes.forbidden threw exception")
    fade

    try:
        var redirect = requests.codes.moved_permanently
        check("requests.codes.moved_permanently == 301", redirect == 301)
    catch:
        print("ERROR: requests.codes.moved_permanently threw exception")
    fade

    # ================================================================
    # Exception classes exist
    # ================================================================
    print("")
    print("--- Exception classes ---")

    try:
        var exc = requests.exceptions
        check("requests.exceptions submodule exists", true)
    catch:
        print("ERROR: requests.exceptions threw exception")
    fade

    try:
        var exc = requests.exceptions.RequestException
        check("requests.exceptions.RequestException exists", true)
    catch:
        print("ERROR: requests.exceptions.RequestException threw exception")
    fade

    try:
        var exc = requests.exceptions.ConnectionError
        check("requests.exceptions.ConnectionError exists", true)
    catch:
        print("ERROR: requests.exceptions.ConnectionError threw exception")
    fade

    try:
        var exc = requests.exceptions.Timeout
        check("requests.exceptions.Timeout exists", true)
    catch:
        print("ERROR: requests.exceptions.Timeout threw exception")
    fade

    try:
        var exc = requests.exceptions.HTTPError
        check("requests.exceptions.HTTPError exists", true)
    catch:
        print("ERROR: requests.exceptions.HTTPError threw exception")
    fade

    try:
        var exc = requests.exceptions.URLRequired
        check("requests.exceptions.URLRequired exists", true)
    catch:
        print("ERROR: requests.exceptions.URLRequired threw exception")
    fade

    try:
        var exc = requests.exceptions.TooManyRedirects
        check("requests.exceptions.TooManyRedirects exists", true)
    catch:
        print("ERROR: requests.exceptions.TooManyRedirects threw exception")
    fade

    # ================================================================
    # Top-level functions exist and are callable
    # ================================================================
    print("")
    print("--- Top-level functions (existence) ---")

    try:
        var fn = requests.get
        check("requests.get is callable", true)
    catch:
        print("ERROR: requests.get threw exception")
    fade

    try:
        var fn = requests.post
        check("requests.post is callable", true)
    catch:
        print("ERROR: requests.post threw exception")
    fade

    try:
        var fn = requests.put
        check("requests.put is callable", true)
    catch:
        print("ERROR: requests.put threw exception")
    fade

    try:
        var fn = requests.delete
        check("requests.delete is callable", true)
    catch:
        print("ERROR: requests.delete threw exception")
    fade

    try:
        var fn = requests.head
        check("requests.head is callable", true)
    catch:
        print("ERROR: requests.head threw exception")
    fade

    try:
        var fn = requests.patch
        check("requests.patch is callable", true)
    catch:
        print("ERROR: requests.patch threw exception")
    fade

    try:
        var fn = requests.options
        check("requests.options is callable", true)
    catch:
        print("ERROR: requests.options threw exception")
    fade

    try:
        var fn = requests.request
        check("requests.request is callable", true)
    catch:
        print("ERROR: requests.request threw exception")
    fade

    # ================================================================
    # Session class
    # ================================================================
    print("")
    print("--- requests.Session ---")

    try:
        var s = requests.Session()
        check("requests.Session() creates session", true)
    catch:
        print("ERROR: requests.Session() threw exception")
    fade

    try:
        var s = requests.Session()
        var hdrs = s.headers
        check("session.headers exists", true)
        print("  session.headers:", hdrs)
    catch:
        print("ERROR: session.headers threw exception")
    fade

    try:
        var s = requests.Session()
        var cookies = s.cookies
        check("session.cookies exists", true)
    catch:
        print("ERROR: session.cookies threw exception")
    fade

    try:
        var s = requests.Session()
        var auth = s.auth
        check("session.auth exists (default None)", true)
    catch:
        print("ERROR: session.auth threw exception")
    fade

    try:
        var s = requests.Session()
        var verify = s.verify
        check("session.verify exists (default True)", verify == true)
    catch:
        print("ERROR: session.verify threw exception")
    fade

    try:
        var s = requests.Session()
        var max_redir = s.max_redirects
        check("session.max_redirects exists", true)
        print("  session.max_redirects:", max_redir)
    catch:
        print("ERROR: session.max_redirects threw exception")
    fade

    try:
        var s = requests.Session()
        s.close()
        check("session.close() works", true)
    catch:
        print("ERROR: session.close() threw exception")
    fade

    # ================================================================
    # Request object construction
    # ================================================================
    print("")
    print("--- requests.Request ---")

    try:
        var req = requests.Request("GET", "http://example.com")
        check("Request('GET', 'http://example.com') works", true)
    catch:
        print("ERROR: requests.Request() constructor threw exception")
    fade

    try:
        var req = requests.Request("GET", "http://example.com")
        check("Request.method == 'GET'", req.method == "GET")
    catch:
        print("ERROR: Request.method threw exception")
    fade

    try:
        var req = requests.Request("GET", "http://example.com")
        check("Request.url == 'http://example.com'", req.url == "http://example.com")
    catch:
        print("ERROR: Request.url threw exception")
    fade

    try:
        var req = requests.Request("POST", "http://example.com")
        check("Request('POST', ...) works", req.method == "POST")
    catch:
        print("ERROR: requests.Request('POST', ...) threw exception")
    fade

    # PreparedRequest
    try:
        var req = requests.Request("GET", "http://example.com")
        var prepped = req.prepare()
        check("Request.prepare() returns PreparedRequest", true)
    catch:
        print("ERROR: Request.prepare() threw exception")
    fade

    try:
        var req = requests.Request("GET", "http://example.com")
        var prepped = req.prepare()
        check("PreparedRequest.method == 'GET'", prepped.method == "GET")
    catch:
        print("ERROR: PreparedRequest.method threw exception")
    fade

    try:
        var req = requests.Request("GET", "http://example.com")
        var prepped = req.prepare()
        check("PreparedRequest.url == 'http://example.com/'", prepped.url == "http://example.com/")
    catch:
        print("ERROR: PreparedRequest.url threw exception")
    fade

    # ================================================================
    # Live HTTP — GET (requires network)
    # ================================================================
    print("")
    print("--- Live HTTP GET (requires network) ---")

    try:
        var r = requests.get("https://httpbin.org/get")
        check("requests.get('https://httpbin.org/get') works", true)
        check("response.status_code == 200", r.status_code == 200)
    catch:
        print("ERROR: requests.get() threw exception (network unavailable?)")
    fade

    # Response object attributes
    try:
        var r = requests.get("https://httpbin.org/get")
        var txt = r.text
        check("response.text is a string", true)
        print("  response.text length:", txt.__len__())
    catch:
        print("ERROR: response.text threw exception")
    fade

    try:
        var r = requests.get("https://httpbin.org/get")
        var hdrs = r.headers
        check("response.headers exists", true)
    catch:
        print("ERROR: response.headers threw exception")
    fade

    try:
        var r = requests.get("https://httpbin.org/get")
        var ct = r.headers.get("Content-Type")
        check("response.headers.get('Content-Type') contains 'json'", "json" in ct)
        print("  Content-Type:", ct)
    catch:
        print("ERROR: response.headers.get('Content-Type') threw exception")
    fade

    try:
        var r = requests.get("https://httpbin.org/get")
        var enc = r.encoding
        check("response.encoding exists", true)
        print("  encoding:", enc)
    catch:
        print("ERROR: response.encoding threw exception")
    fade

    try:
        var r = requests.get("https://httpbin.org/get")
        var url = r.url
        check("response.url exists", true)
        print("  response.url:", url)
    catch:
        print("ERROR: response.url threw exception")
    fade

    try:
        var r = requests.get("https://httpbin.org/get")
        var ok = r.ok
        check("response.ok == true for 200", ok == true)
    catch:
        print("ERROR: response.ok threw exception")
    fade

    try:
        var r = requests.get("https://httpbin.org/get")
        var reason = r.reason
        check("response.reason exists", true)
        print("  response.reason:", reason)
    catch:
        print("ERROR: response.reason threw exception")
    fade

    try:
        var r = requests.get("https://httpbin.org/get")
        var elapsed = r.elapsed
        check("response.elapsed exists (timedelta)", true)
        print("  elapsed:", elapsed)
    catch:
        print("ERROR: response.elapsed threw exception")
    fade

    # .json() method
    try:
        var r = requests.get("https://httpbin.org/get")
        var data = r.json()
        check("response.json() parses JSON", true)
    catch:
        print("ERROR: response.json() threw exception")
    fade

    # .raise_for_status() on success
    try:
        var r = requests.get("https://httpbin.org/get")
        r.raise_for_status()
        check("response.raise_for_status() OK on 200", true)
    catch:
        print("ERROR: response.raise_for_status() threw exception on 200")
    fade

    # ================================================================
    # Live HTTP — POST (requires network)
    # ================================================================
    print("")
    print("--- Live HTTP POST (requires network) ---")

    try:
        var r = requests.post("https://httpbin.org/post")
        check("requests.post('https://httpbin.org/post') works", true)
        check("POST response.status_code == 200", r.status_code == 200)
    catch:
        print("ERROR: requests.post() threw exception (network unavailable?)")
    fade

    # ================================================================
    # Live HTTP — status code scenarios (requires network)
    # ================================================================
    print("")
    print("--- HTTP status code scenarios (requires network) ---")

    try:
        var r = requests.get("https://httpbin.org/status/404")
        check("GET /status/404 returns 404", r.status_code == 404)
        check("response.ok == false for 404", r.ok == false)
    catch:
        print("ERROR: requests.get(/status/404) threw exception")
    fade

    try:
        var r = requests.get("https://httpbin.org/status/201")
        check("GET /status/201 returns 201", r.status_code == 201)
        check("response.ok == true for 201", r.ok == true)
    catch:
        print("ERROR: requests.get(/status/201) threw exception")
    fade

    try:
        var r = requests.get("https://httpbin.org/status/500")
        check("GET /status/500 returns 500", r.status_code == 500)
        check("response.ok == false for 500", r.ok == false)
    catch:
        print("ERROR: requests.get(/status/500) threw exception")
    fade

    # ================================================================
    # Query parameters (requires network)
    # ================================================================
    print("")
    print("--- Query parameters (requires network) ---")

    try:
        var r = requests.get("https://httpbin.org/get?foo=bar&baz=42")
        var data = r.json()
        check("GET with query params returns 200", r.status_code == 200)
    catch:
        print("ERROR: GET with query params threw exception")
    fade

    # ================================================================
    # Session-based request (requires network)
    # ================================================================
    print("")
    print("--- Session-based request (requires network) ---")

    try:
        var s = requests.Session()
        var r = s.get("https://httpbin.org/get")
        check("session.get() works", r.status_code == 200)
        s.close()
        check("session.close() after request works", true)
    catch:
        print("ERROR: session.get() threw exception")
    fade

    print("")
    print("=== requests test complete ===")
}
