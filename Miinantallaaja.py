import math
import csv
import random
import time
import haravasto

VOITTO = 1
TAPPIO = 0
PELI_KAYNNISSA = 1
PELI_SEIS = 0

tila = {
    "kentta": [],
    "hiiri_x" : 0,
    "hiiri_y" : 0,
    "avaamattomia_ruutuja": 0,
    "kentta_leveys" : 0,
    "kentta_korkeus": 0,
    "miina_lkm": 0,
    "tilakone": 0,
    "voitto_vai_tappio" : 0,
    "pelin_alkuaika": 0,
    "pelin_loppuaika": 0,
    "paivays": 0,
    "pelin_kesto": 0,
    "siirtojen_maara": 0,
    "kentan_koko": 0
}

hiiri = {
        "x": 0,
        "y": 0,
        "HIIRI_VASEN": "vasen",
        "HIIRI_KESKI": "keski",
        "HIIRI_OIKEA": "oikea"
        }

def valikko():
    del kentta[:]
    del tarkastettu [:]
    del miinan_koordinaatti [:]
    tila["siirtojen_maara"] = 0
    print("Miinantallaaja. Mitä haluat?:")
    print("(U)usi peli")
    print("(T)ilastot")
    print("(L)opeta")
    while True:
        valinta = input("Tee valintasi: ").strip().lower()
        if valinta == "u":
            kentan_tiedot()
            break
        elif valinta == "t":
            tilastot()
        elif valinta == "l":
            lopeta()

def kentan_tiedot():
    while True:
        try:
            tila["kentta_leveys"] = int(input("Anna kentän leveys (max 40): "))
            if tila["kentta_leveys"] < 3 or tila["kentta_leveys"] > 40:
                print("minimi leveys on 3 ja maksimi 40")
                raise ValueError
            tila["kentta_korkeus"] = int(input("Anna kentän korkeus (max 20): "))
            if tila["kentta_korkeus"] < 3 or tila["kentta_korkeus"] > 20:
                print("minimi korkeus on 3 ja maksimi 20")
                raise ValueError
            tila["kentan_koko"] = tila["kentta_leveys"] * tila["kentta_korkeus"]
            tila["miina_lkm"] = int(input("Anna miinojen määrä (Max. määrä on {})? "\
                                          .format(tila["kentan_koko"] -1)))
            if tila["miina_lkm"] < 1 or tila["miina_lkm"] >= tila["kentan_koko"]:
                print("Miinojen minimi on ja maksimi yksi vähemmän kuin ruutuja")
                raise ValueError
            break
        except ValueError:
            print("virhe")
    
def luo_kentat():
#Luo peliruudukon
    for i in range(tila["kentta_korkeus"]):
        kentta.append([])
        for j in range(tila["kentta_leveys"]):
            kentta[-1].append(" ")

    tila["kentta"] = kentta

def miinoita():
# Miinoittaa pelikentän
    i = 0
    while i < tila["miina_lkm"]:
        x = random.randint(0, tila["kentta_leveys"]-1)
        y = random.randint(0, tila["kentta_korkeus"]-1)
        if not tila["kentta"][y][x] == "x":
            tila["kentta"][y][x] = "x"
            i = i + 1
            miinan_koordinaatti.append((x, y))
        continue
    tila["avattavia_ruutuja"] = tila["kentta_leveys"] * tila["kentta_korkeus"] \
                                   - tila["miina_lkm"]

def laske_miinat():
# Laskee kentän miinat
    miina = 0
    for x in range(tila["kentta_leveys"]):
        for y in range(tila["kentta_korkeus"]):
            for yy in range(y-1, y+2):
                if yy < 0 or yy > (tila["kentta_korkeus"] -1):
                    continue
                for xx in range(x-1, x+2):
                    if xx < 0 or xx > (tila["kentta_leveys"] - 1):
                        continue
                    if kentta[yy][xx] == "x":
                        miina += 1
            if kentta[y][x] != "x" and miina > 0:
                kentta[y][x] = miina
            miina = 0

