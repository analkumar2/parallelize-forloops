The aim here is to parallelize any for loop.
The primary fucntion you want ot use is Multiprocessthis_appendsave from the goMultiprocessing4.py script.
testMP2.py gives a simple example.
Do note that multiprocessing can be slower than 'for loops' if the task doesn't require enough CPU resources.