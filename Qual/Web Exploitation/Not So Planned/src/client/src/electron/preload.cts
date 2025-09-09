const electron = require('electron');

const api = {
    getCachedPlans(): Promise<PlanCachedInterface>{
        return electron.ipcRenderer.invoke('get-cached-plans');
    },
    setCachedPlan(plan: PlanInterface){
        return electron.ipcRenderer.invoke('set-cached-plans',plan);
    },
    onPlanUpdated(callback: () => void) {
        const listener = () => callback();
        electron.ipcRenderer.on('plan-updated', listener);
        return () => {
            electron.ipcRenderer.off('plan-updated', listener);
        };
    },
    backupCachedPlan(name: string){
        return electron.ipcRenderer.invoke('backup-cached-plans', name);
    }
}

electron.contextBridge.exposeInMainWorld('api',api);
