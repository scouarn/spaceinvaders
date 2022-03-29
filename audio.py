import platform
os = platform.system() 


# if os == "Windows" :
# 	import winsound

# 	print("Warning : windows audio implementation not tested !")

# 	def play_wav(fname) :
# 		winsound.Playsound(fname, 
# 			winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NOSTOP
# 		)

# 	def stop_all() :
# 		winsound.PlaySound(None, winsound.SND_PURGE)


if os == "Linux" :
	import subprocess

	processes = []


	def play_wav(fname) :
		volume = 75
		p = subprocess.Popen(
			['ffplay', '-nodisp', '-autoexit', '-volume', str(volume), fname],
			stdout=subprocess.DEVNULL,
			stderr=subprocess.DEVNULL,
		)

		processes.append(p)


	def stop_all() :
		while processes :
			processes.pop().kill()


else :
	print("Warning : audio not supported on this platform.")

	def play_wav(fname) :
		pass

	def stop_all() :
		pass
