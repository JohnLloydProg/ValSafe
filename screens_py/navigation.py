from kivy.uix.screenmanager import Screen
from kivy_garden.mapview import MapMarker
from kivy.app import App
from kivy.utils import platform
if platform == 'android' or platform == 'ios':
    from plyer import gps
from kivy.clock import Clock
from math import cos, asin, sqrt
from kivy.graphics import Color, Line
from time import sleep
import requests
import re

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(hav))

def closest(data, v):
    return min(data, key=lambda p: distance(v[0],v[1],p[0],p[1]))

class NavigationScreen(Screen):
    background_color = [1, 87/255, 87/255, 1]
    font_color = [50/255, 50/255, 50/255, 1]
    locations = {
        'Arkong Bato - San Diego Elementary': (14.699043322535008, 120.94922288217826), 
        'Arkong Bato - Barangay Hall': (14.696867656888271, 120.95466879782558), 
        'Arkong Bato - National High School': (14.700264519111334, 120.95034382360193), 
        'Arkong Bato - Chapel': (14.698215242932411, 120.95038134897035),
        'Balangkas - Deato Elementary': (14.71166254034055, 120.94245520337438), 
        'Balangkas - Gospel Church': (14.714952016004425, 120.93907561997531), 
        'Balangkas - Multipurpose Hall': (14.711518641053887, 120.94289178384459), 
        'Bignay - Multipurpose Hall': (14.744453112217208, 120.9912405626815), 
        'Bignay - CNAI Court': (14.736797957291305, 121.00466421337313), 
        'Bignay - National High School': (14.745053095370386, 121.00288887038234), 
        'Bignay - Elementary School': (14.747795241540834, 120.99737834401238), 
        'Bisig - Barangay Hall': (14.711166536725518, 120.94712576868636), 
        'Canumay East - National High School': (14.719540408613659, 120.9937751325149), 
        'Canumay East - Multipurpose Hall': (14.718710937584662, 120.9911968588225), 
        'Canumay West - Elementary School': (14.712531070027172, 120.98958250862195),
        'Canumay West - National High School': (14.71141552795924, 120.98943230490181), 
        'Coloong - Elementary School': (14.725267866003335, 120.94503974200394), 
        'Coloong - Barangay Hall': (14.72459349008547, 120.94367508433272), 
        'Dalandanan - National High School': (14.70882565733933, 120.95709164200383), 
        'Dalandanan - Elementary School': (14.704695818982149, 120.96433292851071),
        'Isla - Elementary School': (14.706555415385319, 120.94987174536435), 
        'Isla - Barangay Hall': (14.706319180385998, 120.95007594713822), 
        'Lawang Bato - National High School': (14.732666211883458, 120.99156255549707), 
        'Lawang Bato - Elementary School': (14.732666211883458, 120.99156255549707), 
        'Lawang Bato - Arty Court': (14.724646307803765, 120.98627688179204), 
        'Lingunan - Barangay Hall': (14.719168228112428, 120.97626761373573), 
        'Lingunan - Elementary School': (14.720273403691404, 120.97585360339534), 
        'Mabolo - Barangay Hall': (14.710766422929629, 120.94869108783666), 
        'Malanday - Fernando Elementary': (14.71709356889198, 120.95559311686222), 
        'Malinta - National High School': (14.691976338422243, 120.96681022666117), 
        'Malinta - St. Jude Court': (14.688522061178235, 120.96449576970876), 
        'Malinta - Pinalagad Elementary': (14.666509807894988, 120.95810796059641), 
        'Palasan - Barangay Hall': (14.704154118289958, 120.94755990188916),
        'Pariancillo Villa - Barangay Hall': (14.707313494802708, 120.94451871316828), 
        'Pariancillo Villa - Basketball Court': (14.706416004795694, 120.94387729782561), 
        'Pasolo - Elementary School': (14.706062518201657, 120.954451082483), 
        'Poblacion - Barangay Hall': (14.708936363559694, 120.94651161154533), 
        'Punturin - Elementary School':   (14.74014647446837, 120.99077311316839), 
        'Punturin - Santa Lucia Covered Court': (14.735870497340885, 120.99111332481189), 
        'Rincon - Elementary School': (14.700012587638493, 120.95998796898996), 
        'Rincon - Barangay Hall': (14.699985276715006, 120.96038400884783), 
        'Tagalag - Barangay Hall': (14.727506242566655, 120.93777268706562), 
        'Tagalag - Elementary School': (14.724809201810668, 120.9380491689901), 
        'Veinte Reales - Risen Lord Parish': (14.70972436534728, 120.96162824015424), 
        'Veinte Reales - Tugatog Elementary': (14.723895967179626, 120.96687704385354), 
        'Veinte Reales - Barangay Hall': (14.71416835250886, 120.96663885364734), 
        'Veinte Reales - LFS Chapel': (14.721084106244977, 120.96614481316848), 
        'Wawang Pulo - Barangay Hall': (14.733674337333825, 120.927776321685), 
        'Wawang Pulo - Elementary School': (14.733203518025816, 120.92803116382143), 
        'Wawang Pulo - National High School': (14.733426505981452, 120.92839095707494), 
        'Bagbaguin - A. Mariano Elementary School': (14.714223829449038, 120.99995071131873), 
        'Bagbaguin - Barangay Hall': (14.718210127197045, 121.00449939892167), 
        'Bagbaguin - National High School': (14.708260844224645, 121.00356461131867), 
        'Gen. T De Leon - National High School': (14.6877726779573, 120.99963413941293), 
        'Gen. T De Leon - Elementary School': (14.68596765865478, 120.99290532875274), 
        'Gen. T De Leon - De Guzman Elementary': (14.682760825173998, 120.98901983290729), 
        'Karuhatan - St. Joseph Academy': (14.68958030921169, 120.97300628248293), 
        'Mapulang Lupa - Apolonia Elementary School': (14.70187279487994, 121.00026836224326), 
        'Mapulang Lupa - National High School': (14.702905945305277, 121.0098039983943),
        'Mapulang Lupa - Barangay Hall': (14.70264166292847, 121.00149150097877), 
        'Mapulang Lupa - Covered Court': (14.702792672930409, 121.00159945310142), 
        'Marulas - Valenzuela National High School': (14.672726953051956, 120.98532318563605), 
        'Marulas - Constantino Elementary School': (14.67796130649917, 120.98873999173072), 
        'Marulas - San Miguel Elementary': (14.676705543890069, 120.99152669118462), 
        'Marulas - Serrano Elementary School': (14.68122423938457, 120.98252192666111), 
        'Marulas - Elementary School': (14.67598224461125, 120.98547990892288), 
        'Maysan - Barangay Hall': (14.697823667228855, 120.9800250414578), 
        'Maysan - High School Annex': (14.702171918480134, 120.98121754145787), 
        'Maysan - Elementary School': (14.699800565495485, 120.98012850892303), 
        'Maysan - Annville Court': (14.702345893959064, 120.96992215721247), 
        'Parada - Elementary School': (14.69839458872225, 120.98808647823788), 
        'Paso de Blas - Barangay Hall': (14.70789211248982, 120.99275586729662), 
        'Ugong - Lazaro Elementary School': (14.695416077361145, 121.01162123578494), 
        'Ugong - St. Therese Chapel': (14.689064097491155, 121.01099433019516), 
        'Ugong - Words of Wisdom Christian Academy': (14.69082265170658, 121.0064548604995), 
        'Ugong - San Juan dela Cruz Parish': (14.690791517425689, 121.00642267399256)
    }
    list_of_lines = []
    current_location = None
    path = []
    destination = None
    pin = None
    marker = None
    i = 0

    def on_enter(self, *args):
        self.app = App.get_running_app()
        locations = self.ids['evacuation_sites']
        locations.values = self.locations.keys()
        kmap = self.ids['map']
        if platform == 'android' or platform == 'ios':
            gps.configure(on_location=self.on_gps_location, on_status=self.on_gps_status)
            gps.start(minTime=0.3, minDistance=10)
            while not self.current_location:
                sleep(0.5)
            self.marker_update = Clock.schedule_interval(self.update_marker, 0.1)
            kmap.center_on(self.current_location[0], self.current_location[1])
        if self.app.emergency_mode:
            if platform == 'android':
                while not self.current_location:
                    sleep(0.5)
                self.destination = closest(self.locations.values(), self.current_location)
                self.set_location()
                self.track()
        return super().on_enter(*args)
    
    def on_leave(self, *args):
        if platform == 'android':
            if self.list_of_lines:
                for j in range(1, len(self.path), 1):
                    self.canvas.remove(self.list_of_lines[j-1])
                self.list_of_lines.clear()
                self.path.clear()
            gps.stop()
        return super().on_leave(*args)

    def on_gps_location(self, **kwargs):
        self.current_location = (kwargs['lat'], kwargs['lon'])
    
    def update_marker(self, *args):
        if self.current_location:
            kmap = self.ids['map']
            if self.marker:
                kmap.remove_widget(self.marker)
            self.marker = MapMarker(lat=self.current_location[0], lon=self.current_location[1], source='./images/location.png')
            kmap.add_widget(self.marker)
            if self.list_of_lines:
                for j in range(1, len(self.path), 1):
                    self.list_of_lines[j-1].points = [self.path[j-1].pos[0],self.path[j-1].pos[1], self.path[j].pos[0], self.path[j].pos[1]]
        
    def on_gps_status(self, **kwargs):
        pass

    def location_selected(self, spinner):
        self.destination = self.locations[spinner.text]
        if self.list_of_lines:
            for j in range(1, len(self.path), 1):
                self.canvas.remove(self.list_of_lines[j-1])
            self.list_of_lines.clear()
            self.path.clear()
        self.set_location()
    
    def set_location(self):
        kmap = self.ids['map']
        kmap.center_on(self.destination[0], self.destination[1])
        if self.pin:
            kmap.remove_widget(self.pin)
        self.pin = MapMarker(lat=self.destination[0], lon=self.destination[1], source='./images/location-tick.png')
        kmap.add_widget(self.pin)
        
    
    def track(self):
        if self.destination and not self.path:
            self.body = {"coordinates":[[self.current_location[1],self.current_location[0]],[self.destination[1], self.destination[0]]]}
            self.headers = {
                'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
                'Authorization': '5b3ce3597851110001cf6248e32f3f787ba541e8b3d916f4681b9340',
                'Content-Type': 'application/json; charset=utf-8'
                }
            self.call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car/gpx', json=self.body, headers=self.headers)
            self.string_res = self.call.text
            self.tag = 'rtept'
            self.reg_str = '</' + self.tag + '>(.*?)' + '>'
            self.res = re.findall(self.reg_str, self.string_res)
            self.string1 = str(self.res)
            self.tag1 = '"'
            self.reg_str1 = '"' + '(.*?)' + '"'
            self.res1 = re.findall(self.reg_str1, self.string1)
            for i in range(0, len(self.res1)-1, 2):
                lat = float(self.res1[i])
                lon = float(self.res1[i+1])
                marker = MapMarker(lat=lat, lon=lon, source='./images/waypoints.png')
                self.ids['map'].add_widget(marker)
                self.path.append(marker)
            with self.canvas:
                Color(0, 0, 0 ,1)
                for j in range(0, len(self.path)-1, 1):
                    print((self.path[j].pos[0],self.path[j].pos[1], self.path[j+1].pos[0],self.path[j+1].pos[1] ))
                    self.lines = Line(points=(self.path[j].pos[0],self.path[j].pos[1], self.path[j+1].pos[0],self.path[j+1].pos[1] ), width=3)
                    self.list_of_lines.append(self.lines)
