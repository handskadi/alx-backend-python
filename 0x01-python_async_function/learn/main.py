import asyncio

#define an asynchronous function
#we do not create asynchronous modules/the whole program won't be asynchronous, only the  functions needed to be
async def main():
    task = asyncio.create_task(func2())#once we have idle time, we are goin to call that task
    print("A")
    await asyncio.sleep(1) #the await says that we are goin to wait for this to be done
    #we are going to wait for this statement to run, and not do anything else. this is key because we only do async if a program is wasting time
    #this is idle time, hence task is called
    print("B")
    return_val = await task
    print("return: {}".format(return_val))

async def func2():
    print("1")
    await asyncio.sleep(2)
    #since this is sleeping to, when it goes to sleep, main continues but func2 wont e completed, 
    #to allow func2 to run, you can wait for it after main completes
    print("2")
    return 10

asyncio.run(main())