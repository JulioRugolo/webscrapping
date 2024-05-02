const { app, BrowserWindow } = require('electron');
const child_process = require('child_process');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: true
        }
    });

    // Inicie o servidor Flask aqui
    child_process.spawn('python', ['/index.py']);

    mainWindow.loadURL('http://localhost:5000');
    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}


app.on('ready', createWindow);

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', function () {
    if (mainWindow === null) {
        createWindow();
    }
});
