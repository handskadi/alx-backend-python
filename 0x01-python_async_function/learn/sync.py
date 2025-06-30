import asyncio


#to create a coroutine, you create a function with async which creates a rapper around that function and hence
#returns a coroutine object when the function is called.
#the object returned can be executed and to execute a coroutine object you need to  await it
async def main():
    print("main")
    text = "foo"
    task = asyncio.create_task(foo(text))#tells python to execute this function when its processes take a break
    #await task #if we add this statement to the one above, it says, wait for this task to complete before continuing
    await asyncio.sleep(2)#task will get executed here since its currently set to be executed as soon as possible and since
    #here we have paused the function, we now allow the task to run
    print("finished")


async def foo(text):
    print(text)
    #pause the execution of this function by a second
    await asyncio.sleep(1)# returns a sort of coroutine that is executed by await. and now, await will work since its inside an async func


asyncio.run(main())
#to run int we use asyncio.run and pass it a coroutine. which will be the async before it
#to use await keyword it has to be inside an async function
#this here will not run our code since wwe need to create an async event loop
"""await main()"""