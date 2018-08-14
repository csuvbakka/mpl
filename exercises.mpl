Exercise:
Sum a list of numbers. Only multiples of three are considered in the sum, e.g. 3, 6, 9, 12, ...

bool multiple_of_three(int num):
    return num % 3 == 0

input = array<int>{2, 3, 5, 7, 12, 13, 8, 1, 10, 27}
input | filter(multiple_of_three) | reduce(sum)

s = 0
for elem in input:
    if multiple_of_three(elem):
        s += elem

struct Sum:
    T sum
    void operator()(T elem):
        sum += elem

    T result():
        return sum

T reduce(container, fun)
where
    fun is ReduceFn
requires container is Iterable
:
    for elem in container:
        fun(elem)

    return fun.result()
