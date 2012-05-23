GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmaps_img(points):
    marker = '&'.join('markers=%s,%s' % (a.lat, a.lon) for a in points)
    return GMAPS_URL + marker

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required =True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty()

class AsciiChanHandler(Handler):
#    art_key=""
    def render_front(self, title="", art="", error=""):

        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 10")#, art_key)

        arts=list(arts)

        points = filter(None, (a.coords for a in arts))

        img_url=None

        if points:
            img_url=gmaps_img(points)

        self.render("asciichansubmit.html",title=title, art=art, error=error, arts=arts, img_url=img_url)

    def get(self):
        #self.write(repr(get_coords(self.request.remote_addr)))
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art=self.request.get("art")

        if title and art:
            a=Art( title = title, art = art)##parent= art_key,
            coords = get_coords(self.request.remote_addr)
            if coords:
                a.coords = coords
            a.put()

            self.redirect("/asciichan")
        else:
            error ="we need both a title adn some artwork!"
            self.render_front(title, art , error)