import tensorflow as tf
import numpy as np
import os

def imdb_load_data_local(root_dir, subdir) :
    
    data_dir = os.path.join(root_dir, subdir)

    labels = []
    texts = []

    for label_type in ['neg', 'pos']:
        dir_name = os.path.join(data_dir, label_type)
        for fname in os.listdir(dir_name):
            if fname[-4:] == '.txt':
                f = open(os.path.join(dir_name, fname))
                texts.append(f.read())
                f.close()
                if label_type == 'neg':
                    labels.append(0)
                else:
                    labels.append(1)
    
    return (texts, labels)

def imdb_load_data(max_words, imdb_dir="./aclImdb") :
    
    arg_max_words = max_words
    
    training_samples = 25000  # We will be training on 25000 samples
    test_samples = 25000  # We will be testing on 25000 samples

    try :
        max_words_tf = arg_max_words
        
        imdb = tf.keras.datasets.imdb

        (train_data_tf, train_labels_tf), (test_data_tf, test_labels_tf) = imdb.load_data(num_words=max_words_tf)
    
        word_index_tf = imdb.get_word_index()
        
        word_index_tf = {k:(v+3) for k,v in word_index_tf.items()} 
        word_index_tf["<PAD>"] = 0
        word_index_tf["<START>"] = 1
        word_index_tf["<UNK>"] = 2  # unknown
        word_index_tf["<UNUSED>"] = 3

        reverse_word_index_tf = dict([(value, key) for (key, value) in word_index_tf.items()])

        max_words = max_words_tf
    
        train_data = train_data_tf
        train_labels = train_labels_tf
        test_data = test_data_tf
        test_labels = test_labels_tf

        word_index = word_index_tf
        reverse_word_index = reverse_word_index_tf
    
    except :
        max_words_local = arg_max_words+1
        
        train_texts_local, train_labels_local =  imdb_load_data_local(imdb_dir, "train")
        test_texts_local, test_labels_local =  imdb_load_data_local(imdb_dir, "test")
        
        texts = []
        texts.extend(train_texts_local)
        texts.extend(test_texts_local)
        
        labels = []
        labels.extend(train_labels_local)
        labels.extend(test_labels_local)
        
        
        tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=max_words_local)
        tokenizer.fit_on_texts(texts)
        sequences = tokenizer.texts_to_sequences(texts)

        word_index_local = tokenizer.word_index
        tokenizer.word_index["<PAD>"] = 0
        
        reverse_word_index_local = dict([(value, key) for (key, value) in word_index_local.items()])
        
        data = np.asarray(sequences)
        labels = np.asarray(labels)
        
        train_data_local = data[:training_samples]
        train_labels_local = labels[:training_samples]
        test_data_local = data[training_samples: training_samples + test_samples]
        test_labels_local = labels[training_samples: training_samples + test_samples]

        max_words = max_words_local
    
        train_data = train_data_local
        train_labels = train_labels_local
        test_data = test_data_local
        test_labels = test_labels_local

        word_index = word_index_local
        reverse_word_index = reverse_word_index_local
        
    
    train_tup = (train_data, train_labels)
    test_tup = (test_data, test_labels)
    index_tup = (word_index, reverse_word_index)

    return (train_tup, test_tup, index_tup, max_words)