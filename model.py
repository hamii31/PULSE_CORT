import matplotlib.pyplot as plt
import numpy as np

# A dimensionless model of the CRH -> ACTH synthesis pathway

# CONSTANTS FOR A ULTRADIAN OSCILLATION 
P_2 = 15 # feedback strength (GR-cortisol inhibition of ACTH)
P_3 = 7.5 # ACTH degradation rate
P_4 = 0.05 # half-saturation for GR upregulation
P_5 = 0.11 # basal GR synthesis
P_6 = 2.9 # GR degradation rate
A_0 = 0.1 # ACTH
O_0 = 0.1 # CORT
R_0 = 0.1 # glucocorticoid receptor density in the pituitary


def da_dt (crh, r, o, a, p_2, p_3):
    return ((crh / (1 + p_2 * r * o)) - p_3 * a)

def dr_dt (o, r, p_4, p_5, p_6) :
    return (((o * r) ** 2 / (p_4 + (o * r) ** 2)) + p_5 - p_6 * r)

def do_dt (a, o):
    return a - o

tau = 5.0 # delay (10 min) 0.9627 
dt = 0.001
steps = 200000
delay_steps = round(tau/dt)

for crh in np.arange(1.0, 15.0, 1.0):
    ts, a_hist, r_hist, o_hist = [], [], [], []
    a, r, o = A_0, R_0, O_0

    for i in range(steps):
        # record current state at time i*dt
        ts.append(i * dt)
        a_hist.append(a)
        r_hist.append(r)
        o_hist.append(o)
        
        # look up a(t - tau)
        if i >= delay_steps:
            a_delayed = a_hist[i - delay_steps]
        else:
            a_delayed = A_0

        da = da_dt(crh, r, o, a, P_2, P_3)
        dr = dr_dt(o, r, P_4, P_5, P_6)
        do = a_delayed - o

        a += da * dt
        r += dr * dt
        o += do * dt

    plt.title(f"CORT production at {crh} CRH")
    plt.plot(ts, a_hist, label='ACTH (a)')
    plt.plot(ts, o_hist, label='CORT (o)')
    plt.plot(ts, r_hist, label='GR density (r)')
    plt.xlabel('dimensionless time')
    plt.ylabel('concentration')
    plt.legend()
    plt.show()
