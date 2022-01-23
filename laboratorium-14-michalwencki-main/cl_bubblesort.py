from array import array


def cl_bubblesort(input_array:array)-> array:
    n = len(input_array)
    output_array=input_array.copy()
    while(n>1):
        for i in range(0, n-1):
            if (output_array[i]>output_array[i+1]):
                output_array[i], output_array[i+1] = output_array[i+1], output_array[i]
        n=n-1
    return output_array