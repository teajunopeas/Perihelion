# Calculos para el primer més
tau = 3/4
p_0 = 26000
m_n = 0.25



p_n = p_0
p_n1 = 28000


delta_n = tau*(p_n - p_n1)/p_0

m_n1 = m_n * (delta_n + (delta_n**2 + 4 )**0.5)

print("m_n1:", m_n1)
