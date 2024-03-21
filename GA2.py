import openvsp as vsp 
import os
import numpy as np
import random
import math
from pandas import read_csv
import matplotlib.pyplot as plt

os.chdir("C:/MDO/Python/Algoritmo genético")
vsp.SetVSPAEROPath('C:/MDO/OpenVSP-Corrigido')

class Aircraft():
    def __init__(self, envergadura, lista_cordaInicial, aerofolio, lista_incidencia, sweepPrimeiraSec, geracao = 0, numeroIndividuo = 0):
        
        self.geracao = geracao
        self.numeroIndividuo = numeroIndividuo
        
        if self.geracao == 0:
            
            # --- ASA ---
            # Envergadura
            porcentagem = random.choice([0.4,0.45,0.5,0.55,0.6,0.65,0.7])
            self.envergadura_inicial = (random.choice(envergadura))
            self.primeiraEnvergadura = porcentagem*(self.envergadura_inicial/2)
            self.segundaEnvergadura = (1-porcentagem)*(self.envergadura_inicial/2)
            # Corda
            self.CordaPrimeiraSec = random.choice(lista_cordaInicial)
            self.CordaSegundaSecRoot = self.CordaPrimeiraSec
            self.CordaSegundaSecTip = random.uniform(0.3, 1)*self.CordaPrimeiraSec
            self.aerofolio = aerofolio
            # Sweep
            self.sweepSect01 = random.choice(sweepPrimeiraSec)
            sweepMaximo = float(math.degrees(math.atan(((self.CordaSegundaSecRoot-self.CordaSegundaSecTip)/self.segundaEnvergadura))))
            self.sweepSect02 = random.choice(np.arange(0.0,sweepMaximo))
            
        else:
            
            # --- ASA ---
            # Envergadura
            self.primeiraEnvergadura = envergadura[0]
            self.segundaEnvergadura = envergadura[1]
            self.envergadura_total = (self.primeiraEnvergadura + self.segundaEnvergadura)*2
            # Corda
            self.CordaPrimeiraSec = lista_cordaInicial[0]
            self.CordaSegundaSecRoot = self.CordaPrimeiraSec
            self.CordaSegundaSecTip = lista_cordaInicial[1]
            self.aerofolio = aerofolio
            # Sweep
            sweepMaximo = float(math.degrees(math.atan(((self.CordaSegundaSecRoot-self.CordaSegundaSecTip)/self.segundaEnvergadura))))
            self.sweepSect01 = sweepPrimeiraSec[0]            
            if sweepPrimeiraSec[1] > sweepMaximo:
                self.sweepSect02 = sweepMaximo
            else:
                self.sweepSect02 = sweepPrimeiraSec[1]
                
                
            
          
        self.incidenciaTotal = random.choice(lista_incidencia)
        self.incidenciaSec01 = self.incidenciaTotal
        self.incidenciaSec02 = self.incidenciaTotal
        self.incidenciaSec03 = self.incidenciaTotal
        
        # --- EMPENAGEM HORIZONTAL ----
        
        self.volumeHorizontal = 0
        self.cordaHorizontal = 0
        self.envergaduraHorizontal = 0
        
        # --- EMPENAGEM VERTICAL ------
        
        self.volumeVertical = 0
        self.cordaVertical = 0
        self.envergaduraVertical = 0
        
        # --- Simulação ----
        
        self.CLxAlpha = []
        self.CDoxAlpha = []
        
        # desempenh0
        
        self.distDecolagem = 0
        self.massaDecolagem = 0
        
        # avaliação
        
        self.nota_avaliacao = self.distDecolagem
        
        
        self.cromossomo = [[self.primeiraEnvergadura, self.segundaEnvergadura], [self.CordaPrimeiraSec,
                           self.CordaSegundaSecTip], [self.sweepSect01, self.sweepSect02]]
        
    def modelarAsa(self):
    
        
        # --------------------------- Adiciona e modela a asa ---------------------------------------------------------
        print( (" -- GN%sIND%s --" % (self.geracao,self.numeroIndividuo)))
        
        wing_id = vsp.AddGeom("WING")
        errorMgr.PopErrorAndPrint(stdout)
            
        vsp.SetGeomName(wing_id, "Asa inicial")
        errorMgr.PopErrorAndPrint(stdout)
            
        chord_id = vsp.GetParm(wing_id, "TotalChord", "WingGeom")
        vsp.SetParmVal(chord_id, self.CordaPrimeiraSec)
        xsec_surf = vsp.GetXSecSurf(wing_id, 0)
        vsp.InsertXSec( wing_id, 1, vsp.XS_FILE_AIRFOIL)
        vsp.ChangeXSecShape(xsec_surf, 0, vsp.XS_FILE_AIRFOIL)
        xsec = vsp.GetXSec(xsec_surf, 0);
        vsp.ReadFileAirfoil(xsec, self.aerofolio);
        vsp.ChangeXSecShape(xsec_surf, 1, vsp.XS_FILE_AIRFOIL)
        xsec = vsp.GetXSec(xsec_surf, 1)
        vsp.ReadFileAirfoil(xsec, self.aerofolio)
        xsec = vsp.GetXSec(xsec_surf, 2)
        vsp.ReadFileAirfoil(xsec, self.aerofolio)
            
        vsp.Update()
            
        sweep_sec1_wing = vsp.GetParm(wing_id, "Sweep", "XSec_1") # muda o sweep da seção 1
        vsp.SetParmVal(sweep_sec1_wing, self.sweepSect01)
        sweep_sec1_wing = vsp.GetParm(wing_id, "Sweep", "XSec_2") # muda o sweep da seção 1
        vsp.SetParmVal(sweep_sec1_wing, self.sweepSect02)
        sweep_sec1_wing = vsp.GetParm(wing_id, "Twist", "XSec_1") # muda a incidência da seção 1
        vsp.SetParmVal(sweep_sec1_wing, self.incidenciaSec02)
        sweep_sec1_wing = vsp.GetParm(wing_id, "Twist", "XSec_2") # muda a incidência da seção 1
        vsp.SetParmVal(sweep_sec1_wing, self.incidenciaSec03)
        vsp.Update()
            
        incidence_id = vsp.GetParm(wing_id, "Twist", "XSec_0")
        vsp.SetParmVal(incidence_id, self.incidenciaSec01)
        incidenceLOC_id = vsp.GetParm(wing_id, "Twist_Location", "Plan")
        vsp.SetParmVal(incidenceLOC_id, 0.25)
        vsp.Update()
            
        vsp.SetDriverGroup( wing_id, 1, vsp.AR_WSECT_DRIVER, vsp.ROOTC_WSECT_DRIVER, vsp.TIPC_WSECT_DRIVER )
        vsp.Update()
        vsp.SetParmVal( wing_id, "Root_Chord", "XSec_1", self.CordaPrimeiraSec )
        vsp.SetParmVal( wing_id, "Tip_Chord", "XSec_1", self.CordaSegundaSecRoot )
        vsp.Update()
        vsp.SetParmVal( wing_id, "Root_Chord", "XSec_2", self.CordaSegundaSecRoot )
        vsp.SetParmVal( wing_id, "Tip_Chord", "XSec_2", self.CordaSegundaSecTip )
        vsp.Update()

        vsp.SetParmVal( wing_id, "Span", "XSec_1", self.primeiraEnvergadura )
        vsp.SetParmVal( wing_id, "Span", "XSec_2", self.segundaEnvergadura )
        vsp.Update()

        separacao_id = vsp.GetParm(wing_id, "Y_Rel_Location", "XForm")
        vsp.SetParmVal(separacao_id, 0.05)
        vsp.Update()
        
        # --------------------------- Adiciona e modela a empenagem horizontal -------------------------------------------
         
        horizontal_id = vsp.AddGeom("WING")
        vsp.SetGeomName(horizontal_id, "Empenagem Horizontal")
        vsp.Update()
        
        # Parametros da asa para modelagem da empenagem
        Sw = vsp.GetParmVal(wing_id,"TotalArea", "WingGeom")
        Cw = vsp.GetParmVal(wing_id,"TotalChord", "WingGeom")
        bw = vsp.GetParmVal(wing_id,"TotalSpan", "WingGeom")
        ARw = bw/Cw
        
        # Parâmetros da empenagem horizontal
        #self.volumeHorizontal = random.choice([0.8,0.9,1.0,1.1])
        self.volumeHorizontal = random.choice([0.8]) #[0.8,0.9]
        bracoHistorico = 1.0
        #listaBracos = [bracoHistorico*1.1,bracoHistorico*1.05,bracoHistorico,bracoHistorico*0.95,bracoHistorico*0.90]
        listaBracos = [bracoHistorico*1.1,bracoHistorico*1.05,bracoHistorico]
        braco = random.choice(listaBracos)
        areaHozitonal = (Cw*Sw* self.volumeHorizontal)/braco
        ARh = (2/3)*ARw
        self.envergaduraHorizontal = math.sqrt(ARh*areaHozitonal)
        self. cordaHorizontal =  self.envergaduraHorizontal/ARh
        vsp.Update()
        
        # definindo altura segundo rosa pg129
        # Z = 0.2
        # lii = braco-(0.25*Cw)+(0.25*self.cordaHorizontal)
        # lRef = lii - 0.75*Cw
        # angDownWash = (0.10 + 0.5*5)
        # H = lRef*math.tan(angDownWash)
        # #print(H)
        
        # altura = (Z*Cw)-H
        #print(altura)
        altura = 0.15
        
        # Modelando a empenagem horizontal
        vsp.SetParmVal( horizontal_id, "Root_Chord", "XSec_1",  self.cordaHorizontal )
        vsp.SetParmVal( horizontal_id, "Tip_Chord", "XSec_1",  self.cordaHorizontal )
        spanH_id = vsp.GetParm(horizontal_id, "TotalSpan", "WingGeom")
        vsp.SetParmVal(spanH_id,  self.envergaduraHorizontal)
        
        bracoH_id = vsp.GetParm(horizontal_id, "X_Rel_Location", "XForm")
        vsp.SetParmVal(bracoH_id, braco)
        vsp.Update()
        
        alturaH_id = vsp.GetParm(horizontal_id, "Z_Rel_Location", "XForm")
        vsp.SetParmVal(alturaH_id, altura)
        vsp.Update()
        
        sweep_sec1_horizontal = vsp.GetParm(horizontal_id, "Sweep", "XSec_1") # muda o sweep da seção 1
        vsp.SetParmVal(sweep_sec1_horizontal, 0)
        vsp.Update()
        
        # --------------------------- Adiciona e modela a empenagem vertical -------------------------------------------
        self.volumeVertical = random.choice([0.07]) # [0.07,0.08,0.09]
        vertical_id = vsp.AddGeom("WING")
        vsp.SetGeomName(vertical_id, "Empenagem Vertical")
        
        anguloVertical_id = vsp.GetParm(vertical_id, "X_Rel_Rotation", "XForm")
        vsp.SetParmVal(anguloVertical_id, 90)
        vsp.Update()
        
        dist_vertical = vsp.GetParm(vertical_id, "Y_Rel_Location", "XForm")
        distancia = self.envergaduraHorizontal/2 + 0.015
        vsp.SetParmVal(dist_vertical, distancia)
        
        areaVertical = (bw*Sw* self.volumeHorizontal)/braco
        self.cordaVertical = self.cordaHorizontal
        ARv = 1.36
        self.envergaduraVertical = ARv*self.cordaVertical # TEM QUE MUDAR CARAMBA
        
        vsp.SetParmVal( vertical_id, "Root_Chord", "XSec_1",  self.cordaVertical )
        vsp.SetParmVal( vertical_id, "Tip_Chord", "XSec_1",  self.cordaVertical )
        spanV_id = vsp.GetParm(vertical_id, "TotalSpan", "WingGeom")
        vsp.SetParmVal(spanV_id,  self.envergaduraVertical)
        
        bracoV_id = vsp.GetParm(vertical_id, "X_Rel_Location", "XForm")
        vsp.SetParmVal(bracoV_id, braco)
        
        alturaV_id = vsp.GetParm(vertical_id, "Z_Rel_Location", "XForm")
        vsp.SetParmVal(alturaV_id, (-self.envergaduraVertical/4)+altura)
        
        sweep_sec1_horizontal = vsp.GetParm(vertical_id, "Sweep", "XSec_1") # muda o sweep da seção 1
        vsp.SetParmVal(sweep_sec1_horizontal, 0)
        
        # -------------------------------------------------------------------------------------------------------------
        if ((os.path.isdir("C:/MDO/Python/Algoritmo genético/GN%s" % (self.geracao))) == False):
            os.mkdir("C:/MDO\Python/Algoritmo genético/GN%s" % (self.geracao))
            
        os.mkdir("C:/MDO/Python/Algoritmo genético/GN%s/GN%sIND%s" % (self.geracao,self.geracao,self.numeroIndividuo))
        os.chdir("C:/MDO/Python/Algoritmo genético/GN%s/GN%sIND%s" % (self.geracao,self.geracao,self.numeroIndividuo))
        fname = "GN%sIND%s.vsp3" % (self.geracao,self.numeroIndividuo)
               
        sref=[float(0)]*1
        bref=[float(0)]*1
        cref=[float(0)]*1
        
        sref[0]=(vsp.GetParmVal(wing_id,"TotalArea", "WingGeom"))
        #print('Área de referencia: ' + str(sref))
        bref[0]=(vsp.GetParmVal(wing_id,"TotalSpan", "WingGeom"))
        cref[0]=(vsp.GetParmVal(wing_id,"TotalChord", "WingGeom"))

        vsp.WriteVSPFile(fname, vsp.SET_ALL)
        vsp.Update()
        
        # ------------------ SIMULANDO ----------- --------------------------------------------------------------------
    
        vsp.ClearVSPModel()
        vsp.Update()
        vsp.ReadVSPFile(fname)
        vsp.Update()

        compgeom_name = "VSPAEROComputeGeometry"

        #vsp.SetAnalysisInputDefaults(compgeom_name)
        vsp.SetDoubleAnalysisInput( compgeom_name, "AnalysisMethod", [vsp.VORTEX_LATTICE])
        vsp.SetDoubleAnalysisInput( compgeom_name, "GeomSet", [0])

        vsp.Update()

        rid = vsp.ExecAnalysis( compgeom_name )

        # -------------------------------------- ANÁLIZE VSPAEROSweep --------------------------------------

        vsp.ClearVSPModel()
        vsp.Update()
        vsp.ReadVSPFile(fname)
        vsp.Update()

        AEROVSP_analysis = "VSPAEROSweep"

        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, "AnalysisMethod", [vsp.VORTEX_LATTICE])

        vsp.Update()

        alphaStart = [-3]
        alphaEnd = [15]
        alphaPoints = [alphaEnd[0] - alphaStart[0] + 1]
        reynolds = [500000]

        geom_set = [0]
        vsp.SetIntAnalysisInput( AEROVSP_analysis, "GeomSet", geom_set)
        vsp.Update()
        ref_flag = [1]
        vsp.SetIntAnalysisInput( AEROVSP_analysis, "RefFlag", ref_flag)
        vsp.Update()
        wid = vsp.FindGeomsWithName( "Asa inicial" )
        vsp.Update()
        vsp.SetStringAnalysisInput( AEROVSP_analysis, "WingID", wid)
        vsp.Update()
        
        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, 'Sref', sref )
        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, 'bref', bref )
        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, 'cref', cref )
        vsp.SetIntAnalysisInput( AEROVSP_analysis, "RefFlag", ref_flag )

        # --------------------------------------------------------------

        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, "AlphaEnd", alphaEnd)
        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, "AlphaStart", alphaStart)
        vsp.SetIntAnalysisInput( AEROVSP_analysis, "AlphaNpts", alphaPoints)
        vsp.Update()

        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, "ReCref", reynolds)
        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, "Rho", [1.2])
        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, "Vinf", [14.22])
        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, "ReCref", [500000])

        vsp.SetDoubleAnalysisInput( AEROVSP_analysis, "Xcg", [0.170])

        vsp.Update()

        vsp.PrintAnalysisInputs(AEROVSP_analysis)

        Sweep_resid = vsp.ExecAnalysis(AEROVSP_analysis)
        vsp.PrintResults(Sweep_resid)
        
        print("Simulação " + ("GN%sIND%s.vsp3" % (self.geracao,self.numeroIndividuo)) + " concluída.")
        
        # ------------ Inserindo os coeficientes na classe -------------
        
        df = read_csv(("GN%sIND%s" % (self.geracao,self.numeroIndividuo) +"_DegenGeom.polar"), sep='\s+')
        #data = df.values
        
        N = abs(alphaStart[0]) + abs(alphaEnd[0]) + 1
        
        # print("Resultados de CL")
        for i in range(N):
            self.CLxAlpha.append(df.iloc[i][3])
            
        # print("Resultados de Cmy")   
        for i in range(N):
            self.CDoxAlpha.append(df.iloc[i][4])
            
        
        # --------------- Avaliação ------------------------------------
        
        MTOW = 15*9.81
        g = 9.81
        rho = 1.1
        sref = float(sref[0])
        mi = 0.035
        T = 43 #newtons
        pista = 52
        
        CLmax = max(self.CLxAlpha)
        #print('CL máximo: ' + str(CLmax))
        CL_5graus = self.CLxAlpha[1] # NA VERDADE É ANGULO 0 COM 5 DE INCIDENCIA
        #print('CL em 5º: ' + str(CL_5graus))
        CDo_5graus = self.CDoxAlpha[1]
        #print('CDo em 5º: ' + str(CDo_5graus))
        
        Vstall = math.sqrt((2*MTOW)/(rho*sref*CLmax))
       # print('Velocidade stall: ' + str(Vstall))
        V_decolagem = 1.2*Vstall
        #print('Velocidade de decolagem: ' + str(V_decolagem))
        
        # efeitoSolo = ((16*0.3/bref)**2)/(1+((16*0.3/bref)**2))
        # efeitoSolo = efeitoSolo*(CL_5graus/(math.pi*reynolds*))
        
        arrastoDecolagem = 0.5*rho*(V_decolagem**2)*sref*CDo_5graus#  usando 70% da velocidade de decolagem segunda a recomendação d anderson pg 524
        sustentacaoDecolagem = 0.5*rho*(V_decolagem**2)*sref*CL_5graus
        
        forcasHorizontais = T - (arrastoDecolagem + mi*(MTOW - sustentacaoDecolagem))
        
        self.distDecolagem = (1.44*(MTOW**2))/(g*rho*sref*CLmax*forcasHorizontais)
        pesoDecolagem = math.sqrt((((g*rho*sref*CL_5graus*T)*pista)/1.44))
        self.massaDecolagem = pesoDecolagem/g
        
        if self.distDecolagem > 55:
            self.distDecolagem = 1000
            
        self.nota_avaliacao = self.massaDecolagem/self.distDecolagem

        print("Peso de decolagem: " + str(round(self.massaDecolagem,2)) + 'kg')
        print('Distancia de pista: ' + str(round((self.distDecolagem),2)))
        print('')
        
        vsp.VSPRenew()   
        vsp.ClearVSPModel()
        vsp.Update()
                        
        # ----------- Operadores genéticos ----------------------------
        
        os.chdir("C:/MDO\Python/Algoritmo genético")
    def mutacao(self, taxaMutacao):
        idx = 0
        for idx in range(len(self.cromossomo)):
            
            if random.random() < taxaMutacao:
                               
                #print('MUTAÇÃO')
                 
                if idx == 0:  
                    #print(idx)
                    self.CordaSegundaSecTip = random.choice([0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])*self.CordaPrimeiraSec
                                      
                elif idx == 1:
                    #print(idx)
                    porcentagem = random.choice([0.4,0.45,0.5,0.55,0.6,0.65,0.7])
                    self.envergadura_total = (random.choice(envergadura))
                    self.primeiraEnvergadura = porcentagem*(self.envergadura_total/2)
                    self.segundaEnvergadura = (1-porcentagem)*(self.envergadura_total/2)
                     
                elif idx == 2:
                    #print(idx)
                    self.sweepSect02 = float(math.degrees(math.atan(((self.CordaSegundaSecRoot-self.CordaSegundaSecTip)/self.segundaEnvergadura))))
                     
            self.cromossomo = [[self.primeiraEnvergadura, self.segundaEnvergadura], [self.CordaPrimeiraSec,
                               self.CordaSegundaSecTip], [self.sweepSect01, self.sweepSect02]]
        return self
                     
    def crossover(self, outro_individuo, numeroIndividuo):
        print("CROSSOVER")
        
                
        corte = round(random.random() * len(self.cromossomo))
        cromossomo01 = outro_individuo.cromossomo[0:corte] + self.cromossomo[corte::]      
        cromossomo02 = self.cromossomo[0:corte] + outro_individuo.cromossomo[corte::]
        
        #filhos = [Aircraft(cromossomo01[0],cromossomo01[1],self.aerofolio, [self.incidenciaTotal], cromossomo01[2], self.geracao + 1,numeroIndividuo)]
        
        filhos = [Aircraft(cromossomo01[0],cromossomo01[1],self.aerofolio, [self.incidenciaTotal], cromossomo01[2], self.geracao + 1,numeroIndividuo),
                  Aircraft(cromossomo02[0],cromossomo02[1],self.aerofolio, [self.incidenciaTotal], cromossomo02[2], self.geracao + 1,numeroIndividuo+1)]
        
        # filhos[0] = filhos[0].mutacao(0.05)
        # filhos[1] = filhos[1].mutacao(0.05)
        
        filhos[0].modelarAsa()
        filhos[1].modelarAsa()

        return filhos
    
