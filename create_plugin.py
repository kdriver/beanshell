"""This module queries space-track for a list of norad id's.

It generates beanshell script suitbal for use in NorssTrack plug-ins directory.
"""
##
##  Copyright Notice:
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  For full licencing terms, please refer to the GNU General Public License
##  (gpl-3_0.txt) distributed with this release, or see
##  http://www.gnu.org/licenses/.
##


import configparser
import json

import requests

import beanshell_template_text
import test_data


class MyError(Exception):
    """Generic excpetion handler."""
    def __init___(self, args):
        """Initialise the MyError class."""
        Exception.__init__(self, f"my exception was raised with arguments {args}")
        self.args = args



uriBase = "https://www.space-track.org"
requestLogin = "/ajaxauth/login"

requestFindStarlinks = "/class/tle_latest/NORAD_CAT_ID/>40000/ORDINAL/1/OBJECT_NAME/\
                        STARLINK~~/format/json/orderby/NORAD_CAT_ID%20asc"
#requestNoradId = "https://www.space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/61447/orderby/NORAD_CAT_ID%20asc/limit/1/"
requestNoradId = "https://www.space-track.org/basicspacedata/query/class/gp/NORAD_CAT_ID/{sat_list}/orderby/NORAD_CAT_ID%20asc/emptyresult/show"


# ACTION REQUIRED FOR YOU:
# =========================
# Provide a config file in the same directory as this file SLTrack.ini, with this format
# [configuration]
# username = XXX
# password = YYY
#

# Use configparser package to pull in the ini file (pip install configparser)
config = configparser.ConfigParser()
config.read("./SLTrack.ini")
configUsr = config.get("configuration", "username")
configPwd = config.get("configuration", "password")
configOut = config.get("configuration", "output")
siteCred = {"identity": configUsr, "password": configPwd}

online = True

def get_tles_from_spacetrack(ids: dict):
    """Funtion to query Space track with the list of NoradId."""
    if online:
        # use requests package to drive the RESTful session with space-track.org
        with requests.Session() as session:
            # run the session in a with block to force session to close if we exit

            # need to log in first. note that we get a 200 to say the web site got the
            # data not that we are logged in
            resp = session.post(uriBase + requestLogin, data=siteCred)
            if resp.status_code != 200:
                raise MyError(resp, "POST fail on login")
            else:
                print("Logged in OK ")

            # this query picks up all Starlink satellites from the catalog.
            # Note - a 401 failure shows you have bad credentials
            sat_list = ""
            first = True
            for norad_id in ids:
                sat_list = norad_id if first else sat_list + "," + norad_id
                first = False

            print(requestNoradId.format(sat_list=sat_list))
            resp = session.get(requestNoradId.format(sat_list=sat_list))
            if resp.status_code != 200:
                print(resp)
                raise MyError(resp, "GET fail on request ")

                # use the json package to break the json formatted response text into a
                # Python structure (a list of dictionaries)
            retData = json.loads(resp.text)
            session.close()
    else:
        print("Offline testing")
        retData = test_data.multi_response
    return retData

def create_bsh(st_data, satellites):
    """Create a beanshell script based on the retrieved TLE."""
    bean_shell = ""
    header_text = beanshell_template_text.imports_text
    body_text = ""
    for sat in st_data:
        ident = sat["NORAD_CAT_ID"]
        name = sat["OBJECT_NAME"]
        tle_1 = sat["TLE_LINE1"]
        tle_2 = sat["TLE_LINE2"]
        colour =  satellites[ident]["colour"]
        varName = satellites[ident]["var_name"]
        body_text = body_text + beanshell_template_text.sat_object.\
            format(varName=varName,sat_text=name,tle_line1=tle_1,tle_line2=tle_2,colour=colour) + "\n\n" #noqa

    bean_shell = header_text + body_text
    return bean_shell

skynet_colour = "Color.PINK"
luch_colour = "Color.RED"
sj_colour = "Color.YELLOW"
plug_in_sats = { "49044": { "var_name" : "iss_sat" ,  "colour" : "Color.GREEN"},
                 "55841": { "var_name" : "luch_sat" ,  "colour" : luch_colour},
                 "40258": { "var_name" : "luch_ol_sat" ,  "colour" : luch_colour},
                 "23426": { "var_name" : "luch_2__sat" ,  "colour" : luch_colour},
                 "41838": { "var_name" : "sj17_sat" ,  "colour" : sj_colour},
                 "55131": { "var_name" : "sj23_sat" ,  "colour" : sj_colour},
                 "30794": { "var_name" : "sn5a_sat", "colour" : skynet_colour},
                 "32294": { "var_name" : "sn5b_sat", "colour" : skynet_colour},
                 "33055": { "var_name" : "sn5c_sat", "colour" : skynet_colour},
                 "39034": { "var_name" : "sn5d_sat", "colour" : skynet_colour}
                 }

def main():
    """The main function."""
    retData = get_tles_from_spacetrack(plug_in_sats)
    beanshell = create_bsh(retData,plug_in_sats)
    with open("beanshell.bsh",mode="w") as bean:
        bean.write(beanshell)
        bean.close()
    print("wrote beanshell to beanshell.bsh")

if __name__ == "__main__":
    main()
