import os

def remove_files_from_directory(folder_name, folder_contents):
    for files in folder_contents:
        os.remove(folder_name + "/" + files)

if __name__ == "__main__":
    folder_names = ["./nn-data", "./keras-nn-data", "./rl-learning-data"]

    nn_data = os.listdir(folder_names[0])
    keras_nn_data = os.listdir(folder_names[1])
    rl_learning_data = os.listdir(folder_names[2])

    remove_files_from_directory(folder_names[0], nn_data)

    remove_files_from_directory(folder_names[1], keras_nn_data)

    remove_files_from_directory(folder_names[2], rl_learning_data)
