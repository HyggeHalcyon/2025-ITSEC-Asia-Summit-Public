import { exec } from 'node:child_process';
import fs from 'node:fs/promises'

export class PlanCached {
    constructor(private path: string, private plans: PlanCachedInterface){
        this.save();
    }
    async save(){
        return fs.writeFile(this.path, JSON.stringify(this.plans));
    }
    getCachedPlans(): PlanCachedInterface{
        return this.plans;
    }
    setCachedPlan(plan: PlanInterface){
        this.plans.plans.push(plan);
        this.save();
    }
    backupCachedPlan(name: string){
        let command = '';
        switch (process.platform){
            case 'win32':
                command=`powershell -Command "Compress-Archive -Path ${this.path} -DestinationPath ${name}.zip"`;
                exec(command);
                break;
            case 'darwin':
                command=`zip -r ${this.path} ${name}.zip`;
                exec(command);
                break;
            case 'linux':
                command=`zip ${name}.zip ${this.path}`;
                exec(command);
                break;
            default:
                break;
        }
    }
    static async init(path: string){
        try{
            const data = JSON.parse(await fs.readFile(path, 'utf-8'));
            return new PlanCached(path, data);
        }catch{
            return new PlanCached(path, {plans: []});
        }
    }

}



