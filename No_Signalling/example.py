from no_signalling import no_signalling , chsh
from inequalities import *
import matplotlib.pyplot as plt

## Example for plotting triparty inequality vs biparty ( in this case svetlichny vs chsh )
## See available inequality functions from inequalities.py and set dx and lim accordingly

def __main__():   
  step = 0.5
  lim = 8
  conv = 1
  x = []
  y = []
  dx = -8
  while dx <= lim:
    P = no_signalling()
    P.create_optimize(chsh())
    temp = svetlichny_facet()
    P.add_inequality(temp,dx)
    for i in range(len(temp)):
      temp[i][3] = temp[i][3] * -1
    P.add_inequality(temp,-1*dx) 
    solutions = P.linear_prog()
    result = P.print_sol(solutions)
    print result
    x.append(dx)
    y.append(result)
    dx = dx + step  

  plt.plot(x,y)
  plt.show()   


if __name__=="__main__":
  __main__()


