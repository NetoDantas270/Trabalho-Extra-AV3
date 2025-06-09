import numpy as np
import matplotlib.pyplot as plt


class GlobalRandomSearch:
    def __init__(self,max_it,f,cidades,origem):
        
        self.max_it = max_it
        self.f = f
        self.origem = origem        
        self.cidades = np.vstack((origem,cidades))                
        self.x_opt = np.random.permutation(self.cidades.shape[0]-1)+1
        self.x_opt = np.concatenate((np.array([0]),self.x_opt))
        self.f_opt = self.f(self.cidades,self.x_opt)
        
        self.ax = plt.subplot()
        self.linhas = []
        self.ax.scatter(self.cidades[:,0],self.cidades[:,1])
        self.plot_opt()
        
        
        pass
    
    def plot_opt(self,cor='k'):
        if len(self.linhas)!=0:
            for linha in self.linhas:
                linha[0].remove()
            self.linhas = []
        for i in range(len(self.x_opt)):
            p1 = self.cidades[self.x_opt[i]]
            p2 = self.cidades[self.x_opt[(i+1)%len(self.x_opt)]]
            if i == 0:
                l = self.ax.plot([p1[0],p2[0]],[p1[1],p2[1]],c='g')
            elif i == len(self.x_opt)-1:
                l = self.ax.plot([p1[0],p2[0]],[p1[1],p2[1]],c='cyan')
            else:
                l = self.ax.plot([p1[0],p2[0]],[p1[1],p2[1]],c=cor)
            self.linhas.append(l)    
                
    def perturb(self):
        x_cand = np.random.permutation(self.cidades.shape[0]-1)+1
        x_cand = np.concatenate((np.array([0]),x_cand))
        return x_cand
    def busca(self):
        it = 0
        while it < self.max_it:
            x_cand = self.perturb()
          
                
            f_cand = self.f(self.cidades,x_cand)
            
            if f_cand < self.f_opt:
                self.x_opt = x_cand
                self.f_opt = f_cand
                self.plot_opt()   
                plt.pause(.5)    
            it+=1
        self.plot_opt(cor='pink')       
        plt.show()
            
            
class LocalRandomSearch:
    def __init__(self,max_it,trocas,f,cidades,origem):
        self.trocas = trocas
        self.max_it = max_it
        self.f = f
        self.origem = origem        
        self.cidades = np.vstack((origem,cidades))                
        self.x_opt = np.random.permutation(self.cidades.shape[0]-1)+1
        self.x_opt = np.concatenate((np.array([0]),self.x_opt))
        self.f_opt = self.f(self.cidades,self.x_opt)
        
        self.ax = plt.subplot()
        self.linhas = []
        self.ax.scatter(self.cidades[:,0],self.cidades[:,1])
        self.plot_opt()
        
        
        pass
    
    def plot_opt(self,cor='k'):
        if len(self.linhas)!=0:
            for linha in self.linhas:
                linha[0].remove()
            self.linhas = []
        for i in range(len(self.x_opt)):
            p1 = self.cidades[self.x_opt[i]]
            p2 = self.cidades[self.x_opt[(i+1)%len(self.x_opt)]]
            if i == 0:
                l = self.ax.plot([p1[0],p2[0]],[p1[1],p2[1]],c='g')
            elif i == len(self.x_opt)-1:
                l = self.ax.plot([p1[0],p2[0]],[p1[1],p2[1]],c='cyan')
            else:
                l = self.ax.plot([p1[0],p2[0]],[p1[1],p2[1]],c=cor)
            self.linhas.append(l)    
                
    def perturb(self):
        idx1,idx2 = (np.random.permutation(self.cidades.shape[0]-1)+1)[:2]
        x_cand = np.copy(self.x_opt)
        x_cand[idx1],x_cand[idx2] = x_cand[idx2],x_cand[idx1]

        return x_cand
    
    def busca(self):
        it = 0
        while it < self.max_it:
            x_cand = self.perturb()
                
            f_cand = self.f(self.cidades,x_cand)
            
            if f_cand < self.f_opt:
                self.x_opt = x_cand
                self.f_opt = f_cand
                self.plot_opt()   
                plt.pause(.5)    
            it+=1
        self.plot_opt(cor='pink')       
        plt.show()

