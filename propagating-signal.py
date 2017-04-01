from matplotlib import pyplot

# initial conditions
y = [0] * 1000
y[480:520] = [1] * 40

# time-step
dt = 0.01

# our rule for reaction-diffusion
def advance(dt):
	global y
	n = len(y)
	new_y = list(y)
	for j in xrange(n):
		new_y[j] += dt * (20 * (y[j - 1] - 2 * y[j] + y[(j + 1) % n])
						   - y[j] * (1 - y[j]) * (0.3 - y[j]))
	y = new_y

# advance through t (t = i * dt) is at least 100; plot
# every 20
i = 0
while i * dt <= 100:
	if i * dt % 20 == 0:
		pyplot.plot(y, label='t = %g' % (i * dt))
	advance(dt)
	i += 1
	print i * dt

pyplot.legend()
pyplot.show()