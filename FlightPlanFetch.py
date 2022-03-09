import json, urllib.request
import PySimpleGUI as sg

class SIMBRIEF(object):
    def __init__(self,username):
        self.username = username
        self.fpData = {}
        self.flightnumber = ''
        self.aircraft = ''
        self.depArr = ''
        self.rnw = ''
        self.altitude = ''
        self.ci = ''
        self.blockFuel = ''
        self.route = ''
        self.depMetar = ''
        self.arrMetar = ''

    def set_username(self,username:str):
        self.username = username

    def get_username(self):
        return self.username


    def fetchFlightPlan(self):
            with urllib.request.urlopen(f'https://www.simbrief.com/api/xml.fetcher.php?username={self.username}&json=1') as data:
                self.fpData = json.load(data)

    def get_flightPlan_key(self,key:str)->dict:
        '''Returns a dictionary using the provided key from the imported Flight Plan'''
        return self.fpData[key]

    def get_fpData(self):
        return self.fpData

    def generate_brief(self)->None:
        '''Generates and sets the briefing information'''

        #Creates smaller Dicts for localised data
        general = self.get_flightPlan_key('general')
        aircraft = self.get_flightPlan_key('aircraft')
        origin = self.get_flightPlan_key('origin')
        destination = self.get_flightPlan_key('destination')
        weather = self.get_flightPlan_key('weather')
        fuel = self.get_flightPlan_key('fuel')
        
        #-----------FLIGHT BRIEF------------
        self.flightnumber = general["icao_airline"] + general["flight_number"]
        self.aircraft = aircraft["icaocode"]
        self.depArr = origin["icao_code"] + '/' + destination["icao_code"]
        self.rwy = origin["plan_rwy"] + '/' + destination["plan_rwy"]
        self.altitude = general["initial_altitude"]
        self.ci = general["costindex"]
        self.blockFuel = fuel["plan_ramp"]
        #------------ROUTE------------
        route = general["route"].split()
        newRoute = route
        
        try:
            for x in range(0,len(route),12):
                newRoute.insert(x, '\n')
            self.route = ' '.join(newRoute)
        except:
            self.route = general["route"]
        

        #------------WEATHER------------
        self.depMetar = weather["orig_metar"]
        self.arrMetar = weather["dest_metar"]

    def get_flightNumber(self):
        return self.flightnumber
    
    def get_aircraft(self):
        return self.aircraft

    def get_depArr(self):
        return self.depArr

    def get_rwy(self):
        return self.rwy

    def get_altitude(self):
        return self.altitude

    def get_ci(self):
        return self.ci

    def get_blockFuel(self):
        return self.blockFuel

    def get_route(self):
        return self.route

    def get_depMetar(self):
        return self.depMetar

    def get_arrMetar(self):
        return self.arrMetar
  

sg.theme('Dark Grey 10')

myLayout = [
    [sg.Text("SIMBRIEF USERNAME:"), sg.Input(key='-INPUT-')],
    [sg.Button("Search")],
    [sg.Text(key='-StatusLabel-',size=(12,1)), sg.Text(key='-Status-')],
    [sg.Text(key='-FlightNumberLabel-',size=(12,1)),sg.Text(key='-FlightNumber-')],
    [sg.Text(key='-AircraftLabel-',size=(12,1)),sg.Text(key='-Aircraft-')],
    [sg.Text(key='-Dep/ArrLabel-',size=(12,1)),sg.Text(key='-Dep/Arr-')],
    [sg.Text(key='-RwyLabel-',size=(12,1)),sg.Text(key='-Rwy-')],
    [sg.Text(key='-AltitudeLabel-',size=(12,1)),sg.Text(key='-Altitude-')],
    [sg.Text(key='-CiLabel-',size=(12,1)),  sg.Text(key='-Ci-',size=(40,None))],
    [sg.Text(key='-BlockFuelLabel-',size=(12,1)),sg.Text(key='-BlockFuel-')],
    [sg.Text(key='-RouteLabel-',size=(12,1)),sg.Text(key='-Route-')],
    [sg.Text(key='-DepMetarLabel-',size=(12,1)),sg.Text(key='-DepMetar-')],
    [sg.Text(key='-ArrMetarLabel-',size=(12,1)),sg.Text(key='-ArrMetar-')]

]
sg.theme('Dark Grey 10')


