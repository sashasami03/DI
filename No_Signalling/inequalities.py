
##Mermin game a xor b xor c = x.y.z
##limit : 0 - 8 ( divide by 8.0 to probability )

def mermin_game_1():
  mermin = []
  for x in range(2):
    for y in range(2):
      for z in range(2):
        for a in range(2):
	  for b in range(2):
	    for c in range(2):
	      if ( a ^ b ^ c ) == ( x * y * z):
	        mermin.append([[0,1,2],[x,y,z],[a,b,c],1])  	 
  return mermin


##Mermin game a xor b xor c = x.y xor y.z	
##limit : 0 - 8 ( divide by 8.0 to probability )
def mermin_game_2():
  mermin = []
  for x in range(2):
    for y in range(2):
      for z in range(2):
        for a in range(2):
	  for b in range(2):
	    for c in range(2):
	      if ( a ^ b ^ c ) == ( (x * y) ^ (y * z)  ):
	        mermin.append([[0,1,2],[x,y,z],[a,b,c],1])  	 
  return mermin


##Svetlichny game a xor b xor c = x.y xor y.z xor z.x
##limit : 0 - 8 ( divide by 8.0 to get probability )	
def svetlichny_game():
  stev = []
  for x in range(2):
    for y in range(2):
      for z in range(2):
        for a in range(2):
	  for b in range(2):
	    for c in range(2):
	      if ( a ^ b ^ c ) == ( (x * y) ^ (y * z) ^ (z * x)  ):
	        stev.append([[0,1,2],[x,y,z],[a,b,c],1])  	 
  return stev

##Mermin fact <A_1B_0C_0> + <A_0B_1C_0> + <A_0B_0C_1> - <A_1B_1C_1>	
##limit : -4 - 4 
def mermin_facet():
  mermin = []
  meas =[[1,0,0],[0,1,0],[0,0,1],[1,1,1]] 
  val = [1,-1] 
  for m in range(len(meas)):
    x = meas[m][0]
    y = meas[m][1]
    z = meas[m][2]
    for a in range(2):
      for b in range(2):
        for c in range(2):
          mermin.append([[0,1,2],[x,y,z],[a,b,c],val[a]*val[b]*val[c]*val[x*y*z]])	       
   
  return mermin

##Svetlichny facet
##limit : -8 - 8
def svetlichny_facet():
  mermin = []
  val = [1,-1]   
  for x in range(2):
    for y in range(2):
      for z in range(2):
	sign = (-1)**(x*y+y*z+z*x) 
        for a in range(2):
          for b in range(2):
            for c in range(2):
              mermin.append([[0,1,2],[x,y,z],[a,b,c],val[a]*val[b]*val[c]*sign])	       
   
  return mermin

##Chsh facet  <A_0B_0> + <A_1B_0> + <A_0B_1> - <A_1B_1>
##limit: -4 4
def chsh_facet():
  chsh = []
  parties = [0,1]
  meas =[[0,0],[1,0],[0,1],[1,1]]
  val = [1,-1]
  for m in range(len(meas)):
    x = meas[m][0]
    y = meas[m][1]
    for a in range(2):
      for b in range(2):
        chsh.append([parties,[x,y],[a,b],val[a]*val[b]*val[x*y]])
  return chsh


