The aim here is to parallelize any for loop.
The primary fucntion you want ot use is Multiprocessthis_appendsave from the goMultiprocessing.py script.
testMP.py gives a simple example.
Do note that multiprocessing can be slower than 'for loops' if the task doesn't require enough CPU resources.
