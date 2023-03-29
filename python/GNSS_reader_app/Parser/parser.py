import pandas as pd
import numpy as np
col1 = ['NAV-HPPOSLLH','version','reserved0','invalidLlh','iTOW','lon','lat','height','hMSL','hAcc','vAcc']
col2 = ['NAV-STATUS','iTOW','gpsFix','gpsFixOk','diffSoln','wknSet','towSet','diffCorr','carrSolnValid',
        'mapMatching','psmState','spoofDetState','carrSoln','ttff','msss']
col3 = ['NAV-RELPOSNED','version','reserved0','refStationID','iTOW','relPosN','relPosE','relPosD','relPosLength',
'relPosHeading','reserved1','relPosHPN','relPosHPE','relPosHPD','relPosHPLength','accN','accE','accD','accLength',
'accHeading','reserved2','gnssFixOK','diffSoln','relPosValid','carrSoln','isMoving','refPosMiss','refObsMiss',
'relPosHeadingValid','relPosNormalized']
out_col = ['ID','time', 'lat','lon', 'alt', 'rel_dist2D', 'rel_dist3D', 'rel_yaw', 'rel_pitch']

class GNSS_Base:
    def __init__(self):
        self.NAV_HPPOSLLH = pd.DataFrame(columns=col1)
        self.NAV_STATUS = pd.DataFrame(columns=col2)
        self.OUTPUT = pd.DataFrame(columns=out_col)
        self.time1 =[]
        self.time2 =[]
        self.out_tab= []
        self.X0 = 0
        self.Y0 = 0
        self.H0 = 0

class GNSS_Rover(GNSS_Base):
    def __init__(self):
        super().__init__()
        self.NAV_RELPOSNED = pd.DataFrame(columns=col3)
        self.NAV_RELPOSNED_filtered = pd.DataFrame(columns=col3)


def read_GPS_txt(row_, object):
    row = row_.split(",")
    # row = [i.strip() for i in row_]
    if row[0] == 'NAV-HPPOSLLH':

        # dodawanie kolejnych ramek do tablicy
        HPPOSLLH = pd.DataFrame([row], columns=col1)
        # object.NAV_HPPOSLLH = pd.concat([object.NAV_HPPOSLLH, HPPOSLLH], ignore_index=True)

        # nadpisywanie ramki w tablicy
        object.NAV_HPPOSLLH = pd.DataFrame([row], columns=col1)

    if row[0] == 'NAV-STATUS':

        # dodawanie kolejnych ramek do tablicy
        STATUS = pd.DataFrame([row], columns=col2)
        # object.NAV_STATUS = pd.concat([object.NAV_STATUS, STATUS],  ignore_index=True)

        # nadpisywanie ramki w tablicy
        object.NAV_STATUS = pd.DataFrame([row], columns=col2)

    if row[0] == 'NAV-RELPOSNED':

        # dodawanie kolejnych ramek do tablicy
        RELPOSNED = pd.DataFrame([row], columns=col3)
        # object.NAV_RELPOSNED = pd.concat([object.NAV_RELPOSNED, RELPOSNED], ignore_index=True)

        # nadpisywanie ramki w tablicy
        object.NAV_RELPOSNED = pd.DataFrame([row], columns=col3)


def convert_base(object):

    # change NAV_HPPOSLLH data to numeric
    # object.NAV_HPPOSLLH['time'] = pd.to_numeric(object.NAV_HPPOSLLH['time'])
    object.NAV_HPPOSLLH['invalidLlh'] = pd.to_numeric(object.NAV_HPPOSLLH['invalidLlh'])
    object.NAV_HPPOSLLH['iTOW'] = pd.to_numeric(object.NAV_HPPOSLLH['iTOW'])
    object.NAV_HPPOSLLH['lon'] = pd.to_numeric(object.NAV_HPPOSLLH['lon'])
    object.NAV_HPPOSLLH['lat'] = pd.to_numeric(object.NAV_HPPOSLLH['lat'])
    object.NAV_HPPOSLLH['height'] = pd.to_numeric(object.NAV_HPPOSLLH['height']) /1000
    object.NAV_HPPOSLLH['hMSL'] = pd.to_numeric(object.NAV_HPPOSLLH['hMSL']) /1000

    # change NAV_STATUS data to numeric
    # object.NAV_STATUS['time'] = pd.to_numeric(object.NAV_STATUS['time'])
    object.NAV_STATUS['iTOW'] = pd.to_numeric(object.NAV_STATUS['iTOW'])
    object.NAV_STATUS['gpsFix'] = pd.to_numeric(object.NAV_STATUS['gpsFix'])
    object.NAV_STATUS['gpsFixOk'] = pd.to_numeric(object.NAV_STATUS['gpsFixOk'])
    object.NAV_STATUS['diffSoln'] = pd.to_numeric(object.NAV_STATUS['diffSoln'])
    object.NAV_STATUS['wknSet'] = pd.to_numeric(object.NAV_STATUS['wknSet'])
    object.NAV_STATUS['towSet'] = pd.to_numeric(object.NAV_STATUS['towSet'])
    object.NAV_STATUS['diffCorr'] = pd.to_numeric(object.NAV_STATUS['diffCorr'])
    object.NAV_STATUS['carrSolnValid'] = pd.to_numeric(object.NAV_STATUS['carrSolnValid'])
    object.NAV_STATUS['mapMatching'] = pd.to_numeric(object.NAV_STATUS['mapMatching'])
    object.NAV_STATUS['psmState'] = pd.to_numeric(object.NAV_STATUS['psmState'])
    object.NAV_STATUS['spoofDetState'] = pd.to_numeric(object.NAV_STATUS['spoofDetState'])
    object.NAV_STATUS['carrSoln'] = pd.to_numeric(object.NAV_STATUS['carrSoln'])
    object.NAV_STATUS['ttff'] = pd.to_numeric(object.NAV_STATUS['ttff'])
    object.NAV_STATUS['msss'] = pd.to_numeric(object.NAV_STATUS['msss'])

    # save only wanted colums
    # object.NAV_HPPOSLLH = object.NAV_HPPOSLLH[['invalidLlh','iTOW', 'lon','lat', 'height', 'hMSL']]
    # object.NAV_STATUS = object.NAV_STATUS[['iTOW','gpsFix','gpsFixOk', 'diffSoln','wknSet','towSet','diffCorr',
    #                                        'carrSolnValid', 'mapMatching', 'psmState', 'spoofDetState','carrSoln',
    #                                        'ttff', 'msss']]

