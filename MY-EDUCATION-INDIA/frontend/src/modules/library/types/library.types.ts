export interface LibraryBook {
  id: string;
  isbn: string;
  title: string;
  subtitle?: string;
  categoryId: string;
  authorName: string;
  publisherName?: string;
  edition?: string;
  publicationYear?: number;
  language: string;
  totalCopiesCount: number;
  availableCopiesCount: number;
  isReferenceOnly: boolean;
  coverImageUrl?: string;
  description?: string;
}

export interface LibraryBookCopy {
  id: string;
  bookId: string;
  accessionNumber: string;
  barcode: string;
  rfidTag?: string;
  status: "AVAILABLE" | "ISSUED" | "RESERVED" | "LOST" | "DAMAGED" | "WEEDED";
  condition: "NEW" | "GOOD" | "FAIR" | "WORN" | "DAMAGED";
  purchasePrice: number;
  callNumber?: string;
}

export interface LibraryMember {
  id: string;
  userId: string;
  membershipCardNumber: string;
  memberType: "STUDENT" | "FACULTY" | "STAFF" | "RESEARCHER";
  maxBorrowLimit: number;
  issuePeriodDays: number;
  isActive: boolean;
  currentIssuedCount: number;
  totalFinesDue: number;
}

export interface LibraryDashboardMetrics {
  totalTitles: number;
  totalPhysicalCopies: number;
  availableCopies: number;
  activeIssuedCopies: number;
  totalMembers: number;
  overdueIssuesCount: number;
  totalFinesCollected: number;
  digitalResourcesCount: number;
}

export interface DigitalResource {
  id: string;
  title: string;
  categoryId: string;
  resourceType: "EBOOK" | "JOURNAL" | "RESEARCH_PAPER" | "THESIS" | "QUESTION_PAPER" | "NOTES";
  authorOrCreator: string;
  fileFormat: string;
  fileSizeBytes: number;
  fileUrl: string;
  downloadAllowed: boolean;
  viewCount: number;
  downloadCount: number;
}
