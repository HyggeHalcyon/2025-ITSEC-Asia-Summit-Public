interface PlanInterface {
    uuid: string;
    title: string;
    type: Number;
}

interface PlanCachedInterface {
    plans: PlanInterface[];
}

interface Window{
    api: {
        setCachedPlan: (plan: PlanInterface) => void,
        getCachedPlans: () => Promise<PlanCachedInterface>,
        onPlanUpdated: (callback: () => void) => () => void;
        backupCachedPlan: (name: string) => void
    }
}