import requests



STATUS_JSON_TEMPLATE = "{protocol}://{domain}:{port}/status-json.xsl"


def get_status(domain, port=8000, protocol="http"):
    res = requests.get(STATUS_JSON_TEMPLATE.format(protocol, domain, port))
    #st.write(res.json())
    return res.json()


class Station:
    """ Station encapsulates the properties belonging to an icecast stream running on a Host.

    Station objects can be learned about using Host.status() which will populate Host.stations
    as an iterable, so you can do this:

        host = icecast.Host("icecast.rocks")
        try:
            host.load()
        except Exception as err:
            print(err)
            return

        if host.ok:
            for station in host.stations:
                print(station.name)
                print(station.description)
                print(station.now_playing)

    Be aware that Icecast status does not guarantee that all fields exist for each station.

    Attribute defaults for the Station object are thus set to empty strings to grease
    the wheels of string interpolation (i.e. so you don't have to test for None in your 
    results display logic).
    """
    def __init__(self, **kwargs):
        self.listenurl = kwargs.get("listenurl")
        self.server_name = kwargs.get("server_name")
        self.mountpoint = self.listenurl.split("/")[2]

        # Now Playing
        self.title = kwargs.get("title", "")

        ## TODO Number of listeners


class Host:

    def __init__(self, domain, **kwargs):
        self.domain = domain
        self.port = kwargs.get("port", 8000)
        self.protocol = kwargs.get("protocol", "http")

        self.status = {}
        self.error = None

    @property
    def url(self):
        return self.protocol + "://" + self.domain + ":" + self.port

    @property
    def ok(self):
        if self.status and not self.error:
            return True
        return False

    def _load_status(self):
        try:
            self.status = get_status(self.domain, self.port, self.protocol)
        except Exception as err:
            self.error = err

    @property
    def status(self):
        "Returns cached Icecast host status. If latest status desired, use Host.refresh() first."
        if not self.status:
            self._load_status()
        return self.status

    def refresh(self):
        """Refreshes icecast Host status from the server (overwrite previous status, if set).

        No return; after using, read from Host.status (dict) or Host.stations (list).
        
        Errors (if any) will be stored in Host.error as Exception object.
        """
        self._load_status()

    @property
    def stations(self):
        "Returns a list of stations (if they exist), otherwise an empty list."
        out = []

        # Since .status is a magic @property, this `if` statement does a lot of work.
        if self.status:
            for source in status["icestats"]["source"]:
                out.append(Station(**source))

        return out

