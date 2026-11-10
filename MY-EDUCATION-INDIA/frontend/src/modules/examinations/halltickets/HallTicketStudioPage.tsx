import React, { useState, useMemo } from "react";
import { Link } from "react-router-dom";
import {
  QrCode,
  Download,
  Printer,
  ShieldCheck,
  CheckCircle2,
  Search,
  Filter,
  Check,
  X,
  FileText,
  Clock,
  Building2,
  Users,
  AlertTriangle,
  ChevronRight,
  Eye,
  Lock,
  Unlock,
  Sparkles,
  Barcode,
  Award,
  Hash,
  ExternalLink,
} from "lucide-react";

interface PaperEntry {
  course_code: string;
  course_title: string;
  paper_code: string;
  exam_date: string;
  slot_code: string;
  start_time: string;
  end_time: string;
  room_number: string;
  seat_number: string;
  is_practical: boolean;
}

interface HallTicket {
  id: string;
  enrollment_no: string;
  roll_number: string;
  candidate_name: string;
  father_name: string;
  program_name: string;
  department_name: string;
  semester_code: string;
  academic_year: string;
  exam_center_code: string;
  exam_center_name: string;
  exam_center_address: string;
  ticket_number: string;
  barcode_data: string;
  qr_verification_code: string;
  digital_signature_hash: string;
  controller_name: string;
  signed_at: string;
  issue_date: string;
  status: "ISSUED" | "DOWNLOADED" | "BLOCKED" | "CANCELLED";
  eligibility_status: "ELIGIBLE" | "CONDITIONAL_ATTENDANCE" | "DETAINED";
  paper_entries: PaperEntry[];
  student_instructions: string[];
  download_count: number;
}

const DEFAULT_INSTRUCTIONS = [
  "1. Candidates must arrive at the Examination Center at least 45 minutes prior to commencement.",
  "2. Entry gates will be locked strictly 15 minutes before scheduled start time; no candidate shall be admitted thereafter.",
  "3. Mandatory valid original Government ID (Aadhaar / Voter ID / Passport) alongside this Hall Ticket is required for entry.",
  "4. Electronic gadgets, smart watches, mobile phones, programmable calculators, and unauthorized papers are strictly banned.",
  "5. Candidates must sit only at their allocated Seat Number displayed outside the Examination Hall.",
  "6. Do not write your name, phone number, or any identifying marks on the Question Paper or Answer Booklet.",
  "7. Candidates must maintain strict silence and obey all directives of the Room Invigilators and Flying Squad.",
  "8. Possession of unauthorized material will be treated as Malpractice under the Institutional Conduct Code.",
];

