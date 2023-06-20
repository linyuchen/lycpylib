

def file_open(path, method: str = "r", content: str = ""):
    """
    open a file,read or write

    @param path:the file path
    @type path:string

    @param method:the open method
    @type method:"r","rb","w","wb","a",if the method is r or rb,content could be None

    @param content:the content of the writing
    @type content:string

    """

    f = open(path, str(method))
    if method == "r" or method == "rb":
        data = f.read()
        f.close()
        return data
    elif method == "w" or method == "a" or method == "wb":
        f.write(content)
    else:
        raise Exception(f"method {method} not allow")
    f.close()


if __name__ == '__main__':
    file_open("test.txt", "w", "HelloKitty")
