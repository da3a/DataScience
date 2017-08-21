import tensorflow as tf

hello = tf.constant('hello tensor flow!!!!')

sess = tf.Session()
print(sess.run(hello))

a = tf.constant(1)
b = tf.constant(2)

print('a + b = {0}'.format(sess.run(a+b)))