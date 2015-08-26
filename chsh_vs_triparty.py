from __future__ import print_function
import matplotlib.pyplot as plt
from ncpol2sdpa import SdpRelaxation, solve_sdp, Probability

def expectation_value_tri(P, input_):
    vals = [-1, 1]
    return sum(a*b*c*P([a, b, c], input_) for a in vals for b in vals for c in vals)

def expectation_value_bi(P, input_ , parties):
    vals = [-1, 1]
    return sum(a*b*P([a, b], input_ ,parties) for a in vals for b in vals )

def chsh(P):
   return expectation_value_bi(P, [0,0] ,['A','B']) + expectation_value_bi(P, [0, 1],['A','B']) + \
      expectation_value_bi(P, [1,0],['A','B']) - expectation_value_bi(P, [1, 1],['A','B'])

def mermin(P):   
   return expectation_value_tri(P, [1, 0, 0]) + expectation_value_tri(P, [0, 1, 0]) + \
      expectation_value_tri(P, [0, 0, 1]) - expectation_value_tri(P, [1, 1, 1])

def svetlichny(P):   
  Stev = 0
  for x in range(2):
    for y in range(2):
      for z in range(2):
	Stev = Stev + (-1)**( x*y + y*z + z*x )* expectation_value_tri(P,[x,y,z]) 
  return Stev

def __main__():   
  # chsh quantum bound : 4
  # mermin quantum bound : 4
  # svetlichny quantum bound 4sqrt(2) ~ 5.65 

  P = Probability([2, 2], [2, 2], [2, 2])
  Chsh = chsh(P)
  Mermin = mermin(P)
  Svetlichny = svetlichny(P)
   
  dx = 0
  div = 1.0
  step = 0.4
  lim = 5.6
  x = []
  y = []
  while dx  <= lim :
  
    print (dx)
    ineq = []
    ineq.append(Svetlichny - dx)
    ineq.append(-1*Svetlichny + dx)
    sdpRelaxation = SdpRelaxation(P.get_all_operators(), verbose=0)
    sdpRelaxation.get_relaxation(2, substitutions = P.substitutions,inequalities = ineq)
    sdpRelaxation.set_objective(-Chsh)
    solve_sdp(sdpRelaxation, solver="cvxopt")
    x.append(dx)
    y.append(abs(sdpRelaxation.primal)/div)
    dx = dx + step 

  plt.plot(x,y,'k')   
  plt.show()   

if __name__=="__main__":
   __main__()
