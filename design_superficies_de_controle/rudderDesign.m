parametros

%% Parâmetros de design

dc = 0.1;% distância

V_wind = 2.99; % Velocidade do vento em SJC (m/s)
V_total_airspeed = sqrt(((V_wind^2)+(V_approach^2)));

n_vt = 0.95; % eficiência da empenagem vertical

b_rudder = b_vt;
b_ratioRudder = b_rudder/b_vt;
c_ratio = 0.25;

beta = (atan((V_wind)/(V_approach)));
beta = rad2deg(beta);

F_wind_areaLateral = 0.5*rho*(V_wind^2)*S_lateral_fuselagem*0.6; % coeficiente usado como 0.6 igual ao sadraey

beta = (atan((V_wind)/(V_approach)));

Kf1 = 0.75;
Kf2 = 1.3;

Cn_betha = Kf1*CL_alpha_vt(1-0)*n_vt*V_vt;

Cy_betha = -Kf2*CL_alpha_vt*(1-0)*n_vt*S_vt/S_wing;

eficienciaRudder = 0.45; % retirada do gráfico de superfície de controle na razão de 0.25

Cy_delta_R = CL_alpha_vt*n_vt*eficienciaRudder*b_ratioRudder*(S_vt/S_wing);

Cn_delta_R = -CL_alpha_vt*V_vt*n_vt*b_ratioRudder;

%% Realizando equações simultâneas

syms sigma deltaR

fatorEquacao01 = (Cn_betha*(beta-sigma)+Cn_delta_R*deltaR);
equation01 = 0.5*rho*(V_total_airspeed^2)*S_wing*b_wing*fatorEquacao01+F_wind_areaLateral*dc*cos(sigma) == 0;

fatorEquacao02 = (Cy_betha*(beta-sigma)+Cy_delta_R*deltaR);
equation02 = 0.5*rho*(V_total_airspeed^2)*S_wing*fatorEquacao02 == F_wind_areaLateral;

sol = solve([equation01,equation02],[sigma, deltaR]);

deflecWind = (sol.sigma)*57.3 % deflexão necessária para girar o avião com o vento de 2.99(m/s) [6.7 mph]
sol.deltaR

% OBS: necessário não colocar ";" nas linhas 45 e 46 pois ocorre erro (bug)








