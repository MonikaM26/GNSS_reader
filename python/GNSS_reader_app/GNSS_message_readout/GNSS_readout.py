import serial.tools.list_ports
from pyubx2 import UBXReader


def read_serial_port(port, baudrate):
    serialInst = serial.Serial()
    serialInst.baudrate = baudrate
    serialInst.port = port
    serialInst.open()
    if serialInst.in_waiting:
        line = serialInst.readline()
        print(line)
        decoded_line = line.decode('utf')
    else:
        decoded_line = "brak"



def read_data(ubr):
    (raw_data, msg) = ubr.read()
        # string = bytes.fromhex(data)
        # msg = UBXReader.parse(string)
        # NAV - HPPOSLLH,
        # NAV-HPPOSLLH, version , reserved0, invalidLlh, iTOW, lon, lat, height, hMSL, hAcc, vAcc

        # NAV-STATUS
        # NAV-STATUS,iTOW,gpsFix,gpsFixOk,diffSoln,wknSet,towSet,diffCorr,carrSolnValid,mapMatching,psmState,spoofDetState,
        # carrSoln,ttff,msss

        # NAV - RELPOSNED
        # NAV-RELPOSNED,version,reserved0,refStationID,iTOW,relPosN,relPosE,relPosD,relPosLength,relPosHeading,reserved1,
        # relPosHPN,relPosHPE,relPosHPD,relPosHPLength,accN,accE,accD,accLength,accHeading,reserved2,gnssFixOK,diffSoln,
        # relPosValid,carrSoln,isMoving,refPosMiss,refObsMiss,relPosHeadingValid,relPosNormalized

    if msg.identity == 'NAV-HPPOSLLH':
        # g = open(file_out1, 'a')
        lines = str(msg.identity) + ',' + str(msg.version) + ',' + str(msg.reserved0) + ',' + str(msg.invalidLlh) +\
        ',' + str(msg.iTOW) + ',' + str(msg.lon) + ',' + str(msg.lat) + ',' + str(msg.height)+ ',' + str(msg.hMSL) +\
        ',' + str(msg.hAcc) + ',' + str(msg.vAcc)
        # g.writelines(lines)
        # g.close()

    elif msg.identity == 'NAV-STATUS':
        # g = open(file_out2, 'a')
        lines = str(msg.identity) + ',' + str(msg.iTOW) + ',' + str(msg.gpsFix) + ',' + str(msg.gpsFixOk) +\
        ',' + str(msg.diffSoln) + ',' + str(msg.wknSet) + ',' + str(msg.towSet) + ',' + str(msg.diffCorr)+ ',' + \
        str(msg.carrSolnValid) + ',' + str(msg.mapMatching) + ',' + str(msg.psmState) + ',' + str(msg.spoofDetState) + \
        ',' + str(msg.carrSoln) + ',' + str(msg.ttff) + ',' + str(msg.msss)
        # g.writelines(lines)
        # g.close()

    elif msg.identity == 'NAV-RELPOSNED':
        # g = open(file_out3, 'a')
        lines = str(msg.identity) + ',' + str(msg.version) + ',' + str(msg.reserved0) + ',' + str(msg.refStationID) +\
        ',' + str(msg.iTOW) + ',' + str(msg.relPosN) + ',' + str(msg.relPosE) + ',' + str(msg.relPosD) + ',' + \
        str(msg.relPosLength) + ',' + str(msg.relPosHeading) + ',' + str(msg.reserved1) + ',' + str(msg.relPosHPN) + \
        ',' + str(msg.relPosHPE) + ',' + str(msg.relPosHPD) + ',' + str(msg.relPosHPLength) + ',' + str(msg.accN) +\
        ',' + str(msg.accE) + ',' + str(msg.accD) + ',' + str(msg.accLength) + ',' + \
        str(msg.accHeading) + ',' + str(msg.reserved2) + ',' + str(msg.gnssFixOK) + ',' + str(msg.diffSoln) +\
        ',' + str(msg.relPosValid) + ',' + str(msg.carrSoln) + ',' + str(msg.isMoving) + ',' + str(msg.refPosMiss) + \
        ',' + str(msg.refObsMiss) + ',' + str(msg.relPosHeadingValid) + ',' + str(msg.relPosNormalized)
        # g.writelines(lines)
        # g.close()
    else:
        lines = ""
    return lines