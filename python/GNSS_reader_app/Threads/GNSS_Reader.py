import serial
import threading
import time
from serial import Serial
from pyubx2 import UBXReader
from multiprocessing import Queue


class GNSSThread(threading.Thread):
    """
    UBX-NAV_HPPOSLLH -- High precision geodetic position solution (periodic/polled)
        version -- message verison
        reserved0 -- reserved
        invalidLlh -- 1 = Invalid lon, lat, height, hMSL, lonHp, latHp, heightHp and hMSLHp
        iTOW [ms] -- GPS time of week of the navigation epoch.
        lon [scale 1e-7] [deg] -- Longitude
        lat [scale 1e-7] [deg] -- Latitude
        height [mm] -- Height above ellipsoid
        hMSL [mm] -- Height above mean sea level
        lonHp [1e-9] [deg] -- High precision component of longitude in deg * 1e-7 = lon + (lonHp * 1e-2)
        latHp [1e-9] [deg] -- High precision component of latitude. Must be in the range -99 +99. Precise latitude in deg * 1e-7 = lat + (latHp * 1e-2)
        heightHp [0.1] [mm] -- High precision component of height above ellipsoid. Must be in the range -9..+9. Precise height in mm = height + (heightHp * 0.1).
        hMSLHp [0.1] [mm] -- High precision component of height above mean sea level. Must be in range -9..+9. Precise height in mm = hMSL + (hMSLHp * 0.1)
        hAcc [0.1] [mm] -- Horizontal accuracy estimate
        vAcc [0.1] [mm] -- Vertical accuracy estimate


    UBX-NAV-STAUS -- Receiver navigation status
        iTOW [ms] -- GPS time of week of the navigation epoch.
        gpsFix -- GPSfix Type, this value does not qualify a fix as valid and within the limits. See note on flag gpsFixOk below.
            0x00 = no fix
            0x01 = dead reckoning only
            0x02 = 2D-fix
            0x03 = 3D-fix
            0x04 = GPS + dead reckoning combined
            0x05 = Time only fix
            0x06..0xff = reserved
        gpsFixOk -- 1 = position and velocity valid and within DOP and ACC Masks.
        diffSoln -- 1 = differential corrections were applied
        wknSet -- 1 = Week Number valid (see section Time validity in the integration manual for details)
        towSet -- 1 = Time of Week valid (see section Time validity in the integration manual for details)
        diffCorr -- 1 = differential corrections available
        carrSolnValid -- 1 = valid carrSoln
        mapMatching -- map matching status:
            00: none
            01: valid but not used, i.e. map matching data was received, but was too old
            10: valid and used, map matching data was applied
            11: valid and used, map matching data was applied. In case of sensor unavailability map matching data enables dead reckoning.
            This requires map matched latitude/longitude or heading data.
        psmState -- power save mode state (not supported for protocol versions less than 13.01)
            0 = ACQUISITION [or when psm disabled]
            1 = TRACKING
            2 = POWER OPTIMIZED TRACKING
            3 = INACTIVE
        spoofDetState -- Spoofing detection state (not supported for protocol versions less than 18.00)
            0: Unknown or deactivated
            1: No spoofing indicated
            2: Spoofing indicated
            3: Multiple spoofing indications
        carrSoln -- Carrier phase range solution status:
            0 = no carrier phase range solution
            1 = carrier phase range solution with floating ambiguities
            2 = carrier phase range solution with fixed ambiguities
        ttff [ms] -- Time to first fix (millisecond time tag)
        msss [ms] -- Milliseconds since Startup / Reset

    UBX-NAV-RELPOSNED -- Relative positioning information in NED frame (Periodic/polled)
    This message contains the relative position vector from the reference station to the rover, including accuracy
    figures, in the local topological system defined at the reference station.

    The NED frame is defined as the local topological system at the reference station. The relative position
    vector components in this message, along with their associated accuracies, are given in that local topological
    system.

        version -- message verison
        reserved0 -- reserved
        refStationId -- Reference station ID. Must be in the range 0..4095.
        iTOW [ms] -- GPS time of week of the navigation epoch.
        relPosN [cm] -- North component of relative position vector
        relPosE [cm] -- East component of relative position vector
        relPosD [cm] -- Down component of relative position vector
        relPosLength [cm] -- Length of the relative position vector
        relPosHeading [1e-5] [deg] -- Heading of the relative position vector
        reserved1 -- reserved
        relPosHPN [0.1] [mm] -- High-precision North component of relative position vector. Must be in the range -99 to +99.
            The full North component of the relative position vector, in units of cm, is given by relPosN + (relPosHPN * 1e-2)
        relPosHPE [0.1] [mm] -- High-precision East component of relative position vector. Must be in the range -99 to +99.
            The full East component of the relative position vector, in units of cm, is given by relPosE + (relPosHPE * 1e-2)
        relPosHPD [0.1] [mm] -- High-precision Down component of relative position vector. Must be in the range -99 to +99.
            The full Down component of the relative position vector, in units of cm, is given by relPosD + (relPosHPD * 1e-2)
        relPosHPLength [0.1] [mm] -- High-precision component of the length of the relative position vector. Must be in the range -99 to +99.
            The full length of the relative position vector, in units of cm, is given by relPosLength + (relPosHPLength * 1e-2)
        accN [0.1] [mm] -- Accuracy of relative position North component
        accE [0.1] [mm] -- Accuracy of relative position East component
        accD [0.1] [mm] -- Accuracy of relative position Down component
        accLength [0.1] [mm] -- Accuracy of length of the relative position vector
        accHeading [1e-5] [deg] -- Accuracy of heading of the relative position vector
        reserved2 -- reserved
        gnssFixOK -- A valid fix (i.e within DOP & accuracy masks)
        diffSoln -- 1 if differential corrections were applied
        relPosValid -- 1 if relative position components and accuracies are valid and, in moving base mode only, if baseline is valid
        carrSoln -- Carrier phase range solution status:
            0 = no carrier phase range solution
            1 = carrier phase range solution with floating ambiguities
            2 = carrier phase range solution with fixed ambiguities
        isMoving -- 1 if the receiver is operating in moving base mode
        refPosMiss -- 1 if extrapolated reference position was used to compute moving base solution this epoch.
        refObsMiss -- 1 if extrapolated reference observations were used to compute moving base solution this epoch.
        relPosHeadingValid -- 1 if relPosHeading is valid
        relPosNormalized -- 1 if the components of the relative position vector (including the high-precision parts) are normalized

    """

    def __init__(
            self,
            serial_port: str,
            device: str,
            start_time: float,
            msgq: Queue,
            msgq2: Queue,
            semaphore,
            # stop_program:bool,
            baudrate: int = 460800,
            timeout: int = 3,
            daemon: bool = True,
            **kwargs
    ):

        super(GNSSThread, self).__init__(daemon=daemon)

        self.gnss_name = device
        self.serial_port = serial_port
        self.msgq = msgq
        self.msgq2 = msgq2
        self.semaphore = semaphore
        print(f'\tTrying to connect to: {serial_port} at {baudrate}  BAUD.')
        try:
            self.ubx_stream = Serial(port=serial_port, baudrate=baudrate, timeout=timeout)

            print(f'\tConnected to {device} {serial_port} at {baudrate} BAUD.')
            self.ubx_reader = UBXReader(self.ubx_stream)
            self.gnss_name = device
            self.start_time = start_time
        except serial.serialutil.SerialException:
            print(f"\t\033[31mFailed to connect with {device} {serial_port} at {baudrate} BAUD.\033[39m\t{time.time()}")
            exit()
        print(f"\033[32m\t{self.gnss_name.capitalize()} Initialized Correctly\033[39m\t{time.time()}")



    def run(self):
        read_t_start = 0
        read_t_end = 0

        while True:
            read_t_start = time.time()
            dt = read_t_start - read_t_end

            val = self.read()
            self.msgq.put(val)
            if self.semaphore._value==0:
                self.msgq2.put(val)
            read_t_end = read_t_start

    def read(self) -> dict:
        while True:
            (raw, parsed) = self.ubx_reader.read()
            if parsed.identity == "NAV-HPPOSLLH":
                return {"name": self.gnss_name, "time": time.time(), "lon": parsed.lon, "lat": parsed.lat,
                        "height": parsed.height}