export const HallTicketStudioPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<"ROSTER" | "VERIFY" | "BATCH_OPS">("ROSTER");
  const [searchQuery, setSearchQuery] = useState("");
  const [filterDepartment, setFilterDepartment] = useState("ALL");
  const [filterStatus, setFilterStatus] = useState("ALL");
  const [selectedTicket, setSelectedTicket] = useState<HallTicket | null>(null);
  const [isPreviewModalOpen, setIsPreviewModalOpen] = useState(false);
  const [isBulkGenModalOpen, setIsBulkGenModalOpen] = useState(false);
  const [verifyInput, setVerifyInput] = useState("HT-2026-AUT-001");
  const [verifyResult, setVerifyResult] = useState<any | null>(null);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(null), 4000);
  };

  // Standard Paper Schedule Entries
  const csePapers: PaperEntry[] = [
    {
      course_code: "CS-301-P",
      course_title: "DBMS Practical & SQL Laboratory",
      paper_code: "QP-2026-CS301-PR",
      exam_date: "2026-12-05",
      slot_code: "SLOT-MORNING-A",
      start_time: "09:30",
      end_time: "12:30",
      room_number: "LAB-01",
      seat_number: "LAB-01-T01",
      is_practical: true,
    },
    {
      course_code: "CS-301",
      course_title: "Database Management Systems",
      paper_code: "QP-2026-CS301-TH",
      exam_date: "2026-12-12",
      slot_code: "SLOT-MORNING-A",
      start_time: "09:30",
      end_time: "12:30",
      room_number: "HALL-A1",
      seat_number: "HALL-A1-R1-S01",
      is_practical: false,
    },
    {
      course_code: "CS-302",
      course_title: "Operating Systems & Concurrency",
      paper_code: "QP-2026-CS302-TH",
      exam_date: "2026-12-15",
      slot_code: "SLOT-MORNING-A",
      start_time: "09:30",
      end_time: "12:30",
      room_number: "HALL-A1",
      seat_number: "HALL-A1-R1-S01",
      is_practical: false,
    },
    {
      course_code: "CS-303",
      course_title: "Computer Networks & Protocols",
      paper_code: "QP-2026-CS303-TH",
      exam_date: "2026-12-21",
      slot_code: "SLOT-MORNING-A",
      start_time: "09:30",
      end_time: "12:30",
      room_number: "HALL-A1",
      seat_number: "HALL-A1-R1-S01",
      is_practical: false,
    },
  ];

  // Candidate Hall Tickets state
  const [tickets, setTickets] = useState<HallTicket[]>([
    {
      id: "ht-1",
      enrollment_no: "MEI2023CS001",
      roll_number: "230105001",
      candidate_name: "Aarav Sharma",
      father_name: "Shri R. K. Sharma",
      program_name: "B.Tech Computer Science & Engineering",
      department_name: "Computer Science & Engineering",
      semester_code: "SEM-5",
      academic_year: "2026-2027",
      exam_center_code: "TC-IND-01",
      exam_center_name: "Main Examination Complex, MEI Autonomous Campus",
      exam_center_address: "Campus Ring Road, Indore, Madhya Pradesh - 452010",
      ticket_number: "HT-2026-AUT-001",
      barcode_data: "*HT2026AUT001*",
      qr_verification_code: "https://verify.myeducation.in/ems/ht/HT-2026-AUT-001?sig=e9b418a2f30c",
      digital_signature_hash: "a8f5b493c042971d8820c3a59fbe724810dc2e7183e91d643e26487e4125b018",
      controller_name: "Dr. V. K. Maheshwari, Controller of Examinations",
      signed_at: "2026-11-28 10:30:00",
      issue_date: "2026-11-28",
      status: "ISSUED",
      eligibility_status: "ELIGIBLE",
      paper_entries: csePapers,
      student_instructions: DEFAULT_INSTRUCTIONS,
      download_count: 2,
    },
    {
      id: "ht-2",
      enrollment_no: "MEI2023CS002",
      roll_number: "230105002",
      candidate_name: "Ananya Verma",
      father_name: "Shri S. P. Verma",
      program_name: "B.Tech Computer Science & Engineering",
      department_name: "Computer Science & Engineering",
      semester_code: "SEM-5",
      academic_year: "2026-2027",
      exam_center_code: "TC-IND-01",
      exam_center_name: "Main Examination Complex, MEI Autonomous Campus",
      exam_center_address: "Campus Ring Road, Indore, Madhya Pradesh - 452010",
      ticket_number: "HT-2026-AUT-002",
      barcode_data: "*HT2026AUT002*",
      qr_verification_code: "https://verify.myeducation.in/ems/ht/HT-2026-AUT-002?sig=8c01fa9125da",
      digital_signature_hash: "74bf91295c024d898a39e801cd349781b4908ef123d91782635418b7654a903e",
      controller_name: "Dr. V. K. Maheshwari, Controller of Examinations",
      signed_at: "2026-11-28 10:30:00",
      issue_date: "2026-11-28",
      status: "DOWNLOADED",
      eligibility_status: "ELIGIBLE",
      paper_entries: csePapers,
      student_instructions: DEFAULT_INSTRUCTIONS,
      download_count: 3,
    },
    {
      id: "ht-3",
      enrollment_no: "MEI2023EC015",
      roll_number: "230203015",
      candidate_name: "Rohan Patel",
      father_name: "Shri H. M. Patel",
      program_name: "B.Tech Electronics & Communication",
      department_name: "Electronics & Communication",
      semester_code: "SEM-3",
      academic_year: "2026-2027",
      exam_center_code: "TC-IND-01",
      exam_center_name: "Main Examination Complex, MEI Autonomous Campus",
      exam_center_address: "Campus Ring Road, Indore, Madhya Pradesh - 452010",
      ticket_number: "HT-2026-AUT-003",
      barcode_data: "*HT2026AUT003*",
      qr_verification_code: "https://verify.myeducation.in/ems/ht/HT-2026-AUT-003?sig=4b19c283aa01",
      digital_signature_hash: "5d0184b9319c8324e902a7b6c59124310dfb9281734e0192837461928374a5bc",
      controller_name: "Dr. V. K. Maheshwari, Controller of Examinations",
      signed_at: "2026-11-28 10:30:00",
      issue_date: "2026-11-28",
      status: "ISSUED",
      eligibility_status: "ELIGIBLE",
      paper_entries: [
        {
          course_code: "EC-201",
          course_title: "Analog Integrated Circuits",
          paper_code: "QP-2026-EC201-TH",
          exam_date: "2026-12-14",
          slot_code: "SLOT-MORNING-A",
          start_time: "09:30",
          end_time: "12:30",
          room_number: "HALL-B2",
          seat_number: "HALL-B2-R1-S01",
          is_practical: false,
        },
      ],
      student_instructions: DEFAULT_INSTRUCTIONS,
      download_count: 1,
    },
    {
      id: "ht-4",
      enrollment_no: "MEI2023ME022",
      roll_number: "230307022",
      candidate_name: "Priya Deshmukh",
      father_name: "Shri A. K. Deshmukh",
      program_name: "B.Tech Mechanical Engineering",
      department_name: "Mechanical Engineering",
      semester_code: "SEM-7",
      academic_year: "2026-2027",
      exam_center_code: "TC-IND-01",
      exam_center_name: "Main Examination Complex, MEI Autonomous Campus",
      exam_center_address: "Campus Ring Road, Indore, Madhya Pradesh - 452010",
      ticket_number: "HT-2026-AUT-004",
      barcode_data: "*HT2026AUT004*",
      qr_verification_code: "https://verify.myeducation.in/ems/ht/HT-2026-AUT-004?sig=78da09bc12ea",
      digital_signature_hash: "81903ba849102837461928374619283749102837461928374619283746192837",
      controller_name: "Dr. V. K. Maheshwari, Controller of Examinations",
      signed_at: "2026-11-28 10:30:00",
      issue_date: "2026-11-28",
      status: "ISSUED",
      eligibility_status: "ELIGIBLE",
      paper_entries: [
        {
          course_code: "ME-401",
          course_title: "Heat and Mass Transfer",
          paper_code: "QP-2026-ME401-TH",
          exam_date: "2026-12-18",
          slot_code: "SLOT-AFTERNOON-B",
          start_time: "14:00",
          end_time: "17:00",
          room_number: "HALL-A1",
          seat_number: "HALL-A1-R3-S14",
          is_practical: false,
        },
      ],
      student_instructions: DEFAULT_INSTRUCTIONS,
      download_count: 1,
    },
    {
      id: "ht-5",
      enrollment_no: "MEI2023CS013",
      roll_number: "230105013",
      candidate_name: "Karan Johar",
      father_name: "Shri Y. P. Johar",
      program_name: "B.Tech Computer Science & Engineering",
      department_name: "Computer Science & Engineering",
      semester_code: "SEM-5",
      academic_year: "2026-2027",
      exam_center_code: "TC-IND-01",
      exam_center_name: "Main Examination Complex, MEI Autonomous Campus",
      exam_center_address: "Campus Ring Road, Indore, Madhya Pradesh - 452010",
      ticket_number: "HT-2026-AUT-013",
      barcode_data: "*HT2026AUT013*",
      qr_verification_code: "https://verify.myeducation.in/ems/ht/HT-2026-AUT-013?sig=19a82c9f8012",
      digital_signature_hash: "1928374619283746192837461928374619283746192837461928374619283746",
      controller_name: "Dr. V. K. Maheshwari, Controller of Examinations",
      signed_at: "2026-11-28 10:30:00",
      issue_date: "2026-11-28",
      status: "BLOCKED",
      eligibility_status: "DETAINED",
      paper_entries: csePapers,
      student_instructions: DEFAULT_INSTRUCTIONS,
      download_count: 0,
    },
  ]);

  // Filtered tickets
  const filteredTickets = useMemo(() => {
    return tickets.filter((t) => {
      const matchQuery =
        t.candidate_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.roll_number.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.enrollment_no.toLowerCase().includes(searchQuery.toLowerCase()) ||
        t.ticket_number.toLowerCase().includes(searchQuery.toLowerCase());
      const matchDept = filterDepartment === "ALL" || t.department_name.includes(filterDepartment);
      const matchStatus = filterStatus === "ALL" || t.status === filterStatus;
      return matchQuery && matchDept && matchStatus;
    });
  }, [tickets, searchQuery, filterDepartment, filterStatus]);

  // Metrics
  const totalTickets = tickets.length;
  const issuedTickets = tickets.filter((t) => t.status === "ISSUED" || t.status === "DOWNLOADED").length;
  const downloadedCount = tickets.filter((t) => t.download_count > 0).length;
  const blockedTickets = tickets.filter((t) => t.status === "BLOCKED").length;

  // Toggle Block Status
  const handleToggleBlock = (ticketId: string) => {
    setTickets(
      tickets.map((t) => {
        if (t.id === ticketId) {
          const newStatus = t.status === "BLOCKED" ? "ISSUED" : "BLOCKED";
          const newElig = newStatus === "BLOCKED" ? "DETAINED" : "ELIGIBLE";
          showToast(`Admit card ${t.ticket_number} is now ${newStatus}.`);
          return { ...t, status: newStatus, eligibility_status: newElig as any };
        }
        return t;
      })
    );
  };

  // Live QR Verification
  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    const query = verifyInput.trim();
    const found = tickets.find(
      (t) =>
        t.ticket_number.toLowerCase() === query.toLowerCase() ||
        t.roll_number.toLowerCase() === query.toLowerCase() ||
        t.enrollment_no.toLowerCase() === query.toLowerCase()
    );

    if (found) {
      setVerifyResult({
        isValid: found.status !== "BLOCKED",
        ticket: found,
        message:
          found.status !== "BLOCKED"
            ? "Admit Card is GENUINE & VALID. Permitted for institutional examination hall entry."
            : "Admit Card is BLOCKED / DETAINED. Hall entry prohibited by COE directive.",
      });
    } else {
      setVerifyResult({
        isValid: false,
        message: "Admit Card verification FAILED. Record not found in Autonomous Campus database.",
      });
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 p-4 md:p-8">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-indigo-900 text-white px-4 py-3 rounded-xl shadow-2xl flex items-center gap-3 border border-indigo-700 animate-in fade-in slide-in-from-bottom-2">
          <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
          <span className="text-xs font-semibold">{toastMessage}</span>
        </div>
      )}

      <div className="max-w-7xl mx-auto space-y-6">
        {/* Breadcrumb & Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-5">
          <div>
            <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400 mb-1">
              <Link to="/exams" className="hover:underline">EMS</Link>
              <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
              <Link to="/exams/planning" className="hover:underline">Planning</Link>
              <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
              <span>Hall Ticket System</span>
              <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 ml-2">
                Phase 4 Module 5
              </span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight flex items-center gap-3">
              <QrCode className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
              Examination Hall Ticket & Admit Card Studio
            </h1>
            <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">
              Cryptographic admit card generation with barcodes, QR verification, seating numbers, and digital signatures.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={() => {
                showToast("Generating batch PDF for all issued admit cards (A4 duplex)...");
                window.print();
              }}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold rounded-lg border border-slate-300 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800 transition"
            >
              <Printer className="w-4 h-4 text-slate-600 dark:text-slate-400" />
              Bulk Print Admit Cards
            </button>

            <button
              onClick={() => setIsBulkGenModalOpen(true)}
              className="inline-flex items-center gap-1.5 px-3.5 py-2 text-xs font-semibold rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm transition"
            >
              <Sparkles className="w-4 h-4" />
              Bulk Generate Admit Cards
            </button>
          </div>
        </div>

        {/* Institutional Summary KPIs */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Total Hall Tickets</span>
              <FileText className="w-4 h-4 text-indigo-500" />
            </div>
            <div className="mt-2 text-2xl font-black text-slate-900 dark:text-white">{totalTickets}</div>
            <div className="text-[11px] text-slate-500 mt-0.5">Autumn Semester 2026</div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Admit Cards Downloaded</span>
              <Download className="w-4 h-4 text-emerald-500" />
            </div>
            <div className="mt-2 text-2xl font-black text-slate-900 dark:text-white">{downloadedCount}</div>
            <div className="text-[11px] text-emerald-600 dark:text-emerald-400 mt-0.5 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" />
              Candidate Verified
            </div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Eligible & Issued</span>
              <ShieldCheck className="w-4 h-4 text-blue-500" />
            </div>
            <div className="mt-2 text-2xl font-black text-slate-900 dark:text-white">{issuedTickets}</div>
            <div className="text-[11px] text-blue-600 dark:text-blue-400 mt-0.5">
              Fee & Attendance Cleared
            </div>
          </div>

          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400">Blocked / Detained</span>
              <Lock className="w-4 h-4 text-rose-500" />
            </div>
            <div className="mt-2 text-2xl font-black text-rose-600 dark:text-rose-400">{blockedTickets}</div>
            <div className="text-[11px] text-rose-500 mt-0.5">Attendance / Fee Shortage</div>
          </div>
        </div>

        {/* View Tabs */}
        <div className="border-b border-slate-200 dark:border-slate-800">
          <nav className="flex space-x-2 md:space-x-4 overflow-x-auto pb-px" aria-label="Tabs">
            {[
              { id: "ROSTER", label: "Candidate Admit Card Roster", icon: Users },
              { id: "VERIFY", label: "Live QR Verification Terminal", icon: QrCode },
              { id: "BATCH_OPS", label: "Batch Operations & Instructions", icon: Printer },
            ].map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`inline-flex items-center gap-2 py-3 px-3 text-sm font-semibold border-b-2 whitespace-nowrap transition-colors ${
                    isActive
                      ? "border-indigo-600 text-indigo-600 dark:border-indigo-400 dark:text-indigo-400"
                      : "border-transparent text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>

        {/* TAB 1: CANDIDATE ROSTER */}
        {activeTab === "ROSTER" && (
          <div className="space-y-4">
            {/* Search and Filters */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div className="flex flex-wrap items-center gap-2 flex-1">
                <div className="relative flex-1 min-w-[200px] max-w-sm">
                  <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                  <input
                    type="text"
                    placeholder="Search candidate, roll, enrollment, ticket..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <select
                  value={filterDepartment}
                  onChange={(e) => setFilterDepartment(e.target.value)}
                  className="px-2.5 py-1.5 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="ALL">All Departments</option>
                  <option value="Computer Science">Computer Science</option>
                  <option value="Electronics">Electronics</option>
                  <option value="Mechanical">Mechanical</option>
                </select>

                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="px-2.5 py-1.5 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  <option value="ALL">All Statuses</option>
                  <option value="ISSUED">Issued</option>
                  <option value="DOWNLOADED">Downloaded</option>
                  <option value="BLOCKED">Blocked</option>
                </select>
              </div>
            </div>

            {/* Roster Table */}
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl overflow-hidden shadow-sm">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-200 dark:border-slate-800">
                    <tr>
                      <th className="px-4 py-3">Hall Ticket No.</th>
                      <th className="px-4 py-3">Candidate Details</th>
                      <th className="px-4 py-3">Program & Sem</th>
                      <th className="px-4 py-3">Exam Center</th>
                      <th className="px-4 py-3">Allocated Room & Seat</th>
                      <th className="px-4 py-3">Eligibility</th>
                      <th className="px-4 py-3">Status</th>
                      <th className="px-4 py-3 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 dark:divide-slate-800 font-medium">
                    {filteredTickets.map((t) => (
                      <tr key={t.id} className="hover:bg-slate-50/60 dark:hover:bg-slate-800/40 transition">
                        <td className="px-4 py-3">
                          <div className="font-mono font-bold text-indigo-600 dark:text-indigo-400">{t.ticket_number}</div>
                          <div className="text-[10px] text-slate-500 font-mono">{t.barcode_data}</div>
                        </td>

                        <td className="px-4 py-3">
                          <div className="font-bold text-slate-900 dark:text-white">{t.candidate_name}</div>
                          <div className="text-[10px] text-slate-500 font-mono">Roll: {t.roll_number} • Enr: {t.enrollment_no}</div>
                        </td>

                        <td className="px-4 py-3">
                          <div className="text-slate-700 dark:text-slate-300 font-medium">{t.program_name}</div>
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                            {t.semester_code}
                          </span>
                        </td>

                        <td className="px-4 py-3">
                          <div className="font-bold text-slate-800 dark:text-slate-200 font-mono">{t.exam_center_code}</div>
                          <div className="text-[10px] text-slate-500 truncate max-w-[140px]">{t.exam_center_name}</div>
                        </td>

                        <td className="px-4 py-3 font-mono">
                          <div className="font-bold text-indigo-600 dark:text-indigo-400">
                            {t.paper_entries[0]?.seat_number || "HALL-A1-S01"}
                          </div>
                          <div className="text-[10px] text-slate-500">{t.paper_entries[0]?.room_number || "HALL-A1"}</div>
                        </td>

                        <td className="px-4 py-3">
                          <span
                            className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold ${
                              t.eligibility_status === "ELIGIBLE"
                                ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300"
                                : t.eligibility_status === "CONDITIONAL_ATTENDANCE"
                                ? "bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300"
                                : "bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300"
                            }`}
                          >
                            {t.eligibility_status.replace("_", " ")}
                          </span>
                        </td>

                        <td className="px-4 py-3">
                          <span
                            className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold ${
                              t.status === "DOWNLOADED"
                                ? "bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300"
                                : t.status === "ISSUED"
                                ? "bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300"
                                : "bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300"
                            }`}
                          >
                            {t.status}
                          </span>
                        </td>

                        <td className="px-4 py-3 text-right">
                          <div className="inline-flex items-center gap-2">
                            <button
                              onClick={() => {
                                setSelectedTicket(t);
                                setIsPreviewModalOpen(true);
                              }}
                              className="px-2.5 py-1 rounded bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-100 font-semibold text-xs flex items-center gap-1"
                            >
                              <Eye className="w-3.5 h-3.5" />
                              Admit Card
                            </button>

                            <button
                              onClick={() => handleToggleBlock(t.id)}
                              className={`p-1 rounded ${
                                t.status === "BLOCKED"
                                  ? "text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-950"
                                  : "text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950"
                              }`}
                              title={t.status === "BLOCKED" ? "Unblock Ticket" : "Block Ticket"}
                            >
                              {t.status === "BLOCKED" ? <Unlock className="w-4 h-4" /> : <Lock className="w-4 h-4" />}
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: LIVE QR VERIFICATION TERMINAL */}
        {activeTab === "VERIFY" && (
          <div className="space-y-6">
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm max-w-2xl mx-auto space-y-4">
              <div className="text-center space-y-1">
                <QrCode className="w-10 h-10 text-indigo-600 mx-auto" />
                <h3 className="text-base font-bold text-slate-900 dark:text-white">
                  Gate Security & Invigilator QR Verification Terminal
                </h3>
                <p className="text-xs text-slate-500">
                  Scan optical QR code or input Ticket / Roll Number for instantaneous authenticity verification.
                </p>
              </div>

              <form onSubmit={handleVerify} className="space-y-3 pt-2">
                <div className="flex gap-2">
                  <input
                    type="text"
                    required
                    placeholder="e.g. HT-2026-AUT-001 or 230105001..."
                    value={verifyInput}
                    onChange={(e) => setVerifyInput(e.target.value)}
                    className="flex-1 px-3 py-2 text-xs rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                  <button
                    type="submit"
                    className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow-sm"
                  >
                    Verify Admit Card
                  </button>
                </div>
              </form>

              {verifyResult && (
                <div
                  className={`mt-4 p-4 rounded-xl border text-xs space-y-3 ${
                    verifyResult.isValid
                      ? "border-emerald-200 dark:border-emerald-900 bg-emerald-50/50 dark:bg-emerald-950/20"
                      : "border-rose-200 dark:border-rose-900 bg-rose-50/50 dark:bg-rose-950/20"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    {verifyResult.isValid ? (
                      <CheckCircle2 className="w-5 h-5 text-emerald-600" />
                    ) : (
                      <AlertTriangle className="w-5 h-5 text-rose-600" />
                    )}
                    <span className="font-bold text-sm">
                      {verifyResult.isValid ? "VERIFICATION SUCCESSFUL" : "VERIFICATION FAILED"}
                    </span>
                  </div>

                  <p className="text-slate-700 dark:text-slate-300">{verifyResult.message}</p>

                  {verifyResult.ticket && (
                    <div className="bg-white dark:bg-slate-900 p-3 rounded-lg border border-slate-200 dark:border-slate-800 grid grid-cols-2 gap-2 text-[11px]">
                      <div>
                        <span className="text-slate-500">Candidate Name:</span>
                        <div className="font-bold text-slate-900 dark:text-white">
                          {verifyResult.ticket.candidate_name}
                        </div>
                      </div>
                      <div>
                        <span className="text-slate-500">Roll / Enrollment:</span>
                        <div className="font-mono font-bold text-slate-900 dark:text-white">
                          {verifyResult.ticket.roll_number} • {verifyResult.ticket.enrollment_no}
                        </div>
                      </div>
                      <div>
                        <span className="text-slate-500">Allocated Seat:</span>
                        <div className="font-mono font-bold text-indigo-600 dark:text-indigo-400">
                          {verifyResult.ticket.paper_entries[0]?.seat_number}
                        </div>
                      </div>
                      <div>
                        <span className="text-slate-500">Digital Signature:</span>
                        <div className="font-mono text-[9px] text-slate-500 truncate">
                          {verifyResult.ticket.digital_signature_hash}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 3: BATCH OPERATIONS & INSTRUCTIONS */}
        {activeTab === "BATCH_OPS" && (
          <div className="space-y-6">
            <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 shadow-sm space-y-4">
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <FileText className="w-5 h-5 text-indigo-600" />
                Institutional Candidate Conduct & Examination Guidelines
              </h3>
              <p className="text-xs text-slate-500">
                Printed on the reverse of every admit card per Academic Council & State Regulatory directives.
              </p>

              <div className="space-y-2 pt-2">
                {DEFAULT_INSTRUCTIONS.map((inst, idx) => (
                  <div
                    key={idx}
                    className="p-3 bg-slate-50 dark:bg-slate-800/40 rounded-lg border border-slate-200 dark:border-slate-800 text-xs text-slate-700 dark:text-slate-300 flex items-start gap-2.5"
                  >
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                    <span>{inst}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* MODAL: ADMIT CARD OFFICIAL PREVIEW */}
      {isPreviewModalOpen && selectedTicket && (
        <div className="fixed inset-0 bg-slate-900/70 backdrop-blur-sm flex items-center justify-center p-4 z-50 overflow-y-auto">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-3xl w-full p-6 shadow-2xl space-y-5 my-8">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <QrCode className="w-5 h-5 text-indigo-600" />
                <span className="font-bold text-sm text-slate-900 dark:text-white">
                  Official Examination Admit Card Viewer
                </span>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => {
                    showToast(`Admit card for ${selectedTicket.candidate_name} downloaded.`);
                    window.print();
                  }}
                  className="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold flex items-center gap-1.5 shadow-sm"
                >
                  <Download className="w-3.5 h-3.5" /> Download PDF
                </button>
                <button
                  onClick={() => setIsPreviewModalOpen(false)}
                  className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 p-1"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
            </div>

            {/* ADMIT CARD PREVIEW PAPER LAYOUT */}
            <div className="border-2 border-indigo-900/40 dark:border-indigo-400/40 rounded-xl p-6 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 space-y-5 shadow-sm">
              {/* Institutional Header */}
              <div className="text-center border-b-2 border-indigo-900/20 dark:border-indigo-400/20 pb-4 space-y-1">
                <div className="text-xs font-black uppercase tracking-widest text-indigo-700 dark:text-indigo-400">
                  MY EDUCATION INDIA AUTONOMOUS CAMPUS, INDORE
                </div>
                <div className="text-base font-extrabold text-slate-900 dark:text-white">
                  END-SEMESTER EXAMINATION ADMIT CARD (HALL TICKET)
                </div>
                <div className="text-xs text-slate-600 dark:text-slate-400 font-medium">
                  Academic Session 2026-2027 • Autumn Semester Final Examination
                </div>
              </div>

              {/* Top Barcode and Ticket ID */}
              <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-2 text-xs">
                <div>
                  <span className="text-slate-500">Hall Ticket Number:</span>{" "}
                  <strong className="font-mono text-indigo-600 dark:text-indigo-400">{selectedTicket.ticket_number}</strong>
                </div>
                <div className="font-mono font-black tracking-widest text-slate-800 dark:text-slate-200">
                  {selectedTicket.barcode_data}
                </div>
              </div>

              {/* Student Demographics & Center Info */}
              <div className="grid grid-cols-3 gap-4 text-xs">
                <div className="col-span-2 grid grid-cols-2 gap-3 border-r border-slate-200 dark:border-slate-800 pr-4">
                  <div>
                    <span className="text-slate-500 block text-[10px]">Candidate Full Name</span>
                    <strong className="text-sm font-bold text-slate-900 dark:text-white">
                      {selectedTicket.candidate_name}
                    </strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Father's / Guardian's Name</span>
                    <strong className="text-slate-800 dark:text-slate-200">{selectedTicket.father_name}</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Roll Number</span>
                    <strong className="font-mono text-slate-900 dark:text-white">{selectedTicket.roll_number}</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Enrollment Number</span>
                    <strong className="font-mono text-slate-900 dark:text-white">{selectedTicket.enrollment_no}</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Degree Program</span>
                    <strong className="text-slate-800 dark:text-slate-200">{selectedTicket.program_name}</strong>
                  </div>
                  <div>
                    <span className="text-slate-500 block text-[10px]">Semester & Term</span>
                    <strong className="text-slate-800 dark:text-slate-200">{selectedTicket.semester_code}</strong>
                  </div>
                  <div className="col-span-2 border-t border-slate-100 dark:border-slate-800 pt-2">
                    <span className="text-slate-500 block text-[10px]">Assigned Examination Center</span>
                    <strong className="text-indigo-700 dark:text-indigo-400 block font-semibold">
                      {selectedTicket.exam_center_code} - {selectedTicket.exam_center_name}
                    </strong>
                    <span className="text-[10px] text-slate-500">{selectedTicket.exam_center_address}</span>
                  </div>
                </div>

                {/* Candidate Photo & Live QR Badge */}
                <div className="flex flex-col items-center justify-center space-y-3 pl-2">
                  <div className="w-24 h-28 border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-lg flex flex-col items-center justify-center bg-slate-50 dark:bg-slate-800 text-center p-2">
                    <span className="text-[10px] font-bold text-slate-500">AFFIXED PHOTO</span>
                    <div className="w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-950 text-indigo-700 dark:text-indigo-300 flex items-center justify-center font-bold text-xs mt-1">
                      {selectedTicket.candidate_name.charAt(0)}
                    </div>
                  </div>
                  <div className="p-2 border border-slate-200 dark:border-slate-800 rounded-lg bg-white dark:bg-slate-900 text-center">
                    <QrCode className="w-12 h-12 text-slate-900 dark:text-white mx-auto" />
                    <span className="text-[9px] text-slate-400 font-mono block mt-0.5">Scan to Verify</span>
                  </div>
                </div>
              </div>

              {/* Examination Papers & Seating Allocation Table */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-2">
                  Paper Schedule & Allocated Seating Plan
                </h4>
                <div className="border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-50 dark:bg-slate-800/60 text-slate-500 font-semibold border-b border-slate-200 dark:border-slate-800">
                      <tr>
                        <th className="px-3 py-2">Date & Time</th>
                        <th className="px-3 py-2">Paper Code</th>
                        <th className="px-3 py-2">Subject / Course Title</th>
                        <th className="px-3 py-2">Hall / Lab</th>
                        <th className="px-3 py-2">Allocated Seat</th>
                        <th className="px-3 py-2">Invigilator Sign</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-slate-800 font-medium">
                      {selectedTicket.paper_entries.map((p, idx) => (
                        <tr key={idx} className="hover:bg-slate-50/50">
                          <td className="px-3 py-2 font-mono">
                            <div>{p.exam_date}</div>
                            <div className="text-[10px] text-indigo-600 dark:text-indigo-400">
                              {p.start_time} - {p.end_time}
                            </div>
                          </td>
                          <td className="px-3 py-2 font-mono font-bold text-slate-800 dark:text-slate-200">
                            {p.paper_code}
                          </td>
                          <td className="px-3 py-2">
                            <div>{p.course_title}</div>
                            <div className="text-[10px] text-slate-500 font-mono">{p.course_code}</div>
                          </td>
                          <td className="px-3 py-2 font-mono font-bold">{p.room_number}</td>
                          <td className="px-3 py-2 font-mono font-black text-indigo-600 dark:text-indigo-400">
                            {p.seat_number}
                          </td>
                          <td className="px-3 py-2 border-l border-dashed border-slate-200 dark:border-slate-800 text-slate-300 font-serif italic text-center">
                            ___________
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Security Seals & Digital Signature */}
              <div className="flex flex-col sm:flex-row items-center justify-between border-t-2 border-slate-100 dark:border-slate-800 pt-4 gap-4 text-xs">
                <div className="space-y-1">
                  <div className="flex items-center gap-1.5 text-emerald-600 dark:text-emerald-400 font-bold">
                    <ShieldCheck className="w-4 h-4" />
                    <span>Cryptographically Signed by Autonomous Controller Cell</span>
                  </div>
                  <div className="font-mono text-[9px] text-slate-500 max-w-sm truncate">
                    SHA256 Checksum: {selectedTicket.digital_signature_hash}
                  </div>
                  <div className="text-[10px] text-slate-400">
                    Timestamp: {selectedTicket.signed_at} • Issued: {selectedTicket.issue_date}
                  </div>
                </div>

                <div className="text-center sm:text-right">
                  <div className="font-serif italic font-bold text-indigo-700 dark:text-indigo-300 text-sm">
                    {selectedTicket.controller_name}
                  </div>
                  <div className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">
                    Controller of Examinations (MEI Indore)
                  </div>
                </div>
              </div>

              {/* Student Guidelines Footer */}
              <div className="border-t border-slate-100 dark:border-slate-800 pt-3 text-[10px] text-slate-500 space-y-1">
                <strong>Mandatory Instructions:</strong> Arrive 45 mins prior to commencement. Gates lock strictly 15 minutes prior. Original Government Photo ID required. Mobile phones & unauthorized materials strictly prohibited.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* MODAL: BULK GENERATE */}
      {isBulkGenModalOpen && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3">
              <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-indigo-600" />
                Bulk Generate Admit Cards
              </h3>
              <button
                onClick={() => setIsBulkGenModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <p className="text-slate-600 dark:text-slate-400">
                This will generate official admit cards with QR codes, barcodes, and seat allocations for all registered candidates in Autumn 2026.
              </p>

              <div className="space-y-2 bg-slate-50 dark:bg-slate-800/40 p-3 rounded-xl border border-slate-200 dark:border-slate-800">
                <label className="flex items-center gap-2 font-semibold">
                  <input type="checkbox" defaultChecked className="rounded text-indigo-600" />
                  <span>Enforce Institutional Fee Clearance Verification</span>
                </label>
                <label className="flex items-center gap-2 font-semibold">
                  <input type="checkbox" defaultChecked className="rounded text-indigo-600" />
                  <span>Enforce 75% Minimum Attendance Floor Verification</span>
                </label>
                <label className="flex items-center gap-2 font-semibold">
                  <input type="checkbox" defaultChecked className="rounded text-indigo-600" />
                  <span>Attach CoE Digital Signature Cryptographic Hash</span>
                </label>
              </div>

              <div className="flex justify-end gap-2 pt-3 border-t border-slate-100 dark:border-slate-800">
                <button
                  type="button"
                  onClick={() => setIsBulkGenModalOpen(false)}
                  className="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300"
                >
                  Cancel
                </button>
                <button
                  onClick={() => {
                    showToast("Bulk admit card generation completed! 25 tickets generated.");
                    setIsBulkGenModalOpen(false);
                  }}
                  className="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white font-semibold"
                >
                  Generate All
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
export default HallTicketStudioPage;
