#CSS 605 Agent Based model
#Promotion and Fire Model
#Valentin, Richard
''''' Version 5 of the model
    Policy A,
    Lawyers working with each other,
    after their working,
    lawyers with the performance score greater than the 90th percentiles of all agents will stay and promote to frim partner.
    Other lawyers will leave the firm.
    Policy B,
    Lawyers working with each other,
    after their working,
    fire the last five percentiles of the lawyers based on their skill scores and hire new lawyers.
    '''''

import random
import statistics as stats
import numpy as np

# Define Agents Class
# Define and their attributes and behaviors.
Avg_P = 0

class Lawyer(object):
    def __init__(self,LawyerID,Firm):
        self.LawyerID = LawyerID
        self.Firm = Firm
        self.partner = 0 # No one starts as a partner
        self.skill = random.gauss(80,20) # For now, just to put a number
        self.xp = random.randint(0,10) # Years after passing the bar
        self.performance = self.skill + self.xp # This is main attribute
        self.per = random.randint(0,1)#personalities
    
    # What happens at every time step for each Lawyer
    def step(self):
        self.workwithpal()
        self.update()
    
    def workwithpal(self):
        perf = []
        top50 = []
        bottom = []
        top10 = []
        mid =[]
        
        for i in self.Firm.lawyers:
            perf.append(i.performance)
            if i.performance > np.percentile(perf,50):
                top50.append(i)
            
            if i.performance < np.percentile(perf, 20):
                bottom.append(i)
            
            if i.performance > np.percentile(perf, 10):
                top10.append(i)
            
            if i.performance > np.percentile(perf, 20) and i.performance < np.percentile(perf, 90):
                mid.append(i)
    
        if self.performance > np.percentile(perf, 10):
            partner = random.sample(self.Firm.lawyers, 1)
            #inidividualist
            if self.per == 0 or self.LawyerID == partner[0].LawyerID:
                self.skill += (0.1 * partner[0].performance) #Learn from teamwork, which is interaction of the agents
            # collectivist
            if self.per == 1:
                self.skill += (0.2 * partner[0].performance)

        if self.performance < np.percentile(perf, 20):
            partner = random.sample(top50, 1)
            #inidividualist
            if self.per == 0 or self.LawyerID == partner[0].LawyerID:
            self.skill += (0.1 * partner[0].performance) #Learn from teamwork, which is interaction of the agents
            # collectivist
            if self.per == 1:
                self.skill += (0.2 * partner[0].performance)

        if self.performance >= np.percentile(perf, 20) and self.performance <= np.percentile(perf, 90):
            partner = random.sample(mid, 1)
            #inidividualist
            if self.per == 0 or self.LawyerID == partner[0].LawyerID:
            self.skill += (0.1 * partner[0].performance) #Learn from teamwork, which is interaction of the agents
            # collectivist
            if self.per == 1:
                self.skill += (0.2 * partner[0].performance)

    def update(self):
        self.performance = self.skill + self.xp
        self.xp += 1
        perf = []
        for i in self.Firm.lawyers:
            perf.append(i.performance)
        Avg_P = stats.mean(perf)
        if self.performance > Avg_P:#how to get the average
            self.per = 0
        else:
            self.per = 1


