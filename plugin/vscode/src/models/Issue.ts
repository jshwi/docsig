/** Single docsig diagnostic from JSON CLI output. */
export interface Issue {
  /** One-based source line; null for file-level issues. */
  line: number | null;
  message: string;
  /** 2 maps to error severity; otherwise warning. */
  exit: number;
}
