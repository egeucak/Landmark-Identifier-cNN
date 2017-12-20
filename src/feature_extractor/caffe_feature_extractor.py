import numpy as np
import os, sys, getopt
import time
"""
#########################################################
#   Input file is a text file that has paths of images  #
#########################################################
"""
# Main path to your caffe installation
caffe_root = '/home/ege/caffe/'

# Model prototxt file
model_prototxt = caffe_root + 'models/resnet_152/ResNet-152-deploy.prototxt'

# Model caffemodel file
model_trained = caffe_root + 'models/resnet_152/ResNet-152-model.caffemodel'

# File containing the class labels
imagenet_labels = caffe_root + 'data/ilsvrc12/synset_words.txt'

# Path to the mean image (used for input processing)
mean_path = caffe_root + 'python/caffe/imagenet/ilsvrc_2012_mean.npy'

# Name of the layer we want to extract
layer_name = 'pool5'

#sys.path.insert(0, caffe_root + 'python')
import caffe

def main(argv):
    inputfile = 'input.txt'
    outputfile = 'output.npy'

    print ('Reading images from "', inputfile)
    print ('Writing vectors to "', outputfile)

    # Setting this to CPU, but feel free to use GPU if you have CUDA installed
    caffe.set_mode_gpu()
    # Loading the Caffe model, setting preprocessing parameters
    net = caffe.Classifier(model_prototxt, model_trained,
                           mean=np.load(mean_path).mean(1).mean(1),
                           channel_swap=(2,1,0),
                           raw_scale=255,
                           image_dims=(256, 256))

    # Loading class labels
    '''with open(imagenet_labels) as f:
        labels = f.readlines()'''

    # This prints information about the network layers (names and sizes)
    # You can uncomment this, to have a look inside the network and choose which layer to print
    #print ([(k, v.data.shape) for k, v in net.blobs.items()])
    #exit()

    weights = []

    # Processing one image at a time, printint predictions and writing the vector to a file
    with open(inputfile, 'r') as reader:
        with open(outputfile, 'w') as writer:
            writer.truncate()
            for image_path in reader:
                image_path = image_path.strip()
                input_image = caffe.io.load_image(image_path)
                prediction = net.predict([input_image], oversample=False)
                '''print("------")
                print (os.path.basename(image_path), ' : ' , ' (', prediction[0][prediction[0].argmax()] , ')')
                print(len(net.blobs[layer_name].data[0].reshape(1,-1)[0]))'''
                print("Doing the thing...")
                weights.append(net.blobs[layer_name].data[0].reshape(1,-1)[0])
                #np.savetxt(writer, net.blobs[layer_name].data[0].reshape(1,-1), fmt='%.8g')
                #print("------")
    weights = np.asarray(weights)
    np.save(outputfile, weights)

if __name__ == "__main__":
    main(sys.argv[1:])
