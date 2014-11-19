import httplib
import datetime


def exists(site, path):
    conn = httplib.HTTPConnection(site)
    conn.request('HEAD', path)
    response = conn.getresponse()
    conn.close()
    return response.status == 200

def get_img(date):
    site = "sohowww.nascom.nasa.gov"
    location = "/data/synoptic/sunspots/"
    # Pictures exist from 20011001 to 20110113 and from 20110307
    if date >= datetime.date(2011, 03, 07):
        fname = "sunspots_512_"+str(date).replace("-", "")+".jpg"
    else:
        fname = "sunspots_"+str(date).replace("-", "")+".jpg"
    if exists(site, location+fname):
        return "http://"+site+location+fname
    else:
        return None