def convert_rover(object, GNSS):

    convert_base(object)
    if GNSS == 1:
        # change NAV_RELPOSNED data to numeric
        object.NAV_RELPOSNED['time'] = pd.to_numeric(object.NAV_RELPOSNED['time'])
        object.NAV_RELPOSNED['iTOW'] = pd.to_numeric(object.NAV_RELPOSNED['iTOW'])
        object.NAV_RELPOSNED['relPosN'] = pd.to_numeric(object.NAV_RELPOSNED['relPosN'])
        object.NAV_RELPOSNED['relPosE'] = pd.to_numeric(object.NAV_RELPOSNED['relPosE'])
        object.NAV_RELPOSNED['relPosD'] = pd.to_numeric(object.NAV_RELPOSNED['relPosD'])
        object.NAV_RELPOSNED['relPosLength'] = pd.to_numeric(object.NAV_RELPOSNED['relPosLength'])
        object.NAV_RELPOSNED['relPosHeading'] = pd.to_numeric(object.NAV_RELPOSNED['relPosHeading'])
        object.NAV_RELPOSNED['relPosHPN'] = pd.to_numeric(object.NAV_RELPOSNED['relPosHPN'])
        object.NAV_RELPOSNED['relPosHPE'] = pd.to_numeric(object.NAV_RELPOSNED['relPosHPE'])
        object.NAV_RELPOSNED['relPosHPD'] = pd.to_numeric(object.NAV_RELPOSNED['relPosHPD'])
        object.NAV_RELPOSNED['relPosHPLength'] = pd.to_numeric(object.NAV_RELPOSNED['relPosHPLength'])

        object.NAV_RELPOSNED['relPosN'] = object.NAV_RELPOSNED['relPosN'] + \
                                          object.NAV_RELPOSNED['relPosHPN'] / 100
        object.NAV_RELPOSNED['relPosE'] = object.NAV_RELPOSNED['relPosHPE'] +\
                                            object.NAV_RELPOSNED['relPosE'] / 100
        object.NAV_RELPOSNED['relPosD'] = object.NAV_RELPOSNED['relPosD'] + \
                                          object.NAV_RELPOSNED['relPosHPD'] / 100
        object.NAV_RELPOSNED['relPosLength'] = object.NAV_RELPOSNED['relPosLength'] + \
                                                               object.NAV_RELPOSNED['relPosHPLength'] / 100
        object.NAV_RELPOSNED['relPosHeading'] = object.NAV_RELPOSNED['relPosHeading'] * np.pi/180
        yaw = []
        for i in range(len(object.NAV_RELPOSNED['relPosHeading'])):
            if object.NAV_RELPOSNED['relPosHeading'][i] > np.pi:
                yaw.append(object.NAV_RELPOSNED['relPosHeading'][i] -2*np.pi)
            else:
                yaw.append(object.NAV_RELPOSNED['relPosHeading'][i])
        object.NAV_RELPOSNED['relPosHeading'] = yaw



        # save only wanted colums
        # object.NAV_RELPOSNED = object.NAV_RELPOSNED[['iTOW','relPosN','relPosE','relPosD', 'relPosLength', 'relPosHeading',
        #                                          'relPosHPN','relPosHPE','relPosHPD','relPosHPLength','time']]
