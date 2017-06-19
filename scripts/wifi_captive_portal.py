import mechanize


def captive_portal(wifi_ssid, cp_username, cp_password):
    br = mechanize.Browser()

    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    
    if(wifi_ssid == "Google Starbucks"):
        if(cp_starbucks(br)):
            return True
    else:
        return False


def cp_starbucks(br):
    try:
        r = br.open('http://www.google.com')
        html = r.read()

        br.select_form(nr=0)

        br.submit()
        # print br.response().read()
        return True

    except:
        return False
