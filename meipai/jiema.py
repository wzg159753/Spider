


class Decode(object):

    def getHex(self, a):
        return {
            'str': a[4:],
            'hex': ''.join(list(a[:4])[:-1]) #.reverse().join("")
        }

    def decode(self, a):
        b = self.getHex(a)
        print(b)


if __name__ == '__main__':
    a = "6161aHR0cNCuduXDovL212dmlkZW8xMS5tZWl0dWRhdGEuY29tLzVjMmRlYWJlYTA5YzczZ3dmZmdsYWY3ODY5X0gyNjRfMV81ZjM4ZWU1NmE1NzVjZi5tcDQ/az0zYzJjYmVmOWI0ZDU2NmRlOTI5NGFhNzU0Mzc2M2Q1YiZ0PTVjMzJ3XH2kZmM3"
    dec = Decode()
    dec.decode(a)