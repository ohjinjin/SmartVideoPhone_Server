# SmartVideoPhone_Server
SmartVideoPhone for Women

The server recognizes the face using the Harr Cascade algorithm with OpenCV.

## collect datas for training
We can get 30 images for training like following image after executing **collect_datas.py**


![ex_captureImage1](./collecting_ex1.jpg)


collect training datas by detecting only the face part while shooting like this :


![ex_datafortrain](./1.2.jpg)

then the set of datas for training is created.

## train datas for training
run **recognize.py** after run **train_datas.py** to training using these datas.
We can see the face recoginition works well.

![ex_captureImage2](./test_ex1.jpg)

More datas Better result.
