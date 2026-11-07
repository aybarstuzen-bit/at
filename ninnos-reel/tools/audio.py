import numpy as np, wave, sys
SR=48000; T=34.0; N=int(SR*T)
L=np.zeros(N); R=np.zeros(N)
t=np.arange(N)/SR
rng=np.random.default_rng(7)
def add(sig,start,pan=0.5,g=1.0):
    i=int(start*SR); n=min(len(sig),N-i)
    L[i:i+n]+=sig[:n]*g*(1-pan)*2**0.5*0.707*1.0; R[i:i+n]+=sig[:n]*g*pan*2**0.5*0.707
def env(n,a,d):
    e=np.ones(n); a=int(a*SR); d=int(d*SR)
    e[:a]=np.linspace(0,1,a); e[-d:]*=np.linspace(1,0,d); return e
# BEFORE 0-9s: low uneasy pad (minor second rub) + clock ticks
n=int(9.4*SR); tt=np.arange(n)/SR
pad=(np.sin(2*np.pi*110*tt)+0.6*np.sin(2*np.pi*116.5*tt)+0.4*np.sin(2*np.pi*164.8*tt))*0.05
pad*=env(n,0.4,1.2); add(pad,0)
for k in range(18):
    s=0.25+k*0.5
    m=int(0.04*SR); x=rng.standard_normal(m)*np.exp(-np.linspace(0,9,m))
    x=np.convolve(x,np.ones(6)/6,'same')*(0.10 if k%2==0 else 0.06)
    add(x,s,pan=0.45 if k%2 else 0.55)
# reveal chime at 9.0
def bell(f,dur,g):
    n=int(dur*SR); tt=np.arange(n)/SR
    x=(np.sin(2*np.pi*f*tt)+0.5*np.sin(2*np.pi*f*2.0*tt)*np.exp(-tt*3)+0.25*np.sin(2*np.pi*f*3.01*tt)*np.exp(-tt*5))
    a=int(0.004*SR); x[:a]*=np.linspace(0,1,a)
    return x*np.exp(-tt*2.2)*g
for i,f in enumerate([783.99,987.77,1174.66,1567.98]):
    add(bell(f,2.5,0.10),9.0+i*0.09,pan=0.3+0.13*i)
# music box lullaby from 9.4 (original pentatonic melody in D major, 3/4, 84 bpm)
beat=60/84
D=293.66
notes={'D':0,'E':2,'F#':4,'A':7,'B':9,'d':12,'e':14,'f':16,'a':19}
mel=[('F#',1),('A',1),('d',1),('B',2),('A',1),('F#',1),('E',1),('D',1),('E',3),
     ('F#',1),('A',1),('B',1),('d',2),('B',1),('A',1),('F#',1),('E',1),('D',3),
     ('A',1),('d',1),('e',1),('f',2),('e',1),('d',1),('B',1),('A',1),('B',3),
     ('A',1),('F#',1),('E',1),('D',2),('E',1),('F#',2),('E',1),('D',3)]
bass=[('D',),('A',),('B',),('F#',),('G',),('D',),('E',),('A',)]
t0=9.6; pos=t0
while pos<T-1.5:
    for nm,b in mel:
        if pos>T-1.5: break
        f=D*2**(notes[nm]/12)*2
        add(bell(f,2.2,0.075),pos,pan=0.5+0.15*np.sin(pos))
        pos+=b*beat
# soft bass/pad under lullaby
chords=[[0,4,7],[7,11,14],[9,12,16],[4,7,11]]
p=t0; ci=0
while p<T-1:
    n=int(beat*3*SR); tt=np.arange(n)/SR
    x=sum(np.sin(2*np.pi*D/2*2**(s/12)*tt) for s in chords[ci%4])*0.018
    x*=env(n,0.5,0.6); add(x,p); p+=beat*3; ci+=1
# shushing (pis pis) noise pulses 11.4-17.2, then soft white noise bed
def shh(dur,g):
    n=int(dur*SR); x=rng.standard_normal(n)
    X=np.fft.rfft(x); f=np.fft.rfftfreq(n,1/SR)
    X*=np.exp(-((f-4500)/2500)**2)+0.3*np.exp(-((f-8000)/3000)**2)
    x=np.fft.irfft(X,n); x/=np.abs(x).max()
    e=np.sin(np.linspace(0,np.pi,n))**1.5
    return x*e*g
for k in range(6):
    add(shh(0.75,0.05),11.5+k*0.95,pan=0.5)
nb=int((T-17.2)*SR); x=rng.standard_normal(nb); x=np.convolve(x,np.ones(12)/12,'same')
x/=np.abs(x).max(); x*=0.012*env(nb,1.5,2.0); add(x,17.2)
# sensor ping 17.4
add(bell(1318.5,1.2,0.06),17.4,0.6); add(bell(1760,1.2,0.05),17.55,0.4)
# master fade + normalize
m=max(np.abs(L).max(),np.abs(R).max()); g=0.85/m
fade=np.ones(N); fn=int(1.4*SR); fade[-fn:]=np.linspace(1,0,fn)
fi=int(0.03*SR); fade[:fi]=np.linspace(0,1,fi)
st=np.stack([L*g*fade,R*g*fade],1)
pcm=(st*32767).astype('<i2')
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
