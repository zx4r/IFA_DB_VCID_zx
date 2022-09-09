#! C:/Users/Administrator/AppData/Local/Programs/Python/Python310/python.exe

from website import create_app

app = create_app()

#####Webseite starten & wird bei Source-Code Änderungen angepasst
if __name__ == '__main__':   
    app.run('194.209.230.50', port=3000)

#app.run(debug=True)
    

