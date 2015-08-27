from inequalities import *
from cvxopt import matrix , solvers
from sympy import Symbol
import matplotlib.pyplot as plt
import numpy
import sys



class no_signalling:
   
  ##concatenate list to string
  def lis_to_string(self,lis):
    string = ""
    for i in range(len(lis)):
      string = string + str(lis[i])   
    return string 
  
  ##to change the sign of co-efficients of an expression
  def change_sign(self,terms):
    temp = terms[:]
    for i in range(len(temp)):
      temp[i][3] = -1 * temp[i][3]
    return temp  
       
       
  

  ##running linear prog
  def linear_prog(self):
    A = matrix(self.a)
    B = matrix(self.b)
    C = matrix(self.c)
    A = matrix.trans(A)
    A = A * 1.0
    B = B * 1.0
    C = C  * 1.0 
    sol = solvers.lp(C,A,B)
    return sol['x'] 

  ##printing contraint matrix and all inequalities
  def print_ineq(self):
    for i in range(len(self.a)):
       print self.a[i]
    print self.b
    for i in range(len(self.a)):
       ineq = 0        
       for j in range(26):
	  ineq = ineq + self.a[i][j] * self.dic_var_nam[self.dic_var_idx[j]]
       print ineq," <= ",self.b[i]


  ##printting the solution and optimum value
  def print_sol(self,sol):
    for i in range(26):
       print self.dic_var_idx[i]," = ",sol[i]
    result = 0
    for i in range(26):
       result = result + self.c[i]*sol[i]  
    print "Result is ", result * -1 + self.const    
    return result * -1 + self.const


  ##creating variable names
  def create_string(self,p,m,o):
     parties = ""
     meas = ""
     out = ""
     for i in range(len(p)):
       parties = parties + str(p[i])
     for i in range(len(m)):
       meas = meas + str(m[i])
     for i in range(len(o)):
       out = out + str(o[i])
     return "p_(" + parties + ")_(" + meas + ")_(" + out + ")" 
   
  
  ## for adding inequalities from outside
  def add_inequality(self,terms,lesthn):
    val = lesthn
    ineq = []
    for i in range(len(terms)):
       par = self.lis_to_string(terms[i][0])
       meas = self.lis_to_string(terms[i][1])
       out = self.lis_to_string(terms[i][2])
       coff = terms[i][3]
       val =val + coff * self.tab_3[(par,meas,out)][1] * -1
       for j in range(len(self.tab_3[(par,meas,out)][0])):
	   
         temp = coff * self.tab_3[(par,meas,out)][0][j][3]
	 add = self.tab_3[(par,meas,out)][0][j][:]
         add[3] = temp	
	 ineq.append(add)
    self.create_inequality(ineq,val)		
      
       

         
       
  ## creating inequality and appending the same to a and b matrices     
  def create_inequality(self,ineq,val):
     temp = 26 * [0]
     for i in range(len(ineq)):
       var = self.create_string(ineq[i][0],ineq[i][1],ineq[i][2])
       temp[self.dic_var[var]] = temp[self.dic_var[var]] + ineq[i][3]

     self.a.append(temp)
     self.b.append(val)


  ##for specifyinh objective function from outside
  def create_objective(self,terms,constn):
    val = constn
    self.const = 0
    ineq = []
    for i in range(26):
      self.c[i] = 0
    for i in range(len(terms)):
       par = self.lis_to_string(terms[i][0])
       meas = self.lis_to_string(terms[i][1])
       out = self.lis_to_string(terms[i][2])
       coff = terms[i][3]
       val =val + coff * self.tab_3[(par,meas,out)][1] 
       for j in range(len(self.tab_3[(par,meas,out)][0])):
	   
         temp = coff * self.tab_3[(par,meas,out)][0][j][3]
	 add = self.tab_3[(par,meas,out)][0][j][:]
         add[3] = temp	
	 ineq.append(add)
    self.const = val
    self.create_optimize(ineq)		


  ##creating of optimum function c   
  def create_optimize(self,ineq):
   
     for i in range(len(ineq)):
       var = self.create_string(ineq[i][0],ineq[i][1],ineq[i][2])
       self.c[self.dic_var[var]] = self.c[self.dic_var[var]] + ineq[i][3]
     print "objective ",self.c       


  ##initialization   
  def __init__(self):

    self.tab_3 = {}
    self.dic_var = {}
    self.dic_var_idx = {}
    self.dic_var_nam = {}
    self.a = []
    self.b = []
    self.c = 26 * [0]
    self.const = 0
    self.optimize_sign = -1
    idx = 0
    selection = [1,2,4,3,5,6,7]
    for i in range(len(selection)):
       which_selected = []
       temp_var = selection[i]

       for j in range(3):
         if temp_var % 2 == 1:
           which_selected.append(j)
         temp_var = temp_var/2
       for j in range(2**(len(which_selected))):
         meas = []
         out = []
         m = j
         for l in range(len(which_selected)):
           meas.append(m % 2)
           out.append(0)
           m = m/2
         meas.reverse() 
         var = self.create_string(which_selected,meas,out)
         self.dic_var[var] = idx
         self.dic_var_idx[idx] = var
         self.dic_var_nam[var] = Symbol(var)	 
         idx = idx + 1
    
    for p in range(3):
      for x in range(2):
        tab_num = str(x)
        par = str(p)
        self.tab_3[(par,tab_num,"0")] = ([[[p],[x],[0],1]],0)   
        self.tab_3[(par,tab_num,"1")] = ([[[p],[x],[0],-1]],1)   

   	   
    for p1 in range(3):
      for p2 in range(p1+1,3,1):
        for x in range(2):
          for y in range(2):
            tab_num = str(x) + str(y)
	    par = str(p1) + str(p2)
            self.tab_3[(par,tab_num,"00")] = ([[[p1,p2],[x,y],[0,0],1]],0)   
            self.tab_3[(par,tab_num,"10")] = ([[[p1,p2],[x,y],[0,0],-1],[[p2],[y],[0],1]],0)   
            self.tab_3[(par,tab_num,"01")] = ([[[p1,p2],[x,y],[0,0],-1],[[p1],[x],[0],1]],0)   
            self.tab_3[(par,tab_num,"11")] = ([[[p1,p2],[x,y],[0,0],1],[[p2],[y],[0],-1],[[p1],[x],[0],-1]],1)

    for x in range(2):
       for y in range(2):
	  for z in range(2):
	      tab_num = str(x) + str(y) +str(z)
	      self.tab_3[("012",tab_num,"000")] = ([[[0,1,2],[x,y,z],[0,0,0],1]],0)   
	      self.tab_3[("012",tab_num,"100")] = ([[[1,2],[y,z],[0,0],1],[[0,1,2],[x,y,z],[0,0,0],-1]],0)  
              self.tab_3[("012",tab_num,"010")] = ([[[0,2],[x,z],[0,0],1],[[0,1,2],[x,y,z],[0,0,0],-1]],0)   
              self.tab_3[("012",tab_num,"110")] = ([[[0,1,2],[x,y,z],[0,0,0],1],[[1,2],[y,z],[0,0],-1],[[0,2],[x,z],[0,0],-1],[[2],[z],[0],1]],0)   
              self.tab_3[("012",tab_num,"001")] = ([[[0,1],[x,y],[0,0],1],[[0,1,2],[x,y,z],[0,0,0],-1]],0)
              self.tab_3[("012",tab_num,"101")] = ([[[1],[y],[0],1],[[1,2],[y,z],[0,0],-1],[[0,1],[x,y],[0,0],-1],[[0,1,2],[x,y,z],[0,0,0],1]],0)   
              self.tab_3[("012",tab_num,"011")] = ([[[0],[x],[0],1],[[0,2],[x,z],[0,0],-1],[[0,1],[x,y],[0,0],-1],[[0,1,2],[x,y,z],[0,0,0],1]],0)   
              self.tab_3[("012",tab_num,"111")] = ([[[0],[x],[0],-1],[[1],[y],[0],-1],[[2],[z],[0],-1],[[1,2],[y,z],[0,0],1],[[0,2],[x,z],[0,0],1],[[0,1],[x,y],[0,0],1],[[0,1,2],[x,y,z],[0,0,0],-1]],1)             
	    

    for x in range(2):
       for y in range(2):
	  for z in range(2):
	     for a in range(2):
		for b in range(2):
		   for c in range(2):
                     self.add_inequality([[[0,1,2],[x,y,z],[a,b,c],-1]],0)             







