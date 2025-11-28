import time

age = 1 # int.
name =  "Isabella" # string.


# prints, useful for displaying informations in the console.
print("---------------------")
print("My name is", name)
print("---------------------")
if age != 15: # if the variable age is different as 15, then it will execute from this:
    print("oops, I'm dumb asf, im still loading age...")
    age = 15
    time.sleep(4) # to this, (this is a 4 second timer)
if age == 15: # if the variable is 15, then it will execute from here
    print("I am", age, "years old.") # to here
    while age <= 29:
        age += 1
        print("---------------------")
        print("Going up...")
        print(age)   
        time.sleep(1.5)
print("---------------------")