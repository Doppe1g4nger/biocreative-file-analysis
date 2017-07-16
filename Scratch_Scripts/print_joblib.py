try:
    from machine_learning_tests import helper_functions as helpers
except ModuleNotFoundError:
    import helper_functions as helpers

from sklearn.externals import joblib

if __name__ == "__main__":
    for file in helpers.get_all_files("./"):
        thing = joblib.load(file)
        print(thing, type(thing))
