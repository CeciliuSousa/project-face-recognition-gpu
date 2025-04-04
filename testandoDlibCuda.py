import dlib
print(dlib.DLIB_USE_CUDA)  # Deve dar True
print(dlib.cuda.get_num_devices())  # Deve dar 1 (ou mais)