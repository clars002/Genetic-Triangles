# Genetic-Triangles

Usage
--------------------------------------
This is a Python program that relies on the Pillow 10.4.0 package. To start, you’ll need to install that in your local environment, either with ‘pip install pillow’ or ‘pip install requirements’ (the latter must be from the root directory of the program, where the requirements.txt resides).
The main driver is found in the src/generate_image.py file. To execute the program with the default parameters, ensure that Python is installed, then simply run ‘python src/generate_image.py’ from the root directory of the program.
There are several optional arguments:

‘--image [IMAGE]’, where [IMAGE] is the path to the desired input image (to be imitated by the genetic algorithm). By default, this is “src/resources/images/bunny.png”. Please note that execution times grow exponentially larger as the input image grows in resolution (16x16 to 32x32 is most reasonable).

‘--triangles [TRIANGLES]’, where [TRIANGLES] is the number of triangles per individual image in the population. This has a fairly heavy effect on runtimes, and the default is 24.

‘--population [POPULATION]’, where [POPULATION] is the number of individuals in the population each generation. This, too, has a heavy performance impact, and the default is 64.

‘--generations [GENERATIONS]’, where [GENERATIONS] is the number of generations after which the program automatically stops. By default, this is 50000, but this many generations can take a while.

‘--scaling_factor [SCALING_FACTOR]’, where [SCALING_FACTOR] is the power to which individuals’ selection weights are exponentiated before selection. By default, this is 50, in order to create a strong selection pressure.

‘--mutation_rate [MUTATION_RATE]’, where [MUTATION_RATE] is the portion of triangles which will be randomly altered every generation on average. A triangle selected for mutation can have any of its vertices randomly moved as well as its color randomly altered. By default, this is 0.01 (relatively low so as to encourage eventual convergence). This parameter has a heavy performance impact.

‘--crossover_rate [CROSSOVER_RATE]’, where [CROSSOVER_RATE] is the portion of all possible parent combinations that will reproduce on average each generation. By default, this is 0.02 (testing seems to show that relatively low values work well with the other default parameters). This parameter has a heavy performance impact.

‘--throttle [THROTTLE]’, where [THROTTLE] is the portion of CPU time to sleep relative to running the algorithm (e.g. a value of 1 would result in about 50% of the CPU utilization you’d experience with a value of 0). By default, this is 0, equivalent to no throttling at all. A value of .5 or more may help CPU utilization and temperatures (albeit while slowing the program about 25%).

‘--output_interval [OUTPUT_INTERVAL], where [OUTPUT_INTERVAL] is the number of generations to skip between outputting images and CLI text. By default, this is 10, so the output folder will get a new image every 10 generations.

Running the program with no extra arguments is equivalent to:
‘python src/generate_image.py --image resources/images/bunny.png --triangles 24 --population 64 --generations 50000 --scaling_factor 50 --mutation_rate 0.01 --crossover_rate 0.02 --throttle 0 --output_interval 10’
--------------------------------------
Thank you for your time!
