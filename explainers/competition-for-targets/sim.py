import numpy as np
def sim(n=10,steps=400,seed=3,rate=1.6,sd=0.03,T=2.2):
    rng=np.random.default_rng(seed)
    x=1+sd*rng.standard_normal(n)
    xs=[x.copy()]
    dt=T/steps
    for _ in range(steps):
        rel=x/x.mean()
        h=rel**8/(1+rel**8)
        dx=0.1+ 3.0*h - 1.5*x
        x=np.maximum(x+dt*dx*rate,0.05)
        xs.append(x.copy())
    return np.array(xs)
if __name__=="__main__":
    xs=sim()
    print(np.round(xs[::40],2))
