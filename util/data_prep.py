import numpy as np
import shutil
import os


def create_directory(data_dir):
    if data_dir.count('/') > 1:
        try:
            shutil.rmtree(data_dir, ignore_errors=False)
        except FileNotFoundError:
            pass
        os.makedirs(data_dir)
        print("Successfully cleaned directory " + data_dir)
    else:
        raise ValueError("Refusing to delete testing data directory " + data_dir + " as we prevent you from doing stupid things!")


def create_category_subdir(data_dir, category_name):
    data_category_dir = data_dir + '/' + category_name
    if not os.path.exists(data_category_dir):
        os.mkdir(data_category_dir)


def split_files_into_test_train(training_data_dir, testing_data_dir, subdir, file, testing_data_pct):
    input_file = os.path.join(subdir, file)
    if np.random.rand(1) < testing_data_pct:
        shutil.copy(input_file, testing_data_dir + '/' + os.path.basename(subdir) + '/' + file)
        return 0, 1
    else:
        shutil.copy(input_file, training_data_dir + '/' + os.path.basename(subdir) + '/' + file)
        return 1, 0


def split_dataset_into_test_and_train_sets(all_data_dir, training_data_dir, testing_data_dir, testing_data_pct):

    create_directory(testing_data_dir)
    create_directory(training_data_dir)

    num_training_files = 0
    num_testing_files = 0

    for subdir, dirs, files in os.walk(all_data_dir):
        category_name = os.path.basename(subdir)

        # Don't create a subdirectory for the root directory
        if category_name == os.path.basename(all_data_dir):
            continue

        create_category_subdir(training_data_dir, category_name)
        create_category_subdir(testing_data_dir, category_name)

        for file in files:
            test_count, train_count = split_files_into_test_train(training_data_dir, testing_data_dir,subdir, file,
                                                                  testing_data_pct)
            num_testing_files += test_count
            num_training_files += train_count

    print("Processed " + str(num_training_files) + " training files.")
    print("Processed " + str(num_testing_files) + " testing files.")


def main():
    full_dataset_dir = "../data/full/"
    training_data_dir =  "../data/train"
    testing_data_dir = "../data/val"
    testing_pct = 0.1
    split_dataset_into_test_and_train_sets(full_dataset_dir, training_data_dir, testing_data_dir, testing_pct)


if __name__ == "__main__":
    main()