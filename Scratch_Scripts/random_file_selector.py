import pickle
from random import randint
from random import shuffle
from timeit import default_timer

from machine_learning_tests.helper_functions import get_all_files

if __name__ == "__main__":
    base_path = "/data/Random FullText Selections/"
    path = input("Give path to directory to select random files from: ")
    file_load_start = default_timer()
    all_files = get_all_files(path)
    file_load_end = default_timer()
    print("Time to load files:", (file_load_end - file_load_start) / 60, "minutes")
    subset_size = 0
    one_run = True if input("One run? (y/n): ") == "y" else False
    if one_run:
        subset_size = int(input("Size of run?: "))
    while subset_size < len(all_files):
        process_start = default_timer()
        subset = set()
        shuffle(all_files)
        start_index = randint(0, len(all_files) - subset_size)  # Could remove, only improves perceived randomness.
        for random_choice in all_files[start_index:start_index + subset_size]:
            file_id = random_choice.split("/")[-1].strip(".txt")
            subset.add((file_id, random_choice))
        with open(base_path + "set_of_id_filepath_tuples_size_" + str(subset_size) + ".pkl", "wb") as outfile:
            pickle.dump(subset, outfile)
        process_end = default_timer()
        print("Time to process random batch of size {batch_size}:".format(batch_size=subset_size),
              (process_end - process_start) / 60, "minutes")
        subset_size += 10000
        if one_run:
            break
