import {
  Bell,
  UserCircle,
} from "lucide-react";

function Navbar() {
  return (
    <header className="h-16 bg-white border-b border-slate-200 flex items-center justify-between px-6">

      {/* LEFT SIDE */}

      <div>
        <h2 className="text-lg font-semibold text-slate-800">
          Neighbour Management System
        </h2>

        <p className="text-xs text-slate-500">
          4G → 5G Network Monitoring
        </p>
      </div>


      {/* RIGHT SIDE */}

      <div className="flex items-center gap-6">

        {/* Notification */}

        <button
          className="relative text-slate-500 hover:text-slate-800"
          title="Notifications"
        >
          <Bell size={21} />

          <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-red-500 rounded-full">
          </span>
        </button>


        {/* User */}

        <div className="flex items-center gap-3">

          <UserCircle
            size={32}
            className="text-slate-500"
          />

          <div>
            <p className="text-sm font-semibold text-slate-800">
              Administrator
            </p>

            <p className="text-xs text-slate-500">
              Network Operator
            </p>
          </div>

        </div>

      </div>

    </header>
  );
}

export default Navbar;