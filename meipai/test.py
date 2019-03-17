import execjs


with open('aa.js', 'r') as f:
    result = execjs.compile(f.read())
a = "6161aHR0cNCuduXDovL212dmlkZW8xMS5tZWl0dWRhdGEuY29tLzVjMmRlYWJlYTA5YzczZ3dmZmdsYWY3ODY5X0gyNjRfMV81ZjM4ZWU1NmE1NzVjZi5tcDQ/az0zYzJjYmVmOWI0ZDU2NmRlOTI5NGFhNzU0Mzc2M2Q1YiZ0PTVjMzJ3XH2kZmM3"
print(result.call("decode", a))