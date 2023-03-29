import math
from numpy import pi, sin, cos,sqrt
import numpy as np

# conversion units wgs82-> puwg1992
# y,x = wgs84_to_puwg92(lattitude,longitude)



def wgs84_to_puwg92(B, L):
    # Obliczenie na podstawie
    # http://www.asgeupos.pl/webpg/graph/img/_news/00051/w4p.pdf

    # B - szerokość geodezyjna (Y)
    # L - długość geodezyjna (X)

    # Zmienne pomocnicze

    L0 = 19
    m0 = 0.9993
    PI = 3.141592653589790
    R0 = 6367449.14577

    eMimosrod = 0.081819191042800
    Bradians = math.radians(B)
    lam = L

    # wyliczenie fi

    fiRad = 2 * (math.atan(
        pow((1 - eMimosrod * math.sin(Bradians)) / (1 + eMimosrod * math.sin(Bradians)), eMimosrod / 2) * math.tan(
            Bradians / 2 + PI / 4)) - PI / 4)

    # Sfera na plaszczyzne Lamberta (Mercatora)

    lamRad = math.radians(lam)
    L0Rad = math.radians(L0)
    Xmer = math.atan(math.sin(fiRad) / (math.cos(fiRad) * math.cos(lamRad - L0Rad)))
    Ymer = 0.5 * math.log(
        (1 + math.cos(fiRad) * math.sin(lamRad - L0Rad)) / (1 - math.cos(fiRad) * math.sin(lamRad - L0Rad)))

    # Lambert (Mercator) rzutowany na Gaussa-Kruegera
    # Wspolczynniki W

    a2 = 0.0008377318247344
    a4 = 0.000000760852779
    a6 = 0.000000001197638
    a8 = 0.000000000002443

    Xgk = R0 * (Xmer + (a2 * math.sin(2 * Xmer) * math.cosh(2 * Ymer)) + (
                a4 * math.sin(4 * Xmer) * math.cosh(4 * Ymer)) + (a6 * math.sin(6 * Xmer) * math.cosh(6 * Ymer)) + (
                            a8 * math.sin((8 * Xmer) * math.cosh(8 * Ymer))))
    Ygk = R0 * (Ymer + (a2 * math.cos(2 * Xmer) * math.sinh(2 * Ymer)) + (
                a4 * math.cos(4 * Xmer) * math.sinh(4 * Ymer)) + (a6 * math.cos(6 * Xmer) * math.sinh(6 * Ymer)) + (
                            a8 * math.cos((8 * Xmer) * math.sinh(8 * Ymer))))

    xPuwg = m0 * Xgk - 5300000
    yPuwg = m0 * Ygk + 500000

    return yPuwg, xPuwg

# obliczenie przemieszczenia w NED po wcześniejszej zamianie jednostek wgs84-> puwg1992

def WGStoNEDfunc(tab_lat, tab_lon, tab_alt, struct, meas_number):
    X = []
    Y = []
    H = np.array(tab_alt)

    for i in range(len(tab_lat)):
        y, x = wgs84_to_puwg92(tab_lat[i], tab_lon[i])
        X.append(x)
        Y.append(y)
    X = np.array(X)
    Y = np.array(Y)

    if meas_number == 0:
        # usredniona pozycja
        struct.X0 = np.mean(X)
        struct.Y0 = np.mean(Y)
        struct.H0 = np.mean(H)

        # pozycja względna do bazowej
        X = X - X
        Y = Y - Y
        H = H - H

    else:
        # odległość od bazy
        X = np.array(X) - struct.X0
        Y = np.array(Y) - struct.Y0
        H = np.array(H) - struct.H0

    # usredniona odleglosc xyz od bazy
    struct.OUTPUT['X'] = [np.mean(X)]
    struct.OUTPUT['Y'] = [np.mean(Y)]
    struct.OUTPUT['H'] = [np.mean(H)]

    return X,Y,H

def get_angles(X,Y,H,object, meas_number):
    # x na osi pionowej , y na poziomej !
    n = len(X)

    psi = []
    theta = []
    dist2D = []
    dist3D = []
    for i in range(1, n):
        dH = H[i]
        dist = np.sqrt((X[i])**2 + (Y[i])**2)

        dist2D.append(round(dist,3))
        dist3D.append(round(np.sqrt((X[i])**2 + (Y[i])**2 +
                                    (H[i])**2),3))
        theta.append(round(math.atan(dH/dist)*180/np.pi,3))
        psi_ = math.atan2((Y[i]), (X[i]))
        if psi_ < 0:
            psi_ += 2*np.pi
        psi.append(round(psi_*180/np.pi,3))

    if meas_number == 0:
        object.OUTPUT['rel_pitch'] = [0]
        object.OUTPUT['rel_yaw'] = [0]
        object.OUTPUT['rel_dist2D'] = [0]
        object.OUTPUT['rel_dist3D'] = [0]
    else:
        object.OUTPUT['rel_pitch'] = [np.mean(theta)]
        object.OUTPUT['rel_yaw'] = [np.mean(psi)]
        object.OUTPUT['rel_dist2D'] =[np.mean(dist2D)]
        object.OUTPUT['rel_dist3D'] = [np.mean(dist3D)]


 # sprawdzenie
# R.X0 = 51.92711368
# R.Y0 = 20.70594104
# R.H0 = 0
# x1 =  51.92710817
# y1 = 20.70594104
#  h1 = 10
# from Parser.parser import GNSS_Base, GNSS_Rover
# R = GNSS_Rover()
#
# X,Y,H = WGStoNEDfunc([51.92711368,51.92711368], [20.70594104,20.70594104], [0,0], R,0)
# print(R.X0, R.Y0, R.H0)
# print(X,Y,H)
# X,Y,H = WGStoNEDfunc([51.92710817,51.92710817], [20.70594104,20.70594104], [10,10], R,1)
# print(R.X0, R.Y0, R.H0)
# print(X,Y,H)
# print("out",R.OUTPUT.X.values, R.OUTPUT.Y.values, R.OUTPUT.H.values )
#
# # 617241.94
# # 452557.63
# y1,x1 = wgs84_to_puwg92(51.92711368, 20.70594104)
# y2,x2 = wgs84_to_puwg92(51.92710817, 20.70594104)
# dx = x2-x1
# dy = y2-y1
# dh = 10
# # -------------------------
# get_angles