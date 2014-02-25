from google.appengine.ext import ndb
import webapp2


MAIN_PAGE_HTML = open('main.html').read()
HEAD_HTML = open('head.html').read()

class Data(ndb.Model):
  """Models an individual Data entry with content 1 and 2 and number and date."""
  taxesPaid = ndb.FloatProperty()
  pensions = ndb.FloatProperty()
  healthcare = ndb.FloatProperty()
  education = ndb.FloatProperty()
  defense = ndb.FloatProperty()
  welfare = ndb.FloatProperty()
  number = ndb.IntegerProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):

    def get(self):
        self.response.write('<html>')
        self.response.write(HEAD_HTML)
        self.response.write('<body id="body">')
        self.response.write(MAIN_PAGE_HTML)
        


class Comparison(webapp2.RequestHandler):

    def post(self):
        """this queries the old data, and then gets the new data, 
        calculates the average, posts that average back to the database,
        so that we can query the average the next time"""
        try:
            old_data = Data.query().order(-Data.date).fetch(1)
            old_taxesPaid = old_data[0].taxesPaid
            old_pensions = old_data[0].pensions
            old_healthcare = old_data[0].healthcare
            old_education = old_data[0].education
            old_defense = old_data[0].defense
            old_welfare = old_data[0].welfare
        except IndexError:
            #this is hopefully only for initialization purposes
            old_taxesPaid = 0.0
            old_pensions = 0.0 
            old_healthcare = 0.0 
            old_education = 0.0 
            old_defense = 0.0 
            old_welfare = 0.0    
        
        try:
            #try block, in case they don't input a float
            taxesPaid = float(self.request.get('taxesPaid'))
        except ValueError:
            taxesPaid = 0.0   
        try:        
            pensions = float(self.request.get('pensions'))
        except ValueError:
            pensions = 0.0            
        try:    
            healthcare = float(self.request.get('healthcare'))
        except ValueError:
            healthcare = 0.0     
        try:         
            education = float(self.request.get('education')) 
        except ValueError:
            education = 0.0    
        try:            
            defense = float(self.request.get('defense'))
        except ValueError:
            defense = 0.0     
        try:     
            welfare = float(self.request.get('welfare'))
        except ValueError:
            welfare = 0.0     


        try:
            num = old_data[0].number + 1 
        except (TypeError, IndexError):
            #this is hopefully only for initialization purposes
            num = 1
        try:
            avgTaxes = taxesPaid/num + old_taxesPaid*(num-1)/num
            avgPensions = pensions/num +old_pensions*(num-1)/num
            avgHealthcare = healthcare/num +old_healthcare*(num-1)/num
            avgEducation = education/num +old_education*(num-1)/num
            avgDefense = defense/num +old_defense*(num-1)/num
            avgWelfare = welfare/num +old_welfare*(num-1)/num
        except TypeError:
            avgTaxes = taxesPaid
            avgPensions = pensions
            avgHealthcare = healthcare
            avgEducation = education
            avgDefense = defense
            avgWelfare = welfare
            
                         
        new_data = Data(taxesPaid = avgTaxes, pensions = avgPensions, \
        healthcare = avgHealthcare, education = avgEducation, \
        defense = avgDefense, welfare = avgWelfare, number = num)
        new_data.put()
        
        """what you will notice below is a bunch of garbage code, 
        that should be taken care of doing templates... 
        I don't know how to do templates... 
        so that's why we have this garbage code"""
        self.response.write('<html>')
        self.response.write(HEAD_HTML)
        self.response.write('<body><p>Your taxes: </p><table><tr><td>taxesPaid</td><td>pensions</td><td>healtcare</td><td>education</td><td>defense</td><td>welfare</td></tr><tr><td>')
        self.response.write(taxesPaid)
        self.response.write('</td><td>')
        self.response.write(pensions)
        self.response.write('</td><td>')
        self.response.write(healthcare)
        self.response.write('</td><td>')
        self.response.write(education)
        self.response.write('</td><td>')
        self.response.write(defense)
        self.response.write('</td><td>')
        self.response.write(welfare)
        self.response.write('</td></tr></table>')   
        
        self.response.write('<p>What others have said (average):</p><table><tr><td>taxesPaid</td><td>pensions</td><td>healtcare</td><td>education</td><td>defense</td><td>welfare</td></tr><tr><td>')
        self.response.write(round(avgTaxes,2))
        self.response.write('</td><td>')
        self.response.write(round(avgPensions,2))
        self.response.write('</td><td>')
        self.response.write(round(avgHealthcare,2))
        self.response.write('</td><td>')
        self.response.write(round(avgEducation,2))
        self.response.write('</td><td>')
        self.response.write(round(avgDefense,2))
        self.response.write('</td><td>')
        self.response.write(round(avgWelfare,2))
        self.response.write('</td></tr></table>')
 
        self.response.write('</body></html>')



application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/compare', Comparison),
], debug=True)
