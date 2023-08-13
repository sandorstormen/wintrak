const { app, BrowserWindow } = require('electron')
const path = require('path')
const fs = require("fs");
const os = require('os');
const initPath = path.join(app.getPath('userData'), "init.json");

function createWindow() {
  try {
    data = JSON.parse(fs.readFileSync(initPath, 'utf8'));
  }
  catch (e) {
  }

  if (data && data.bounds) {
    width = data.bounds.width;
    height = data.bounds.height;
    x = data.bounds.x;
    y = data.bounds.y;
  }

  const win = new BrowserWindow({
    width: width,
    height: height,
    x: x,
    y: y,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: true,
    }
  })
  win.removeMenu()
  win.title = "WinTrak"
  win.webContents.openDevTools()
  win.loadFile('web/index.html', { query: { home_dir: os.homedir() } })
  // win.loadURL('file://web/index.html?home_dir=' + encodeURIComponent(os.homedir()))

  win.on('close', () => {
    var data = {
      bounds: win.getBounds()
    };
    fs.writeFileSync(initPath, JSON.stringify(data));
  });
}

app.whenReady().then(() => {
  createWindow()
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})