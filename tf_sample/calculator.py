import tensorflow as tf

class Model(object):
    num1 = 0
    num2 = 0

    @property
    def num1(self) -> int: return self._num1

    @num1.setter
    def num1(self, num1): self._num1 = num1

    @property
    def num2(self) -> int: return self._num2

    @num2.setter
    def num2(self, num2): self._num2 = num2

class Service(object):

    this = Model()

    @tf.function
    def plus(self, num1, num2): return tf.add(num1, num2)

    @tf.function
    def minus(self, num1, num2): return tf.subtract(num1, num2)

    @tf.function
    def multiple(self, num1, num2): return tf.multiply(num1, num2)

    @tf.function
    def div(self, num1, num2): return tf.divide(num1, num2)

if __name__ == '__main__':
    model = Model()
    service = Service()

    def menu():
        model = Model()
        service = Service()

        def print_menu():
            print('0. 종료')
            print('+')
            print('-')
            print('*')
            print('/')
            return input('메뉴 입력\n')

        while 1:
            num1 = input('숫자1 입력\n')
            a = tf.constant(int(num1))
            menu = print_menu()
            num2 = input('숫자2 입력\n')
            b = tf.constant(int(num2))
            if menu == '+':
                print('a + b = {}'.format(service.plus(a, b)))
            if menu == '-':
                print('a - b = {}'.format(service.minus(a, b)))
            if menu == '*':
                print('a * b = {}'.format(service.multiple(a, b)))
            if menu == '/':
                print('a / b = {}'.format(service.div(a, b)))
            elif menu == '0':
                break

