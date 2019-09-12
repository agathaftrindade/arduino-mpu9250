import turtle
import serial
import time
import numpy as np
import pandas as pd

bob = turtle.Turtle()
bob.shape("turtle")
bob.color('red', 'yellow')
bob.begin_fill()


dir = 1
ax, ay, az = 0, 0, 0
gx, gy, gz = 0, 0, 0


time.sleep(1)

def read_serial():
	with serial.Serial('/dev/ttyACM0', 115200, timeout=1) as ser:
		while True:
			line = ser.readline().decode()	# read a '\n' terminated line
			line = str(line).strip('\r\n').split("\t")
			# print(line)
			if len(line) < 3: continue

			ax = float(line[0])
			ay = float(line[1])
			az = float(line[2])

			# gx = float(line[3])
			# gy = float(line[4])
			# gz = float(line[5])
			gx = 0
			gy = 0
			gz = 0

			yield ax, ay, az, gx, gy, gz

def main():
	start_time = time.time()

	base_a = []
	base_g = []
	# for ax, ay, az, gx, gy, gz in read_serial():
	# 	base_a.append((ax, ay, az))
	# 	base_g.append((gx, gy, gz))
	# 	if time.time() - start_time > 5:
	# 		break
	# base_a = pd.DataFrame(base_a)
	# base_g = pd.DataFrame(base_g)

	# base_a.to_csv('base_a.csv', header=False, index=False)
	# base_g.to_csv('base_g.csv', header=False, index=False)

	base_a = pd.read_csv('base_a.csv')
	base_g = pd.read_csv('base_g.csv')

	print('calibrated')

	a_means, a_stds = base_a.mean(axis=0), base_a.std(axis=0)
	g_means, g_stds = base_g.mean(axis=0), base_g.std(axis=0)

	ax_mean, ay_mean, az_mean = a_means
	ax_std, ay_std, az_std = a_stds

	gx_mean, gy_mean, gz_mean = g_means
	gx_std, gy_std, gz_std = g_stds

	print(gx_mean, gx_std)

	for ax, ay, az, gx, gy, gz in read_serial():
		x, y = bob.pos()
		# print(ax, ax_mean, ax_std)


		SENSIBILITY = 5

		ax_high = ax > ax_mean + ax_std * SENSIBILITY
		ay_high = ay > ay_mean + ay_std * SENSIBILITY
		az_high = az > az_mean + az_std * SENSIBILITY

		ax_low = ax < ax_mean - ax_std * SENSIBILITY
		ay_low = ay < ay_mean - ay_std * SENSIBILITY
		az_low = az < az_mean - az_std * SENSIBILITY

		dir_code = ''.join((
			'H' if ax_high else 'L' if ax_low else '.',
			'H' if ay_high else 'L' if ay_low else '.',
			'H' if az_high else 'L' if az_low else '.',
		))
		print(dir_code)

		if dir_code == '...':
			pass
		elif dir_code == '.HH' and x > -250:
			bob.setheading(180)
			bob.forward(10)
		elif dir_code == '.LH' and x < 250:
			bob.setheading(0)
			bob.forward(10)
		elif dir_code == 'H.H' and y > -350:
			bob.setheading(270)
			bob.forward(10)
		elif dir_code == 'L.H' and y < 350:
			bob.setheading(90)
			bob.forward(10)


main()

turtle.end_fill()
turtle.done()

