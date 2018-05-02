from sympy import *

#q1L, q1H, q2 = symbols('q1L q1H q2')
#aH, aL, c, theta = symbols('aH, aL, c, theta', Integer= True)
#aH =4
#aL = 2
#theta = 2/3
#c =1
#solve([Eq(aH-q2-2*q1H-c, 0), Eq(aL-q2-2*q1L-c, 0), Eq(theta*(aH-q1H)-(1-theta)*(aL-q1L)-c-2*q2, 0)], [q1L, q1H, q2])

from pymprog import *
from scipy import optimize

#pi= symbols('pi')
#pjH, pjL,theta, bH, bL, a, c= symbols('pjH pjL theta bH bL a  c', Integer = True)
#eq1 = diff(theta*(pi-c)*(a-pi-bH*pjH)+(1-theta)*(pi-c)(a-pi-bH*pjL), pi)
#eq2 = diff(theta*(pi-c)*(a-pi-bL*pjH)+(1-theta)*(pi-c)(a-pi-bL*pjL), pi)

H = symbols('H')
P, A, alfa, bta, gama, omega, n = symbols('P, A, alfa, bta, gama, omega, n', Interger = True)
P = 22.9186
omega = 63.8756
gamma = 0.487
alfa = -0.0111
beta = 0.358
A = 2.467
n = 3070.28
H = (P*A*(alfa**alfa)*(bta**bta)*(gama**gama)*(P**(-bta))*(omega**(-alfa))*(n**(alfa+bta-1)))**((1-alfa-bta-gama)**(-1))
print(H)