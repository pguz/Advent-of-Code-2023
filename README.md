# Advent of Code 2023

As written in the [Wikipedia](https://en.wikipedia.org/wiki/Advent_of_Code)
> Advent of Code is an annual set of Christmas-themed computer programming challenges that follow an Advent calendar

My solutions to the [Advent of Code 2023](https://adventofcode.com/2023) are written in Python.

## Running code
The code was written using `Python 3.8.10`, however it should be compatible with the default `python3` command.

To run the solution for a given day for a given task firstly place input data in the AoC-file-specific format inside inputs directory in the naming referring to the given day ie. `09.txt` and then run simply:
```sh
python3 run_solution.py --day 09 --task 02
```
The output is the duration of calculations:
```sh
day_09_task_02 took 0.00646[s]
```

By default the solution is run 100 times to have a stabilized duration result. However there is a possibility to set it to your needs:
```sh
python3 run_solution.py --day 09 --task 02 --retry 10
```

You may want to check the calculated result with the expected one. In that case run:
```sh
python3 run_solution.py --day 09 --task 02 --expected-result 100
```
There is also created results.json file, where you can set all calculated results. Thanks to that the message will be displayed if the calculated result will not match the result from the file.

To run all tasks, the special script has been created:
```sh
./run_all.sh
```