def tutki_ja_avaa_ruudut():
#tutkii ja avaa ruudut. tätä pitäisi parantaa. suorituskyky hyytyy pahasti isoilla ruudukoilla
    haravasto.aloita_ruutujen_piirto()
    tulva = []
    if kentta[tila["hiiri_y"]][tila["hiiri_x"]] == "x":
        miinan_koordinaatti.append((tila["hiiri_x"], tila["hiiri_y"]))
        tila["pelin_loppuaika"] = time.time()
        tila["voitto_vai_tappio"] = TAPPIO
        tila["tilakone"] = PELI_SEIS
        for x, y in miinan_koordinaatti:
            haravasto.lisaa_piirrettava_ruutu(kentta[y][x], x*40,\
                                          y*40)
    
    if kentta[tila["hiiri_y"]][tila["hiiri_x"]] == 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8:
        haravasto.lisaa_piirrettava_ruutu(kentta[tila["hiiri_y"]][tila["hiiri_x"]],\
                                           tila["hiiri_x"]*40, tila["hiiri_y"]*40)
        tarkastettu.append((tila["hiiri_x"], tila["hiiri_y"]))
        tila["avaamattomia_ruutuja"] -= 1
    
    if kentta[tila["hiiri_y"]][tila["hiiri_x"]] == " ":
        tulva.append((tila["hiiri_x"], tila["hiiri_y"]))
        while tulva:
            (x, y) = tulva.pop()
            if kentta[y][x] == " ":
                kentta[y][x] = 0
                haravasto.lisaa_piirrettava_ruutu(kentta[y][x],\
                            x*40, y*40)
                tarkastettu.append((x, y))
            for yy in range(y-1, y+2, 1):
                if yy < 0 or yy > (tila["kentta_korkeus"] -1):
                    continue
                for xx in range(x-1, x+2, 1):
                    if xx < 0 or xx > (tila["kentta_leveys"] - 1):
                        continue
                    if kentta[yy][xx] == " ":
                        tulva.append((xx, yy))
                        tarkastettu.append((xx, yy))
                    elif kentta[yy][xx] == 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8:
                        haravasto.lisaa_piirrettava_ruutu(kentta[yy][xx],\
                            xx*40, yy*40)
                        tarkastettu.append((xx, yy))

    if tila["avattavia_ruutuja"] == len(tarkasta_lista(tarkastettu)):
        tila["voitto_vai_tappio"] = VOITTO
        tila["pelin_loppuaika"] = time.time()
        tila["tilakone"] = PELI_SEIS
    haravasto.piirra_ruudut()

def tarkasta_lista(lista):
    return list(set(lista))

def piirra_kentta():
# Täyttää 
    haravasto.aloita_ruutujen_piirto()
    for rivi_nro, rivin_arvo in enumerate(kentta):
        for alkion_nro, alkion_sisalto in enumerate(rivin_arvo):
            haravasto.lisaa_piirrettava_ruutu(" ", alkion_nro * 40,\
                                                   rivi_nro * 40)
    haravasto.piirra_ruudut()

def tilastot():
   
    tiedoston_luku()

def tiedoston_tallennus():
    print("tallennus")

    if tila["voitto_vai_tappio"] == 1:
        tila["voitto_vai_tappio"] = str("VOITTO")
    else:
        tila["voitto_vai_tappio"] = str("TAPPIO")
    try:
        with open("tilastot.csv", "a") as kohde:
            writer = csv.writer(kohde)
            writer.writerow([tila["paivays"], tila["voitto_vai_tappio"],\
                             tila["pelin_kesto"], tila["kentan_koko"],\
                             tila["miina_lkm"],\
                             tila["siirtojen_maara"]])
    except IOError:
        print("Kohdetiedostoa ei voitu avata. Tallennus epäonnistui")

def tiedoston_luku():
    print("Päivämäärä\tTulos\tPeliaika\tKoko\tMiinat\tSiirrot")
    print()
    try:
        with open("tilastot.csv", newline="") as lahde:
            csvreader = csv.reader(lahde)
            for rivi in csvreader:

                print("\t".join(rivi))
    except IOError:
        print("Tiedoston lataaminen ei onnistunut")
  

def lopeta():
    
    tila["pelin_kesto"] = (tila["pelin_loppuaika"] - tila["pelin_alkuaika"])
    tila["pelin_kesto"] = time.strftime("%H:%M:%S", time.gmtime(tila["pelin_kesto"]))
    tiedoston_tallennus()
    haravasto.lopeta()
    main()

def kasittele_hiiri(x, y, nappi, muokkausnapit):
    
    if nappi == 1:
        tila["hiiri_x"] = math.ceil(x / 40) -1
        tila["hiiri_y"] = math.ceil(y / 40) -1
        haravasto.aseta_piirto_kasittelija(tutki_ja_avaa_ruudut)
    if tila["tilakone"] != PELI_KAYNNISSA:
        lopeta()
    else:
        tila["siirtojen_maara"] += 1

def main():
    valikko()
    luo_kentat() #
    miinoita()
    laske_miinat()
    haravasto.lataa_kuvat("/home/pi/Lataukset/spritet")
    haravasto.luo_ikkuna(tila["kentta_leveys"] * 40, tila["kentta_korkeus"] *40)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)    
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    tila["tilakone"] = PELI_KAYNNISSA
    tila["pelin_alkuaika"] = time.time()
    tila["paivays"] = time.strftime("%d, %b %Y %H:%M")
    haravasto.aloita()

if __name__ == "__main__":
    miinan_koordinaatti = []
    kentta = []
    tarkastettu = []
    main()
    
