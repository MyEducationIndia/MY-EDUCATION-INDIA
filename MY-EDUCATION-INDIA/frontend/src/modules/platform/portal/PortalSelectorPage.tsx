import React from "react";
import { GraduationCap, BookOpen, Users, PhoneCall, Landmark, Building, Terminal, Shield, CheckCircle } from "lucide-react";
import { Link } from "react-router-dom";

export const PortalSelectorPage: React.FC = () => {
  const portals = [
    { title: "Student Scholar Portal", role: "STUDENT", icon: GraduationCap, route: "/student", color: "bg-blue-50 text-blue-600" },
    { title: "Faculty & Professor Portal", role: "FACULTY", icon: BookOpen, route: "/faculty", color: "bg-indigo-50 text-indigo-600" },
    { title: "Admissions Counsellor Portal", role: "COUNSELLOR", icon: PhoneCall, route: "/admin/crm", color: "bg-amber-50 text-amber-600" },
    { title: "Bursar & Accountant Portal", role: "ACCOUNTANT", icon: Landmark, route: "/admin/fees", color: "bg-emerald-50 text-emerald-600" },
    { title: "Branch Operations Portal", role: "BRANCH_ADMIN", icon: Building, route: "/admin/dashboard", color: "bg-purple-50 text-purple-600" },
    { title: "Developer Command Console", role: "DEVELOPER", icon: Terminal, route: "/developer", color: "bg-slate-100 text-slate-800" }
  ];

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Enterprise Experience Portals</h1>
        <p className="text-sm text-gray-500">Dedicated institutional viewports configured by role-based access control</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {portals.map((p, idx) => {
          const Icon = p.icon;
          return (
            <Link key={idx} to={p.route} className="bg-white p-5 rounded-xl border border-gray-200 hover:border-indigo-400 hover:shadow-md transition-all">
              <div className="flex items-center gap-3">
                <div className={`p-3 rounded-xl ${p.color}`}><Icon className="w-6 h-6" /></div>
                <div>
                  <h3 className="font-semibold text-gray-900">{p.title}</h3>
                  <span className="text-xs text-gray-500 uppercase tracking-wider">Role: {p.role}</span>
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
};