class SimulatedAnnealing:
    def __init__(self, max_it, f, cidades, origem, temp_inicial, trocas, alfa=0.99):
        self.max_it = max_it
        self.f = f
        self.T = temp_inicial
        self.alfa = alfa
        self.trocas = trocas
        
        self.origem = origem
        self.cidades = np.vstack((origem, cidades))
        
        self.x_best = np.random.permutation(self.cidades.shape[0] - 1) + 1
        self.x_best = np.concatenate((np.array([0]), self.x_best))
        self.f_best = self.f(self.cidades, self.x_best)
        
        self.x_cand = np.copy(self.x_best)
        self.f_cand = self.f_best

        self.fig, self.ax = plt.subplots(1, 2, figsize=(16, 7))
        self.linhas = []
        
        self.ax[0].set_title("Melhor Rota Encontrada")
        self.ax[0].scatter(self.cidades[:, 0], self.cidades[:, 1])
        self.plot_opt()
        
        self.progress_history = []
        self.ax[1].set_title("Progresso do Custo (Distância)")
        self.ax[1].set_xlabel("Iteração")
        self.ax[1].set_ylabel("Melhor Distância")
        self.ax[1].grid(True)
        self.progress_line, = self.ax[1].plot([], [], 'b-')


    def plot_opt(self, cor='k'):
        if len(self.linhas) != 0:
            for linha in self.linhas:
                linha[0].remove()
            self.linhas = []
        for i in range(len(self.x_best)):
            p1 = self.cidades[self.x_best[i]]
            p2 = self.cidades[self.x_best[(i + 1) % len(self.x_best)]]
            ax_mapa = self.ax[0]
            if i == 0:
                l = ax_mapa.plot([p1[0], p2[0]], [p1[1], p2[1]], c='g')
            elif i == len(self.x_best) - 1:
                l = ax_mapa.plot([p1[0], p2[0]], [p1[1], p2[1]], c='cyan')
            else:
                l = ax_mapa.plot([p1[0], p2[0]], [p1[1], p2[1]], c=cor)
            self.linhas.append(l)

    def update_progress_plot(self):
        self.progress_line.set_xdata(range(len(self.progress_history)))
        self.progress_line.set_ydata(self.progress_history)
        self.ax[1].relim()
        self.ax[1].autoscale_view()

    def perturb(self):
        x_cand = np.copy(self.x_best)
        for _ in range(self.trocas):
            idx = np.random.choice(range(1, self.cidades.shape[0]), 2, replace=False)
            x_cand[idx[0]], x_cand[idx[1]] = x_cand[idx[1]], x_cand[idx[0]]
        return x_cand

    def busca(self):
        i = 0
        while i < self.max_it:
            self.x_cand = self.perturb()
            self.f_cand = self.f(self.cidades, self.x_cand)
            delta_f = self.f_cand - self.f_best
            
            if delta_f < 0 or np.random.rand() < np.exp(-delta_f / self.T):
                self.f_best = self.f_cand
                self.x_best = np.copy(self.x_cand)

                if delta_f < 0:
                    self.plot_opt()
                    self.update_progress_plot()
                    self.fig.canvas.draw()
                    self.fig.canvas.flush_events()
                    plt.pause(0.001)

            self.T *= self.alfa
            
            self.progress_history.append(self.f_best)
            i += 1

            if i % 100 == 0:
                 self.update_progress_plot()
                 plt.pause(0.001)

        print(f"Busca finalizada. Custo final: {self.f_best:.2f}")
        self.plot_opt(cor='pink')
        self.update_progress_plot() 
        self.fig.tight_layout() 
        plt.show()