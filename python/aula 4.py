import random
import time

a = ["alhkahskhkasdfhlhfsda8uiy24789qw7oi74qy6759q484756918324987fyu0fadhjo!@#$%¨&*()¨$sed%rf&gyhiou&ïgt*oh","!@#$%¨&*()(*&¨%$#$%¨%$#$%¨&¨%$#@$%¨&*¨%$#@$%¨&*())","5678594325678954326578594367584367589483657849TYUR4JEFDCVBFHEDNJK","76tiyu25gtwe876fgyuhbk2jwg4evf!@!@#$%¨&*()RFTGYHUJYRDYFTGHJYCFHGV","HIHIHIHAAAAA"]
b = int

z = input("enter your password: \n > ")
c = "123deoliveira4"
if z == c:
    while True:
        x = int(input("pick a number: \n> "))

        if x % 2 == 0:
           print("it is an even number!")
        else:
           print("it is an odd number!")

        y = int(input("whats your age? \n > "))

        if y >= 18 and y <= 110:
            print("youre overage!")
        elif y <= 18 and y >= 0:
            print("youre underage!")
        else:
           print("are you lying? if yes ure a nig-")
           break
else:
    print("wrong moderfocka-")
    time.sleep(3)
    while True:
        time.sleep(0.0000005)
        b = random.randint(0,4)
        print(a[b])