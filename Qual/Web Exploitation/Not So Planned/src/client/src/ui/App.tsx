import React, { useState, useEffect } from 'react';
import { HashRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Sidebar from './components/Sidebar';
import './App.css';
import CreatePlan from './pages/CreatePlan';
import ViewPlan from './pages/ViewPlan';
import SearchPlan from './pages/SearchPlan';
import PlanList from './pages/PlanList';
import {defaultUUID} from './InitConf';

function App() {
  const [data, setData] = useState<PlanInterface[]>([]);

  useEffect(() => {
    const handleUpdate = async () => {
      const plan = await window.api.getCachedPlans();
      setData(plan.plans);
    };
    handleUpdate();
    const unsubscribe = window.api.onPlanUpdated(handleUpdate);
    return () => {
      if (unsubscribe) unsubscribe();
    };
  }, []);

  const HomeRedirect = () => {
    if (defaultUUID=== "") {
      return <Navigate to="/create-plan" replace />;
    }
    return <Navigate to={`/view-plan/${defaultUUID}`} replace />;
  };

  return (
    <Router>
      <div className="flex h-screen">

        <div className="flex-1 overflow-y-auto">
          <Routes>
            <Route path="/plan-list" element={<PlanList plan={data} />} />
            <Route path="/create-plan" element={<CreatePlan />} />
            <Route path="/search-plan" element={<SearchPlan />} />
            <Route path="/view-plan/:uuid" element={<ViewPlan />} />
            <Route path="/" element={<HomeRedirect />} />
          </Routes>
        </div>
          <Sidebar />
      </div>
    </Router>
  );
}

export default App;
