import streamlit as st
import requests

from streamlit_autorefresh import st_autorefresh


count = st_autorefresh(interval=2000, limit=100, key="nowplaying_refresher")


server = "icecast.rocks"
protocol = "http"
port = 8000

status_json = f"{protocol}://{server}:{port}/status-json.xsl"

st.title(f"Radio Dashboard for {server}")

mountpoints = ["mobradio", "pandora"]


def get_status():
    res = requests.get(status_json)
    #st.write(res.json())
    return res.json()


def radio_dashbox(mountpoint):
    status = get_status()
    listenurl = f"{protocol}://{server}:{port}/{mountpoint}"
    
    # loop through until we find the matching mountpoint
    for source in status["icestats"]["source"]:
        if source["listenurl"] == listenurl:
            st.header(source["server_name"])
            st.audio(listenurl)
            if count %3 == 0:
                st.write(f"Now Playing: %s" % source["title"]) 
            else:
                st.write(f"Now Playing: %s" % source["title"])


for mnt in mountpoints:
    radio_dashbox(mnt)


### automatic reloading of page (and a button to manually refresh)

st.button("Re-run")


