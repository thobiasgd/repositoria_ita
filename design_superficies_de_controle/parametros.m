clear all
clc

%% Parâmetros Físicos

x_mg = 35.64/1000; 
d_mg = 273.75/1000;
z_t = 253.92/1000; 
l_mg = 22.77/1000;
z_al = 162.66/1000; 
x_ac_h = 94.95/1000; 

massa = 13.463;
g = 9.81;
MTOW = massa*g;

corda_media_aerodinamica = 0.6253;

a = 0;
if a == 0
    lt = 0.91772;
    margemCgAc = 0.28 - 0.25;
end
if a == 1
    lt = 0.91772-0.01*corda_media_aerodinamica;
    margemCgAc = 0.30 - 0.25;
end


b_wing = (0.745+0.405)*2;
S_wing_trapezoidal = 0.227*2;
S_wing_retangular = (0.64*0.745)*2;
S_wing = S_wing_trapezoidal + S_wing_retangular;
Ar_wing = (b_wing^2)/S_wing;

iw = 5;
iht = -1;

c_wing_base = 0.64;
c_wing_tip = 0.479;
%corda_media_aerodinamica = 0.6253; 
c_ht = 0.208;
c_vt = c_ht;
b_ht = 0.666;

S_ht = c_ht* b_ht;
%lt = 0.91772;
lref = lt - 0.75*corda_media_aerodinamica+(0.25*c_ht); % Distância do bordo de fuga da asa até o Ca da empenagem
V_ht = (lt*S_ht)*(S_wing*corda_media_aerodinamica);
H_ht = 0.15;

afilamento = 0.7967;

b_vt = 0.25;
S_vt = c_vt*b_vt;
lv = lt;
V_vt = (lv*S_vt)/(S_wing*b_wing);
zv = 377.92/1000; 

S_lateral_fuselagem = 0.1411; 
L_fuselagem = 1.5;
zw = 134.68/1000; % MIGUÉ - distancia da asa até o centro da fuselagem
alturaFuselagem = 297.5/1000;
diametroMaximoFuselagem = 94/1000; % MIGUÉ

I_XX = 0.6266; 
I_YY = 1.0804;

mi_asfalto = 0.04; % Coeficiente de fricção do asfalto

%% Parâmetro de desempenho

V_stall = 9.96;
V_approach = 1.3*V_stall;
V_cruize = 13.75;
V_rotacional = 1.2*V_stall;
V_to = 11.95;
V_max = 25.09;

T = 40; % Tração do motor (N)

%% Parâmetros Aerodinâmicos

rho = 1.225; 

downwashVar = 0.67737; 
downwash0 = 0.095; 

CL_wing_0 = 0.762949;
CL_ht_0 = 0;

CL_alpha_ht = 3.304;
CL_alpha_wing = 3.390;
CL_alpha_vt = 1.716; 

Cm_ac_wing = -0.059; %-0.3; % MIGUÉ - Seria muito bom encontrar esse valor
Cm_vt = -0.068853; % escolhido em 13º

range_alpha_wing = (-5:0.5:15)/57.3;

Cl_cruzeiro = MTOW/(0.5*rho*(V_cruize^2*S_wing)); 
CL_takeOff = 1.058820; % Usei o Cl em 5º
CD_takeOff = 0.110720; % Usei o CD em 5º

K = 0.09724;

%% Forças

D_takeOff = 0.5*rho*(V_rotacional^2)*S_wing*CD_takeOff;
L_takeOff = 0.5*rho*(V_rotacional^2)*S_wing*CL_takeOff;
M_takeOff = 0.5*rho*(V_rotacional^2)*Cm_ac_wing*S_wing*corda_media_aerodinamica;

F_friction = mi_asfalto*(MTOW-L_takeOff);




















