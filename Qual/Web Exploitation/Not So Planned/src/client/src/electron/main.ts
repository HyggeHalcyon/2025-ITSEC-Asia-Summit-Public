import {app, BrowserWindow, ipcMain } from 'electron';
import path from 'path';
import { PlanCached } from './PlanCached.js';
const cachePath = path.join(app.getPath('userData'), '/config.json');
const planCached = PlanCached.init(cachePath);
const DEV_PATH = 'http://localhost:5123'
const PROD_PATH = path.join(app.getAppPath(), '/dist-react/index.html');

app.on('ready', () =>{
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            preload: path.join(app.getAppPath(),
            process.env.NODE_ENV === "development" ? "." : "..",
            'dist-electron/preload.cjs'), 
        },
    });
    if(process.env.NODE_ENV === 'development') {
        console.log('Running on localhost:5123');
        mainWindow.loadURL(DEV_PATH);
    }else{
        mainWindow.loadFile(PROD_PATH);
    }

    planCached.then(planCache => {
        ipcMain.handle('set-cached-plans', (_, plan: PlanInterface) =>{
            planCache.setCachedPlan(plan);
            mainWindow.webContents.send('plan-updated');
        });
        ipcMain.handle('get-cached-plans', _ => {
            return planCache.getCachedPlans();
        });
        ipcMain.handle('backup-cached-plans', (_, name: string) => {
            return planCache.backupCachedPlan(name);
        });
    });
})