# Firm Class
class Firm(object):
    def __init__(self):
        self.lawyers = [Lawyer(x,self) for x in range(100)] # Create 100 agents
    
    def stepA(self): # Time step for firm with Policy A
        self.work()
        self.promote()
        self.leave()
        self.hireA()
        self.results()
    
    def stepB(self): # Time step for firm with Policy B
        self.work()
        self.fire()
        self.hireB()
        self.results()
    
    def work(self):
        for aLawyer in self.lawyers:
            aLawyer.step() # Teamwork and Updates

    def promote(self): # Function for making partners
        tmp_prom = []
        for aLawyer in self.lawyers:
            if aLawyer.partner == 0:
                tmp_prom.append(aLawyer.performance)
        for aLawyer in self.lawyers:
            if aLawyer.performance >= np.percentile(tmp_prom,90):
                aLawyer.partner = 1

    def fire(self):
        # There should always leave the same amount of lawyers.
        n_start = len(self.lawyers)
        tmp_fire = []
        for aLawyer in self.lawyers:
            if aLawyer.partner == 0:
                tmp_fire.append(aLawyer.performance)
            for aLawyer in self.lawyers:
                if aLawyer.performance <= np.percentile(tmp_fire, 10):
                    self.lawyers.remove(aLawyer)
        n_fin = len(self.lawyers)
        n_delta = n_start - n_fin
        print("Start: %i Finish: %i There are total %i leaving the Firm" %(n_start, n_fin, n_delta))

    def leave(self):
        n_start = len(self.lawyers)
        for aLawyer in self.lawyers:
            if aLawyer.partner == 0 and (0.5 * aLawyer.xp) >= 10:
                self.lawyers.remove(aLawyer)
            elif aLawyer.partner == 0 and aLawyer.xp >= 10:
                self.lawyers.remove(aLawyer)
        n_fin = len(self.lawyers)
        n_delta = n_start - n_fin
        print("Start: %i Finish: %i There are total %i leaving the Firm" %(n_start, n_fin, n_delta))

    def hireA(self):
        tmp_id = []
        tmp_nopar = []
    
        for aLawyer in self.lawyers:
            tmp_id.append(aLawyer.LawyerID)
            if aLawyer.partner == 0: # store IDs of lawyers
                tmp_nopar.append(aLawyer.LawyerID)
        for aLawyer in self.lawyers: # Change partners ID
            # Lawyers with ID in the 100s are promoted partners
            while (aLawyer.partner == 1) and (aLawyer.LawyerID in tmp_id):
                aLawyer.LawyerID = random.randint(100,1000)
        for k in range(100-len(tmp_nopar)):
            # Lawyers with ID in the 1000s are new hires
            self.lawyers.append(Lawyer(random.randint(1000,10000),self))

    def hireB(self):
        tmp_lst = list(range(100)) # List with IDs 0 to 99
        tmp_id = [] # Empty list, will be filled with IDs after Leave()
        for aLawyer in self.lawyers:
            tmp_id.append(aLawyer.LawyerID)
        for k in tmp_lst:
            if k not in tmp_id:
                self.lawyers.append(Lawyer(k,self)) # Replace Lawyers

    def results(self):
        performance = []
    
        for aLawyer in self.lawyers:
            performance.append(aLawyer.performance)
        
        mean_peformance = stats.mean(performance)
        stddev_performance = stats.stdev(performance)
        n_lawyers = len(performance)
        print('Mean of All Agents Skill Score: ' , mean_peformance)
        print('Standard Deviation of Agent Skill Score: ' , stddev_performance)
        print('Number of Laywers in the Firm: ', n_lawyers)
        print('\n')
    
    def SaveReport2File(self,fileName):
        
        # open a file for writing
        fileObj = open(fileName, 'w')  # 'w' open for writing mode
        
        # write aggregate varables at each step to the file
        # prepare the lines to write
        lineList = []
        
        # add header first
        lineList.append("step;TotalIncome;TotalRiceProduction;\n")
        
        # add aggregate variables at each tiem step
        numSteps = len(self.totalIncomeHis)
        for i in range(numSteps):
            #oneLine = str(i) + ';' + str(self.totalIncomeHis[i]) + ';' + str(self.totalRiceProductionHis[i]) + ';' + '\n'
            oneLine = "%s;%0.2f;%0.2f;\n" %(i,self.totalIncomeHis[i],self.totalRiceProductionHis[i])
            lineList.append(oneLine)
        
        # write all the lines to a file
        fileObj.writelines(lineList)
        
        # close a file
        fileObj.close()

class Sim(object):
    def __init__(self):
        self.firm = Firm()
    
    def runA(self):
        print("+++++++++++++++++++++++++++++++++++++++", "POLICY A", "+++++++++++++++++++++++++++++++++++++++++")
        for years in range(10):
            print('=====================================', 'YEAR', years, '===================================')
            self.firm.stepA()
    def runB(self):
        print("+++++++++++++++++++++++++++++++++++++++", "POLICY B", "+++++++++++++++++++++++++++++++++++++++++")
        for years in range(10):
            print('=====================================', 'YEAR', years, '===================================')
            self.firm.stepB()

# Main function
if __name__ == '__main__':
    aSim = Sim()
    aSim.runA()
    bSim = Sim()
    bSim.runB()

