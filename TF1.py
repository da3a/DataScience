import tensorflow as tf

hello = tf.constant('hello tensor flow!!!!')

sess = tf.Session()
print(sess.run(hello))

