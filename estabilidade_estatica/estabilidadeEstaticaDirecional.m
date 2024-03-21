parametros

%% Obtendo valores de Kn através do gráfico

pt1 = (lt^2)/S_lateral_fuselagem; %5.96
pt2 = sqrt(0.156/0.07724); %1.42
pt3 = 0.156/0.092; %1.6957

Kn = 0.0045;

%% Obtendo valores de Krl através do gráfico

Krl = 1.0; % ATUALIZAR

%% Contribuição do Conjunto Asa/Fuselagem

Cn_beta_wing_fus = -Kn*Krl*((S_lateral_fuselagem*L_fuselagem)/(S_wing*b_wing));

contribuicaoDirecionalAsaFuselagem = Cn_beta_wing_fus*[-5:0.5:5];

plot(contribuicaoDirecionalAsaFuselagem,'LineWidth', 3)
hold on

% Contribuição da Empenagem Vertical
AproximacaoFatorVertical = 0.724 + 3.06*((S_vt*S_wing)/(1)) + 0.4*(zw/alturaFuselagem)+0.009*Ar_wing;% obtido na página 44 de RicardoH_MONo
Cn_beta_vt = AproximacaoFatorVertical*V_vt*CL_alpha_vt;

contribuicaoDirecionalEmpenagem = Cn_beta_vt*[-5:0.5:5];

plot(contribuicaoDirecionalEmpenagem)

% Contribuição Total
contribuicaoDirecionalTotal = contribuicaoDirecionalAsaFuselagem + contribuicaoDirecionalEmpenagem;

plot(contribuicaoDirecionalTotal,'LineWidth', 3)

hold off
legend('Cont. Asa/Fuselagem', 'Cont. Vt', 'Total')

grid on
legend("Position", [0.64054,0.75997,0.24429,0.094877])
colorbar off
xlabel("\beta",'FontSize',20)
ylabel("C_l\beta",'FontSize',20)
ax = gca;
