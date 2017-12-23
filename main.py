import search

halls = ["64degrees", "canyonvista","cafeventanas","foodworx","64","cv",\
  "cafev","garbage","oceanview","ovt","64north","pines","goodys","clubmed",\
  "roots","bistro",]

def main():
    search.Listener()

def help():
	print("I need help")


answer = search.wait_until(100)
print(answer)
