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


class Lawyer(object):
    def __init__(self,LawyerID,Firm):
        self.LawyerID = LawyerID
        self.Firm = Firm
        self.partner = 0 # No one starts as a partner
        self.skill = random.gauss(80,20) # For now, just to put a number
        self.bar = random.randint(0,10) # Years after passing the bar
        self.firmxp = 0 # Years of experience in the firm.
        self.performance = self.skill + self.bar + self.firmxp # This is main attribute
    
    # What happens at every time step for each Lawyer
    def step(self):
        self.workwithpal()
        self.update()
    
    def workwithpal(self):
        partner = random.sample(self.Firm.lawyers, 1)
        self.skill += (0.2 * partner[0].performance) #Learn from teamwork, which is interaction of the agents
    
    def update(self):
        self.performance = self.skill + self.bar + self.firmxp
        self.bar += 1
        self.firmxp += 1


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
    # Here, the no. of lawyers who leave should vary
    n_start = len(self.lawyers)
    for aLawyer in self.lawyers:
        if aLawyer.partner == 0 and ((0.5 * aLawyer.bar) + aLawyer.firmxp) >= 10:
            self.lawyers.remove(aLawyer)
            elif aLawyer.partner == 0 and aLawyer.firmxp >= 10:
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
    skills = []
    for aLawyer in self.lawyers:
        skills.append(aLawyer.skill)
        mean_skill = stats.mean(skills)
        stddev_skill = stats.stdev(skills)
        n_lawyers = len(self.lawyers)
        print('Mean of All Agents Skill Score: ' , mean_skill)
        print('Standard Deviation of Agent Skill Score: ' , stddev_skill)
        print('Number of Laywers in the Firm: ', n_lawyers)
        print('\n')


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