class AlgoritmoGenetico():
    def __init__(self, tamanhoPopulacao):
        
        self.tamanhoPopulacao = tamanhoPopulacao
        self.populacao = []
        self.geracao = 0
        self.melhor_solucao = 0 # é do tipo individuo/classe
        self.melhorCromossomo = []
        self.lista_solucoes = []
        
    def inicializa_populacao(self, envergadura, lista_cordaInicial, aerofolio, lista_incidencia,sweepPrimeiraSec): # criando a populacao
        for i in range(self.tamanhoPopulacao):
            vsp.VSPRenew()
            self.populacao.append(Aircraft(envergadura, lista_cordaInicial, aerofolio, lista_incidencia,sweepPrimeiraSec,0,i))
            self.populacao[i].modelarAsa()
            vsp.VSPRenew()
            self.melhor_solucao = self.populacao[0]
            
    def ordena_populacao(self):
        self.populacao = sorted(self.populacao, key = lambda populacao: populacao.nota_avaliacao, reverse = True)
        
    def melhor_individuo(self, individuo):
        if individuo.nota_avaliacao > self.melhor_solucao.nota_avaliacao:
            self.melhor_solucao = individuo
            
    def soma_avaliacoes(self):
        soma = 0
        for individuo in self.populacao:
            soma += individuo.nota_avaliacao  
        return soma
    
    def seleciona_pai(self, soma_avaliacao):
        pai = -1
        valor_sorteado = random.random()*soma_avaliacao
        soma = 0
        i = 0 
        while i < len(self.populacao) and soma < valor_sorteado:
            soma += self.populacao[i].nota_avaliacao
            pai += 1
            i += 1
        return pai
    
    def resolver(self, taxa_mutacao, envergadura, lista_cordaInicial, aerofolio, lista_incidencia, sweepPrimeiraSec):
        self.inicializa_populacao(envergadura, lista_cordaInicial, aerofolio, lista_incidencia, sweepPrimeiraSec)
        
        self.ordena_populacao()
        self.melhor_solucao = self.populacao[0]
        self.lista_solucoes.append(self.melhor_solucao.nota_avaliacao)
        
        iteracao = self.melhor_solucao.nota_avaliacao
        populacoesRestantes = 500
        
        while((populacoesRestantes > 0)):
            soma_avaliacao = self.soma_avaliacoes()
            nova_populacao = []
            
            # Realizando crossover
            numeroIndividuo = 0
            for u in range(round(len(self.populacao)/2)):
                
                pai1 = self.seleciona_pai(soma_avaliacao)
                pai2 = self.seleciona_pai(soma_avaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2], numeroIndividuo)

                nova_populacao.append(filhos[0])
                nova_populacao.append(filhos[1])
                
                #print(self.populacao)
                numeroIndividuo = numeroIndividuo + 2
                
            self.populacao = nova_populacao
                
            self.ordena_populacao()
            
            melhor = self.populacao[0]
            self.lista_solucoes.append(melhor.nota_avaliacao)
            self.melhor_individuo(melhor) # isso é uma função
            self.geracao += 1
            
            # print(list(np.arange(0,self.geracao)))            
            # print(self.lista_solucoes)
            plt.plot(list(np.arange(0,self.geracao+1)),self.lista_solucoes)
            plt.title("Progressão dos indivíduos")
            plt.xlabel("Geração", size = 16,)
            plt.ylabel("Nota de avaliação", size = 16)
            plt.savefig('progressao.png')
            plt.show()
            
            print(self.melhor_solucao)
                       
            if (melhor.nota_avaliacao < 1.1*(self.lista_solucoes[-1])):
                populacoesRestantes = populacoesRestantes - 1
            else:
                populacoesRestantes = 500

vsp.VSPRenew()

stdout = vsp.cvar.cstdout
errorMgr = vsp.ErrorMgrSingleton_getInstance()

vsp.VSPCheckSetup()
errorMgr.PopErrorAndPrint(stdout)

errorMgr.PopErrorAndPrint(stdout)

# ----------- Parâmetros --------------------

envergadura = [2]
cordasIniciais = list(np.arange(0.3,0.6,0.05))
aerofolio = "seligdatfile.dat"
incidencia = [5]
sweep01 = [0]
taxaMutacao = 0.05

# ------------- Parâmetros GA --------------

tamanhoPopulacao =  20 # TEM QUE SER PAR

# ------------------------------------------

GA = AlgoritmoGenetico(tamanhoPopulacao)
GA.resolver(taxaMutacao, envergadura, cordasIniciais, aerofolio, incidencia, sweep01)


# -----------------------------------------------------------------

teste = Aircraft([2], [0.3,0.2,0.1], 'seligdatafile.dat', [5], [0])
        
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        