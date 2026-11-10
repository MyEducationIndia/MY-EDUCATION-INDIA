import React from "react";
import { QrCode, Barcode, CheckCircle2 } from "lucide-react";

export const BookCopiesAccessionPage: React.FC = () => {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Accession Register & Book Copies</h1>
      <p className="text-sm text-gray-500">Track physical copy barcodes, RFID tags, condition status, and acquisition ledgers</p>
    </div>
  );
};
