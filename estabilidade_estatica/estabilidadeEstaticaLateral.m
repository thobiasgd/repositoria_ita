parametros
estabilidadeEstaticaDirecional

%% Contribuição do Conjunto Asa/Fuselagem

deltaClBeta_zw = ((1.2*sqrt(Ar_wing)/57.3))*(zw/b_wing)*(2*diametroMaximoFuselagem/b_wing);

Cy_beta_AsaFuselagem = (Cl_cruzeiro*-0.035) + deltaClBeta_zw; % Adquirido na pagina 48 de RicardoH_MONo

%% Contribuição da Empenagem Vertical

r1 = 0.082; % Metade da altura máxima da seção da fuselagem abaixo da empenagem vertical
termoObtencaoValorK = (b_vt*2)/(2*r1);
k = 0.8; % obtido pela figura 29 de RicardoH_MONo
Cy_beta_vt = -k*CL_alpha_vt*AproximacaoFatorVertical*(S_vt*S_wing)*((zv-lv*0.0872665)/b_wing);

%% Contribuição da Empenagem Vertical

cy_beta_total = Cy_beta_AsaFuselagem + Cy_beta_vt; % Valor deve ser negativo para que contribua positivamente para a estabilidade lateral. Fazer variar com CL_wing

%plot(((zv-lv*range_alpha_wing)/b_wing))



















