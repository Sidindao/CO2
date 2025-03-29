import math
import json
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import requests

def haversine(lat1, lon1, lat2, lon2):
    """renvoie la distance a vol d'oiseau entre 2 points en km"""
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1

    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    R = 6371.0
    distance = R * c

    return round(distance, 4)

def fetch_distance_osrm(transport, lat1, lon1, lat2, lon2):
    """revoie la distance pour le mode de transport donné entre 2 adresses en km"""
    url = f"https://router.project-osrm.org/route/v1/{transport}/"\
        f"{lat1},{lon1};{lat2},{lon2}?overview=false"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "routes" in data and len(data["routes"]) > 0:
            return {transport: (data["routes"][0]["distance"]/1000)}
        print(f"Aucune route trouvée pour {transport}.")
        return None
    print(f"Erreur lors de la requête pour {transport}: {response.status_code}")
    return None

def osrm(lat1, lon1, lat2, lon2):
    """renvoie la distance entre 2 points, en km, 
        pour chaque mode de transport géré par OSRM"""
    transports = ["car", "bike", "foot"]
    final = {}

    with ThreadPoolExecutor() as executor:
        fetch_distance_partial = partial(fetch_distance_osrm, \
            lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2)
        results = list(executor.map(fetch_distance_partial, transports))

    for result in results:
        if result is not None:
            final.update(result)

    return final

def get_lat_long(address):
    """renvoie la latitude et la longitude d'une adresse donnée"""
    time.sleep(1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:134.0)'
    }
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=jsonv2"
    response = requests.get(url, headers=headers)
    if response and response.status_code == 200:
        data = response.json()
        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
    return None, None

def get_all_distances(lat1, long1, lat2, long2):
    """renvoie la distance pour chacun des modes de transports"""
    distances = osrm(lat1, long1, lat2, long2)
    distances.update({'plane':haversine(lat1, long1, lat2, long2)})
    return distances
