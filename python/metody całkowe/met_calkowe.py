""" Actual velocity and displacement calculation based on
    - Runge Kutta 4th order integration method
        based on: https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_methods """


class PosVelCalculate:
    def Runge_Kutta(self, a, N, dt, C):
        # a - first value
        # N - sample number
        # dt - delta time
        # C - ZUPT - parameter to stop integrating until this parameter changes (0 - integrate, 1 - pause integrating process)
        v = 0
        p = 0
        path = 0
        v_ZUPT = []
        p_ZUPT = []
        a1 = 0  # last value
        for i in range(N):
            a_ = a[i]  # current value
            v1 = v
            p1 = p

            v2 = v + 0.5 * dt[i] * a1
            p2 = p + 0.5 * dt[i] * v2

            a2 = (a1 + a_) / 2
            v3 = v + 0.5 * dt[i] * a2
            p3 = p + 0.5 * dt[i] * v3

            a3 = (a1 + a_) / 2
            v4 = v + 0.5 * dt[i] * a3
            p4 = p + 0.5 * dt[i] * v4
            a4 = a_

            # integration according to ZUPT value
            if C[i] == 1:
                v = 0
                p = p
            else:
                v = v + 1 / 6 * dt[i] * (a1 + 2 * a2 + 2 * a3 + a4)
                p = p + 1 / 6 * dt[i] * (v1 + 2 * v2 + 2 * v3 + v4)
            v_ZUPT.append(v)
            p_ZUPT.append(p)
            a1 = a_
            path = path + abs(1 / 6 * dt[i] * (v1 + 2 * v2 + 2 * v3 + v4))
        print("Displacement based on Runge Kutta 4th order: ", path, "[m]")
        return v_ZUPT, p_ZUPT