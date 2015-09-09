from no_signalling import no_signalling
from inequalities import *
import matplotlib.pyplot as plt
import sys

## Example for plotting triparty inequality vs biparty ( in this case svetlichny vs chsh )
## See available inequality functions from inequalities.py and set dx and lim accordingly

def __main__():   
  step = 0.1
  lim = 8
  conv = 1
  x = []
  y = []
  dx = 0
  while dx <= lim:

    P = no_signalling()
    P.create_objective(P.change_sign((chsh_facet(),0)))

    temp = svetlichny_facet()
    P.add_inequality((temp,dx)) 
    P.add_inequality(P.change_sign((temp,dx))) 
    

    solutions = P.linear_prog()

    if not solutions :
      print "Infeasible solution found for variable ( exiting )", dx
      break

    result = P.print_sol(solutions)
    print result , " for dx = " , dx
    P.print_tabs(solutions)
    P.print_ineq()

    x.append(dx)
    y.append(result * -1)

    dx = dx + step  

  plt.plot(x,y)
  plt.show()   


if __name__=="__main__":
  __main__()


