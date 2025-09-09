import React from 'react';
import menuItems from '../const/menu.json';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
      return (
    <div className="w-30 h-screen bg-black/50 flex flex-col shadow-lg">
      <nav className="flex flex-col gap-4 w-full my-5">
        {menuItems.map((item, index) => (
          <NavLink
            key={index}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-1 py-2 px-2 transition mx-auto ${
                isActive
                  ? "bg-white/30 text-white backdrop-blur-md bg-white/10 shadow-lg rounded-lg"
                  : "hover:scale-150 transition duration-300 rounded-lg"
              }`
            }
          >
            <img src={item.icon} alt={item.target} className="w-12 h-12" />
          </NavLink>
        ))}
      </nav>
    </div>
  );
}

export default Sidebar;