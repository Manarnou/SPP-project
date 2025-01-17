import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

n1 = 1.5  # glass prism

########### function to extract and extrapolate data of refractive indices of metals vs incident wavelenght #############
def index(cond):
    if cond == 0 :
        lambda_n, n_real = np.loadtxt("Real_n_gold.txt", unpack=True)
        lambda_k, k_imag = np.loadtxt("imag_n_gold.txt", unpack=True)
    elif cond == 1:
        lambda_n, n_real = np.loadtxt("Real_n_silver.txt", unpack=True)
        lambda_k, k_imag = np.loadtxt("imag_n_silver.txt", unpack=True)
    elif cond==2 :
        lambda_n, n_real = np.loadtxt("Real_n_aluminum.txt", unpack=True)
        lambda_k, k_imag = np.loadtxt("imag_n_aluminum.txt", unpack=True)
    elif cond==3 :
        lambda_n, n_real = np.loadtxt("Real_n_copper.txt", unpack=True)
        lambda_k, k_imag = np.loadtxt("imag_n_copper.txt", unpack=True)
    else:
        print("invalid input")
        exit()
    n_interp = interp1d(lambda_n, n_real, kind='linear', fill_value="extrapolate")
    k_interp = interp1d(lambda_k, k_imag, kind='linear', fill_value="extrapolate")

    return n_interp, k_interp

######### Calculations of reflectivity  vector correpsonding to different incident angles ##############
def function(wavelength_um,n3,d_,cond):
    n_interp, k_interp =index(cond)
    ni, ki = n_interp(wavelength_um), k_interp(wavelength_um)
    n2 = ni + 1j * ki
    theta1_deg = np.linspace(0, 90, 1000)
    theta1_rad = np.radians(theta1_deg)
    ct1 = np.cos(theta1_rad)
    theta2_rad = np.arcsin(n1 * np.sin(theta1_rad) / n2)
    theta3_rad = np.arcsin(n2 * np.sin(theta2_rad) / n3)
    for i in range(len(theta1_rad)):
        if theta3_rad.imag[i] > 0:
            theta3_rad[i] = np.conj(theta3_rad[i])
    ct3 = np.cos(theta3_rad)
    ct2 = np.cos(theta2_rad)
    r12 = (n2 * ct1 - n1 * ct2) / (n2 * ct1 + n1 * ct2)
    r23 = (n3 * ct2 - n2 * ct3) / (n3 * ct2 + n2 * ct3)
    k = (2 * np.pi / (wavelength_um*1e-6)) * n2 * ct2
    delta = k * d_
    Rg = (r12 + r23 * np.exp(2j * delta)) / (1 + r12 * r23 * np.exp(2j * delta))
    Rg_mag1 = np.abs(Rg)**2
    theta_min=theta1_deg[np.argmin(Rg_mag1)]
    return Rg_mag1, theta1_deg, theta_min


########### Calculations of the reflectivity value corresponding to the SPR angle theta_min #############
def function2(wavelenght_um,n3,d_,theta_min, cond):
    n_interp, k_interp =index(cond)
    ni, ki = n_interp(wavelength_um), k_interp(wavelength_um)
    n2 = ni + 1j * ki
    theta1_deg=theta_min
    theta1_rad = np.radians(theta1_deg)
    ct1 = np.cos(theta1_rad)
    theta2_rad = np.arcsin(n1 * np.sin(theta1_rad) / n2)
    theta3_rad = np.arcsin(n2 * np.sin(theta2_rad) / n3)
    if theta3_rad.imag > 0:
        theta3_rad = np.conj(theta3_rad)
    ct3 = np.cos(theta3_rad)
    ct2 = np.cos(theta2_rad)
    r12 = (n2 * ct1 - n1 * ct2) / (n2 * ct1 + n1 * ct2)
    r23 = (n3 * ct2 - n2 * ct3) / (n3 * ct2 + n2 * ct3)
    k = (2 * np.pi / (wavelength_um*1e-6)) * n2 * ct2
    delta = k * d_
    Rg = (r12 + r23 * np.exp(2j * delta)) / (1 + r12 * r23 * np.exp(2j * delta))
    Rg_mag1 = np.abs(Rg)**2
    return Rg_mag1


