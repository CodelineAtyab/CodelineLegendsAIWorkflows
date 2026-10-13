def pos_neg(a, b, negative):
  if (a<0 and b>0 and negative == False) or (a>0 and b<0 and negative == False) or a<0 and b<0 and negative == True:
    return True
  
  else:
    return False
