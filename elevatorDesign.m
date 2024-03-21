estabilidadeEstaticaLongitudinal

%% Requisitos do projeto

aceleracaoAngular = 10/57.3; % rad/s²
aceleracaoLinear = (T-D_takeOff-F_friction)/massa; % m/s²
b_ratiobElevator = 1;
deflexaoMaximaProfundor = 25;

%% Momentos durante a decolagem

T = 6.155; % MIGUÉ TOTAL

MW = MTOW*x_mg ; % Momento fornecido pelo peso
MD = d_mg*D_takeOff; % Momento fornecido pelo arrasto total
MT = T*z_t; % Momento fornecido pela tração do motor
ML_wf = L_takeOff*l_mg; % Momento fornecido pela sustentação do conjunto asa fuselagem (considerou-se apenas da asa)
MA = massa*aceleracaoLinear*z_al; % Momento fornecido pela aceleração linear

%% Modelagem

L_req_ht = (ML_wf+M_takeOff+MA-MW+MD-MT-(aceleracaoAngular*I_YY))/(x_ac_h-x_mg); % Sustentação requerida pela empenagem para rotacionar a aeronave

downwash_takeOff = downwash0 + downwashVar*(iw/57.3);
alpha_ht_takeOff = (iw) + (iht) - downwash_takeOff*57.3;

CL_ht_req = (2*L_req_ht)/(rho*V_rotacional*S_ht);

t_e = ((alpha_ht_takeOff/57.3)+(CL_ht_req/CL_alpha_ht))/(-deflexaoMaximaProfundor/57.3); % valor do gráfico de design de superfícies de controle
fprintf('%d', t_e)

CLdE=-CL_alpha_ht*eficienciaEmpenagem*S_ht*t_e/S_wing;
CmdE = -CL_alpha_ht*eficienciaEmpenagem*V_ht*t_e;

Cma1 = CL_alpha_wing*(x_mg-x_ac_h)-CL_alpha_ht*eficienciaEmpenagem*S_ht*(lt/corda_media_aerodinamica)*(1-downwashVar)/S_wing;

%% Plotando gráficos

i = 1;
for U1=V_stall:V_max
    qbar1 = 0.5*rho*(U1^2);
    CL1 = (MTOW)/(qbar1*S_wing);
    f1 = (T*z_t)/(qbar1*S_wing*corda_media_aerodinamica);
    dE1(i) = -((f1*CL_alpha_wing)+(CL1-CL_wing_0)*Cma1)/(CL_alpha_wing*CmdE-Cma1*CLdE);
    V(i)=U1;
    i=i+1;
end

plot(V,dE1*57.3)

grid on
xlabel("v(m/s)",'FontSize',20)
ylabel("\delta_E (º)",'FontSize',20)














