parametros

H = lref * tan(downwash(Cl_cruzeiro,Ar_wing));% altura do downwash até uma parada lá
Z = (H+H_ht)/corda_media_aerodinamica; % Analizar gráfico de eficiencia da empenagem

% OBS: para conseguir o valor abaixo, deve-se analisar o gráfico de
% eficiência da empenagem

eficienciaEmpenagem = 0.95;

%% Estabilidade Longitudinal Estática

% Contribuição da empenagem horizontal
Cm0_ht = (-V_ht*eficienciaEmpenagem*CL_ht_0)+(V_ht*eficienciaEmpenagem*CL_alpha_ht*(((downwash0 + iw - iht)/57.3)));
Cm_alpha_ht = -V_ht*eficienciaEmpenagem*CL_alpha_ht*(1-downwashVar);
contribuicaoLongitudinalEmpenagem = Cm0_ht + Cm_alpha_ht*range_alpha_wing;

%% Plotando gráficos

hold on

% Contribuição da asa
Cm0_wing = Cm_ac_wing + CL_wing_0*margemCgAc; % VERIFICAR posição CG e AC - respectivamente
Cm_alpha_wing = CL_alpha_wing*margemCgAc;
contribuicaoLongitudinalAsa = Cm0_wing + Cm_alpha_wing*range_alpha_wing;


% Contribuição total
Cm0_total = Cm0_ht + Cm0_wing;
Cm_alpha_total = Cm_alpha_ht + Cm_alpha_wing;

contribuicaoLongitudinalTotal = Cm0_total + Cm_alpha_total*range_alpha_wing;

%% Plotando gráficos

if a == a
    plot(range_alpha_wing*(57.3),contribuicaoLongitudinalEmpenagem,'LineWidth', 3)
    plot(range_alpha_wing*(57.3),contribuicaoLongitudinalAsa,'LineWidth', 3)
    plot(range_alpha_wing*(57.3),contribuicaoLongitudinalTotal,'LineWidth', 3)
    
    legend('Cont. Ht','Cont Asa', 'Total')
    
    grid on
    legend("Position", [0.64054,0.75997,0.24429,0.094877])
    colorbar off
    xlabel("\alpha",'FontSize',20)
    ylabel("C_m\alpha",'FontSize',20)
end

hold off








