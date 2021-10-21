import os
def file_sizes():
    return { filename: os.path.getsize(filename) for filename in os.listdir('.')}