window  = sg.Window(title="FPF - Discord CBRadi0#0001",layout=myLayout)


while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    try:
        #Initiate Class
        FlightPlan = SIMBRIEF(values['-INPUT-'])
        FlightPlan.fetchFlightPlan()
        FlightPlan.generate_brief()
        #Populate Text Boxes Once Connected
        window['-StatusLabel-'].update(f'Connection:',text_color='white')
        
        window['-Status-'].update("CONNECTED",text_color='green')
        
        window['-FlightNumberLabel-'].update(f'Flight Number:',text_color='white')
        
        window['-FlightNumber-'].update(f'{FlightPlan.get_flightNumber()}',text_color='white')

        window['-AircraftLabel-'].update(f'Aircraft:',text_color='white')
        
        window['-Aircraft-'].update(f'{FlightPlan.get_aircraft()}',text_color='white')

        window['-Dep/ArrLabel-'].update(f'Dep/Arr:',text_color='white')
        
        window['-Dep/Arr-'].update(f'{FlightPlan.get_depArr()}',text_color='white')

        window['-RwyLabel-'].update(f'Dep/Arr Rwy:',text_color='white')
        
        window['-Rwy-'].update(f'{FlightPlan.get_rwy()}',text_color='white')

        window['-AltitudeLabel-'].update(f'Flight Level:',text_color='white')
        
        window['-Altitude-'].update(f'{FlightPlan.get_altitude()}',text_color='white')

        window['-CiLabel-'].update(f'Cost Index:',text_color='white')
        
        window['-Ci-'].update(f'{FlightPlan.get_ci()}',text_color='white')

        window['-BlockFuelLabel-'].update(f'Block Fuel:',text_color='white')
        
        window['-BlockFuel-'].update(f'{FlightPlan.get_blockFuel()}',text_color='white')

        window['-RouteLabel-'].update(f'Route:',text_color='white')
        
        window['-Route-'].update(f'{FlightPlan.get_route()}',text_color='white')

        window['-DepMetarLabel-'].update(f'Dep Metar:',text_color='white')
        
        window['-DepMetar-'].update(f'{FlightPlan.get_depMetar()}',text_color='orange')

        window['-ArrMetarLabel-'].update(f'Arr Metar:',text_color='white')
        
        window['-ArrMetar-'].update(f'{FlightPlan.get_arrMetar()}',text_color='orange')
        
        
        
    except:
        window['-StatusLabel-'].update(f'Connection:',text_color='white')
        window['-Status-'].update('USERNAME NOT FOUND',text_color='orange')
        window['-FlightNumberLabel-'].update(f'Flight Number:',text_color='white')
        
        window['-FlightNumber-'].update(f'',text_color='white')
        window['-AircraftLabel-'].update(f'Aircraft:',text_color='white')
        window['-Aircraft-'].update(f'',text_color='white')
        window['-Dep/ArrLabel-'].update(f'Dep/Arr:',text_color='white')
        window['-Dep/Arr-'].update(f'',text_color='white')
        window['-RwyLabel-'].update(f'Dep/Arr Rwy:',text_color='white')
        window['-Rwy-'].update(f'',text_color='white')
        window['-AltitudeLabel-'].update(f'Flight Level:',text_color='white')
        window['-Altitude-'].update(f'',text_color='white')
        window['-CiLabel-'].update(f'Cost Index:',text_color='white')
        window['-Ci-'].update(f'',text_color='white')
        window['-BlockFuelLabel-'].update(f'Block Fuel:',text_color='white')        
        window['-BlockFuel-'].update(f'',text_color='white')
        window['-RouteLabel-'].update(f'Route:',text_color='white')        
        window['-Route-'].update(f'',text_color='white')
        window['-DepMetarLabel-'].update(f'Dep Metar:',text_color='white')     
        window['-DepMetar-'].update(f'',text_color='orange')
        window['-ArrMetarLabel-'].update(f'Arr Metar:',text_color='white')
        window['-ArrMetar-'].update(f'',text_color='orange')
        
#window.close()