############## case study: Rg vs theta different n and d ############@#################
wavelength_um = 0.6328
lambda_ = wavelength_um* 10**(-6)
d=50*1e-9
n3_=np.array([1.0, 1.1, 1.2, 1.3 ])
cond=0                                     #for gold
Rg_mag1=np.zeros(len(n3_))
theta_min1=np.zeros(len(n3_))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
x,y,theta_min_n1=function(wavelength_um, 1 , d, cond)

for j in range((len(n3_))):
    Rg_mag1,theta_deg, z=function(wavelength_um, n3_[j], d,cond)
    ax1.plot(theta_deg, Rg_mag1, label=f'n={n3_[j]}')

n3_=np.linspace(1,1.05, 50)
RgMin=np.zeros(len(n3_))
d_nm=np.array([30, 40, 50, 60])
d1=d_nm*1e-9


for i in range((len(d1))):
    x,y,theta_min_n1=function(wavelength_um, 1 , d1[i])
    for j in range((len(n3_))):
        RgMin[j]=function2(wavelength_um,n3_[j],d1[i],theta_min_n1, cond)
    ax2.plot(n3_, RgMin , linestyle='--',marker='x', label=f'd={d_nm[i]}nm')

ax1.legend()
ax2.legend()
ax1.grid(True)
ax2.grid(True)
ax1.set_xlabel('Incident angle (degrees)')
ax1.set_ylabel('Reflectivity')
ax2.set_xlabel('Refractive index of dielectric')
ax2.set_ylabel('Reflectivity at SPR angle')
ax1.set_xlim(0,90)
ax2.set_xlim(1,np.max(n3_))
ax1.set_ylim(0,1)
plt.tight_layout()
#plt.savefig('FIGURE2-slide10-d-gold-RG-RgMin-n3.png',dpi=300)
#plt.show()


################### choice of metal ###############################
wavelength_um = 0.6328
lambda_ = wavelength_um* 10**(-6)
d_in=np.linspace(30,50,2)
d=d_in*1e-9
n3_=np.linspace(1,1.04, 10)
RgMin=np.zeros((len(n3_),len(d)))
opt_d=np.zeros(4)
max_sensitivity=np.zeros(4)

cond=np.array([0,1,2,3])
label_map = { 0: 'Gold', 1: 'silver', 2: 'Aluminum', 3: 'Copper' }

for c in range(len(cond)):
    st=np.zeros(len(d))
    for j in range(len(d)):
        x, y, theta_min_n1=function(wavelength_um, 1 , d[j],cond[c])
        for i in range(len(n3_)):
            RgMin[i:j]=function2(wavelength_um,n3_[i],d[j],theta_min_n1, cond[c])
        if c == 0 :
            plt.plot(n3_ ,RgMin[:,j],label=f'd={d_in[j]}')

    for i in range(len(d)):
        st[i] = np.mean(np.diff(RgMin[:,i])/np.diff(n3_))
    opt_d[c]=d_in[np.argmax(st)]
    max_sensitivity[c]=np.max(st)

    label=label_map.get(cond[c], None)
    plt.plot(opt_d[c], max_sensitivity[c], marker='X',  markersize=12, markeredgewidth=0.4, label=label)
    plt.text(opt_d[c], max_sensitivity[c]+0.4 , f'{opt_d[c]:.2f}', fontsize=10, ha='left', va='bottom')

plt.xlabel('Optimum thickness (nm)')
plt.ylabel(r'$\Delta \theta_\text{SPR} / \Delta n$')
plt.grid(True)
plt.legend()
#plt.savefig('FIGURE-optD-diff-metals.png', dpi=300)
#plt.show()




