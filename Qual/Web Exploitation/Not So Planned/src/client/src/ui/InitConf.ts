let uuid: string = "";

try {
    const cache = await window.api.getCachedPlans();
    const plan: PlanInterface[] | undefined = cache?.plans;

    if (plan && plan.length > 0 && plan[0]?.uuid) {
      uuid = plan[0].uuid;
    }
}   catch (error) {
    console.error("Failed to get cached plans:", error);
}

export const defaultUUID: string = uuid;