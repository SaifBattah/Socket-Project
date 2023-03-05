from socket import *

serverPort = 6500
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
data = []


def readfile():
    """Read the data of items from the items.txt"""
    file = open("items.txt", "r")
    info = file.readlines()
    for line in info:  
        li = line.replace("\n", "") 
        li = li.split(";")
        li[1] = int(li[1])
        data.append(li)

print("The server is ready to receive")

readfile()

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    print("IP: " + addr[0] + ", Port: " + str(addr[1]))
    print(sentence)
    ip = addr[0]
    port = addr[1]
    string_list = sentence.split(' ')  # Split request from spaces
    method = string_list[0]
    requestFile = string_list[1]
    connectionSocket.send(f"HTTP/1.1 200 OK\r\n".encode())
    file = requestFile.split('?')[0]  # symbol doesn't matter after ?
    file = file.lstrip('/')
    try:
        if file == '':
            file = 'main.html'  # main page
        elif file == 'sortbyname' or file == 'sortbyprice':
            # if the user requests to sort the Brands, it will enter this IF condition
            if file == 'sortbyname':
                # Sort the data according to the names ascending
                data.sort()
                outstring='<html><head><style>#brands {border-collapse: collapse;}#brands td,#brands th { border: 1px solid lightgrey;padding: 10px; } #brands tr:hover { background-color: greenyellow;}#brands th {padding-top: 14px;padding-bottom: 14x;text-align: center;color: white;}</style></head><body><center><h1>Sort By Name</h1><table id="brands"><tr style="background-color: black;"><th>Brand</th><th>items</th><th>Price</th></tr>'
            else:
                # ascending the data according to the prices
                data.sort(key=lambda data: data[1])
                outstring = '<html><head><style>#brands {border-collapse: collapse;}#brands td,#brands th { border: 1px solid lightgrey;padding: 10px; } #brands tr:hover { background-color: greenyellow;}#brands th {padding-top: 14px;padding-bottom: 14x;text-align: center;color: white;}</style></head><body><center><h1>Sort By Price</h1><table id="brands"><tr style="background-color: black;"><th>Brand</th><th>items</th><th>Price</th></tr>'
            # We will use sort.html to show our sorted data
            file = 'sort.html'
            for Brand in data:
                # FOR loop used to replace the brands for the items and in the right place
                if str(Brand[0]).startswith("Football"):
                    outstring += '<tr><th style="width: 10%"><img src="F.png" style="width: 50px"></th>'
                elif str(Brand[0]).startswith("Chevrolet"):
                    outstring += '<tr><th style="width: 10%"><img src="C.jpg" style="width: 50px"></th>'
                elif str(Brand[0]).startswith("Xiaomi"):
                    outstring += '<tr><th style="width: 10%"><img src="X.png" style="width: 50px"></th>'
                elif str(Brand[0]).startswith("Messi"):
                    outstring += '<tr><th style="width: 10%"><img src="M.png" style="width: 50px"></th>'
                else:
                    outstring += '<tr><th style="width: 10%"><img src="S.jpg" style="width: 50px"></th>'
                outstring += '<td>' + Brand[0] + '</td><td>$' + str(Brand[1]) + '</td></tr>'
            outstring += "</table></center></body></html>"
            # sort.html will overwrite the outString
            f = open("sort.html", "w")
            f.write(outstring)
            f.close()
        # file will be opened and read in byte
        requestFile = open(file, 'rb')
        response = requestFile.read()
        requestFile.close()
        # this if for any picture request in the project
        if file.endswith(".jpg"):
            connectionSocket.send(f"Content-Type: image/jpeg \r\n".encode())
        elif file.endswith(".png"):
            connectionSocket.send(f"Content-Type: image/png \r\n".encode())
        elif file.endswith(".css"):
            connectionSocket.send(f"Content-Type: text/css \r\n".encode())
        else:
            connectionSocket.send(f"Content-Type: text/html \r\n".encode())
    except Exception as e:
        # the error page with our names and IDs
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = ('<html><head><title>Error 404</title></head><body><br><br><br><br><center><div style="border: 3px solid black"><div><h2 style="color: red">The file is not found</h2></div><div><img src="error.jpg" align=center height="250px"></div><div><p>IDs and Names of project partners:</p><li><b>Ali Siaj 1190408</b></li><li><b>Imran Jerjawe 1190095</b></li><li><b>Saif Battah 1170986</b></li></div></div></center></body></html>' + str(
            ip) + ', Port: ' + str(port) + '</h2></center></body></html>').encode('utf-8')
    connectionSocket.send(f"\r\n".encode())
    connectionSocket.send(response)
    connectionSocket.close()