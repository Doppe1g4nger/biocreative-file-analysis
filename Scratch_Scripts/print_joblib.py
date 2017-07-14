try:
    from machine_learning_tests import helper_functions as h
except ModuleNotFoundError:
    import helper_functions as h
from sklearn.externals import joblib

if __name__ == "__main__":
    for file in h.get_all_files("./"):
        thing = joblib.load(file)
        print(thing, type(thing))