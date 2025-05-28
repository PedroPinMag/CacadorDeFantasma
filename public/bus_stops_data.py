# public/bus_stops_data.py

BUS_STOPS = [
    {'id': 'km50', 'name': 'Quilômetro 50', 'latitude': -22.740421473802673, 'longitude': -43.70627516559626},
    {'id': 'farm_uni', 'name': 'Farmácia Universitária', 'latitude': 22.742979254853402, 'longitude': -43.70376826621893},
    {'id': '2_pass', 'name': 'Segunda Passarela', 'latitude': -22.74691866559942, 'longitude': -43.69999918399076},
    {'id': '1_pass', 'name': 'Primeira Passarela', 'latitude': -22.746894659597366, 'longitude': -43.699913047944584},
    {'id': 'coq', 'name': 'Coqueiral', 'latitude': -22.749933492412648, 'longitude': -43.6971082161724},
    {'id': 'if-ext', 'name': 'IF - Instituto Florestal (PISTA)', 'latitude': -22.755775852364767, 'longitude':  -43.69176186381274},
    {'id': 'iv', 'name': 'IV - Instituto de Veterinária', 'latitude': -22.757411122176567, 'longitude': -43.69018305715937},
    {'id': 'port', 'name': 'Pórtico', 'latitude': -22.76140374243765, 'longitude': -43.68674425871395},
    {'id': 'ib', 'name': 'Instituto de Biologia', 'latitude': -22.76319810600015, 'longitude': -43.68990669237829},
    {'id': 'p1', 'name': 'P1 - Principal', 'latitude': -22.764379440574007, 'longitude': -43.689337375851416},
    {'id': 'biblio', 'name': 'Biblioteca Central', 'latitude': -22.765537600490703, 'longitude': -43.68760884757829},
    {'id': 'pit', 'name': 'Pitágoras', 'latitude': -22.766749522376124, 'longitude': -43.68599203493384},
    {'id': 'ichs', 'name': 'ICHS/PPG', 'latitude': -22.767293036209587, 'longitude': -43.685342951920624},
    {'id': 'pat', 'name': 'PAT- Pavilhão de Aulas Teóricas', 'latitude': -22.77046286109231, 'longitude': -43.68515401133775},
    {'id': 'esquina', 'name': 'Esquina do IZ', 'latitude': -22.77162468742067, 'longitude': -43.68780455486672},
    {'id': 'iz', 'name': 'IZ - Instituto de Zootecnia', 'latitude': -22.773138488058112, 'longitude': -43.68673549810623},
    {'id': 'it', 'name': 'IT -Instituto de Tecnologia', 'latitude': -22.775639930850144, 'longitude': -43.68614194557662},
    {'id': 'degeo', 'name': 'DEGEO - Instituto de Geociências', 'latitude': -22.780848273251607,  'longitude': -43.68290642662923},
    {'id': 'petro', 'name': 'Petrologia', 'latitude': -22.77905675497217, 'longitude': -43.679876203936594},
    {'id': 'p1-fund', 'name': 'Fundos P1', 'latitude': -22.765757667035814, 'longitude': -43.690271133128036},
    {'id': 'quadras', 'name': 'Quadras', 'latitude': -22.770370511979834, 'longitude': -43.68977339179137},
    {'id': 'hv', 'name': 'HV - Hospital Veterinário', 'latitude': -22.759083889010803, 'longitude': -43.69309363809877},
    {'id': 'ia', 'name': 'IA - Instituto de Agronomia', 'latitude': -22.759656740455764, 'longitude': -43.69654803914885},
    {'id': 'pu', 'name': 'PU - Prefeitura Universitária', 'latitude': -22.7727616281268, 'longitude': -43.6920277857371},
    {'id': 'if-int', 'name': 'IF - Instituto Florestal (INTERNO)', 'latitude': -22.75726272577619, 'longitude': -43.69679720802906},
    {'id': 'gin', 'name': 'Ginásio', 'latitude': -22.769543553571516, 'longitude': -43.6922721239717056},
    {'id': 'rod', 'name': 'Rodoviária Universitária', 'latitude': -22.766430637892352, 'longitude': -43.6900129279948},
    {'id': 'solos', 'name': 'Museu de solos', 'latitude': -22.764599742015392, 'longitude':  -43.69326743760037},
    {'id': 'herb', 'name': 'Herbário', 'latitude': -22.763684286494236, 'longitude': -43.695633777315585},

    # Add all other relevant UFRRJ bus stops here
    # Example: {'id': 'iv', 'name': 'IV - Instituto de Veterinária', 'latitude': ..., 'longitude': ...},
]

# Helper function to calculate distance (you'll need this later)
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance # in kilometers