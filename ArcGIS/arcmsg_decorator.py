import arcpy
import time
from functools import wraps

'''
A decorator that prints the function name, input, and run time 
to the console and in to python tool messages
'''

def arcmsg(func):

    def time_now():
        t = time.localtime()
        current_time = time.strftime("%D %H:%M:%S", t)
        return current_time

    @wraps(func)
    def wrapper(*args, **kwargs):

        arcpy.AddMessage(f'\n{time_now()} Start {func.__name__}')
        for a in args:
            arcpy.AddMessage(f'\t"{a}"')
        for kw in kwargs:
            arcpy.AddMessage(f'\t{kw}: "{kwargs[kw]}"')

        t1 = time.time()
        result = func(*args, **kwargs)
        seconds = time.time() - t1
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        arcpy.AddMessage(f'Completed {func.__name__} in: {int(h)}h {int(m)}m {round(s,2)}s\n')
        print('')

        return result

    return wrapper

# # Example 1
# @arcmsg
# def my_func(arg1, arg2=None):
#     # Code
#     return
# 
# my_func(arg1, arg2=10)

# Prints the following:
# 05/21/21 08:23:20 Start my_func
#     "arg1"
#     arg2: "10"
# 
# Completed my_func in: 0h 0m 1.20s


# # Example 2
# Buffer_msg = arcmsg(arcpy.analysis.Buffer)

# Buffer_msg(
#     "D:\gis_data\in_features",
#     "D:\gis_data\out_features",
#     line_buffer_Dist=1,
#     line_end_type="FLAT"
# )

# Prints the following:
# 05/21/21 08:23:20 Start arcpy.analysis.Buffer
#     "D:\gis_data\in_features"
#     "D:\gis_data\out_features"
#     line_buffer_Dist: "1""
#     line_end_type: "FLAT"
# 
# Completed my_func in: 0h 0m 1.20s
