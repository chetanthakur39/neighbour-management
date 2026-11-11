import {
  LayoutDashboard,
  Network,
  ShieldCheck,
  Radio,
  RadioTower,
  BarChart3,
  ChevronDown,
  RotateCcw,
} from "lucide-react";

import { NavLink } from "react-router-dom";


function Sidebar() {
  return (
    <aside className="w-64 min-h-screen bg-slate-900 text-white border-r border-slate-800">

      {/* Application Logo */}

      <div className="h-16 flex items-center px-6 border-b border-slate-800">

        <div>
          <h1 className="text-lg font-bold">
            Neighbour Manager
          </h1>

          <p className="text-xs text-slate-400">
            4G → 5G Network
          </p>
        </div>

      </div>


      {/* Navigation */}

      <nav className="p-4 space-y-2">


        {/* ================================================= */}
        {/* DASHBOARD                                         */}
        {/* ================================================= */}

        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `w-full flex items-center gap-3 px-4 py-3 rounded-lg ${
              isActive
                ? "bg-blue-600 text-white"
                : "text-slate-300 hover:bg-slate-800"
            }`
          }
        >

          <LayoutDashboard size={20} />

          <span>
            Dashboard
          </span>

        </NavLink>


        {/* ================================================= */}
        {/* NEIGHBOURS                                        */}
        {/* ================================================= */}

        <NavLink
          to="/neighbours"
          className={({ isActive }) =>
            `w-full flex items-center gap-3 px-4 py-3 rounded-lg ${
              isActive
                ? "bg-blue-600 text-white"
                : "text-slate-300 hover:bg-slate-800"
            }`
          }
        >

          <Network size={20} />

          <span>
            Neighbours
          </span>

        </NavLink>


        {/* ================================================= */}
        {/* VALIDATION                                        */}
        {/* ================================================= */}

        <NavLink
          to="/validation"
          className={({ isActive }) =>
            `w-full flex items-center gap-3 px-4 py-3 rounded-lg ${
              isActive
                ? "bg-blue-600 text-white"
                : "text-slate-300 hover:bg-slate-800"
            }`
          }
        >

          <ShieldCheck size={20} />

          <span>
            Validation
          </span>

        </NavLink>


        {/* ================================================= */}
        {/* AUTOMATION                                        */}
        {/* ================================================= */}

        <NavLink
          to="/automation"
          className={({ isActive }) =>
            `w-full flex items-center gap-3 px-4 py-3 rounded-lg ${
              isActive
                ? "bg-blue-600 text-white"
                : "text-slate-300 hover:bg-slate-800"
            }`
          }
        >

          <RotateCcw size={20} />

          <span>
            Automation
          </span>

        </NavLink>


        {/* ================================================= */}
        {/* 4G NETWORK                                        */}
        {/* ================================================= */}

        <div className="pt-5">

          <div className="flex items-center justify-between px-4 py-2 text-xs font-semibold text-slate-500 uppercase">

            <span>
              4G Network
            </span>

            <ChevronDown size={16} />

          </div>


          {/* Enodes */}

          <NavLink
            to="/4g/enodes"
            className={({ isActive }) =>
              `w-full flex items-center gap-3 px-4 py-2 text-sm rounded-lg ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >

            <Radio size={18} />

            <span>
              Enodes
            </span>

          </NavLink>


          {/* ECells */}

          <NavLink
            to="/4g/ecells"
            className={({ isActive }) =>
              `w-full flex items-center gap-3 px-4 py-2 text-sm rounded-lg ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >

            <Radio size={18} />

            <span>
              ECells
            </span>

          </NavLink>


          {/* 4G Configuration */}

          <NavLink
            to="/4g/configuration"
            className={({ isActive }) =>
              `w-full flex items-center gap-3 px-4 py-2 text-sm rounded-lg ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >

            <Radio size={18} />

            <span>
              Configuration
            </span>

          </NavLink>

        </div>


        {/* ================================================= */}
        {/* 5G NETWORK                                        */}
        {/* ================================================= */}

        <div className="pt-5">

          <div className="flex items-center justify-between px-4 py-2 text-xs font-semibold text-slate-500 uppercase">

            <span>
              5G Network
            </span>

            <ChevronDown size={16} />

          </div>


          {/* Gnodes */}

          <NavLink
            to="/5g/gnodes"
            className={({ isActive }) =>
              `w-full flex items-center gap-3 px-4 py-2 text-sm rounded-lg ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >

            <RadioTower size={18} />

            <span>
              Gnodes
            </span>

          </NavLink>


          {/* GCells */}

          <NavLink
            to="/5g/gcells"
            className={({ isActive }) =>
              `w-full flex items-center gap-3 px-4 py-2 text-sm rounded-lg ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >

            <RadioTower size={18} />

            <span>
              GCells
            </span>

          </NavLink>


          {/* 5G Configuration */}

          <NavLink
            to="/5g/configuration"
            className={({ isActive }) =>
              `w-full flex items-center gap-3 px-4 py-2 text-sm rounded-lg ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >

            <RadioTower size={18} />

            <span>
              Configuration
            </span>

          </NavLink>

        </div>


        {/* ================================================= */}
        {/* REPORTS                                           */}
        {/* ================================================= */}

        <div className="pt-5">

          <NavLink
            to="/reports"
            className={({ isActive }) =>
              `w-full flex items-center gap-3 px-4 py-3 rounded-lg ${
                isActive
                  ? "bg-blue-600 text-white"
                  : "text-slate-300 hover:bg-slate-800"
              }`
            }
          >

            <BarChart3 size={20} />

            <span>
              Reports
            </span>

          </NavLink>

        </div>

      </nav>

    </aside>
  );
}


export default Sidebar;