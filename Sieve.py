#Algorithm:
# 1) Mark 0 and 1 as being special. Remember 2 as the current prime.
# 2) Mark the current prime. Starting there, step through list with step size equal to the current prime, marking each one traversed as composite.
# 3) Starting above the current prime, find the lowest unmarked number. This number is the new current prime. 
#    Remember it, mark it prime, and go back to 2. If there are no more unmarked numbers, we are done.
Unknown=0
Prime=1
Composite=2
Special=3
n=1000
numbers=[Unknown]*n
numbers[0]=Special
numbers[1]=Special
CurrentPrime=2
done=False
while not done:
    numbers[CurrentPrime]=Prime 
    for CurrentComposite in range(CurrentPrime*2,n,CurrentPrime):
        numbers[CurrentComposite]=Composite
    done=True
    for candidate in range(CurrentPrime+1,n):
        if numbers[candidate]==Unknown:
            done=False
            CurrentPrime=candidate
            break
for candidate in range(0,n):
    if numbers[candidate]==Prime:
        print(candidate);
