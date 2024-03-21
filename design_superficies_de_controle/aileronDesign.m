parametros

ca_cw = 0.25;
thetaA = 0.45; % eficiencia do aileron retirada do gráfico das relações de corda superficie de controle e asa

deflexaoMaximaAileron = 25/57.3; % convertido para radiano

yi = 0.75*(b_wing/2);
yo = (b_wing/2);
yD = 0.4*(b_wing/2);

Cl_theta_aileron1 = (2*CL_alpha_wing*thetaA*c_wing_base)/(S_wing*b_wing); % taxa de variação do coeficiente de momento do aileron
Cl_theta_aileron2 = (((yo^2)/2)+((2/3)*((afilamento-1)/b_wing))*((yo)^3)) - (((yi^2)/2)+((2/3)*((afilamento-1)/b_wing))*((yi)^3));
Cl_theta_aileron = Cl_theta_aileron1 * Cl_theta_aileron2;

Cl_aileron = Cl_theta_aileron * deflexaoMaximaAileron;% coeficiente de momento gerado pelo aileron quando na maxima deflexão

L_aileron_maximo = 0.5*rho*(V_approach^2)*S_wing*Cl_aileron*b_wing; % momento gerado pelo aileron quando na maxima deflexão

Pss = sqrt((2*L_aileron_maximo)/(rho*(S_wing+S_ht+S_vt)*0.9*(yD^3))); % rad/s

bankAngle = ((I_XX)/(rho*(yD^3)*(S_wing+S_ht+S_vt)*0.9))*log(Pss^2);
Pponto = (Pss^2)/(2*bankAngle);

tempoBanckAngle = sqrt((2*bankAngle)/Pponto); % ESSE TEMPO DEVE SER MENOR QUE O REQUERIDO PELA TABELA DO SADRAEY, REFAÇA

tempoGrafico = 0:0.02:5;
anguloBankGrafico = 0:(30/(length(tempoGrafico)-1)):30;

for i=1:length(tempoGrafico)
    a(i) = ((tempoGrafico(i)^2)*Pponto);
end

plot(tempoGrafico,a)

grid on
xlabel("t(s)",'FontSize',20)
ylabel("\phi",'FontSize',20)




