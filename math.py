def angleFromMaximas(x1, x2, L):
	dist = abs(x1 - x2)
	opp = dist/2
	angle = arcsin(opp/L)
	return angle
	
def maximumHeight(alpha, L):
	return L*L*cos(alpha)
	
def bottomVelocity(alpha, L):
	return sqrt(2*9.81 * L * (1-cos(alpha)))
	

	
